from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import RidgeCV
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import GroupKFold, LeaveOneGroupOut, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
DESC = PAPER / "physical_descriptors_station.csv"
SHIFT = PAPER / "distribution_shift_baselines.csv"
MATRIX = PAPER / "light_degradation_station.csv"
OUT = PAPER / "knowledge_vs_shift_full_matrix_results.csv"
PRED = PAPER / "knowledge_vs_shift_full_matrix_predictions.csv"
REPORT = PAPER / "knowledge_vs_shift_full_matrix_report.md"


PHYSICAL_COLS = [
    "wet_day_fraction_gt1mm",
    "wet_day_mean_intensity",
    "daily_precip_cv",
    "monthly_climatology_amplitude",
    "top3_month_precip_fraction",
    "occurrence_lag1_autocorr",
    "wet_intensity_lag1_autocorr",
    "dry_spell_mean_days",
    "dry_spell_p95_days",
    "wet_day_p95",
    "wet_day_p99",
    "extreme_tail_ratio_p99_p95",
]

SHIFT_COLS = [
    "kl_source_to_target",
    "kl_target_to_source",
    "wasserstein_precip",
    "mmd_rbf_precip",
    "shift_mean_abs",
    "shift_variance_abs",
    "shift_wet_fraction_abs",
    "shift_p95_abs",
    "shift_p99_abs",
    "shift_monthly_l2",
    "region_centroid_distance_deg",
]


def fit_predict(df: pd.DataFrame, feature_cols: list[str], label: str, cv_kind: str) -> tuple[dict, pd.DataFrame]:
    y = df["mae_out_minus_in"].to_numpy()
    x = df[feature_cols].replace([np.inf, -np.inf], np.nan)
    x = x.fillna(x.median(numeric_only=True))

    if cv_kind == "leave_target_region_out":
        cv = LeaveOneGroupOut()
        groups = df["target_region"].to_numpy()
    elif cv_kind == "group_by_cell":
        n_splits = min(5, df["cell5"].nunique())
        cv = GroupKFold(n_splits=n_splits)
        groups = df["cell5"].to_numpy()
    else:
        raise ValueError(cv_kind)

    ridge = make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-3, 3, 13)))
    rf = RandomForestRegressor(
        n_estimators=400,
        min_samples_leaf=20,
        random_state=20260523,
        n_jobs=-1,
    )
    pred_ridge = cross_val_predict(ridge, x, y, cv=cv, groups=groups)
    pred_rf = cross_val_predict(rf, x, y, cv=cv, groups=groups)

    rows = []
    for model_name, pred in [("ridge", pred_ridge), ("random_forest", pred_rf)]:
        rows.append(
            {
                "feature_set": label,
                "cv_kind": cv_kind,
                "model": model_name,
                "n": len(df),
                "n_features": len(feature_cols),
                "mae": mean_absolute_error(y, pred),
                "r2": r2_score(y, pred),
            }
        )
    pred_df = df[
        [
            "canonical_station_uid",
            "source_region",
            "target_region",
            "cell5",
            "mae_out_minus_in",
        ]
    ].copy()
    pred_df[f"{label}_{cv_kind}_ridge_pred"] = pred_ridge
    pred_df[f"{label}_{cv_kind}_rf_pred"] = pred_rf
    return rows, pred_df


def main() -> None:
    desc = pd.read_csv(DESC)
    shift = pd.read_csv(SHIFT)
    matrix = pd.read_csv(MATRIX)
    matrix = matrix[~matrix["is_in_region"]].copy()

    df = matrix.merge(
        desc,
        left_on=["canonical_station_uid", "target_region", "cell5"],
        right_on=["canonical_station_uid", "ar6_region", "cell5"],
        how="left",
    )
    df = df.merge(shift, on=["source_region", "target_region"], how="left")
    df = df[df["mae_out_minus_in"].notna()].copy()

    feature_sets = {
        "physical_knowledge": PHYSICAL_COLS,
        "generic_shift": SHIFT_COLS,
        "physical_plus_shift": PHYSICAL_COLS + SHIFT_COLS,
    }

    result_rows = []
    pred_parts = []
    for cv_kind in ["leave_target_region_out", "group_by_cell"]:
        for label, cols in feature_sets.items():
            rows, preds = fit_predict(df, cols, label, cv_kind)
            result_rows.extend(rows)
            pred_parts.append(preds)

    results = pd.DataFrame(result_rows)
    results.to_csv(OUT, index=False)

    # Merge prediction columns for audit.
    pred = pred_parts[0]
    key = ["canonical_station_uid", "source_region", "target_region", "cell5", "mae_out_minus_in"]
    for part in pred_parts[1:]:
        pred = pred.merge(part, on=key, how="left")
    pred.to_csv(PRED, index=False)

    by_pair = (
        df.groupby(["source_region", "target_region"])
        .agg(n=("canonical_station_uid", "nunique"), mean_target=("mae_out_minus_in", "mean"))
        .reset_index()
    )

    lines = [
        "# Knowledge vs shift full matrix report",
        "",
        "Target:",
        "",
        "- `mae_out_minus_in` from `light_degradation_station.csv`.",
        "- Only out-of-region source-target rows are used.",
        "",
        "Feature sets:",
        "",
        "- physical knowledge: destination-station physical descriptors;",
        "- generic shift: source-target distribution-shift metrics;",
        "- combined: both.",
        "",
        "Validation:",
        "",
        "- leave-target-region-out;",
        "- grouped by 5 x 5 cell.",
        "",
        "## Source-target target summary",
        "",
        by_pair.to_markdown(index=False),
        "",
        "## Predictive results",
        "",
        results.to_markdown(index=False),
        "",
        "## Interpretation rule",
        "",
        "This is still a light-model result. It can guide the KBS paper framing, but final claims require the preregistered model set.",
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"wrote {PRED}")
    print(f"wrote {REPORT}")
    print(results.to_string(index=False))


if __name__ == "__main__":
    main()

