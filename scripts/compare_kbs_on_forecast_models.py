from __future__ import annotations

from pathlib import Path
import os

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import RidgeCV
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import GroupKFold, LeaveOneGroupOut, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from experiment_config import physical_descriptor_paths, shift_baseline_paths


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
DESC = Path(os.environ.get("PHYKTAS_PHYSICAL_DESCRIPTORS", physical_descriptor_paths()[0]))
SHIFT = Path(os.environ.get("PHYKTAS_SHIFT_BASELINES", shift_baseline_paths()[0]))
if os.environ.get("FORECAST_METRICS"):
    FORECAST_FILES = [Path(p) for p in os.environ["FORECAST_METRICS"].split(";") if p.strip()]
else:
    FORECAST_FILES = [
        PAPER / "forecast_patchtst_station_metrics.csv",
        PAPER / "forecast_baseline_station_metrics.csv",
        PAPER / "forecast_spatial_baseline_station_metrics.csv",
        PAPER / "forecast_stgnn_station_metrics.csv",
        PAPER / "forecast_graphwavenet_station_metrics.csv",
    ]
META = Path(os.environ.get("FORECAST_META", PAPER / "forecast_dataset_operational_sample_metadata.csv"))
EXPERIMENT_TAG = os.environ.get("FORECAST_EXPERIMENT_TAG", "").strip()
SUFFIX = f"_{EXPERIMENT_TAG}" if EXPERIMENT_TAG else ""
OUT = PAPER / f"kbs_forecast_model_comparison{SUFFIX}_results.csv"
PRED = PAPER / f"kbs_forecast_model_comparison{SUFFIX}_predictions.csv"
REPORT = PAPER / f"kbs_forecast_model_comparison{SUFFIX}_report.md"

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


def evaluate(df: pd.DataFrame, cols: list[str], feature_set: str, cv_kind: str, model_name: str):
    y = df["mae_out_minus_in"].to_numpy()
    x = df[cols].replace([np.inf, -np.inf], np.nan)
    x = x.fillna(x.median(numeric_only=True))
    if cv_kind == "leave_target_region_out":
        cv = LeaveOneGroupOut()
        groups = df["target_region"].to_numpy()
    elif cv_kind == "group_by_cell":
        cv = GroupKFold(n_splits=min(5, df["cell5"].nunique()))
        groups = df["cell5"].to_numpy()
    else:
        raise ValueError(cv_kind)

    ridge = make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-3, 3, 13)))
    rf = RandomForestRegressor(
        n_estimators=400,
        min_samples_leaf=10,
        random_state=20260524,
        n_jobs=-1,
    )
    rows = []
    pred_df = df[["station_idx", "source_region", "target_region", "cell5", "mae_out_minus_in", "model"]].copy()
    for estimator_name, estimator in [("ridge", ridge), ("random_forest", rf)]:
        pred = cross_val_predict(estimator, x, y, cv=cv, groups=groups)
        rows.append(
            {
                "forecast_model": model_name,
                "feature_set": feature_set,
                "cv_kind": cv_kind,
                "estimator": estimator_name,
                "n": len(df),
                "n_features": len(cols),
                "mae": mean_absolute_error(y, pred),
                "r2": r2_score(y, pred),
            }
        )
        pred_df[f"{feature_set}_{cv_kind}_{estimator_name}_pred"] = pred
    return rows, pred_df


def main() -> None:
    frames = [pd.read_csv(path) for path in FORECAST_FILES if path.exists()]
    if not frames:
        raise FileNotFoundError("No forecast metric files found.")
    forecast = pd.concat(frames, ignore_index=True)
    forecast = forecast[~(forecast["source_region"] == forecast["target_region"])].copy()
    meta = pd.read_csv(META)[["station_idx", "canonical_station_uid"]]
    forecast = forecast.merge(meta, on="station_idx", how="left")
    desc = pd.read_csv(DESC)
    shift = pd.read_csv(SHIFT)
    df = forecast.merge(
        desc,
        left_on=["canonical_station_uid", "target_region", "cell5"],
        right_on=["canonical_station_uid", "ar6_region", "cell5"],
        how="left",
    ).merge(shift, on=["source_region", "target_region"], how="left")
    df = df[df["mae_out_minus_in"].notna()].copy()

    feature_sets = {
        "physical_knowledge": PHYSICAL_COLS,
        "generic_shift": SHIFT_COLS,
        "physical_plus_shift": PHYSICAL_COLS + SHIFT_COLS,
    }
    rows = []
    pred_models = []
    for forecast_model, sub in df.groupby("model"):
        model_preds = []
        for cv_kind in ["leave_target_region_out", "group_by_cell"]:
            for label, cols in feature_sets.items():
                r, p = evaluate(sub, cols, label, cv_kind, forecast_model)
                rows.extend(r)
                model_preds.append(p)
        key = ["station_idx", "source_region", "target_region", "cell5", "mae_out_minus_in", "model"]
        pred_model = model_preds[0]
        for p in model_preds[1:]:
            pred_model = pred_model.merge(p, on=key, how="left")
        pred_models.append(pred_model)
    results = pd.DataFrame(rows)
    results.to_csv(OUT, index=False)

    # Predictions are wide within model and stacked across forecast models.
    pred = pd.concat(pred_models, ignore_index=True)
    pred.to_csv(PRED, index=False)

    pair = (
        df.groupby(["model", "source_region", "target_region"])
        .agg(n=("station_idx", "nunique"), mean_degradation=("mae_out_minus_in", "mean"))
        .reset_index()
    )

    lines = [
        "# KBS comparison on forecasting models",
        "",
        "Target:",
        "",
        "- `mae_out_minus_in` from forecast station-metric files.",
        "- Only out-of-region rows.",
        "",
        "Forecast models:",
        "",
        "- `linear_window`",
        "- `patchtst_small`",
        "- `regional_doy_climatology`",
        "- `spatial_knn_ridge`",
        "- `stgcn_diffusion`",
        "- `graphwavenet_transfer`",
        "",
        "Feature sets:",
        "",
        "- physical knowledge;",
        "- generic shift;",
        "- physical plus shift.",
        "",
        "## Forecast degradation summary",
        "",
        pair.to_markdown(index=False),
        "",
        "## KBS predictive comparison",
        "",
        results.to_markdown(index=False),
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"wrote {PRED}")
    print(f"wrote {REPORT}")
    print(results.to_string(index=False))


if __name__ == "__main__":
    main()
