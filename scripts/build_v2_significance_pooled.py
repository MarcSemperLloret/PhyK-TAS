"""Significance of the physical+shift gain, computed on the SAME seed-pooled
group-by-cell pipeline used by build_v2_meta_models / build_v3_fusion, so that
the reported R^2 values are numerically consistent across all tables.

Pools the three station samples, fits one group-by-cell random forest per
feature set, and quantifies uncertainty with a hierarchical bootstrap over
(seed, cell) clusters; compares physical+shift vs generic-shift with a paired
one-sided test, Holm-corrected across the six forecasting models.
"""
from __future__ import annotations

import os
import warnings

import numpy as np
import pandas as pd
from sklearn.metrics import r2_score

warnings.filterwarnings("ignore")

from build_v2_meta_models import (
    PAPER, TAG, SEEDS, PHYSICAL_COLS, SHIFT_COLS, TARGET,
    load_seed, build_splits, oof_predict_sklearn,
)

N_BOOT = int(os.environ.get("PHYKTAS_V2_NBOOT", "2000"))
RNG = np.random.default_rng(20260701)
FEATURES = {"physical": PHYSICAL_COLS, "shift": SHIFT_COLS,
            "combined": PHYSICAL_COLS + SHIFT_COLS}
OUT = PAPER / f"v2_significance_pooled_{TAG}.csv"
REPORT = PAPER / f"v2_significance_pooled_{TAG}_report.md"


def clean(df, cols):
    x = df[cols].replace([np.inf, -np.inf], np.nan)
    return x.fillna(x.median(numeric_only=True)).to_numpy()


def main() -> None:
    df = pd.concat([load_seed(s) for s in SEEDS], ignore_index=True)
    rows = []
    for model, sub in df.groupby("model"):
        sub = sub.reset_index(drop=True)
        y = sub[TARGET].to_numpy()
        splits = build_splits(sub, "group_by_cell")
        cluster = (sub["seed"].astype(str) + "|" + sub["cell5"].astype(str)).to_numpy()
        preds = {k: oof_predict_sklearn("random_forest", clean(sub, c), y, splits)
                 for k, c in FEATURES.items()}
        # hierarchical bootstrap over (seed, cell)
        uniq = np.unique(cluster)
        order = np.argsort(cluster, kind="stable")
        sid = cluster[order]
        starts = np.searchsorted(sid, uniq, "left"); ends = np.searchsorted(sid, uniq, "right")
        rowsby = [order[a:b] for a, b in zip(starts, ends)]
        n = len(uniq)
        bc = np.empty(N_BOOT); bs = np.empty(N_BOOT)
        for b in range(N_BOOT):
            idx = np.concatenate([rowsby[i] for i in RNG.integers(0, n, n)])
            bc[b] = r2_score(y[idx], preds["combined"][idx])
            bs[b] = r2_score(y[idx], preds["shift"][idx])
        delta = bc - bs
        rec = {"model": model,
               "r2_physical": r2_score(y, preds["physical"]),
               "r2_shift": r2_score(y, preds["shift"]),
               "r2_combined": r2_score(y, preds["combined"]),
               "delta_comb_minus_shift": r2_score(y, preds["combined"]) - r2_score(y, preds["shift"]),
               "delta_lo": np.percentile(delta, 2.5),
               "delta_hi": np.percentile(delta, 97.5),
               "p_one_sided": float((delta <= 0).mean())}
        rows.append(rec)
    res = pd.DataFrame(rows)
    # Holm across models
    p = res["p_one_sided"].to_numpy(); order = np.argsort(p); m = len(p)
    adj = np.empty(m); run = 0.0
    for rank, i in enumerate(order):
        run = max(run, (m - rank) * p[i]); adj[i] = min(run, 1.0)
    res["p_holm"] = adj
    res.to_csv(OUT, index=False)
    REPORT.write_text("# Seed-pooled group-by-cell significance\n\n" +
                      res.round(4).to_markdown(index=False), encoding="utf-8")
    print(res.round(4).to_string(index=False))
    print(f"\nwrote {OUT}\nwrote {REPORT}")


if __name__ == "__main__":
    main()
