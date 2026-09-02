"""Main-text figure for the agreement evidence source.

Two panels (group-by-cell, leave-target-region-out): degradation-inference R^2
with 95% hierarchical-bootstrap intervals for the descriptor fusion, the
label-free agreement source (target-model-excluded primary, full-ensemble
warm-start variant), and the three-source fusion. Reads the significance CSV,
so the figure and the reported CIs are the same numbers.
"""
from __future__ import annotations

import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
SUFFIX = os.environ.get("AGREEMENT_OUT_SUFFIX", "all_viable_min100_full").strip()
CSV = PAPER / f"v2_agreement_significance_{SUFFIX}.csv"
FIGDIRS = [
    PAPER / "figures",
    PAPER / "manuscript_latex_infofusion" / "figures",
]

MODELS = [
    ("spatial_knn_ridge", "kNN"),
    ("stgcn_diffusion", "STGCN"),
    ("graphwavenet_transfer", "GWN"),
    ("regional_doy_climatology", "Clim."),
    ("linear_window", "Lin."),
    ("patchtst_small", "PTST"),
]

# Series: entity -> (column stem, color, marker fill). The two agreement
# variants share one hue; the warm-start variant is drawn hollow.
SERIES = [
    ("physical_plus_shift", "Phys+shift (Stage 1)", "#0072B2", True),
    ("label_free_agreement_cold", "Agreement, no local model (Stage 2)", "#E69F00", True),
    ("label_free_agreement", "Agreement, warm start", "#E69F00", False),
    ("physical_plus_shift_plus_agreement_cold", "Three-source fusion (Stage 3)", "#009E73", True),
]

CV_PANELS = [
    ("group_by_cell", "Within calibrated library (group-by-cell)"),
    ("leave_target_region_out", "Unseen region (leave-target-region-out)"),
]


def main() -> None:
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 9.5,
        "axes.labelsize": 10.5,
        "axes.titlesize": 10.5,
        "xtick.labelsize": 9.0,
        "ytick.labelsize": 9.0,
        "legend.fontsize": 9.0,
        "axes.linewidth": 0.7,
    })
    df = pd.read_csv(CSV)

    fig, axes = plt.subplots(2, 1, figsize=(3.48, 4.75), dpi=400, sharey=True)
    offsets = [-0.24, -0.08, 0.08, 0.24]

    for ax, (cv, title) in zip(axes, CV_PANELS):
        sub = df[df["cv_kind"] == cv].set_index("forecast_model")
        ax.axhline(0.0, color="#B9BEC3", lw=0.8, zorder=1)
        for (stem, label, color, filled), off in zip(SERIES, offsets):
            xs, ys, lo_err, hi_err = [], [], [], []
            for i, (model, _) in enumerate(MODELS):
                row = sub.loc[model]
                xs.append(i + off)
                ys.append(row[f"r2_{stem}"])
                lo_err.append(row[f"r2_{stem}"] - row[f"r2_{stem}_lo"])
                hi_err.append(row[f"r2_{stem}_hi"] - row[f"r2_{stem}"])
            ax.errorbar(
                xs, ys, yerr=[lo_err, hi_err],
                fmt="o", ms=4.9, color=color, ecolor=color,
                markerfacecolor=color if filled else "white",
                markeredgecolor="#2F3437", markeredgewidth=0.6,
                elinewidth=1.15, capsize=2.0, zorder=3,
                label=label if cv == "group_by_cell" else None,
            )
        ax.set_title(title)
        ax.set_xticks(range(len(MODELS)))
        ax.set_xticklabels([m[1] for m in MODELS])
        ax.grid(axis="y", color="#ECECEC", linewidth=0.55, zorder=0)
        ax.set_axisbelow(True)
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)
        ax.tick_params(axis="both")

    axes[0].set_ylabel("Degradation-inference $R^2$")
    axes[0].set_ylim(-1.15, 1.08)
    fig.legend(
        loc="upper center", bbox_to_anchor=(0.5, 1.015), ncol=2,
        frameon=False, handletextpad=0.35, columnspacing=1.0,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.88), h_pad=1.0)

    for figdir in FIGDIRS:
        figdir.mkdir(parents=True, exist_ok=True)
        for ext in ("png", "pdf"):
            fig.savefig(figdir / f"fig_v2_agreement_sources.{ext}", bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)
    print("wrote fig_v2_agreement_sources.{png,pdf}")


if __name__ == "__main__":
    main()
