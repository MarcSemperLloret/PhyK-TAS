from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
FIG = PAPER / "figures"
FIG.mkdir(exist_ok=True)

PREFIX = "all_viable_min100_full"
REGION_SET = "all_viable_min100"

THRESHOLDS = PAPER / f"region_thresholds_{REGION_SET}.csv"
ASSIGN = PAPER / "dedup_assignments_core_2005_all_sources.csv"
DESC_REGION = PAPER / f"physical_descriptors_region_{REGION_SET}.csv"
PAIR_ALL = PAPER / f"{PREFIX}_pair_summary_all.csv"
PAIR_UNC = PAPER / f"{PREFIX}_pair_uncertainty.csv"
KBS_UNC = PAPER / f"{PREFIX}_kbs_uncertainty.csv"
DECISIONS = PAPER / f"{PREFIX}_transfer_decisions.csv"

OUT_REGION_AUDIT = PAPER / f"{PREFIX}_region_audit.csv"
OUT_SOURCE_ACCURACY = PAPER / f"{PREFIX}_source_accuracy_vs_transfer.csv"
OUT_SOURCE_ACCURACY_SUMMARY = PAPER / f"{PREFIX}_source_accuracy_vs_transfer_summary.csv"
OUT_MODEL_SUMMARY = PAPER / f"{PREFIX}_model_feature_summary.csv"
REPORT = PAPER / f"{PREFIX}_sanity_report.md"

MODEL_ORDER = [
    "regional_doy_climatology",
    "spatial_knn_ridge",
    "linear_window",
    "patchtst_small",
    "stgcn_diffusion",
    "graphwavenet_transfer",
]
FEATURE_ORDER = ["physical_knowledge", "generic_shift", "physical_plus_shift"]
FEATURE_COLORS = {
    "physical_knowledge": "#4C78A8",
    "generic_shift": "#F58518",
    "physical_plus_shift": "#54A24B",
}
DECISION_COLORS = {"deploy": "#54A24B", "adapt": "#F2C94C", "retrain": "#D9534F"}


def selected_assignments() -> pd.DataFrame:
    thresholds = pd.read_csv(THRESHOLDS)
    assign = pd.read_csv(ASSIGN)
    selected = assign.merge(thresholds[["ar6_region", "coverage_threshold"]], on=["ar6_region", "coverage_threshold"])
    return selected.drop_duplicates("canonical_station_uid")


def build_region_audit() -> pd.DataFrame:
    thresholds = pd.read_csv(THRESHOLDS)
    thresholds = thresholds.rename(
        columns={"n_stations": "n_stations_threshold_file", "n_cell5": "n_cell5_threshold_file"}
    )
    selected = selected_assignments()
    source_counts = (
        selected.groupby(["ar6_region", "source_id"])["canonical_station_uid"]
        .nunique()
        .reset_index(name="n")
        .sort_values(["ar6_region", "n"], ascending=[True, False])
    )
    top_sources = (
        source_counts.groupby("ar6_region")
        .apply(lambda g: ", ".join(f"{r.source_id}:{int(r.n)}" for r in g.head(4).itertuples()), include_groups=False)
        .reset_index(name="top_sources")
    )
    region_counts = (
        selected.groupby("ar6_region")
        .agg(
            n_stations=("canonical_station_uid", "nunique"),
            n_cell5=("cell5", "nunique"),
            lat_mean=("latitude", "mean"),
            lon_mean=("longitude", "mean"),
        )
        .reset_index()
    )
    audit = thresholds.merge(region_counts, on="ar6_region", how="left").merge(top_sources, on="ar6_region", how="left")
    audit = audit.sort_values(["n_stations", "ar6_region"], ascending=[False, True])
    audit.to_csv(OUT_REGION_AUDIT, index=False)
    return audit


def build_model_summary() -> pd.DataFrame:
    kbs = pd.read_csv(KBS_UNC)
    focus = kbs[(kbs["cv_kind"] == "group_by_cell") & (kbs["estimator"] == "random_forest")].copy()
    focus["model_order"] = focus["forecast_model"].map({m: i for i, m in enumerate(MODEL_ORDER)}).fillna(999)
    focus["feature_order"] = focus["feature_set"].map({f: i for i, f in enumerate(FEATURE_ORDER)}).fillna(999)
    focus = focus.sort_values(["model_order", "feature_order"])
    best = (
        focus.sort_values(["forecast_model", "r2_mean"], ascending=[True, False])
        .groupby("forecast_model")
        .head(1)
        .rename(columns={"feature_set": "best_feature_set"})
    )
    model_summary = focus.merge(
        best[["forecast_model", "best_feature_set", "r2_mean"]].rename(columns={"r2_mean": "best_r2_mean"}),
        on="forecast_model",
        how="left",
    )
    model_summary.to_csv(OUT_MODEL_SUMMARY, index=False)
    return model_summary


def source_accuracy_check() -> tuple[pd.DataFrame, pd.DataFrame]:
    pair = pd.read_csv(PAIR_ALL)
    in_region = pair[pair["source_region"] == pair["target_region"]][
        ["run_tag", "model", "source_region", "mae_mean", "brier_mean"]
    ].rename(columns={"mae_mean": "source_in_region_mae", "brier_mean": "source_in_region_brier"})
    out = pair[pair["source_region"] != pair["target_region"]].copy()
    out = out.merge(in_region, on=["run_tag", "model", "source_region"], how="left")
    out["abs_degradation"] = out["mae_out_minus_in_mean"].abs()
    rows = []
    for model, group in out.groupby("model"):
        x = group["source_in_region_mae"]
        y = group["mae_out_minus_in_mean"]
        rows.append(
            {
                "model": model,
                "n_pairs": len(group),
                "pearson_source_mae_vs_degradation": float(x.corr(y, method="pearson")),
                "spearman_source_mae_vs_degradation": float(x.corr(y, method="spearman")),
                "pearson_source_mae_vs_abs_degradation": float(x.corr(group["abs_degradation"], method="pearson")),
                "mean_source_in_region_mae": float(x.mean()),
                "mean_degradation": float(y.mean()),
                "max_degradation": float(y.max()),
            }
        )
    summary = pd.DataFrame(rows).sort_values("model")
    out.to_csv(OUT_SOURCE_ACCURACY, index=False)
    summary.to_csv(OUT_SOURCE_ACCURACY_SUMMARY, index=False)
    return out, summary


def plot_kbs_r2(model_summary: pd.DataFrame) -> None:
    focus = model_summary[model_summary["feature_set"].isin(FEATURE_ORDER)].copy()
    models = [m for m in MODEL_ORDER if m in set(focus["forecast_model"])]
    xbase = np.arange(len(models))
    width = 0.24
    fig, ax = plt.subplots(figsize=(12.5, 5.8), dpi=180)
    for i, feature in enumerate(FEATURE_ORDER):
        sub = focus[focus["feature_set"] == feature].set_index("forecast_model").reindex(models)
        x = xbase + (i - 1) * width
        ax.bar(
            x,
            sub["r2_mean"],
            width=width,
            yerr=sub["r2_sd"].fillna(0),
            capsize=3,
            label=feature,
            color=FEATURE_COLORS[feature],
        )
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(xbase, labels=models, rotation=25, ha="right")
    ax.set_ylabel("R2 predicting out-of-region MAE degradation")
    ax.set_title("PhyK-TAS feature sets across all viable AR6 regions")
    ax.legend(frameon=False, ncols=3, loc="upper center", bbox_to_anchor=(0.5, 1.12))
    fig.tight_layout()
    fig.savefig(FIG / "fig_all_viable_kbs_r2_by_model.png")
    plt.close(fig)


def plot_decisions() -> None:
    decisions = pd.read_csv(DECISIONS)
    counts = (
        decisions.groupby(["model", "conservative_decision"])
        .size()
        .reset_index(name="n_pairs")
        .pivot_table(index="model", columns="conservative_decision", values="n_pairs", fill_value=0)
        .reindex([m for m in MODEL_ORDER if m in set(decisions["model"])])
    )
    for col in ["deploy", "adapt", "retrain"]:
        if col not in counts:
            counts[col] = 0
    fig, ax = plt.subplots(figsize=(10.8, 5.4), dpi=180)
    bottom = np.zeros(len(counts))
    x = np.arange(len(counts))
    for decision in ["deploy", "adapt", "retrain"]:
        vals = counts[decision].to_numpy()
        ax.bar(x, vals, bottom=bottom, label=decision, color=DECISION_COLORS[decision])
        bottom += vals
    ax.set_xticks(x, labels=counts.index, rotation=25, ha="right")
    ax.set_ylabel("Number of out-of-region source-target pairs")
    ax.set_title("Conservative deploy/adapt/retrain decisions")
    ax.legend(frameon=False, ncols=3, loc="upper center", bbox_to_anchor=(0.5, 1.12))
    fig.tight_layout()
    fig.savefig(FIG / "fig_all_viable_decision_counts.png")
    plt.close(fig)


def plot_degradation_heatmaps() -> None:
    pair = pd.read_csv(PAIR_UNC)
    regions = pd.read_csv(THRESHOLDS)["ar6_region"].tolist()
    for model in ["spatial_knn_ridge", "stgcn_diffusion", "graphwavenet_transfer"]:
        sub = pair[pair["model"] == model]
        if sub.empty:
            continue
        mat = np.full((len(regions), len(regions)), np.nan)
        for row in sub.itertuples(index=False):
            i = regions.index(row.source_region)
            j = regions.index(row.target_region)
            mat[i, j] = row.degradation_mean
        vmax = max(0.05, float(np.nanpercentile(np.abs(mat), 95)))
        fig, ax = plt.subplots(figsize=(8.2, 7.2), dpi=180)
        im = ax.imshow(mat, cmap="coolwarm", vmin=-vmax, vmax=vmax)
        ax.set_xticks(np.arange(len(regions)), labels=regions, rotation=45, ha="right")
        ax.set_yticks(np.arange(len(regions)), labels=regions)
        ax.set_xlabel("Target region")
        ax.set_ylabel("Source region")
        ax.set_title(f"Mean MAE degradation: {model}")
        for i in range(len(regions)):
            for j in range(len(regions)):
                value = mat[i, j]
                if np.isfinite(value):
                    ax.text(j, i, f"{value:.2f}", ha="center", va="center", fontsize=6.5)
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="MAE out-minus-in")
        fig.tight_layout()
        fig.savefig(FIG / f"fig_all_viable_degradation_heatmap_{model}.png")
        plt.close(fig)


def plot_source_accuracy(source_df: pd.DataFrame) -> None:
    models = [m for m in MODEL_ORDER if m in set(source_df["model"])]
    fig, axes = plt.subplots(2, 3, figsize=(13.5, 8.0), dpi=180, sharex=False, sharey=False)
    axes = axes.ravel()
    for ax, model in zip(axes, models):
        sub = source_df[source_df["model"] == model]
        ax.scatter(
            sub["source_in_region_mae"],
            sub["mae_out_minus_in_mean"],
            s=12,
            alpha=0.45,
            color="#4C78A8",
            linewidths=0,
        )
        r = sub["source_in_region_mae"].corr(sub["mae_out_minus_in_mean"], method="pearson")
        ax.axhline(0, color="black", linewidth=0.8)
        ax.set_title(f"{model}\nr={r:.2f}", fontsize=9)
        ax.set_xlabel("Source in-region MAE")
        ax.set_ylabel("Out-of-region degradation")
    for ax in axes[len(models) :]:
        ax.axis("off")
    fig.suptitle("Source-region accuracy is not a reliable transfer-risk proxy", y=0.99)
    fig.tight_layout()
    fig.savefig(FIG / "fig_all_viable_source_accuracy_vs_transfer.png")
    plt.close(fig)


def plot_region_map(audit: pd.DataFrame) -> None:
    selected = selected_assignments()
    regions = audit["ar6_region"].tolist()
    fig, ax = plt.subplots(figsize=(13.0, 6.7), dpi=180)
    try:
        import geopandas as gpd  # noqa: F401
        import regionmask

        ar6 = regionmask.defined_regions.ar6.land
        gdf = ar6.to_geodataframe()[["abbrevs", "geometry"]].rename(columns={"abbrevs": "ar6_region"})
        gdf.boundary.plot(ax=ax, color="0.75", linewidth=0.35)
        gdf[gdf["ar6_region"].isin(regions)].plot(ax=ax, color="#D9E8F5", edgecolor="#3D5A80", linewidth=0.7)
    except Exception:
        ax.set_facecolor("#F7F7F7")

    for region, group in selected.groupby("ar6_region"):
        ax.scatter(group["longitude"], group["latitude"], s=4, alpha=0.45, label=region, linewidths=0)
    ax.set_xlim(-180, 180)
    ax.set_ylim(-60, 85)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title("All viable AR6 regions and selected station pool")
    ax.legend(frameon=False, ncols=6, fontsize=8, loc="lower center", bbox_to_anchor=(0.5, -0.24))
    fig.tight_layout()
    fig.savefig(FIG / "fig_all_viable_region_map.png")
    plt.close(fig)


def write_report(
    audit: pd.DataFrame,
    model_summary: pd.DataFrame,
    source_summary: pd.DataFrame,
) -> None:
    desc = pd.read_csv(DESC_REGION)
    desc_cols = [
        "ar6_region",
        "wet_day_fraction_gt1mm_mean",
        "wet_day_mean_intensity_mean",
        "dry_spell_p95_days_median",
        "wet_day_p99_median",
        "top3_month_precip_fraction_mean",
    ]
    desc_table = desc[desc_cols].copy()
    best = (
        model_summary.sort_values(["forecast_model", "r2_mean"], ascending=[True, False])
        .groupby("forecast_model")
        .head(1)[
            [
                "forecast_model",
                "feature_set",
                "mae_mean",
                "r2_mean",
                "r2_sd",
                "r2_min",
                "r2_max",
            ]
        ]
        .sort_values("forecast_model")
    )
    decision_counts = (
        pd.read_csv(DECISIONS)
        .groupby(["model", "conservative_decision"])
        .size()
        .reset_index(name="n_pairs")
        .sort_values(["model", "conservative_decision"])
    )
    files = [
        OUT_REGION_AUDIT.name,
        OUT_MODEL_SUMMARY.name,
        OUT_SOURCE_ACCURACY.name,
        OUT_SOURCE_ACCURACY_SUMMARY.name,
        "figures/fig_all_viable_region_map.png",
        "figures/fig_all_viable_kbs_r2_by_model.png",
        "figures/fig_all_viable_decision_counts.png",
        "figures/fig_all_viable_source_accuracy_vs_transfer.png",
        "figures/fig_all_viable_degradation_heatmap_spatial_knn_ridge.png",
        "figures/fig_all_viable_degradation_heatmap_stgcn_diffusion.png",
        "figures/fig_all_viable_degradation_heatmap_graphwavenet_transfer.png",
    ]
    lines = [
        "# All-viable final sanity report",
        "",
        "Scope:",
        "",
        "- Region set: `all_viable_min100`.",
        "- Experiment prefix: `all_viable_min100_full`.",
        "- Runs: 3 seeds, up to 1000 stations per viable AR6 region.",
        "- Out-of-region pairs per model: 110.",
        "",
        "## Region audit",
        "",
        audit.to_markdown(index=False),
        "",
        "## Regional physical descriptor snapshot",
        "",
        desc_table.to_markdown(index=False),
        "",
        "## Best feature set by model",
        "",
        best.to_markdown(index=False),
        "",
        "## Source accuracy versus transfer degradation",
        "",
        source_summary.to_markdown(index=False),
        "",
        "Interpretation: source-region accuracy is at best an incomplete proxy for transfer risk. The sign and magnitude of the correlation vary by model, so deployment assessment needs source-target descriptors rather than source validation alone.",
        "",
        "## Conservative decision counts",
        "",
        decision_counts.to_markdown(index=False),
        "",
        "## Generated artifacts",
        "",
        *[f"- `{name}`" for name in files],
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    audit = build_region_audit()
    model_summary = build_model_summary()
    source_df, source_summary = source_accuracy_check()
    plot_region_map(audit)
    plot_kbs_r2(model_summary)
    plot_decisions()
    plot_degradation_heatmaps()
    plot_source_accuracy(source_df)
    write_report(audit, model_summary, source_summary)
    print(f"wrote {OUT_REGION_AUDIT}")
    print(f"wrote {OUT_MODEL_SUMMARY}")
    print(f"wrote {OUT_SOURCE_ACCURACY}")
    print(f"wrote {OUT_SOURCE_ACCURACY_SUMMARY}")
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
