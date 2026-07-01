"""PhyK-TAS v2: negative controls for physical descriptors.

This analysis asks whether the physical-descriptor gain survives a simple
sanity check: if the physical descriptors are randomly reassigned across rows,
does the physical+shift feature set still look useful? A real physical signal
should degrade under this permutation, while the shift-only baseline should be
unchanged.

No forecasters are retrained. We reuse station-level transfer-degradation
tables and re-fit only the degradation inferrers.
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import GroupKFold, LeaveOneGroupOut

from build_v2_meta_models import (
    PAPER,
    TAG,
    SEEDS,
    PHYSICAL_COLS,
    SHIFT_COLS,
    TARGET,
    load_seed,
    clean_features,
)

N_REPEATS = int(os.environ.get("PHYKTAS_NEG_REPEATS", "5"))
N_TREES = int(os.environ.get("PHYKTAS_NEG_TREES", "120"))
CV_KINDS = os.environ.get("PHYKTAS_NEG_CV", "group_by_cell").split(",")
MODEL_FILTER = [
    m for m in os.environ.get(
        "PHYKTAS_NEG_MODELS",
        "spatial_knn_ridge,stgcn_diffusion,graphwavenet_transfer",
    ).split(",")
    if m
]
RNG = np.random.default_rng(int(os.environ.get("PHYKTAS_NEG_SEED", "20260701")))

OUT = PAPER / f"v2_negative_controls_{TAG}.csv"
REPORT = PAPER / f"v2_negative_controls_{TAG}_report.md"


def make_splits(df: pd.DataFrame, cv_kind: str):
    if cv_kind == "group_by_cell":
        groups = df["cell5"].to_numpy()
        cv = GroupKFold(n_splits=min(5, df["cell5"].nunique()))
    elif cv_kind == "leave_target_region_out":
        groups = df["target_region"].to_numpy()
        cv = LeaveOneGroupOut()
    else:
        raise ValueError(cv_kind)
    return list(cv.split(np.zeros((len(df), 1)), df[TARGET].to_numpy(), groups))


def rf_oof(X: np.ndarray, y: np.ndarray, splits) -> np.ndarray:
    pred = np.full(len(y), np.nan)
    for tr, te in splits:
        est = RandomForestRegressor(
            n_estimators=N_TREES,
            min_samples_leaf=10,
            random_state=20260524,
            n_jobs=-1,
        )
        est.fit(X[tr], y[tr])
        pred[te] = est.predict(X[te])
    return pred


def permute_physical_block(df: pd.DataFrame) -> pd.DataFrame:
    """Permute physical descriptors as a row block, preserving their joint
    distribution but breaking their source-target-cell alignment."""
    out = df.copy()
    perm = RNG.permutation(len(out))
    out.loc[:, PHYSICAL_COLS] = out.loc[perm, PHYSICAL_COLS].to_numpy()
    return out


def feature_frame(df: pd.DataFrame, feature_set: str) -> pd.DataFrame:
    if feature_set == "physical":
        return df[PHYSICAL_COLS]
    if feature_set == "shift":
        return df[SHIFT_COLS]
    if feature_set == "physical_plus_shift":
        return df[PHYSICAL_COLS + SHIFT_COLS]
    raise ValueError(feature_set)


def eval_feature_set(df: pd.DataFrame, feature_set: str, cv_kind: str, permuted: bool) -> dict:
    work = permute_physical_block(df) if permuted else df
    Xdf = feature_frame(work, feature_set)
    X = Xdf.replace([np.inf, -np.inf], np.nan).fillna(Xdf.median(numeric_only=True)).to_numpy()
    y = work[TARGET].to_numpy()
    pred = rf_oof(X, y, make_splits(work, cv_kind))
    return {
        "mae": mean_absolute_error(y, pred),
        "r2": r2_score(y, pred),
    }


def aggregate_for_inference(df: pd.DataFrame) -> pd.DataFrame:
    """Collapse station rows to the source-target-cell-seed unit used by the
    hierarchical uncertainty analysis. This preserves the inference target while
    making repeated negative controls tractable."""
    keys = ["seed", "model", "source_region", "target_region", "cell5"]
    cols = keys + [TARGET] + PHYSICAL_COLS + SHIFT_COLS
    return df[cols].groupby(keys, as_index=False).mean(numeric_only=True)


def main() -> None:
    df = aggregate_for_inference(pd.concat([load_seed(s) for s in SEEDS], ignore_index=True))
    rows = []
    for cv_kind in CV_KINDS:
        for model, sub in df.groupby("model"):
            if MODEL_FILTER and model not in MODEL_FILTER:
                continue
            sub = sub.reset_index(drop=True)
            for feature_set in ["physical", "shift", "physical_plus_shift"]:
                base = eval_feature_set(sub, feature_set, cv_kind, permuted=False)
                rows.append({
                    "cv_kind": cv_kind,
                    "forecast_model": model,
                    "feature_set": feature_set,
                    "control": "observed",
                    "repeat": 0,
                    **base,
                })
                if feature_set != "shift":
                    for rep in range(1, N_REPEATS + 1):
                        ctrl = eval_feature_set(sub, feature_set, cv_kind, permuted=True)
                        rows.append({
                            "cv_kind": cv_kind,
                            "forecast_model": model,
                            "feature_set": feature_set,
                            "control": "permuted_physical",
                            "repeat": rep,
                            **ctrl,
                        })
            print(f"finished {cv_kind} / {model}")

    res = pd.DataFrame(rows)
    res.to_csv(OUT, index=False)

    summary = (
        res.groupby(["cv_kind", "forecast_model", "feature_set", "control"])
        .agg(r2_mean=("r2", "mean"), r2_sd=("r2", "std"), mae_mean=("mae", "mean"))
        .reset_index()
    )
    lines = [
        f"# PhyK-TAS v2 negative controls ({TAG})",
        "",
        f"Random-forest degradation inferrer. Physical descriptors are permuted "
        f"as a block across rows for {N_REPEATS} repeats, preserving their joint "
        "distribution while breaking physical alignment with each transfer row. "
        f"Rows are aggregated to source-target-cell-seed units; RF trees={N_TREES}.",
        "",
        summary.round(4).to_markdown(index=False),
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
