from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


ROOT = Path(__file__).resolve().parents[2]
FIGDIRS = [
    ROOT / "Paper1" / "figures",
    ROOT / "Paper1" / "manuscript_latex" / "figures",
    ROOT / "Paper1" / "manuscript_latex_eswa" / "figures",
    ROOT / "Paper1" / "manuscript_latex_infofusion" / "figures",
]
for figdir in FIGDIRS:
    figdir.mkdir(parents=True, exist_ok=True)


def box(ax, x, y, w, h, header, body, fc, ec="#2F3437"):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.006,rounding_size=0.018",
        linewidth=1.15, edgecolor=ec, facecolor=fc, mutation_aspect=0.5,
    ))
    ax.plot([x + 0.018, x + w - 0.018], [y + h - 0.122, y + h - 0.122], color=ec, lw=0.6, alpha=0.35)
    ax.text(x + w / 2, y + h - 0.040, header, ha="center", va="top",
            fontsize=10.4, weight="bold", color="#111820", linespacing=0.98)
    ax.text(x + w / 2, y + h * 0.315, body, ha="center", va="center",
            fontsize=8.45, color="#2c333a", linespacing=1.08)


def arrow(ax, start, end, color="#4A4F55", lw=1.8, rad=0.0):
    ax.add_patch(FancyArrowPatch(
        start, end, arrowstyle="-|>", mutation_scale=16,
        linewidth=lw, color=color, connectionstyle=f"arc3,rad={rad}",
    ))


def main() -> None:
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    })
    fig, ax = plt.subplots(figsize=(7.4, 4.25), dpi=400)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    c = ["#E7F1FA", "#ECE8F6", "#DFF2E6", "#E3EEF8", "#E2F4F0"]
    stages = [
        ("Station\narchives", "GHCN-D, ECA&D,\nnational networks"),
        ("Benchmark\ncuration", "AR6 regions,\ndeduplication,\ntime splits"),
        ("Fused\nevidence", "physical regime\ndescriptors +\nshift diagnostics"),
        ("Degradation\ninference", "fusion of models:\nstacking, pooling,\nmonotone priors"),
        ("Conformal\ndecision", "deploy / adapt /\nretrain with\ncalibrated risk"),
    ]

    ax.text(
        0.5, 0.94,
        "PhyK-TAS transfer-risk assessment pipeline",
        ha="center", va="center", fontsize=12.8, weight="bold", color="#111820",
    )
    ax.text(
        0.5, 0.885,
        "from station archives to calibrated deploy/adapt/retrain decisions",
        ha="center", va="center", fontsize=9.4, color="#46515A",
    )

    w, h = 0.245, 0.300
    top_y, bottom_y = 0.525, 0.135
    left_x, mid_x, right_x = 0.075, 0.3775, 0.680

    positions = [
        (right_x, top_y),    # Station archives: start at top right
        (mid_x, top_y),      # Benchmark curation: flow right-to-left
        (left_x, top_y),     # Fused evidence
        (left_x, bottom_y),  # Degradation inference: down from fusion
        (right_x, bottom_y), # Conformal decision: finish left-to-right
    ]

    for (x, y), col, (header, body) in zip(positions, c, stages):
        ec = "#1B6B46" if "Fused" in header else "#27323A"
        lw_col = "#1B6B46" if "Fused" in header else ec
        box(ax, x, y, w, h, header, body, col, ec=lw_col)

    cy_top = top_y + h / 2
    cy_bottom = bottom_y + h / 2
    arrow(ax, (right_x - 0.020, cy_top), (mid_x + w + 0.020, cy_top), color="#5B6268", lw=1.65)
    arrow(ax, (mid_x - 0.020, cy_top), (left_x + w + 0.020, cy_top), color="#5B6268", lw=1.65)
    arrow(ax, (left_x + w / 2, top_y - 0.025), (left_x + w / 2, bottom_y + h + 0.025), color="#5B6268", lw=1.65)
    arrow(ax, (left_x + w + 0.025, cy_bottom), (right_x - 0.025, cy_bottom), color="#5B6268", lw=1.65)

    ax.text(
        0.5, 0.075,
        "feature-level fusion + model-level fusion + uncertainty calibration",
        ha="center", va="center", fontsize=9.0, color="#1B6B46", weight="bold",
    )

    for figdir in FIGDIRS:
        for ext in ["png", "pdf"]:
            fig.savefig(figdir / f"fig_phyk_tas_framework.{ext}", bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


if __name__ == "__main__":
    main()
