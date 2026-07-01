"""PhyK-TAS v2 -- Eje 4b: conformal risk control for the deployment decision.

Replaces the fragile t(2 dof) station-sample interval with a distribution-free
one-sided split-conformal upper bound on transfer degradation. For a source ->
target pair with predicted degradation d_hat, the conformal upper bound is

    d_upper = d_hat + Q_{1-alpha}(calibration residuals),

with the finite-sample-corrected quantile. Marginally, P(d_obs <= d_upper) >=
1 - alpha, so deciding *deploy* only when d_upper <= deploy_threshold bounds the
unsafe-deploy rate by alpha -- a guarantee the current heuristic lacks.

The inferrer is the monotone-constrained gradient boosting model (Eje 2) on the
physical+shift feature set, evaluated group-by-cell (the calibrated-regime
operational setting). Decisions are made at the source-target-pair level.
"""
from __future__ import annotations

import os
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import GroupKFold

warnings.filterwarnings("ignore")

from build_v2_meta_models import (
    PAPER, TAG, SEEDS, PHYSICAL_COLS, SHIFT_COLS, TARGET,
    load_seed, clean_features,
)

MONO_CST = [0] * len(PHYSICAL_COLS) + [1] * len(SHIFT_COLS)
DEPLOY_THR = float(os.environ.get("PHYKTAS_DEPLOY_THR", "0.010"))
ADAPT_THR = float(os.environ.get("PHYKTAS_ADAPT_THR", "0.025"))
ALPHAS = [0.20, 0.10, 0.05]
N_SPLITS_EVAL = int(os.environ.get("PHYKTAS_CONF_SPLITS", "200"))
RNG = np.random.default_rng(20260701)

OUT = PAPER / f"v2_conformal_{TAG}.csv"
REPORT = PAPER / f"v2_conformal_{TAG}_report.md"


def oof_pair_predictions(sub: pd.DataFrame) -> pd.DataFrame:
    """Group-by-cell out-of-fold degradation predictions, aggregated to the
    source-target pair level (mean over stations and seeds)."""
    X = clean_features(sub).to_numpy()
    y = sub[TARGET].to_numpy()
    groups = sub["cell5"].to_numpy()
    cv = GroupKFold(n_splits=min(5, sub["cell5"].nunique()))
    pred = np.full(len(y), np.nan)
    for tr, te in cv.split(X, y, groups):
        est = HistGradientBoostingRegressor(max_iter=400, learning_rate=0.05,
                                            random_state=20260524, monotonic_cst=MONO_CST)
        est.fit(X[tr], y[tr])
        pred[te] = est.predict(X[te])
    out = sub[["source_region", "target_region"]].copy()
    out["d_pred"] = pred
    out["d_obs"] = y
    pair = out.groupby(["source_region", "target_region"]).agg(
        d_pred=("d_pred", "mean"), d_obs=("d_obs", "mean")).reset_index()
    return pair


def conformal_upper_q(residuals: np.ndarray, alpha: float) -> float:
    n = len(residuals)
    k = int(np.ceil((n + 1) * (1 - alpha)))
    k = min(max(k, 1), n)
    return np.sort(residuals)[k - 1]


def evaluate_conformal(pair: pd.DataFrame, alpha: float) -> dict:
    """Repeated split-conformal: calibrate the upper-bound quantile on half the
    pairs, evaluate coverage / decisions on the other half."""
    idx = np.arange(len(pair))
    cover, unsafe, deploys, tested = [], [], [], []
    for _ in range(N_SPLITS_EVAL):
        RNG.shuffle(idx)
        half = len(idx) // 2
        cal, tst = idx[:half], idx[half:]
        res = pair["d_obs"].to_numpy()[cal] - pair["d_pred"].to_numpy()[cal]
        q = conformal_upper_q(res, alpha)
        d_pred_t = pair["d_pred"].to_numpy()[tst]
        d_obs_t = pair["d_obs"].to_numpy()[tst]
        d_upper = d_pred_t + q
        cover.append(np.mean(d_obs_t <= d_upper))
        deploy_mask = d_upper <= DEPLOY_THR
        deploys.append(int(deploy_mask.sum()))
        tested.append(len(tst))
        if deploy_mask.any():
            unsafe.append(np.mean(d_obs_t[deploy_mask] > DEPLOY_THR))
        else:
            unsafe.append(0.0)
    return {
        "alpha": alpha,
        "target_coverage": 1 - alpha,
        "empirical_coverage": float(np.mean(cover)),
        "unsafe_deploy_rate": float(np.mean(unsafe)),
        "mean_deploy_per_split": float(np.mean(deploys)),
        "mean_tested_per_split": float(np.mean(tested)),
    }


def main() -> None:
    df = pd.concat([load_seed(s) for s in SEEDS], ignore_index=True)
    rows = []
    for model, sub in df.groupby("model"):
        pair = oof_pair_predictions(sub.reset_index(drop=True))
        for alpha in ALPHAS:
            rec = {"forecast_model": model, "n_pairs": len(pair)}
            rec.update(evaluate_conformal(pair, alpha))
            rows.append(rec)
            print(f"{model:24s} a={alpha:.2f} cover={rec['empirical_coverage']:.3f} "
                  f"(target {1-alpha:.2f}) unsafe_deploy={rec['unsafe_deploy_rate']:.3f} "
                  f"deploy/split={rec['mean_deploy_per_split']:.1f}")
    res = pd.DataFrame(rows)
    res.to_csv(OUT, index=False)
    lines = [f"# PhyK-TAS v2 conformal decision layer ({TAG})", "",
             f"One-sided split-conformal upper bound on degradation; deploy "
             f"threshold {DEPLOY_THR}. {N_SPLITS_EVAL} random calibration/test "
             "splits per model. Empirical coverage should be >= target; the "
             "unsafe-deploy rate should sit at or below alpha.", "",
             res.round(3).to_markdown(index=False), ""]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nwrote {OUT}\nwrote {REPORT}")


if __name__ == "__main__":
    main()
