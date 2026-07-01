"""PhyK-TAS v2: conformal alpha versus operational cost.

Connects the split-conformal risk knob (alpha) to decision utility. For each
forecast model and alpha, repeated calibration/test splits produce conformal
upper bounds, deploy/adapt/retrain decisions, coverage, unsafe-deploy rate, and
cost-sensitive decision cost.
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd

from build_v2_conformal import (
    ADAPT_THR,
    ALPHAS,
    DEPLOY_THR,
    N_SPLITS_EVAL,
    RNG,
    TAG,
    conformal_upper_q,
    oof_pair_predictions,
)
from build_v2_meta_models import PAPER, SEEDS, load_seed

OUT = PAPER / f"v2_conformal_utility_{TAG}.csv"
REPORT = PAPER / f"v2_conformal_utility_{TAG}_report.md"

COST = {
    ("deploy", "deploy"): 0.0,
    ("deploy", "adapt"): 5.0,
    ("deploy", "retrain"): 10.0,
    ("adapt", "deploy"): 1.0,
    ("adapt", "adapt"): 0.0,
    ("adapt", "retrain"): 4.0,
    ("retrain", "deploy"): 3.0,
    ("retrain", "adapt"): 1.0,
    ("retrain", "retrain"): 0.0,
}


def decision_from_value(x: np.ndarray) -> np.ndarray:
    return np.where(x <= DEPLOY_THR, "deploy", np.where(x <= ADAPT_THR, "adapt", "retrain"))


def evaluate_alpha(pair: pd.DataFrame, alpha: float) -> dict:
    idx = np.arange(len(pair))
    cover, unsafe, deploys, adapts, retrains, costs = [], [], [], [], [], []
    d_pred = pair["d_pred"].to_numpy()
    d_obs = pair["d_obs"].to_numpy()
    obs_decision = decision_from_value(d_obs)

    for _ in range(N_SPLITS_EVAL):
        RNG.shuffle(idx)
        half = len(idx) // 2
        cal, tst = idx[:half], idx[half:]
        residuals = d_obs[cal] - d_pred[cal]
        q = conformal_upper_q(residuals, alpha)
        upper = d_pred[tst] + q
        pred_decision = decision_from_value(upper)
        obs = obs_decision[tst]

        cover.append(np.mean(d_obs[tst] <= upper))
        deploy_mask = pred_decision == "deploy"
        deploys.append(np.mean(pred_decision == "deploy"))
        adapts.append(np.mean(pred_decision == "adapt"))
        retrains.append(np.mean(pred_decision == "retrain"))
        unsafe.append(float(np.mean(obs[deploy_mask] != "deploy")) if deploy_mask.any() else 0.0)
        costs.append(float(np.mean([COST[(p, o)] for p, o in zip(pred_decision, obs)])))

    return {
        "alpha": alpha,
        "target_coverage": 1 - alpha,
        "empirical_coverage": float(np.mean(cover)),
        "unsafe_deploy_rate": float(np.mean(unsafe)),
        "deploy_rate": float(np.mean(deploys)),
        "adapt_rate": float(np.mean(adapts)),
        "retrain_rate": float(np.mean(retrains)),
        "mean_cost": float(np.mean(costs)),
    }


def main() -> None:
    df = pd.concat([load_seed(s) for s in SEEDS], ignore_index=True)
    rows = []
    for model, sub in df.groupby("model"):
        pair = oof_pair_predictions(sub.reset_index(drop=True))
        for alpha in ALPHAS:
            rec = {
                "forecast_model": model,
                "n_pairs": len(pair),
                "n_splits": N_SPLITS_EVAL,
            }
            rec.update(evaluate_alpha(pair, alpha))
            rows.append(rec)
            print(
                f"{model:24s} alpha={alpha:.2f} "
                f"coverage={rec['empirical_coverage']:.3f} "
                f"unsafe={rec['unsafe_deploy_rate']:.3f} "
                f"deploy={rec['deploy_rate']:.3f} cost={rec['mean_cost']:.3f}"
            )

    res = pd.DataFrame(rows)
    res.to_csv(OUT, index=False)

    lines = [
        f"# PhyK-TAS v2 conformal utility ({TAG})",
        "",
        "Repeated split-conformal evaluation linking alpha to empirical coverage, "
        "unsafe deploys, decision rates, and asymmetric decision cost. Costs are "
        "illustrative: deploy-to-adapt=5, deploy-to-retrain=10, adapt-to-deploy=1, "
        "adapt-to-retrain=4, retrain-to-deploy=3, retrain-to-adapt=1.",
        "",
        res.round(4).to_markdown(index=False),
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
