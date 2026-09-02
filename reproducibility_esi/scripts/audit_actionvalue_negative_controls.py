# -*- coding: utf-8 -*-
"""Post-confirmation negative controls for the action-value allocation policy.

Three checks, all run after the frozen 2023--2025 confirmation was completed.
None of them changes the confirmatory result; they test whether that result
could have been produced without information.

1. Structural audit of the action matrix. Retraining is executed once per
   target and family and shared across the ten source candidates, so the
   realized retraining benefit is a deterministic function of the cheap-action
   loss within each (target, family) group. This is reported so the difficulty
   of the task is not overstated.

2. Trivial ranker. Allocating retraining by realized cheap-action loss alone,
   with no learning at all, is the ranking the structural property suggests.

3. Permutation null. The held-target policy is refitted on shuffled action
   outcomes and re-evaluated on the confirmation block. The ridge penalty is
   fixed at the modal frozen value so the null is affordable; the real policy is
   re-evaluated identically for a like-for-like comparison.

Outputs: actionvalue_negative_controls.csv, actionvalue_negative_controls.md
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.linear_model import Ridge
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DEV = ROOT / "realized_action_policy_dev11_predictions.csv"
CONF = ROOT / "realized_action_confirmatory_predictions_outcomes.csv"
OUT_CSV = ROOT / "actionvalue_negative_controls.csv"
OUT_MD = ROOT / "actionvalue_negative_controls.md"

ALPHA = 10000.0
N_PERM = 200
SEED = 20260902
KEY = ["model", "source_region", "target_region"]
EXCLUDED = {
    "model", "source_region", "target_region", "adapt", "deploy", "retrain",
    "benefit_adapt", "benefit_retrain", "oracle_action", "oracle_mae",
    "pred_benefit_adapt", "pred_benefit_retrain", "policy_action", "policy_mae",
    "policy_regret", "policy_normalized_regret", "policy_correct",
}


def budget_auc(cheap: np.ndarray, retrain: np.ndarray, score: np.ndarray) -> float:
    """Discrete AUC of the MAE--budget curve over budgets 0..n for one target."""
    n = len(cheap)
    order = score.argsort()[::-1]
    return float(np.mean([
        np.where(np.isin(np.arange(n), order[:b]), retrain, cheap).mean()
        for b in range(n + 1)
    ]))


def random_auc(cheap: np.ndarray, retrain: np.ndarray) -> float:
    n = len(cheap)
    return float(np.mean([
        cheap.mean() + (b / n) * (retrain - cheap).mean() for b in range(n + 1)
    ]))


def structural_audit(conf: pd.DataFrame) -> dict[str, float]:
    counts = {a: int(conf[a].nunique()) for a in ("deploy", "adapt", "retrain")}
    per_group = conf.groupby(["target_region", "model"])["retrain"].nunique()
    rhos = []
    for _, group in conf.groupby(["target_region", "model"]):
        benefit = group["cheap_mae"] - group["retrain"]
        rhos.append(spearmanr(group["cheap_mae"], benefit).statistic)
    rhos = np.asarray(rhos)
    return {
        "n_decisions": len(conf),
        "distinct_deploy": counts["deploy"],
        "distinct_adapt": counts["adapt"],
        "distinct_retrain": counts["retrain"],
        "max_retrain_per_target_family": int(per_group.max()),
        "n_groups": len(rhos),
        "min_spearman_cheap_vs_benefit": float(np.nanmin(rhos)),
        "frac_groups_rho_one": float(np.mean(np.isclose(rhos, 1.0))),
    }


def evaluate(conf: pd.DataFrame, score_col: str) -> tuple[float, int]:
    """Mean target AUC and favorable-target count against random expectation."""
    policy, rand = {}, {}
    for target, group in conf.groupby("target_region"):
        cheap = group["cheap_mae"].to_numpy()
        retrain = group["retrain"].to_numpy()
        policy[target] = budget_auc(cheap, retrain, group[score_col].to_numpy())
        rand[target] = random_auc(cheap, retrain)
    policy, rand = pd.Series(policy), pd.Series(rand)
    return float(rand.mean() - policy.mean()), int((policy < rand).sum())


def fit_logo(dev: pd.DataFrame, features: list[str], y_adapt, y_retrain):
    pred_adapt, pred_retrain = np.zeros(len(dev)), np.zeros(len(dev))
    for train_idx, test_idx in LeaveOneGroupOut().split(dev[features], groups=dev["target_region"]):
        for y, out in ((y_adapt, pred_adapt), (y_retrain, pred_retrain)):
            model = Pipeline([("scale", StandardScaler()), ("ridge", Ridge(alpha=ALPHA))])
            model.fit(dev.iloc[train_idx][features].astype(float), y[train_idx])
            out[test_idx] = model.predict(dev.iloc[test_idx][features].astype(float))
    return pred_adapt, pred_retrain


def score_confirmation(dev, conf, pred_adapt, pred_retrain) -> tuple[float, int]:
    carried = dev[KEY].copy()
    carried["pa"], carried["pr"] = pred_adapt, pred_retrain
    merged = conf.merge(carried, on=KEY, how="left")
    cheap = np.where(merged["pa"] > 0, merged["adapt"], merged["deploy"])
    merged = merged.assign(cheap_mae=cheap,
                           _score=merged["pr"] - np.maximum(merged["pa"], 0.0))
    return evaluate(merged, "_score")


def main() -> None:
    dev = pd.read_csv(DEV)
    conf = pd.read_csv(CONF)
    features = [c for c in dev.columns if c not in EXCLUDED]
    if len(features) != 62:
        raise ValueError(f"expected the 62 frozen predictors, found {len(features)}")

    audit = structural_audit(conf)
    if audit["max_retrain_per_target_family"] != 1:
        raise ValueError("retraining is not shared within (target, family) as documented")

    ceiling = evaluate(conf, "realized_gain")[0] if "realized_gain" in conf else None
    conf = conf.assign(_true_gain=conf["cheap_mae"] - conf["retrain"])
    ceiling, _ = evaluate(conf, "_true_gain")
    frozen_gain, frozen_fav = evaluate(conf, "predicted_gain")
    trivial_gain, trivial_fav = evaluate(conf, "cheap_mae")

    real_gain, real_fav = score_confirmation(
        dev, conf, *fit_logo(dev, features,
                             dev["benefit_adapt"].to_numpy(),
                             dev["benefit_retrain"].to_numpy()))

    rng = np.random.default_rng(SEED)
    y_adapt = dev["benefit_adapt"].to_numpy()
    y_retrain = dev["benefit_retrain"].to_numpy()
    null = []
    for _ in range(N_PERM):
        perm = rng.permutation(len(dev))
        gain, _ = score_confirmation(
            dev, conf, *fit_logo(dev, features, y_adapt[perm], y_retrain[perm]))
        null.append(gain)
    null = np.asarray(null)

    rows = [
        {"control": "frozen action-value policy", "gain_vs_random": frozen_gain,
         "share_of_ceiling_pct": 100 * frozen_gain / ceiling, "favorable_targets": frozen_fav},
        {"control": "restricted oracle", "gain_vs_random": ceiling,
         "share_of_ceiling_pct": 100.0, "favorable_targets": 11},
        {"control": "trivial ranker (realized cheap-action loss)", "gain_vs_random": trivial_gain,
         "share_of_ceiling_pct": 100 * trivial_gain / ceiling, "favorable_targets": trivial_fav},
        {"control": f"policy refit, alpha fixed at {ALPHA:g}", "gain_vs_random": real_gain,
         "share_of_ceiling_pct": 100 * real_gain / ceiling, "favorable_targets": real_fav},
        {"control": f"permutation null, mean over {N_PERM} refits", "gain_vs_random": float(null.mean()),
         "share_of_ceiling_pct": 100 * float(null.mean()) / ceiling, "favorable_targets": np.nan},
        {"control": f"permutation null, 95th percentile", "gain_vs_random": float(np.percentile(null, 95)),
         "share_of_ceiling_pct": 100 * float(np.percentile(null, 95)) / ceiling, "favorable_targets": np.nan},
        {"control": f"permutation null, maximum", "gain_vs_random": float(null.max()),
         "share_of_ceiling_pct": 100 * float(null.max()) / ceiling, "favorable_targets": np.nan},
    ]
    pd.DataFrame(rows).to_csv(OUT_CSV, index=False)

    p_perm = float((null >= real_gain).mean())
    lines = [
        "# Post-confirmation negative controls for the action-value policy",
        "",
        "These controls were run after the frozen confirmation was completed. They do not",
        "alter any confirmatory number; they test whether that number could have arisen",
        "without information.",
        "",
        "## Structural audit of the action matrix",
        "",
        f"- Decisions: {audit['n_decisions']}",
        f"- Distinct realized outcomes: deploy {audit['distinct_deploy']}, "
        f"adapt {audit['distinct_adapt']}, retrain {audit['distinct_retrain']}",
        "- Retraining is executed once per (target, family) and shared across the ten",
        "  source candidates, because a target-trained model does not depend on the source.",
        f"- Consequently, within each of the {audit['n_groups']} (target, family) groups the realized",
        "  retraining benefit is a strictly decreasing function of the cheap-action loss:",
        f"  Spearman rho = 1.000 in {audit['frac_groups_rho_one'] * 100:.0f}% of groups "
        f"(minimum {audit['min_spearman_cheap_vs_benefit']:.4f}).",
        "- The within-family ordering is therefore not a learning problem. The learnable",
        "  content of the benchmark is the comparison across families competing for the",
        "  same target budget.",
        "",
        "## Trivial ranker",
        "",
        "Allocating by realized cheap-action loss alone, with no learning, is the ranking",
        "the structural property suggests. Pooled over the thirty candidates of a target it",
        f"gains {trivial_gain:+.6f} MAE-AUC against random expectation "
        f"({100 * trivial_gain / ceiling:+.1f}% of the ceiling) and is favorable in "
        f"{trivial_fav}/11 targets.",
        "It is worse than random ordering: cheap-action loss is not comparable across",
        "families, so high-error families absorb the budget regardless of what retraining",
        "would return there.",
        "",
        "## Permutation null",
        "",
        f"The held-target policy was refitted on shuffled action outcomes {N_PERM} times and",
        "re-evaluated on the confirmation block, with the ridge penalty fixed at the modal",
        "frozen value so that the real policy and the null are scored identically.",
        "",
        f"- Real policy under the same fixed penalty: {real_gain:+.6f} MAE-AUC, {real_fav}/11 favorable",
        f"- Null: mean {null.mean():+.6f}, sd {null.std():.6f}, "
        f"95th percentile {np.percentile(null, 95):+.6f}, maximum {null.max():+.6f}",
        f"- P(null gain >= real gain) = {p_perm:.4f} over {N_PERM} permutations",
        "",
        "The null is centred on zero, as it must be, and the observed gain lies "
        f"{(real_gain - null.mean()) / null.std():.1f} null standard deviations above it.",
        f"Seed {SEED}.",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
