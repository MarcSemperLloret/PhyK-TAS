from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import GroupKFold, LeaveOneGroupOut, cross_val_predict


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
FIG = PAPER / "figures"
FIG.mkdir(exist_ok=True)

DESC = PAPER / "physical_descriptors_station.csv"
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

FEATURE_GROUPS = {
    "occurrence": ["wet_day_fraction_gt1mm", "occurrence_lag1_autocorr"],
    "intensity": ["wet_day_mean_intensity", "daily_precip_cv", "wet_intensity_lag1_autocorr"],
    "seasonality": ["monthly_climatology_amplitude", "top3_month_precip_fraction"],
    "intermittency": ["dry_spell_mean_days", "dry_spell_p95_days"],
    "extremes": ["wet_day_p95", "wet_day_p99", "extreme_tail_ratio_p99_p95"],
}
PHYSICAL_ALL = [c for cols in FEATURE_GROUPS.values() for c in cols]
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

OUT_ALL = PAPER / "physical_group_ablation_results_all.csv"
OUT_SUMMARY = PAPER / "physical_group_ablation_summary.csv"
REPORT = PAPER / "physical_group_ablation_report.md"


def load_seed(seed_label: str, cfg: dict) -> pd.DataFrame:
    forecast = pd.concat([pd.read_csv(p) for p in cfg["metrics"]], ignore_index=True)
    forecast = forecast[forecast["source_region"] != forecast["target_region"]].copy()
    meta = pd.read_csv(cfg["meta"])[["station_idx", "canonical_station_uid"]]
    desc = pd.read_csv(DESC)
    shift = pd.read_csv(SHIFT)
    df = forecast.merge(meta, on="station_idx", how="left")
    df = df.merge(
        desc,
        left_on=["canonical_station_uid", "target_region", "cell5"],
        right_on=["canonical_station_uid", "ar6_region", "cell5"],
        how="left",
    ).merge(shift, on=["source_region", "target_region"], how="left")
    df["seed_label"] = seed_label
    return df[df["mae_out_minus_in"].notna()].copy()


def evaluate(df: pd.DataFrame, cols: list[str], cv_kind: str) -> tuple[float, float]:
    x = df[cols].replace([np.inf, -np.inf], np.nan)
    x = x.fillna(x.median(numeric_only=True))
    y = df["mae_out_minus_in"].to_numpy()
    if cv_kind == "group_by_cell":
        cv = GroupKFold(n_splits=min(5, df["cell5"].nunique()))
        groups = df["cell5"].to_numpy()
    elif cv_kind == "leave_target_region_out":
        cv = LeaveOneGroupOut()
        groups = df["target_region"].to_numpy()
    else:
        raise ValueError(cv_kind)
    model = RandomForestRegressor(
        n_estimators=400,
        min_samples_leaf=10,
        random_state=20260524,
        n_jobs=-1,
    )
    pred = cross_val_predict(model, x, y, cv=cv, groups=groups)
    return mean_absolute_error(y, pred), r2_score(y, pred)


def plot_summary(summary: pd.DataFrame) -> None:
    sub = summary[
        (summary["cv_kind"] == "group_by_cell")
        & (summary["feature_group"].isin(list(FEATURE_GROUPS) + ["physical_all", "shift_only", "physical_plus_shift"]))
    ].copy()
    order = ["occurrence", "intensity", "seasonality", "intermittency", "extremes", "physical_all", "shift_only", "physical_plus_shift"]
    models = ["graphwavenet_transfer", "stgcn_diffusion"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), dpi=180, sharey=True)
    for ax, model in zip(axes, models):
        rows = sub[sub["forecast_model"] == model].set_index("feature_group").reindex(order)
        ax.barh(np.arange(len(order)), rows["r2_mean"], xerr=rows["r2_sd"].fillna(0), color="#4C78A8")
        ax.axvline(0, color="black", linewidth=0.8)
        ax.set_yticks(np.arange(len(order)), labels=order)
        ax.set_title(model)
        ax.set_xlabel("R2 predicting degradation")
    fig.suptitle("Physical descriptor group ablation, group-by-cell RF")
    fig.tight_layout()
    fig.savefig(FIG / "fig_physical_group_ablation.png")
    plt.close(fig)


def main() -> None:
    rows = []
    feature_sets = dict(FEATURE_GROUPS)
    feature_sets["physical_all"] = PHYSICAL_ALL
    feature_sets["shift_only"] = SHIFT_COLS
    feature_sets["physical_plus_shift"] = PHYSICAL_ALL + SHIFT_COLS

    for seed_label, cfg in SEEDS.items():
        df = load_seed(seed_label, cfg)
        for forecast_model, sub in df.groupby("model"):
            for cv_kind in ["group_by_cell", "leave_target_region_out"]:
                for feature_group, cols in feature_sets.items():
                    mae, r2 = evaluate(sub, cols, cv_kind)
                    rows.append(
                        {
                            "seed_label": seed_label,
                            "forecast_model": forecast_model,
                            "cv_kind": cv_kind,
                            "feature_group": feature_group,
                            "n_features": len(cols),
                            "n": len(sub),
                            "mae": mae,
                            "r2": r2,
                        }
                    )
    results = pd.DataFrame(rows)
    summary = (
        results.groupby(["forecast_model", "cv_kind", "feature_group", "n_features"])
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
    results.to_csv(OUT_ALL, index=False)
    summary.to_csv(OUT_SUMMARY, index=False)
    plot_summary(summary)

    focus = summary[
        (summary["cv_kind"] == "group_by_cell")
        & (summary["forecast_model"].isin(["graphwavenet_transfer", "stgcn_diffusion"]))
    ].sort_values(["forecast_model", "r2_mean"], ascending=[True, False])
    lines = [
        "# Physical group ablation report",
        "",
        "Ablation uses large-seed ST-GNN metrics and random-forest KBS predictors.",
        "",
        "Feature groups:",
        "",
        "- occurrence;",
        "- intensity;",
        "- seasonality;",
        "- intermittency;",
        "- extremes;",
        "- physical_all;",
        "- shift_only;",
        "- physical_plus_shift.",
        "",
        "## Group-by-cell results",
        "",
        focus.to_markdown(index=False),
        "",
        "Figure:",
        "",
        "- `figures/fig_physical_group_ablation.png`",
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT_ALL}")
    print(f"wrote {OUT_SUMMARY}")
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
