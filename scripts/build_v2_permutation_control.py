"""PhyK-TAS v2 -- negative-control permutation test for aligned physical signal.

Permutes the physical-descriptor block across source--target--cell--seed rows,
which preserves the descriptor distribution but destroys its alignment with each
transfer case. If the physical layer carries genuine aligned signal, physical-only
R^2 and the combined layer's gain over the shift-only baseline should both drop
under permutation. Group-by-cell random forest, pooled over the three seeds.
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

N_PERM = int(os.environ.get("PHYKTAS_PERM", "5"))
RNG = np.random.default_rng(20260701)
MODELS = ["spatial_knn_ridge", "stgcn_diffusion", "graphwavenet_transfer",
          "regional_doy_climatology"]

OUT = PAPER / f"v2_permutation_control_{TAG}.csv"
REPORT = PAPER / f"v2_permutation_control_{TAG}_report.md"


def clean(df, cols):
    x = df[cols].replace([np.inf, -np.inf], np.nan)
    return x.fillna(x.median(numeric_only=True)).to_numpy()


def rf_r2(df, cols, splits, y):
    pred = oof_predict_sklearn("random_forest", clean(df, cols), y, splits)
    return r2_score(y, pred)


def main() -> None:
    df = pd.concat([load_seed(s) for s in SEEDS], ignore_index=True)
    rows = []
    for model in MODELS:
        sub = df[df["model"] == model].reset_index(drop=True)
        if sub.empty:
            continue
        y = sub[TARGET].to_numpy()
        splits = build_splits(sub, "group_by_cell")
        r2_phys = rf_r2(sub, PHYSICAL_COLS, splits, y)
        r2_shift = rf_r2(sub, SHIFT_COLS, splits, y)
        r2_comb = rf_r2(sub, PHYSICAL_COLS + SHIFT_COLS, splits, y)
        gain = r2_comb - r2_shift

        perm_phys, perm_comb = [], []
        for _ in range(N_PERM):
            permuted = sub.copy()
            order = RNG.permutation(len(permuted))
            permuted[PHYSICAL_COLS] = sub[PHYSICAL_COLS].to_numpy()[order]
            perm_phys.append(rf_r2(permuted, PHYSICAL_COLS, splits, y))
            perm_comb.append(rf_r2(permuted, PHYSICAL_COLS + SHIFT_COLS, splits, y))
        perm_phys_m = float(np.mean(perm_phys))
        perm_gain_m = float(np.mean(perm_comb)) - r2_shift

        rec = {
            "model": model,
            "r2_phys": r2_phys, "r2_phys_perm": perm_phys_m,
            "phys_signal_loss": r2_phys - perm_phys_m,
            "r2_shift": r2_shift, "r2_comb": r2_comb,
            "combined_gain": gain, "combined_gain_perm": perm_gain_m,
            "gain_loss": gain - perm_gain_m,
        }
        rows.append(rec)
        print(f"{model:24s} phys {r2_phys:.3f}->{perm_phys_m:.3f} (loss {r2_phys-perm_phys_m:+.3f}) | "
              f"gain {gain:.3f}->{perm_gain_m:.3f} (loss {gain-perm_gain_m:+.3f})")
    res = pd.DataFrame(rows)
    res.to_csv(OUT, index=False)
    lines = [f"# PhyK-TAS negative-control permutation ({TAG})", "",
             f"Group-by-cell random forest, {N_PERM} permutations of the physical "
             "block, pooled over seeds. Positive loss = permutation destroys signal.", "",
             res.round(3).to_markdown(index=False), ""]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nwrote {OUT}\nwrote {REPORT}")


if __name__ == "__main__":
    main()
