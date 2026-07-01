from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score, balanced_accuracy_score, confusion_matrix, mean_absolute_error, r2_score
from sklearn.model_selection import GroupKFold, LeaveOneGroupOut, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import RidgeCV


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
PREFIX = "all_viable_min100_full"
RUN_TAGS = [f"{PREFIX}_s{i}" for i in [1, 2, 3]]

PAIR_ALL = PAPER / f"{PREFIX}_pair_summary_all.csv"
PAIR_UNC = PAPER / f"{PREFIX}_pair_uncertainty.csv"
KBS_UNC = PAPER / f"{PREFIX}_kbs_uncertainty.csv"
DESC = PAPER / "physical_descriptors_station_all_viable_min100.csv"
DESC_REGION = PAPER / "physical_descriptors_region_all_viable_min100.csv"
SHIFT = PAPER / "distribution_shift_baselines_all_viable_min100.csv"

OUT_DECISION_PAIR = PAPER / f"{PREFIX}_decision_validation_pairs.csv"
OUT_DECISION_SUMMARY = PAPER / f"{PREFIX}_decision_validation_summary.csv"
OUT_RELATIVE_KBS = PAPER / f"{PREFIX}_relative_degradation_kbs_results.csv"
OUT_RELATIVE_SUMMARY = PAPER / f"{PREFIX}_relative_degradation_summary.csv"
REPORT = PAPER / f"{PREFIX}_review_response_analyses.md"

MODEL_ORDER = [
    "regional_doy_climatology",
    "spatial_knn_ridge",
    "linear_window",
    "patchtst_small",
    "stgcn_diffusion",
    "graphwavenet_transfer",
]

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

T_CRITICAL_N3 = 4.302652729911275


def classify(score: float, deploy_t: float = 0.010, adapt_t: float = 0.025) -> str:
    if score <= deploy_t:
        return "deploy"
    if score <= adapt_t:
        return "adapt"
    return "retrain"


def best_group_by_cell_features() -> dict[str, str]:
    kbs = pd.read_csv(KBS_UNC)
    focus = kbs[(kbs["cv_kind"] == "group_by_cell") & (kbs["estimator"] == "random_forest")]
    best = focus.sort_values(["forecast_model", "r2_mean"], ascending=[True, False]).groupby("forecast_model").head(1)
    return dict(zip(best["forecast_model"], best["feature_set"]))


def decision_validation() -> tuple[pd.DataFrame, pd.DataFrame]:
    if OUT_DECISION_PAIR.exists() and OUT_DECISION_SUMMARY.exists():
        return pd.read_csv(OUT_DECISION_PAIR), pd.read_csv(OUT_DECISION_SUMMARY)

    best_features = best_group_by_cell_features()
    pair_all = pd.read_csv(PAIR_ALL)
    pair_unc = pd.read_csv(PAIR_UNC)
    observed = pair_unc[pair_unc["source_region"] != pair_unc["target_region"]][
        ["model", "source_region", "target_region", "degradation_mean", "degradation_ci95_halfwidth"]
    ].copy()
    observed["observed_expected_decision"] = observed["degradation_mean"].map(classify)
    observed["observed_conservative_decision"] = (
        observed["degradation_mean"] + observed["degradation_ci95_halfwidth"]
    ).map(classify)

    run_rows = []
    for tag in RUN_TAGS:
        pred_path = PAPER / f"kbs_forecast_model_comparison_{tag}_predictions.csv"
        if not pred_path.exists():
            raise FileNotFoundError(pred_path)
        pred = pd.read_csv(pred_path)
        pred = pred[pred["source_region"] != pred["target_region"]].copy()
        for model, feature in best_features.items():
            col = f"{feature}_group_by_cell_random_forest_pred"
            sub = pred[pred["model"] == model]
            if sub.empty or col not in sub.columns:
                continue
            grouped = (
                sub.groupby(["model", "source_region", "target_region"])[col]
                .mean()
                .reset_index(name="predicted_degradation")
            )
            grouped["run_tag"] = tag
            grouped["feature_set"] = feature
            run_rows.append(grouped)
    pred_runs = pd.concat(run_rows, ignore_index=True)
    pred_pair = (
        pred_runs.groupby(["model", "source_region", "target_region", "feature_set"])
        .agg(
            predicted_degradation_mean=("predicted_degradation", "mean"),
            predicted_degradation_sd=("predicted_degradation", "std"),
            n_runs=("run_tag", "nunique"),
        )
        .reset_index()
    )
    pred_pair["predicted_degradation_sd"] = pred_pair["predicted_degradation_sd"].fillna(0.0)
    pred_pair["predicted_ci95_halfwidth"] = (
        T_CRITICAL_N3 * pred_pair["predicted_degradation_sd"] / np.sqrt(pred_pair["n_runs"].clip(lower=1))
    )
    pred_pair["predicted_expected_decision"] = pred_pair["predicted_degradation_mean"].map(classify)
    pred_pair["predicted_conservative_decision"] = (
        pred_pair["predicted_degradation_mean"] + pred_pair["predicted_ci95_halfwidth"]
    ).map(classify)
    out = pred_pair.merge(observed, on=["model", "source_region", "target_region"], how="left")

    rows = []
    labels = ["deploy", "adapt", "retrain"]
    for model in MODEL_ORDER:
        sub = out[out["model"] == model].copy()
        if sub.empty:
            continue
        for target_col in ["observed_expected_decision", "observed_conservative_decision"]:
            pred_col = "predicted_conservative_decision"
            cm = confusion_matrix(sub[target_col], sub[pred_col], labels=labels)
            unsafe_deploy = int(((sub[pred_col] == "deploy") & (sub[target_col] != "deploy")).sum())
            unnecessary_retrain = int(((sub[pred_col] == "retrain") & (sub[target_col] == "deploy")).sum())
            deploy_n = int((sub[pred_col] == "deploy").sum())
            retrain_n = int((sub[pred_col] == "retrain").sum())
            rows.append(
                {
                    "model": model,
                    "reference": target_col.replace("observed_", "").replace("_decision", ""),
                    "n_pairs": len(sub),
                    "accuracy": accuracy_score(sub[target_col], sub[pred_col]),
                    "balanced_accuracy": balanced_accuracy_score(sub[target_col], sub[pred_col]),
                    "predicted_deploy": deploy_n,
                    "unsafe_deploy": unsafe_deploy,
                    "unsafe_deploy_rate_among_predicted_deploy": unsafe_deploy / deploy_n if deploy_n else 0.0,
                    "predicted_retrain": retrain_n,
                    "unnecessary_retrain": unnecessary_retrain,
                    "unnecessary_retrain_rate_among_predicted_retrain": unnecessary_retrain / retrain_n if retrain_n else 0.0,
                    "confusion_matrix_deploy_adapt_retrain": cm.tolist(),
                }
            )
    summary = pd.DataFrame(rows)
    out.to_csv(OUT_DECISION_PAIR, index=False)
    summary.to_csv(OUT_DECISION_SUMMARY, index=False)
    return out, summary


def station_metric_files() -> list[Path]:
    prefixes = [
        "forecast_baseline",
        "forecast_spatial_baseline",
        "forecast_stgnn",
        "forecast_graphwavenet",
        "forecast_patchtst",
    ]
    files = []
    for tag in RUN_TAGS:
        files.extend(PAPER / f"{prefix}_{tag}_station_metrics.csv" for prefix in prefixes)
    return [path for path in files if path.exists()]


def relative_degradation_kbs() -> tuple[pd.DataFrame, pd.DataFrame]:
    pair = pd.read_csv(PAIR_ALL)
    in_region = pair[pair["source_region"] == pair["target_region"]][
        ["run_tag", "model", "target_region", "mae_mean"]
    ].rename(columns={"mae_mean": "target_in_region_mae"})
    source_in_region = pair[pair["source_region"] == pair["target_region"]][
        ["run_tag", "model", "source_region", "mae_mean"]
    ].rename(columns={"mae_mean": "source_in_region_mae"})
    df = pair[pair["source_region"] != pair["target_region"]].merge(
        in_region, on=["run_tag", "model", "target_region"], how="left"
    ).merge(
        source_in_region, on=["run_tag", "model", "source_region"], how="left"
    )
    df["relative_mae_degradation"] = df["mae_out_minus_in_mean"] / df["target_in_region_mae"].clip(lower=1e-6)
    df["abs_relative_mae_degradation"] = df["relative_mae_degradation"].abs()
    rows = []
    for model, group in df.groupby("model"):
        rows.append(
            {
                "forecast_model": model,
                "n_pairs": len(group),
                "relative_degradation_mean": group["relative_mae_degradation"].mean(),
                "relative_degradation_median": group["relative_mae_degradation"].median(),
                "relative_degradation_p95": group["relative_mae_degradation"].quantile(0.95),
                "pearson_source_mae_vs_relative_degradation": group["source_in_region_mae"].corr(
                    group["relative_mae_degradation"], method="pearson"
                ),
                "spearman_source_mae_vs_relative_degradation": group["source_in_region_mae"].corr(
                    group["relative_mae_degradation"], method="spearman"
                ),
                "pearson_source_mae_vs_abs_relative_degradation": group["source_in_region_mae"].corr(
                    group["abs_relative_mae_degradation"], method="pearson"
                ),
            }
        )
    results = df
    summary = pd.DataFrame(rows).sort_values("forecast_model")
    results.to_csv(OUT_RELATIVE_KBS, index=False)
    summary.to_csv(OUT_RELATIVE_SUMMARY, index=False)
    return results, summary


def write_report(decision_summary: pd.DataFrame, relative_summary: pd.DataFrame) -> None:
    lines = [
        "# Review-response analyses",
        "",
        "## Decision validation",
        "",
        decision_summary.to_markdown(index=False),
        "",
        "## Relative MAE degradation scale check",
        "",
        relative_summary.to_markdown(index=False),
        "",
        "Outputs:",
        "",
        f"- `{OUT_DECISION_PAIR.name}`",
        f"- `{OUT_DECISION_SUMMARY.name}`",
        f"- `{OUT_RELATIVE_KBS.name}`",
        f"- `{OUT_RELATIVE_SUMMARY.name}`",
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    _, decision_summary = decision_validation()
    _, relative_summary = relative_degradation_kbs()
    write_report(decision_summary, relative_summary)
    print(f"wrote {OUT_DECISION_PAIR}")
    print(f"wrote {OUT_DECISION_SUMMARY}")
    print(f"wrote {OUT_RELATIVE_KBS}")
    print(f"wrote {OUT_RELATIVE_SUMMARY}")
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
