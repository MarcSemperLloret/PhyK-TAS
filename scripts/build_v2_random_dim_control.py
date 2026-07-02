"""Equal-dimension random-block control (capacity / dimensionality check).

Complements the permutation control: replaces the physical block with a block of
the SAME dimension filled with random noise. If shift+random matches shift-only
and random-only is near zero, the physical gain cannot be an artifact of simply
adding more columns. Uses a lighter forest (150 trees, 2 draws) since only the
qualitative "adds nothing" conclusion is needed.
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import cross_val_predict, GroupKFold

warnings.filterwarnings("ignore")

from build_v2_meta_models import (
    PAPER, TAG, SEEDS, PHYSICAL_COLS, SHIFT_COLS, TARGET, load_seed,
)

RNG = np.random.default_rng(20260701)
N_DRAW = 2
MODELS = ["spatial_knn_ridge", "stgcn_diffusion", "graphwavenet_transfer",
          "regional_doy_climatology"]
OUT = PAPER / f"v2_random_dim_control_{TAG}.csv"
REPORT = PAPER / f"v2_random_dim_control_{TAG}_report.md"


def rf_r2(X, y, groups):
    est = RandomForestRegressor(n_estimators=150, min_samples_leaf=10,
                                random_state=20260524, n_jobs=-1)
    cv = GroupKFold(n_splits=min(5, len(np.unique(groups))))
    pred = cross_val_predict(est, X, y, cv=cv, groups=groups)
    return r2_score(y, pred)


def clean(df, cols):
    x = df[cols].replace([np.inf, -np.inf], np.nan)
    return x.fillna(x.median(numeric_only=True)).to_numpy()


def main() -> None:
    df = pd.concat([load_seed(s) for s in SEEDS], ignore_index=True)
    rows = []
    for model in MODELS:
        sub = df[df["model"] == model].reset_index(drop=True)
        if sub.empty:
            continue
        y = sub[TARGET].to_numpy()
        g = sub["cell5"].to_numpy()
        Xs = clean(sub, SHIFT_COLS)
        r2_shift = rf_r2(Xs, y, g)
        rand_only, shift_rand = [], []
        for _ in range(N_DRAW):
            R = RNG.standard_normal((len(sub), len(PHYSICAL_COLS)))
            rand_only.append(rf_r2(R, y, g))
            shift_rand.append(rf_r2(np.hstack([Xs, R]), y, g))
        rec = {"model": model, "r2_shift": r2_shift,
               "r2_random_only": float(np.mean(rand_only)),
               "r2_shift_plus_random": float(np.mean(shift_rand))}
        rows.append(rec)
        print(f"{model:24s} shift={r2_shift:.3f} random_only={rec['r2_random_only']:.3f} "
              f"shift+random={rec['r2_shift_plus_random']:.3f}")
    res = pd.DataFrame(rows)
    res.to_csv(OUT, index=False)
    REPORT.write_text("# Equal-dimension random-block control\n\n" +
                      res.round(3).to_markdown(index=False), encoding="utf-8")
    print(f"\nwrote {OUT}\nwrote {REPORT}")


if __name__ == "__main__":
    main()
