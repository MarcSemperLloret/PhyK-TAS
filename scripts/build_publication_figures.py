from __future__ import annotations

from pathlib import Path
from string import ascii_uppercase

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
FIG_DIRS = [PAPER / "figures", PAPER / "manuscript_latex" / "figures"]
for fig_dir in FIG_DIRS:
    fig_dir.mkdir(exist_ok=True)

PREFIX = "all_viable_min100_full"

KBS_UNC = PAPER / f"{PREFIX}_kbs_uncertainty.csv"
PAIR_UNC = PAPER / f"{PREFIX}_pair_uncertainty.csv"
PAIR_ALL = PAPER / f"{PREFIX}_pair_summary_all.csv"
DECISIONS = PAPER / f"{PREFIX}_transfer_decisions.csv"
THRESHOLDS = PAPER / "region_thresholds_all_viable_min100.csv"
SOURCE_ACCURACY = PAPER / f"{PREFIX}_source_accuracy_vs_transfer.csv"
THRESHOLD_SENSITIVITY = PAPER / f"{PREFIX}_threshold_sensitivity.csv"
ASSIGN = PAPER / "dedup_assignments_core_2005_all_sources.csv"

MODEL_ORDER = [
    "regional_doy_climatology",
    "spatial_knn_ridge",
    "linear_window",
    "patchtst_small",
    "stgcn_diffusion",
    "graphwavenet_transfer",
]

MODEL_LABELS = {
    "regional_doy_climatology": "Regional\nclimatology",
    "spatial_knn_ridge": "Spatial\nkNN-ridge",
    "linear_window": "Linear\nwindow",
    "patchtst_small": "PatchTST\nsmall",
    "stgcn_diffusion": "STGCN\ndiffusion",
    "graphwavenet_transfer": "Graph WaveNet\ntransfer",
}

FEATURE_ORDER = ["physical_knowledge", "generic_shift", "physical_plus_shift"]
FEATURE_LABELS = {
    "physical_knowledge": "Physical",
    "generic_shift": "Generic shift",
    "physical_plus_shift": "Physical + shift",
}

FEATURE_COLORS = {
    "physical_knowledge": "#0072B2",
    "generic_shift": "#E69F00",
    "physical_plus_shift": "#009E73",
}

DECISION_ORDER = ["deploy", "adapt", "retrain"]
DECISION_LABELS = {"deploy": "Deploy", "adapt": "Adapt", "retrain": "Retrain"}
DECISION_COLORS = {"deploy": "#009E73", "adapt": "#F0E442", "retrain": "#D55E00"}

REGION_NAMES = {
    "WCE": "Western & Central Europe",
    "NEU": "Northern Europe",
    "WNA": "Western North America",
    "ENA": "Eastern North America",
    "CNA": "Central North America",
    "SAU": "Southern Australia",
    "MED": "Mediterranean",
    "EAU": "Eastern Australia",
    "NWN": "Northwestern North America",
    "NCA": "Northern Central America",
    "EAS": "East Asia",
}

REGION_COLORS = {
    "WCE": "#00A1D5",
    "NEU": "#D55E00",
    "WNA": "#0072B2",
    "ENA": "#E69F00",
    "CNA": "#009E73",
    "SAU": "#CC79A7",
    "MED": "#F0E442",
    "EAU": "#56B4E9",
    "NWN": "#999999",
    "NCA": "#8F6BB1",
    "EAS": "#7CAE00",
}


def configure_style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
            "font.size": 8.5,
            "axes.labelsize": 10,
            "axes.titlesize": 10,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 8,
            "figure.titlesize": 10,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.linewidth": 0.8,
            "xtick.major.width": 0.7,
            "ytick.major.width": 0.7,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.04,
        }
    )


def save_figure(fig: plt.Figure, name: str) -> None:
    for fig_dir in FIG_DIRS:
        fig.savefig(fig_dir / f"{name}.png")
        fig.savefig(fig_dir / f"{name}.pdf")
    plt.close(fig)


def add_panel_label(ax: plt.Axes, label: str) -> None:
    ax.text(
        -0.08,
        1.04,
        label,
        transform=ax.transAxes,
        fontsize=10,
        fontweight="bold",
        va="bottom",
        ha="right",
    )


def figure_graphical_abstract() -> None:
    fig, ax = plt.subplots(figsize=(10.0, 4.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    steps = [
        ("Station\narchives", "AR6 regions\nand temporal splits", "#0072B2"),
        ("Regime\nknowledge", "Physical descriptors\nplus shift metrics", "#009E73"),
        ("Transfer\nexperiments", "Six forecasters\nacross 110 pairs", "#E69F00"),
        ("PhyK-TAS\ninference", "Degradation risk\nfor each transfer", "#CC79A7"),
        ("Deployment\ndecision", "Deploy, adapt,\nor retrain", "#D55E00"),
    ]
    xs = np.linspace(0.10, 0.90, len(steps))
    box_w = 0.145
    box_h = 0.38
    y = 0.52

    for i, (title, subtitle, color) in enumerate(steps):
        box = FancyBboxPatch(
            (xs[i] - box_w / 2, y - box_h / 2),
            box_w,
            box_h,
            boxstyle="round,pad=0.018,rounding_size=0.018",
            facecolor="white",
            edgecolor=color,
            linewidth=1.8,
        )
        ax.add_patch(box)
        ax.text(xs[i], y + 0.075, title, ha="center", va="center", fontsize=14, fontweight="bold", color="#222222")
        ax.text(xs[i], y - 0.095, subtitle, ha="center", va="center", fontsize=10.5, color="#333333", linespacing=1.15)
        if i < len(steps) - 1:
            arrow = FancyArrowPatch(
                (xs[i] + box_w / 2 + 0.012, y),
                (xs[i + 1] - box_w / 2 - 0.012, y),
                arrowstyle="-|>",
                mutation_scale=16,
                linewidth=1.3,
                color="#555555",
            )
            ax.add_patch(arrow)

    ax.text(
        0.5,
        0.91,
        "PhyK-TAS: physically informed transferability assessment for precipitation forecasters",
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold",
        color="#111111",
    )
    ax.text(
        0.5,
        0.14,
        "Core result: physical regime knowledge adds model-dependent transfer-risk signal beyond source-region accuracy.",
        ha="center",
        va="center",
        fontsize=12,
        color="#222222",
    )

    for fig_dir in FIG_DIRS:
        fig.savefig(fig_dir / "graphical_abstract.png", dpi=300, bbox_inches="tight", pad_inches=0.05)
        fig.savefig(fig_dir / "graphical_abstract.pdf", bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


def selected_assignments() -> pd.DataFrame:
    thresholds = pd.read_csv(THRESHOLDS)
    assign = pd.read_csv(ASSIGN)
    return assign.merge(thresholds[["ar6_region", "coverage_threshold"]], on=["ar6_region", "coverage_threshold"])


def figure_region_map() -> None:
    selected = selected_assignments().drop_duplicates("canonical_station_uid")
    thresholds = pd.read_csv(THRESHOLDS)
    regions = thresholds["ar6_region"].tolist()
    counts = selected.groupby("ar6_region")["canonical_station_uid"].nunique().to_dict()

    fig = plt.figure(figsize=(8.0, 4.7))
    gs = gridspec.GridSpec(1, 2, width_ratios=[3.35, 1.2], wspace=0.04)
    ax = fig.add_subplot(gs[0, 0])
    key_ax = fig.add_subplot(gs[0, 1])

    try:
        import regionmask

        ar6 = regionmask.defined_regions.ar6.land
        gdf = ar6.to_geodataframe()[["abbrevs", "geometry"]].rename(columns={"abbrevs": "ar6_region"})
        gdf.boundary.plot(ax=ax, color="0.78", linewidth=0.35)
        for region in regions:
            gdf[gdf["ar6_region"] == region].plot(
                ax=ax,
                color=REGION_COLORS.get(region, "#DDDDDD"),
                alpha=0.18,
                edgecolor=REGION_COLORS.get(region, "0.4"),
                linewidth=0.8,
            )
    except Exception:
        ax.set_facecolor("#FAFAFA")

    for region in regions:
        group = selected[selected["ar6_region"] == region]
        ax.scatter(
            group["longitude"],
            group["latitude"],
            s=3.0,
            alpha=0.42,
            color=REGION_COLORS.get(region, "#555555"),
            linewidths=0,
        )

    label_offsets = {
        "WCE": (2, 4),
        "NEU": (0, 6),
        "MED": (0, -5),
        "NWN": (-2, 8),
        "WNA": (-3, 2),
        "CNA": (0, -3),
        "ENA": (4, 1),
        "NCA": (0, -6),
        "EAU": (3, 3),
        "SAU": (0, -5),
        "EAS": (3, 5),
    }
    for region in regions:
        group = selected[selected["ar6_region"] == region]
        if group.empty:
            continue
        x = group["longitude"].median() + label_offsets.get(region, (0, 0))[0]
        y = group["latitude"].median() + label_offsets.get(region, (0, 0))[1]
        ax.text(
            x,
            y,
            region,
            ha="center",
            va="center",
            fontsize=8.5,
            fontweight="bold",
            color="black",
            bbox={"boxstyle": "round,pad=0.18", "facecolor": "white", "edgecolor": "0.65", "alpha": 0.86, "linewidth": 0.5},
        )

    ax.set_xlim(-175, 165)
    ax.set_ylim(-55, 82)
    ax.set_aspect("auto")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(color="0.90", linewidth=0.4)
    ax.set_axisbelow(True)

    key_ax.axis("off")
    key_ax.text(0.0, 0.98, "AR6 region key", fontsize=10, fontweight="bold", va="top")
    y = 0.90
    for region in regions:
        key_ax.scatter(0.02, y, s=42, color=REGION_COLORS.get(region, "#555555"), alpha=0.85)
        key_ax.text(0.08, y + 0.012, region, fontsize=8.5, fontweight="bold", va="center")
        key_ax.text(0.08, y - 0.023, f"{REGION_NAMES[region]} ({counts.get(region, 0):,} stations)", fontsize=7.5, va="center")
        y -= 0.076
    key_ax.set_xlim(0, 1)
    key_ax.set_ylim(0, 1)

    save_figure(fig, "fig_all_viable_region_map")


def figure_kbs_r2() -> None:
    kbs = pd.read_csv(KBS_UNC)
    focus = kbs[(kbs["cv_kind"] == "group_by_cell") & (kbs["estimator"] == "random_forest")].copy()
    focus["model_order"] = focus["forecast_model"].map({m: i for i, m in enumerate(MODEL_ORDER)})
    focus["feature_order"] = focus["feature_set"].map({f: i for i, f in enumerate(FEATURE_ORDER)})
    focus = focus.sort_values(["model_order", "feature_order"])

    models = [m for m in MODEL_ORDER if m in set(focus["forecast_model"])]
    xbase = np.arange(len(models))
    width = 0.24
    fig, ax = plt.subplots(figsize=(7.2, 3.6))

    for i, feature in enumerate(FEATURE_ORDER):
        sub = focus[focus["feature_set"] == feature].set_index("forecast_model").reindex(models)
        x = xbase + (i - 1) * width
        ax.bar(
            x,
            sub["r2_mean"],
            width=width,
            yerr=sub["r2_sd"].fillna(0),
            capsize=2.5,
            linewidth=0.4,
            edgecolor="white",
            label=FEATURE_LABELS[feature],
            color=FEATURE_COLORS[feature],
        )

    ax.axhline(0, color="0.25", linewidth=0.8)
    ax.set_xticks(xbase, labels=[MODEL_LABELS[m] for m in models])
    ax.set_ylabel(r"$R^2$ for degradation prediction")
    ax.set_ylim(-0.28, 1.04)
    ax.legend(frameon=False, ncols=3, loc="upper center", bbox_to_anchor=(0.5, 1.17))
    ax.grid(axis="y", color="0.9", linewidth=0.6)
    ax.set_axisbelow(True)
    save_figure(fig, "fig_all_viable_kbs_r2_by_model")


def figure_decisions() -> None:
    decisions = pd.read_csv(DECISIONS)
    counts = (
        decisions.groupby(["model", "conservative_decision"])
        .size()
        .reset_index(name="n_pairs")
        .pivot_table(index="model", columns="conservative_decision", values="n_pairs", fill_value=0)
        .reindex([m for m in MODEL_ORDER if m in set(decisions["model"])])
    )
    for decision in DECISION_ORDER:
        if decision not in counts:
            counts[decision] = 0

    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    y = np.arange(len(counts))
    left = np.zeros(len(counts))
    for decision in DECISION_ORDER:
        vals = counts[decision].to_numpy()
        ax.barh(
            y,
            vals,
            left=left,
            label=DECISION_LABELS[decision],
            color=DECISION_COLORS[decision],
            edgecolor="white",
            linewidth=0.5,
        )
        for yi, val, start in zip(y, vals, left):
            if val >= 8:
                ax.text(start + val / 2, yi, f"{int(val)}", ha="center", va="center", fontsize=7)
        left += vals

    ax.set_yticks(y, labels=[MODEL_LABELS[m].replace("\n", " ") for m in counts.index])
    ax.invert_yaxis()
    ax.set_xlabel("Out-of-region source-target pairs")
    ax.set_xlim(0, 110)
    ax.legend(frameon=False, ncols=3, loc="upper center", bbox_to_anchor=(0.5, 1.15))
    ax.grid(axis="x", color="0.9", linewidth=0.6)
    ax.set_axisbelow(True)
    save_figure(fig, "fig_all_viable_decision_counts")


def heatmap_matrix(pair: pd.DataFrame, model: str, regions: list[str]) -> np.ndarray:
    sub = pair[pair["model"] == model]
    mat = np.full((len(regions), len(regions)), np.nan)
    for row in sub.itertuples(index=False):
        mat[regions.index(row.source_region), regions.index(row.target_region)] = row.degradation_mean
    return mat


def figure_degradation_heatmaps() -> None:
    pair = pd.read_csv(PAIR_UNC)
    regions = pd.read_csv(THRESHOLDS)["ar6_region"].tolist()
    models = ["spatial_knn_ridge", "stgcn_diffusion", "graphwavenet_transfer"]
    mats = {model: heatmap_matrix(pair, model, regions) for model in models}
    vmax = max(float(np.nanpercentile(np.abs(mat), 95)) for mat in mats.values())
    vmax = max(0.1, vmax)

    fig, axes = plt.subplots(3, 1, figsize=(5.9, 8.4), constrained_layout=True)
    im = None
    for idx, (ax, model) in enumerate(zip(axes, models)):
        im = ax.imshow(mats[model], cmap="RdBu_r", vmin=-vmax, vmax=vmax)
        ax.set_title(MODEL_LABELS[model].replace("\n", " "))
        ax.set_xticks(np.arange(len(regions)), labels=regions, rotation=45, ha="right")
        ax.set_yticks(np.arange(len(regions)), labels=regions)
        ax.tick_params(length=0, labelsize=8.4)
        add_panel_label(ax, ascii_uppercase[idx])
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_linewidth(0.5)
            spine.set_color("0.75")
    for ax in axes:
        ax.set_ylabel("Source")
    axes[-1].set_xlabel("Target region")
    if im is not None:
        cbar = fig.colorbar(im, ax=axes, fraction=0.045, pad=0.035)
        cbar.set_label("MAE out-minus-in")
    save_figure(fig, "fig_all_viable_degradation_heatmaps")

    for model, mat in mats.items():
        fig_single, ax = plt.subplots(figsize=(5.4, 4.8))
        im_single = ax.imshow(mat, cmap="RdBu_r", vmin=-vmax, vmax=vmax)
        ax.set_xticks(np.arange(len(regions)), labels=regions, rotation=45, ha="right")
        ax.set_yticks(np.arange(len(regions)), labels=regions)
        ax.tick_params(labelsize=9)
        ax.set_xlabel("Target region")
        ax.set_ylabel("Source region")
        ax.set_title(MODEL_LABELS[model].replace("\n", " "))
        cbar = fig_single.colorbar(im_single, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label("MAE out-minus-in")
        save_figure(fig_single, f"fig_all_viable_degradation_heatmap_{model}")


def source_accuracy_data() -> pd.DataFrame:
    if SOURCE_ACCURACY.exists():
        return pd.read_csv(SOURCE_ACCURACY)

    pair = pd.read_csv(PAIR_ALL)
    in_region = pair[pair["source_region"] == pair["target_region"]][
        ["run_tag", "model", "source_region", "mae_mean"]
    ].rename(columns={"mae_mean": "source_in_region_mae"})
    out = pair[pair["source_region"] != pair["target_region"]].copy()
    return out.merge(in_region, on=["run_tag", "model", "source_region"], how="left")


def figure_source_accuracy() -> None:
    source = source_accuracy_data()
    models = [m for m in MODEL_ORDER if m in set(source["model"])]
    fig, axes = plt.subplots(2, 3, figsize=(7.4, 4.8))
    axes = axes.ravel()

    for idx, (ax, model) in enumerate(zip(axes, models)):
        sub = source[source["model"] == model]
        ax.scatter(
            sub["source_in_region_mae"],
            sub["mae_out_minus_in_mean"],
            s=11,
            alpha=0.42,
            color="#0072B2",
            edgecolors="none",
        )
        r = sub["source_in_region_mae"].corr(sub["mae_out_minus_in_mean"], method="pearson")
        ax.axhline(0, color="0.3", linewidth=0.7)
        ax.text(0.03, 0.93, f"r = {r:.2f}", transform=ax.transAxes, ha="left", va="top", fontsize=8)
        ax.set_title(MODEL_LABELS[model].replace("\n", " "))
        add_panel_label(ax, ascii_uppercase[idx])
        ax.grid(color="0.92", linewidth=0.5)
        ax.set_axisbelow(True)

    for ax in axes[3:]:
        ax.set_xlabel("Source in-region MAE")
    for ax in [axes[0], axes[3]]:
        ax.set_ylabel("Out-of-region degradation")

    fig.tight_layout(w_pad=1.1, h_pad=1.3)
    save_figure(fig, "fig_all_viable_source_accuracy_vs_transfer")


def figure_threshold_sensitivity() -> None:
    if not THRESHOLD_SENSITIVITY.exists():
        return

    counts = pd.read_csv(THRESHOLD_SENSITIVITY)
    pivot = counts.pivot_table(
        index=["threshold_profile", "model"],
        columns="decision",
        values="n_pairs",
        fill_value=0,
    ).reset_index()
    for decision in DECISION_ORDER:
        if decision not in pivot:
            pivot[decision] = 0

    profile_order = ["strict", "main", "lenient"]
    models = [m for m in MODEL_ORDER if m in set(pivot["model"])]
    fig, axes = plt.subplots(2, 3, figsize=(7.4, 4.5), sharey=True)
    axes = axes.ravel()
    for idx, (ax, model) in enumerate(zip(axes, models)):
        sub = pivot[pivot["model"] == model].set_index("threshold_profile").reindex(profile_order)
        x = np.arange(len(profile_order))
        bottom = np.zeros(len(profile_order))
        for decision in DECISION_ORDER:
            vals = sub[decision].to_numpy()
            ax.bar(x, vals, bottom=bottom, color=DECISION_COLORS[decision], edgecolor="white", linewidth=0.4)
            bottom += vals
        ax.set_title(MODEL_LABELS[model].replace("\n", " "))
        ax.set_xticks(x, labels=["Strict", "Main", "Lenient"], rotation=25, ha="right")
        add_panel_label(ax, ascii_uppercase[idx])
        ax.grid(axis="y", color="0.92", linewidth=0.5)
        ax.set_axisbelow(True)
    for ax in [axes[0], axes[3]]:
        ax.set_ylabel("Pairs")
    handles = [mpl.patches.Patch(color=DECISION_COLORS[d], label=DECISION_LABELS[d]) for d in DECISION_ORDER]
    fig.legend(handles=handles, frameon=False, ncols=3, loc="upper center", bbox_to_anchor=(0.5, 1.02))
    fig.tight_layout(rect=(0, 0, 1, 0.96), w_pad=1.0, h_pad=1.1)
    save_figure(fig, "fig_all_viable_threshold_sensitivity")


def main() -> None:
    configure_style()
    figure_graphical_abstract()
    figure_region_map()
    figure_kbs_r2()
    figure_decisions()
    figure_degradation_heatmaps()
    figure_source_accuracy()
    figure_threshold_sensitivity()


if __name__ == "__main__":
    main()
