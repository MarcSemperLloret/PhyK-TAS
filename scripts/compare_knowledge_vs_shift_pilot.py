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
DEG = PAPER / "pilot_light_degradation.csv"
OUT = PAPER / "knowledge_vs_shift_pilot_results.csv"
REPORT = PAPER / "knowledge_vs_shift_pilot_report.md"


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


def evaluate_feature_set(df: pd.DataFrame, feature_cols: list[str], label: str) -> dict:
    y = df["degradation_mean_out_minus_in"].to_numpy()
    groups = df["ar6_region"].to_numpy()
    x = df[feature_cols].replace([np.inf, -np.inf], np.nan)
    x = x.fillna(x.median(numeric_only=True))

    # Leave-one-region-out is the stricter preregistration-relevant view.
    logo = LeaveOneGroupOut()
    ridge = make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-3, 3, 13)))
    pred_ridge = cross_val_predict(ridge, x, y, cv=logo, groups=groups)

    rf = RandomForestRegressor(
        n_estimators=300,
        min_samples_leaf=10,
        random_state=20260523,
        n_jobs=-1,
    )
    pred_rf = cross_val_predict(rf, x, y, cv=logo, groups=groups)

    return {
        "feature_set": label,
        "n": len(df),
        "n_features": len(feature_cols),
        "ridge_logo_mae": mean_absolute_error(y, pred_ridge),
        "ridge_logo_r2": r2_score(y, pred_ridge),
        "rf_logo_mae": mean_absolute_error(y, pred_rf),
        "rf_logo_r2": r2_score(y, pred_rf),
    }


def main() -> None:
    desc = pd.read_csv(DESC)
    deg = pd.read_csv(DEG)
    shift = pd.read_csv(SHIFT)

    # Pilot degradation target is station-level. Use station physical descriptors.
    df = deg.merge(desc, on=["canonical_station_uid", "ar6_region", "cell5"], how="left")

    # The pilot target is mean out-region vs in-region; attach target-region average shift to other regions.
    # This is intentionally simple and conservative for the first KBS-vs-shift sanity check.
    shift_summary = (
        shift[shift["source_region"] != shift["target_region"]]
        .groupby("target_region")[SHIFT_COLS]
        .mean()
        .reset_index()
        .rename(columns={"target_region": "ar6_region"})
    )
    df = df.merge(shift_summary, on="ar6_region", how="left")

    rows = []
    rows.append(evaluate_feature_set(df, PHYSICAL_COLS, "physical_knowledge"))
    rows.append(evaluate_feature_set(df, SHIFT_COLS, "generic_shift"))
    rows.append(evaluate_feature_set(df, PHYSICAL_COLS + SHIFT_COLS, "physical_plus_shift"))
    out = pd.DataFrame(rows)
    out.to_csv(OUT, index=False)

    lines = [
        "# Knowledge vs shift pilot report",
        "",
        "This is a first sanity check using the lightweight climatology degradation target.",
        "",
        "Target:",
        "",
        "- `degradation_mean_out_minus_in` from `pilot_light_degradation.csv`.",
        "",
        "Feature sets:",
        "",
        "- physical knowledge: station-level physical descriptors;",
        "- generic shift: target-region average generic distribution-shift metrics;",
        "- combined: both.",
        "",
        "Validation:",
        "",
        "- leave-one-region-out cross-validation.",
        "",
        "Important caveat:",
        "",
        "- This pilot is not the final preregistered model comparison.",
        "- It checks whether the KBS framing has measurable signal before training heavier models.",
        "",
        "## Results",
        "",
        out.to_markdown(index=False),
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"wrote {REPORT}")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()

