"""Retrospective 2023--2025 evaluation of post-confirmation challengers.

This analysis is explicitly post hoc.  It must not be described as frozen or
prospectively confirmatory because the challenger learners were designed after
the 2023--2025 Ridge result had been opened.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon


ROOT = Path(__file__).resolve().parents[1]
KEYS = ["model", "source_region", "target_region"]
CONFIRM_FILES = (
    ROOT / "realized_actions_confirm_spatial_s1.csv",
    ROOT / "realized_actions_confirm_patchtst_head_s1.csv",
    ROOT / "realized_actions_confirm_graphwavenet_head_s1.csv",
)
CHALLENGERS = {
    "ridge_frozen": ROOT / "realized_action_policy_dev11_predictions.csv",
    "tabicl_v2_posthoc": ROOT / "frontier_tabicl_v2_dev_predictions.csv",
    "neural_pointwise_posthoc": ROOT / "budget_integrated_pointwise_dev_predictions.csv",
    "budget_pairwise_posthoc": ROOT / "budget_integrated_pairwise_dev_predictions.csv",
    "soft_budget_ranker_posthoc": ROOT / "budget_integrated_softbudget_dev_predictions.csv",
}


def load_confirm() -> pd.DataFrame:
    long = pd.concat([pd.read_csv(path) for path in CONFIRM_FILES], ignore_index=True)
    if len(long) != 990 or long.duplicated(KEYS + ["action"]).any():
        raise ValueError("Invalid confirmatory action table")
    return (
        long.pivot(index=KEYS, columns="action", values="mae_2023_2025")
        .reset_index()
        .rename_axis(columns=None)
    )


def normalized_predictions(label: str, path: Path) -> pd.DataFrame:
    pred = pd.read_csv(path)
    if pred.duplicated(KEYS).any() or len(pred) != 330:
        raise ValueError(f"Invalid predictions for {label}")
    if "predicted_gain" not in pred:
        pred["predicted_gain"] = pred["pred_benefit_retrain"] - np.maximum(
            0.0, pred["pred_benefit_adapt"]
        )
    return pred[KEYS + ["pred_benefit_adapt", "predicted_gain"]].copy()


def evaluate(label: str, pred: pd.DataFrame, outcomes: pd.DataFrame):
    data = pred.merge(outcomes, on=KEYS, how="inner", validate="one_to_one")
    if len(data) != 330:
        raise ValueError(f"Prediction/outcome mismatch for {label}")
    data["cheap_mae"] = np.where(
        data["pred_benefit_adapt"] > 0, data["adapt"], data["deploy"]
    )
    data["realized_gain"] = data["cheap_mae"] - data["retrain"]
    curve_rows = []
    for target, group in data.groupby("target_region", sort=True):
        group = group.reset_index(drop=True)
        n = len(group)
        cheap = group["cheap_mae"].to_numpy()
        retrain = group["retrain"].to_numpy()
        orders = {
            label: group["predicted_gain"].to_numpy().argsort()[::-1],
            f"{label}__oracle": group["realized_gain"].to_numpy().argsort()[::-1],
        }
        for budget in range(n + 1):
            for policy, order in orders.items():
                mae = cheap.copy()
                mae[order[:budget]] = retrain[order[:budget]]
                curve_rows.append(
                    {
                        "learner": label,
                        "target_region": target,
                        "budget_retrains": budget,
                        "policy": policy,
                        "mean_mae": float(mae.mean()),
                    }
                )
            curve_rows.append(
                {
                    "learner": label,
                    "target_region": target,
                    "budget_retrains": budget,
                    "policy": f"{label}__random",
                    "mean_mae": float(cheap.mean() + (budget / n) * (retrain - cheap).mean()),
                }
            )
    curve = pd.DataFrame(curve_rows)
    auc = (
        curve.groupby(["learner", "target_region", "policy"], as_index=False)["mean_mae"]
        .mean()
        .rename(columns={"mean_mae": "budget_curve_auc"})
    )
    wide = auc.pivot(index="target_region", columns="policy", values="budget_curve_auc")
    delta = wide[label] - wide[f"{label}__random"]
    mean_policy = float(wide[label].mean())
    mean_random = float(wide[f"{label}__random"].mean())
    mean_oracle = float(wide[f"{label}__oracle"].mean())
    summary = {
        "learner": label,
        "mean_budget_curve_auc": mean_policy,
        "mean_random_auc": mean_random,
        "mean_restricted_oracle_auc": mean_oracle,
        "mean_difference_vs_random": float(delta.mean()),
        "targets_better_than_random": int((delta < 0).sum()),
        "wilcoxon_less_vs_random_p": float(wilcoxon(delta, alternative="less").pvalue),
        "random_oracle_gap_closed_fraction": float(
            (mean_random - mean_policy) / (mean_random - mean_oracle)
        ),
    }
    target = pd.DataFrame(
        {
            "learner": label,
            "target_region": wide.index,
            "policy_auc": wide[label].to_numpy(),
            "random_auc": wide[f"{label}__random"].to_numpy(),
            "oracle_auc": wide[f"{label}__oracle"].to_numpy(),
            "difference_vs_random": delta.to_numpy(),
        }
    )
    return curve, target, summary


def main() -> None:
    outcomes = load_confirm()
    curves = []
    targets = []
    summaries = []
    for label, path in CHALLENGERS.items():
        curve, target, summary = evaluate(
            label, normalized_predictions(label, path), outcomes
        )
        curves.append(curve)
        targets.append(target)
        summaries.append(summary)
    curve_all = pd.concat(curves, ignore_index=True)
    target_all = pd.concat(targets, ignore_index=True)
    summary_all = pd.DataFrame(summaries).sort_values("mean_budget_curve_auc")
    curve_all.to_csv(ROOT / "posthoc_actionvalue_challenger_budget_curve.csv", index=False)
    target_all.to_csv(ROOT / "posthoc_actionvalue_challenger_target_auc.csv", index=False)
    summary_all.to_csv(ROOT / "posthoc_actionvalue_challenger_summary.csv", index=False)
    print(summary_all.to_string(index=False))


if __name__ == "__main__":
    main()
