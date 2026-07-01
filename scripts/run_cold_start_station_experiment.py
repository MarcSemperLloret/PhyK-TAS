from __future__ import annotations

from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import RidgeCV
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, r2_score
from sklearn.model_selection import GroupKFold, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
DAILY = ROOT / "Data" / "harmonized" / "precip_daily"
SHIFT = PAPER / "distribution_shift_baselines.csv"

SEEDS = {
    "large_s1": {
        "meta": PAPER / "forecast_dataset_large_metadata.csv",
        "metrics": [
            PAPER / "forecast_graphwavenet_large_station_metrics.csv",
            PAPER / "forecast_stgnn_large_station_metrics.csv",
        ],
    },
    "large_s2": {
        "meta": PAPER / "forecast_dataset_large_large_s2_metadata.csv",
        "metrics": [
            PAPER / "forecast_graphwavenet_large_s2_station_metrics.csv",
            PAPER / "forecast_stgnn_large_s2_station_metrics.csv",
        ],
    },
    "large_s3": {
        "meta": PAPER / "forecast_dataset_large_large_s3_metadata.csv",
        "metrics": [
            PAPER / "forecast_graphwavenet_large_s3_station_metrics.csv",
            PAPER / "forecast_stgnn_large_s3_station_metrics.csv",
        ],
    },
}

WINDOWS = {
    "full_8y": ("2005-01-01", "2012-12-31"),
    "history_5y": ("2008-01-01", "2012-12-31"),
    "history_3y": ("2010-01-01", "2012-12-31"),
    "history_1y": ("2012-01-01", "2012-12-31"),
}

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

METADATA_COLS = ["latitude", "longitude"]
DEPLOY_THRESHOLD = 0.010
ADAPT_THRESHOLD = 0.025

OUT_DESC = PAPER / "cold_start_physical_descriptors_by_window.csv"
OUT_ALL = PAPER / "cold_start_station_results_all.csv"
OUT_SUMMARY = PAPER / "cold_start_station_summary.csv"
OUT_DECISION_ALL = PAPER / "cold_start_station_decision_results_all.csv"
OUT_DECISIONS = PAPER / "cold_start_station_decision_summary.csv"
OUT_PRED = PAPER / "cold_start_station_predictions.csv"
REPORT = PAPER / "cold_start_station_report.md"


def load_seed_metadata() -> pd.DataFrame:
    frames = []
    for seed_label, cfg in SEEDS.items():
        meta = pd.read_csv(cfg["meta"])
        meta["seed_label"] = seed_label
        frames.append(meta)
    meta = pd.concat(frames, ignore_index=True)
    meta[["source_id", "source_station_id"]] = meta["canonical_station_uid"].str.split("::", n=1, expand=True)
    return meta.drop_duplicates(["canonical_station_uid", "source_id", "source_station_id"])


def load_daily(stations: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    con = duckdb.connect()
    frames = []
    for source_id, group in stations.groupby("source_id"):
        ids = pd.DataFrame({"source_station_id": group["source_station_id"].astype(str).unique()})
        con.register("selected_ids", ids)
        glob = str((DAILY / f"source_id={source_id}" / "**" / "*.parquet")).replace("\\", "/")
        q = f"""
        SELECT
          p.source_id,
          p.source_station_id,
          CAST(p.obs_date AS DATE) AS obs_date,
          p.precip_mm
        FROM read_parquet('{glob}', hive_partitioning=true) p
        INNER JOIN selected_ids s USING(source_station_id)
        WHERE CAST(p.obs_date AS DATE) BETWEEN DATE '{start}' AND DATE '{end}'
          AND p.precip_mm IS NOT NULL
        """
        frames.append(con.execute(q).df())
        con.unregister("selected_ids")
    daily = pd.concat(frames, ignore_index=True)
    daily["canonical_station_uid"] = daily["source_id"] + "::" + daily["source_station_id"].astype(str)
    daily = daily.merge(
        stations[["canonical_station_uid", "ar6_region", "cell5", "latitude", "longitude"]],
        on="canonical_station_uid",
        how="inner",
    )
    daily["obs_date"] = pd.to_datetime(daily["obs_date"])
    daily["month"] = daily["obs_date"].dt.month
    return daily


def lag1_autocorr(values: np.ndarray) -> float:
    values = values.astype(float)
    if len(values) < 3:
        return float("nan")
    x = values[:-1]
    y = values[1:]
    if np.nanstd(x) == 0 or np.nanstd(y) == 0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def dry_spell_stats(dates: pd.Series, precip: np.ndarray, start: str, end: str) -> tuple[float, float]:
    df = pd.DataFrame({"date": pd.to_datetime(dates), "precip": precip}).sort_values("date")
    full = pd.DataFrame({"date": pd.date_range(start, end, freq="D")})
    df = full.merge(df, on="date", how="left")
    dry = (df["precip"].fillna(np.nan) <= 1.0).to_numpy()
    observed = df["precip"].notna().to_numpy()
    runs = []
    current = 0
    for is_dry, is_obs in zip(dry, observed):
        if not is_obs:
            if current:
                runs.append(current)
                current = 0
            continue
        if is_dry:
            current += 1
        elif current:
            runs.append(current)
            current = 0
    if current:
        runs.append(current)
    if not runs:
        return float("nan"), float("nan")
    return float(np.mean(runs)), float(np.percentile(runs, 95))


def station_descriptors(daily: pd.DataFrame, start: str, end: str, window_label: str) -> pd.DataFrame:
    rows = []
    for uid, g in daily.groupby("canonical_station_uid", sort=False):
        p = g["precip_mm"].to_numpy(dtype=float)
        wet = p > 1.0
        wet_vals = p[wet]
        monthly = g.groupby("month")["precip_mm"].sum().reindex(range(1, 13), fill_value=0.0)
        total = float(monthly.sum())
        top3_frac = float(monthly.sort_values(ascending=False).head(3).sum() / total) if total > 0 else np.nan
        intensity = np.where(wet, p, np.nan)
        intensity_valid = intensity[np.isfinite(intensity)]
        dry_mean, dry_p95 = dry_spell_stats(g["obs_date"], p, start, end)
        p95 = float(np.percentile(wet_vals, 95)) if len(wet_vals) else np.nan
        p99 = float(np.percentile(wet_vals, 99)) if len(wet_vals) else np.nan
        rows.append(
            {
                "window_label": window_label,
                "canonical_station_uid": uid,
                "ar6_region": g["ar6_region"].iloc[0],
                "cell5": g["cell5"].iloc[0],
                "latitude": float(g["latitude"].iloc[0]),
                "longitude": float(g["longitude"].iloc[0]),
                "n_obs_descriptor": int(len(g)),
                "wet_day_fraction_gt1mm": float(np.mean(wet)),
                "wet_day_mean_intensity": float(np.mean(wet_vals)) if len(wet_vals) else np.nan,
                "daily_precip_cv": float(np.std(p) / np.mean(p)) if np.mean(p) > 0 else np.nan,
                "monthly_climatology_amplitude": float(monthly.max() - monthly.min()),
                "top3_month_precip_fraction": top3_frac,
                "occurrence_lag1_autocorr": lag1_autocorr(wet.astype(float)),
                "wet_intensity_lag1_autocorr": lag1_autocorr(intensity_valid) if len(intensity_valid) > 3 else np.nan,
                "dry_spell_mean_days": dry_mean,
                "dry_spell_p95_days": dry_p95,
                "wet_day_p95": p95,
                "wet_day_p99": p99,
                "extreme_tail_ratio_p99_p95": float(p99 / p95) if p95 and p95 > 0 else np.nan,
            }
        )
    return pd.DataFrame(rows)


def build_or_load_descriptors() -> pd.DataFrame:
    if OUT_DESC.exists():
        return pd.read_csv(OUT_DESC)
    stations = load_seed_metadata()
    frames = []
    for window_label, (start, end) in WINDOWS.items():
        daily = load_daily(stations, start, end)
        frames.append(station_descriptors(daily, start, end, window_label))
    desc = pd.concat(frames, ignore_index=True)
    desc.to_csv(OUT_DESC, index=False)
    return desc


def load_seed_dataset(seed_label: str, cfg: dict, desc: pd.DataFrame) -> pd.DataFrame:
    forecast = pd.concat([pd.read_csv(path) for path in cfg["metrics"]], ignore_index=True)
    forecast = forecast[forecast["source_region"] != forecast["target_region"]].copy()
    meta = pd.read_csv(cfg["meta"])[
        ["station_idx", "canonical_station_uid", "ar6_region", "cell5", "latitude", "longitude"]
    ]
    shift = pd.read_csv(SHIFT)
    df = forecast.merge(meta, on=["station_idx", "cell5"], how="left", suffixes=("", "_meta"))
    df = df.merge(shift, on=["source_region", "target_region"], how="left")
    df["seed_label"] = seed_label
    df = df[df["mae_out_minus_in"].notna()].copy()
    frames = []
    for window_label in WINDOWS:
        sub_desc = desc[desc["window_label"] == window_label]
        sub = df.merge(
            sub_desc,
            left_on=["canonical_station_uid", "target_region", "cell5"],
            right_on=["canonical_station_uid", "ar6_region", "cell5"],
            how="left",
            suffixes=("", "_desc"),
        )
        sub["cold_start_setting"] = window_label
        frames.append(sub)
    metadata = df.copy()
    metadata["cold_start_setting"] = "metadata_plus_shift"
    frames.append(metadata)
    return pd.concat(frames, ignore_index=True)


def decision_class(values: np.ndarray) -> np.ndarray:
    return np.where(values <= DEPLOY_THRESHOLD, "deploy", np.where(values <= ADAPT_THRESHOLD, "adapt", "retrain"))


def evaluate_ml(sub: pd.DataFrame, cols: list[str], estimator_name: str):
    x = sub[cols].replace([np.inf, -np.inf], np.nan)
    x = x.fillna(x.median(numeric_only=True))
    y = sub["mae_out_minus_in"].to_numpy()
    cv = GroupKFold(n_splits=min(5, sub["cell5"].nunique()))
    groups = sub["cell5"].to_numpy()
    if estimator_name == "ridge":
        estimator = make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-3, 3, 13)))
    elif estimator_name == "random_forest":
        estimator = RandomForestRegressor(
            n_estimators=300,
            min_samples_leaf=10,
            random_state=20260524,
            n_jobs=-1,
        )
    elif estimator_name == "hist_gradient_boosting":
        estimator = HistGradientBoostingRegressor(
            max_iter=300,
            learning_rate=0.04,
            min_samples_leaf=20,
            random_state=20260524,
        )
    else:
        raise ValueError(estimator_name)
    pred = cross_val_predict(estimator, x, y, cv=cv, groups=groups)
    return pred


def evaluate_pair_prior(sub: pd.DataFrame) -> np.ndarray:
    y = sub["mae_out_minus_in"].to_numpy()
    pred = np.full(len(sub), np.nan)
    cv = GroupKFold(n_splits=min(5, sub["cell5"].nunique()))
    groups = sub["cell5"].to_numpy()
    keys = ["source_region", "target_region"]
    for train_idx, test_idx in cv.split(sub, y, groups):
        train = sub.iloc[train_idx]
        test = sub.iloc[test_idx]
        pair_mean = train.groupby(keys)["mae_out_minus_in"].mean()
        global_mean = float(train["mae_out_minus_in"].mean())
        pred[test_idx] = [
            float(pair_mean.get((row.source_region, row.target_region), global_mean))
            for row in test[["source_region", "target_region"]].itertuples(index=False)
        ]
    return pred


def summarize_predictions(frame: pd.DataFrame, pred: np.ndarray, estimator_name: str, n_features: int) -> tuple[dict, dict, pd.DataFrame]:
    y = frame["mae_out_minus_in"].to_numpy()
    observed = decision_class(y)
    predicted = decision_class(pred)
    result = {
        "seed_label": frame["seed_label"].iloc[0],
        "forecast_model": frame["model"].iloc[0],
        "cold_start_setting": frame["cold_start_setting"].iloc[0],
        "estimator": estimator_name,
        "n": len(frame),
        "n_features": n_features,
        "mae": mean_absolute_error(y, pred),
        "r2": r2_score(y, pred),
    }
    decision = {
        **{k: result[k] for k in ["seed_label", "forecast_model", "cold_start_setting", "estimator", "n"]},
        "decision_accuracy": accuracy_score(observed, predicted),
        "decision_f1_macro": f1_score(observed, predicted, labels=["deploy", "adapt", "retrain"], average="macro"),
        "false_deploy_rate": float(np.mean((predicted == "deploy") & (observed != "deploy"))),
        "false_retrain_rate": float(np.mean((predicted == "retrain") & (observed != "retrain"))),
        "stable_decision_rate": float(np.mean(observed == predicted)),
    }
    pred_df = frame[
        [
            "seed_label",
            "model",
            "station_idx",
            "canonical_station_uid",
            "source_region",
            "target_region",
            "cell5",
            "cold_start_setting",
            "mae_out_minus_in",
        ]
    ].copy()
    pred_df["estimator"] = estimator_name
    pred_df["predicted_degradation"] = pred
    pred_df["observed_decision"] = observed
    pred_df["predicted_decision"] = predicted
    return result, decision, pred_df


def main() -> None:
    desc = build_or_load_descriptors()
    rows = []
    decision_rows = []
    pred_frames = []

    for seed_label, cfg in SEEDS.items():
        df = load_seed_dataset(seed_label, cfg, desc)
        for (forecast_model, setting), sub in df.groupby(["model", "cold_start_setting"], sort=False):
            if setting in WINDOWS:
                cols = PHYSICAL_COLS + SHIFT_COLS
                estimators = ["ridge", "random_forest", "hist_gradient_boosting"]
            else:
                cols = METADATA_COLS + SHIFT_COLS
                estimators = ["ridge", "random_forest", "hist_gradient_boosting"]
            for estimator_name in estimators:
                pred = evaluate_ml(sub, cols, estimator_name)
                result, decision, pred_df = summarize_predictions(sub, pred, estimator_name, len(cols))
                rows.append(result)
                decision_rows.append(decision)
                pred_frames.append(pred_df)

            pred = evaluate_pair_prior(sub)
            result, decision, pred_df = summarize_predictions(sub, pred, "region_pair_prior", 2)
            rows.append(result)
            decision_rows.append(decision)
            pred_frames.append(pred_df)

    results = pd.DataFrame(rows)
    decisions = pd.DataFrame(decision_rows)
    predictions = pd.concat(pred_frames, ignore_index=True)

    summary = (
        results.groupby(["forecast_model", "cold_start_setting", "estimator", "n_features"])
        .agg(
            n_seeds=("seed_label", "nunique"),
            mae_mean=("mae", "mean"),
            mae_sd=("mae", "std"),
            r2_mean=("r2", "mean"),
            r2_sd=("r2", "std"),
            r2_min=("r2", "min"),
            r2_max=("r2", "max"),
        )
        .reset_index()
    )
    decision_summary = (
        decisions.groupby(["forecast_model", "cold_start_setting", "estimator"])
        .agg(
            n_seeds=("seed_label", "nunique"),
            decision_accuracy_mean=("decision_accuracy", "mean"),
            decision_accuracy_sd=("decision_accuracy", "std"),
            decision_f1_macro_mean=("decision_f1_macro", "mean"),
            false_deploy_rate_mean=("false_deploy_rate", "mean"),
            false_retrain_rate_mean=("false_retrain_rate", "mean"),
            stable_decision_rate_mean=("stable_decision_rate", "mean"),
        )
        .reset_index()
    )

    results.to_csv(OUT_ALL, index=False)
    summary.to_csv(OUT_SUMMARY, index=False)
    decisions.to_csv(OUT_DECISION_ALL, index=False)
    decision_summary.to_csv(OUT_DECISIONS, index=False)
    predictions.to_csv(OUT_PRED, index=False)

    focus = summary[
        (summary["estimator"].isin(["random_forest", "hist_gradient_boosting", "region_pair_prior"]))
        & (summary["forecast_model"].isin(["graphwavenet_transfer", "stgcn_diffusion"]))
    ].sort_values(["forecast_model", "estimator", "cold_start_setting"])
    decision_focus = decision_summary[
        (decision_summary["estimator"].isin(["random_forest", "hist_gradient_boosting", "region_pair_prior"]))
        & (decision_summary["forecast_model"].isin(["graphwavenet_transfer", "stgcn_diffusion"]))
    ].sort_values(["forecast_model", "estimator", "cold_start_setting"])

    lines = [
        "# Target-station cold-start experiment",
        "",
        "This experiment evaluates whether the KBS degradation inference layer remains useful when target-station",
        "physical descriptors are computed from progressively shorter pre-test histories.",
        "",
        "Settings:",
        "",
        "- `full_8y`: descriptors from 2005-2012;",
        "- `history_5y`: descriptors from 2008-2012;",
        "- `history_3y`: descriptors from 2010-2012;",
        "- `history_1y`: descriptors from 2012 only;",
        "- `metadata_plus_shift`: latitude, longitude, and region-level shift descriptors;",
        "- `region_pair_prior`: source-target pair mean estimated inside each group-by-cell fold.",
        "",
        "Decision thresholds: deploy <= 0.010 MAE degradation, adapt <= 0.025, retrain otherwise.",
        "",
        "## Regression summary",
        "",
        focus.to_markdown(index=False),
        "",
        "## Decision summary",
        "",
        decision_focus.to_markdown(index=False),
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")

    print(f"wrote {OUT_DESC}")
    print(f"wrote {OUT_ALL}")
    print(f"wrote {OUT_SUMMARY}")
    print(f"wrote {OUT_DECISION_ALL}")
    print(f"wrote {OUT_DECISIONS}")
    print(f"wrote {OUT_PRED}")
    print(f"wrote {REPORT}")
    print(focus.to_string(index=False))


if __name__ == "__main__":
    main()
