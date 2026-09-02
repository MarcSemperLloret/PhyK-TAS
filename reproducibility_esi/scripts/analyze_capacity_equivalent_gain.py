"""Quantify the operational capacity equivalent of the confirmatory AUC gain.

The analysis uses the already frozen confirmatory budget curves.  It does not
refit or select a policy.  Random expected allocation is linear in the number
of retrainings, so a vertical MAE advantage can be translated into the number
of additional random retrainings required to obtain the same pooled mean MAE.

All uncertainty intervals resample the 11 target regions as clusters.  This is
a post-confirmation practical-significance analysis, not a new confirmatory
hypothesis test.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "realized_action_confirmatory_budget_curve.csv"
SELECTED_BUDGETS = (5, 10, 15, 20, 25)
BOOTSTRAP_REPLICATES = 100_000
SEED = 20260822
TOL = 1e-10


def first_equivalent_budget(curve: np.ndarray, threshold: float) -> float:
    """First fractional budget whose at-most-budget envelope reaches threshold."""
    envelope = np.minimum.accumulate(np.asarray(curve, dtype=float))
    if envelope[0] <= threshold + TOL:
        return 0.0
    for index in range(1, len(envelope)):
        if envelope[index] <= threshold + TOL:
            previous = envelope[index - 1]
            current = envelope[index]
            if abs(previous - current) <= TOL:
                return float(index)
            fraction = (previous - threshold) / (previous - current)
            return float(index - 1 + fraction)
    return float("nan")


def validate_and_pivot(data: pd.DataFrame) -> tuple[list[str], np.ndarray, np.ndarray, np.ndarray]:
    required = {"target_region", "budget_retrains", "policy", "mean_mae"}
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    subset = data.loc[data["policy"].isin(["action_value", "random_expected", "mmd"])].copy()
    if subset.duplicated(["target_region", "budget_retrains", "policy"]).any():
        raise ValueError("Duplicate target-budget-policy rows")

    targets = sorted(subset["target_region"].unique())
    if len(targets) != 11:
        raise ValueError(f"Expected 11 targets, found {len(targets)}")

    expected_budgets = list(range(31))
    arrays: dict[str, list[np.ndarray]] = {name: [] for name in ("action_value", "random_expected", "mmd")}
    for target in targets:
        target_data = subset.loc[subset["target_region"].eq(target)]
        for policy in arrays:
            policy_data = target_data.loc[target_data["policy"].eq(policy)].sort_values("budget_retrains")
            if policy_data["budget_retrains"].tolist() != expected_budgets:
                raise ValueError(f"Incomplete budget grid for {target}/{policy}")
            values = policy_data["mean_mae"].to_numpy(dtype=float)
            if not np.isfinite(values).all():
                raise ValueError(f"Non-finite MAE for {target}/{policy}")
            arrays[policy].append(values)

    action = np.stack(arrays["action_value"])
    random = np.stack(arrays["random_expected"])
    mmd = np.stack(arrays["mmd"])

    if np.max(np.abs(action[:, [0, 30]] - random[:, [0, 30]])) > TOL:
        raise ValueError("Action-value and random endpoints do not coincide")

    random_second_difference = np.diff(random, n=2, axis=1)
    if np.max(np.abs(random_second_difference)) > TOL:
        raise ValueError("Random expected curves are not linear in budget")

    marginal = (random[:, 0] - random[:, 30]) / 30.0
    if np.any(marginal <= 0):
        raise ValueError("Random expected MAE does not improve with capacity in every target")

    return targets, action, random, mmd


def bootstrap_summary(action: np.ndarray, random: np.ndarray) -> tuple[dict, list[dict]]:
    target_count = action.shape[0]
    rng = np.random.default_rng(SEED)
    indices = rng.integers(0, target_count, size=(BOOTSTRAP_REPLICATES, target_count))

    target_auc_gain = (random - action).mean(axis=1)
    target_random_marginal = (random[:, 0] - random[:, 30]) / 30.0
    integrated_samples = (
        target_auc_gain[indices].mean(axis=1)
        / target_random_marginal[indices].mean(axis=1)
    )
    integrated_point = float(target_auc_gain.mean() / target_random_marginal.mean())
    leave_one_target_out = []
    for omitted in range(target_count):
        retained = np.arange(target_count) != omitted
        leave_one_target_out.append(
            float(target_auc_gain[retained].mean() / target_random_marginal[retained].mean())
        )
    integrated = {
        "capacity_equivalent_retrainings": integrated_point,
        "ci95_low": float(np.quantile(integrated_samples, 0.025)),
        "ci95_high": float(np.quantile(integrated_samples, 0.975)),
        "fraction_of_total_capacity": integrated_point / 30.0,
        "leave_one_target_out_min": min(leave_one_target_out),
        "leave_one_target_out_max": max(leave_one_target_out),
        "bootstrap_replicates": BOOTSTRAP_REPLICATES,
        "bootstrap_seed": SEED,
    }

    selected: list[dict] = []
    random_marginal_boot = target_random_marginal[indices].mean(axis=1)
    for budget in SELECTED_BUDGETS:
        action_mean = float(action[:, budget].mean())
        random_mean = float(random[:, budget].mean())
        point_saving = float((random_mean - action_mean) / target_random_marginal.mean())
        saving_samples = (
            random[indices, budget].mean(axis=1) - action[indices, budget].mean(axis=1)
        ) / random_marginal_boot
        selected.append(
            {
                "budget": budget,
                "action_value_mean_mae": action_mean,
                "random_mean_mae": random_mean,
                "random_equivalent_budget": budget + point_saving,
                "capacity_equivalent_saving": point_saving,
                "saving_ci95_low": float(np.quantile(saving_samples, 0.025)),
                "saving_ci95_high": float(np.quantile(saving_samples, 0.975)),
                "relative_saving_vs_policy_budget": point_saving / budget,
                "targets_action_better_than_random": int((action[:, budget] < random[:, budget]).sum()),
                "targets_total": target_count,
            }
        )
    return integrated, selected


def build_report(integrated: dict, selected: pd.DataFrame, target_summary: pd.DataFrame) -> str:
    midpoint = selected.loc[selected["budget"].eq(15)].iloc[0]
    table = selected[
        [
            "budget",
            "random_equivalent_budget",
            "capacity_equivalent_saving",
            "saving_ci95_low",
            "saving_ci95_high",
            "mmd_equivalent_budget",
            "targets_action_better_than_random",
            "targets_action_better_than_mmd",
        ]
    ].copy()
    for column in table.columns:
        if column not in {"budget", "targets_action_better_than_random", "targets_action_better_than_mmd"}:
            table[column] = table[column].map(lambda value: f"{value:.3f}")

    return "\n".join(
        [
            "# Post-confirmation capacity-equivalent analysis",
            "",
            "## Status",
            "",
            "**Exploratory practical-significance analysis of the frozen confirmation.** No policy was refit and no budget was selected as a new confirmatory endpoint.",
            "",
            "## Main result",
            "",
            f"Across the complete 0--30 capacity curve, the AUC advantage is equivalent to {integrated['capacity_equivalent_retrainings']:.2f} additional random retrainings (target-cluster bootstrap 95% CI {integrated['ci95_low']:.2f}--{integrated['ci95_high']:.2f}), or {100 * integrated['fraction_of_total_capacity']:.1f}% of the full 30-decision capacity.",
            f"The estimate remains between {integrated['leave_one_target_out_min']:.2f} and {integrated['leave_one_target_out_max']:.2f} when each target region is omitted in turn.",
            "",
            f"At the natural midpoint budget of 15, PhyK-TAS obtains mean MAE {midpoint['action_value_mean_mae']:.6f}. Random allocation requires an interpolated budget of {midpoint['random_equivalent_budget']:.2f} to reach the same pooled mean MAE: a capacity-equivalent saving of {midpoint['capacity_equivalent_saving']:.2f} retrainings (95% CI {midpoint['saving_ci95_low']:.2f}--{midpoint['saving_ci95_high']:.2f}). The action-value policy is better than random in {int(midpoint['targets_action_better_than_random'])}/11 targets and better than MMD in {int(midpoint['targets_action_better_than_mmd'])}/11 at this budget.",
            "",
            "## Fixed reporting grid of representative budgets",
            "",
            table.to_markdown(index=False),
            "",
            "## Interpretation boundary",
            "",
            "Random expected allocation is exactly linear in budget, which makes the horizontal capacity conversion identifiable on the pooled mean curve. MMD equivalence uses the first crossing of its at-most-budget envelope. The bootstrap resamples target regions, not the 330 decisions. The confidence intervals quantify geographic sampling variability; they are not a second confirmatory test. Target-specific capacity ratios can be unstable when random retraining has a very shallow marginal benefit, so the manuscript-safe claim is the pooled curve result together with the 10/11 target direction, not a universal per-region saving.",
            "",
            "## Target-level audit",
            "",
            f"The full-curve AUC advantage is favorable in {int(target_summary['action_better_auc'].sum())}/11 targets. NCA is the only unfavorable target and must remain visible in any presentation.",
            "",
        ]
    )


def main() -> None:
    data = pd.read_csv(INPUT)
    targets, action, random, mmd = validate_and_pivot(data)
    integrated, selected_rows = bootstrap_summary(action, random)

    pooled_mmd = mmd.mean(axis=0)
    for row in selected_rows:
        budget = int(row["budget"])
        mmd_equivalent = first_equivalent_budget(pooled_mmd, row["action_value_mean_mae"])
        row["mmd_mean_mae"] = float(pooled_mmd[budget])
        row["mmd_equivalent_budget"] = mmd_equivalent
        row["mmd_capacity_equivalent_saving"] = mmd_equivalent - budget
        row["targets_action_better_than_mmd"] = int((action[:, budget] < mmd[:, budget]).sum())

    selected = pd.DataFrame(selected_rows)
    target_auc_gain = (random - action).mean(axis=1)
    target_random_marginal = (random[:, 0] - random[:, 30]) / 30.0
    target_summary = pd.DataFrame(
        {
            "target_region": targets,
            "mean_auc_gain_vs_random": target_auc_gain,
            "random_mae_gain_per_retraining": target_random_marginal,
            "target_capacity_equivalent": target_auc_gain / target_random_marginal,
            "action_better_auc": target_auc_gain > 0,
        }
    )

    result = {
        "analysis_status": "post-confirmation practical-significance analysis",
        "targets": len(targets),
        "budgets": 31,
        "integrated": integrated,
        "selected_budgets": selected_rows,
        "validation": {
            "complete_target_budget_policy_grid": True,
            "action_random_endpoints_equal": True,
            "random_expected_linear_in_budget": True,
            "random_marginal_improvement_positive_in_every_target": True,
        },
    }

    selected.to_csv(ROOT / "capacity_equivalent_selected_budgets.csv", index=False)
    target_summary.to_csv(ROOT / "capacity_equivalent_target_summary.csv", index=False)
    (ROOT / "capacity_equivalent_result.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )
    (ROOT / "capacity_equivalent_report.md").write_text(
        build_report(integrated, selected, target_summary), encoding="utf-8"
    )

    print(json.dumps(result["integrated"], indent=2))
    print(selected.to_string(index=False))


if __name__ == "__main__":
    main()
