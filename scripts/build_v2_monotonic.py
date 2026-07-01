"""PhyK-TAS v2 -- Eje 2: physical/statistical knowledge as monotone constraints.

Distribution-shift descriptors are non-negative magnitudes of source->target
mismatch (KL, Wasserstein, MMD, absolute moment/quantile shifts, centroid
distance). A larger mismatch cannot, in expectation, *reduce* transfer
degradation, so the inferrer should be monotone non-decreasing in each of them.
We impose this as a hard monotonicity constraint on the shift features of a
gradient-boosting inferrer (physical target-descriptors stay unconstrained,
their sign is not universal) and test whether the prior helps -- especially the
leave-target-region-out extrapolation, where unconstrained trees misbehave.
"""
from __future__ import annotations

import os
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import r2_score

warnings.filterwarnings("ignore")

from build_v2_meta_models import (  # reuse the exact data pipeline
    PAPER, TAG, SEEDS, PHYSICAL_COLS, SHIFT_COLS, FEATURES, TARGET,
    load_seed, clean_features, cluster_bootstrap_r2, build_splits,
)

N_BOOT = int(os.environ.get("PHYKTAS_V2_NBOOT", "1000"))
MONO_CST = [0] * len(PHYSICAL_COLS) + [1] * len(SHIFT_COLS)

OUT = PAPER / f"v2_monotonic_{TAG}.csv"
REPORT = PAPER / f"v2_monotonic_{TAG}_report.md"


def gbm(monotonic: bool):
    return HistGradientBoostingRegressor(
        max_iter=400, learning_rate=0.05, random_state=20260524,
        monotonic_cst=MONO_CST if monotonic else None,
    )


def oof(est_factory, X, y, splits):
    pred = np.full(len(y), np.nan)
    for tr, te in splits:
        est = est_factory()
        est.fit(X[tr], y[tr])
        pred[te] = est.predict(X[te])
    return pred


def main() -> None:
    df = pd.concat([load_seed(s) for s in SEEDS], ignore_index=True)
    records = []
    for cv_kind in ["group_by_cell", "leave_target_region_out"]:
        for model, sub in df.groupby("model"):
            sub = sub.reset_index(drop=True)
            X = clean_features(sub).to_numpy()
            y = sub[TARGET].to_numpy()
            cluster = (sub["seed"].astype(str) + "|" + sub["cell5"].astype(str)).to_numpy()
            splits = build_splits(sub, cv_kind)
            for label, mono in [("hist_gbm", False), ("hist_gbm_mono", True)]:
                pred = oof(lambda m=mono: gbm(m), X, y, splits)
                r2 = r2_score(y, pred)
                lo, hi = cluster_bootstrap_r2(y, pred, cluster, N_BOOT)
                records.append({"cv_kind": cv_kind, "forecast_model": model,
                                "estimator": label, "r2": r2, "r2_lo": lo, "r2_hi": hi})
                print(f"{cv_kind:24s} {model:24s} {label:14s} R2={r2:.3f} [{lo:.3f},{hi:.3f}]")
    res = pd.DataFrame(records)
    res.to_csv(OUT, index=False)
    lines = [f"# PhyK-TAS v2 monotonic-constraint comparison ({TAG})", "",
             "Shift features constrained monotone non-decreasing; physical "
             f"descriptors unconstrained. Bootstrap N={N_BOOT}.", ""]
    for cv_kind in ["group_by_cell", "leave_target_region_out"]:
        piv = res[res.cv_kind == cv_kind].pivot_table(
            index="forecast_model", columns="estimator", values="r2")
        piv["delta_mono"] = piv["hist_gbm_mono"] - piv["hist_gbm"]
        lines += [f"## {cv_kind}", "", piv.round(3).to_markdown(), ""]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nwrote {OUT}\nwrote {REPORT}")


if __name__ == "__main__":
    main()
