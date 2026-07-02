"""Conflict-stratified (Mondrian) conformal -- executes the conflict signal
inside the decision layer instead of only reporting it.

Per source-target pair we form the two single-source degradation predictions,
their conflict |f_phys - f_shift|, the combined point prediction, and the
observed degradation. We then compare two split-conformal upper bounds:

  * global: one residual quantile for all pairs;
  * conflict-stratified: a separate quantile per conflict tercile.

If conflict carries deployment-relevant uncertainty, the global bound should
under-cover high-conflict pairs, while the stratified bound should restore
coverage by widening the bound precisely where the sources disagree.
"""
from __future__ import annotations

import os
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

from build_v2_meta_models import (
    PAPER, TAG, SEEDS, PHYSICAL_COLS, SHIFT_COLS, TARGET,
    load_seed, build_splits, oof_predict_sklearn,
)

ALPHA = float(os.environ.get("PHYKTAS_ALPHA", "0.10"))
N_SPLITS = 300
RNG = np.random.default_rng(20260701)
MODELS = ["spatial_knn_ridge", "stgcn_diffusion", "graphwavenet_transfer",
          "regional_doy_climatology"]
OUT = PAPER / f"v3_conflict_conformal_{TAG}.csv"
REPORT = PAPER / f"v3_conflict_conformal_{TAG}_report.md"


def clean(df, cols):
    x = df[cols].replace([np.inf, -np.inf], np.nan)
    return x.fillna(x.median(numeric_only=True)).to_numpy()


def q_upper(resid, alpha):
    n = len(resid)
    k = min(max(int(np.ceil((n + 1) * (1 - alpha))), 1), n)
    return np.sort(resid)[k - 1]


def pair_frame(sub):
    y = sub[TARGET].to_numpy()
    splits = build_splits(sub, "group_by_cell")
    fp = oof_predict_sklearn("random_forest", clean(sub, PHYSICAL_COLS), y, splits)
    fs = oof_predict_sklearn("random_forest", clean(sub, SHIFT_COLS), y, splits)
    fc = oof_predict_sklearn("random_forest", clean(sub, PHYSICAL_COLS + SHIFT_COLS), y, splits)
    d = sub[["source_region", "target_region"]].copy()
    d["d_pred"] = fc; d["d_obs"] = y; d["conflict"] = np.abs(fp - fs)
    return d.groupby(["source_region", "target_region"]).mean().reset_index()


def main() -> None:
    df = pd.concat([load_seed(s) for s in SEEDS], ignore_index=True)
    rows = []
    for model in MODELS:
        sub = df[df["model"] == model].reset_index(drop=True)
        if sub.empty:
            continue
        pair = pair_frame(sub)
        c = pair["conflict"].to_numpy()
        t1, t2 = np.quantile(c, [1/3, 2/3])
        tercile = np.where(c <= t1, 0, np.where(c <= t2, 1, 2))
        pred = pair["d_pred"].to_numpy(); obs = pair["d_obs"].to_numpy()
        idx = np.arange(len(pair))

        # accumulators: coverage per tercile for global vs stratified; widths
        cov_g = {0: [], 1: [], 2: []}; cov_s = {0: [], 1: [], 2: []}
        wid_g = {0: [], 1: [], 2: []}; wid_s = {0: [], 1: [], 2: []}
        for _ in range(N_SPLITS):
            RNG.shuffle(idx)
            half = len(idx) // 2
            cal, tst = idx[:half], idx[half:]
            resid = obs[cal] - pred[cal]
            qg = q_upper(resid, ALPHA)
            # stratified quantile per tercile using calibration pairs of that tercile
            qs = {}
            for k in (0, 1, 2):
                rk = obs[cal][tercile[cal] == k] - pred[cal][tercile[cal] == k]
                qs[k] = q_upper(rk, ALPHA) if len(rk) >= 5 else qg
            for k in (0, 1, 2):
                mk = tst[tercile[tst] == k]
                if len(mk) == 0:
                    continue
                cov_g[k].append(np.mean(obs[mk] <= pred[mk] + qg))
                cov_s[k].append(np.mean(obs[mk] <= pred[mk] + qs[k]))
                wid_g[k].append(qg); wid_s[k].append(qs[k])
        for k, name in [(0, "low"), (1, "mid"), (2, "high")]:
            rows.append({
                "model": model, "conflict_tercile": name,
                "coverage_global": float(np.mean(cov_g[k])),
                "coverage_stratified": float(np.mean(cov_s[k])),
                "width_global": float(np.mean(wid_g[k])),
                "width_stratified": float(np.mean(wid_s[k])),
            })
            print(f"{model:24s} {name:4s} covG={rows[-1]['coverage_global']:.3f} "
                  f"covS={rows[-1]['coverage_stratified']:.3f} "
                  f"wG={rows[-1]['width_global']:.3f} wS={rows[-1]['width_stratified']:.3f}")
    res = pd.DataFrame(rows)
    res.to_csv(OUT, index=False)
    REPORT.write_text(
        f"# Conflict-stratified conformal ({TAG}); target coverage {1-ALPHA:.2f}\n\n"
        + res.round(3).to_markdown(index=False), encoding="utf-8")
    print(f"\nwrote {OUT}\nwrote {REPORT}")


if __name__ == "__main__":
    main()
