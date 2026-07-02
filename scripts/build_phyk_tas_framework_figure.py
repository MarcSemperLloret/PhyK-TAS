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
    ax.plot([x + 0.016, x + w - 0.016], [y + h - 0.175, y + h - 0.175], color=ec, lw=0.55, alpha=0.35)
    ax.text(x + w / 2, y + h - 0.066, header, ha="center", va="top",
            fontsize=11.4, weight="bold", color="#111820", linespacing=1.02)
    ax.text(x + w / 2, y + h * 0.395, body, ha="center", va="center",
            fontsize=8.75, color="#2c333a", linespacing=1.18)


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
    fig, ax = plt.subplots(figsize=(8.8, 3.18), dpi=400)
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
        0.5, 0.925,
        "PhyK-TAS transfer-risk assessment pipeline",
        ha="center", va="center", fontsize=12.6, weight="bold", color="#111820",
    )
    ax.text(
        0.5, 0.852,
        "from station archives to calibrated deploy/adapt/retrain decisions",
        ha="center", va="center", fontsize=9.2, color="#46515A",
    )

    w, h, y, gap = 0.158, 0.57, 0.19, 0.034
    xs = [0.015 + i * (w + gap) for i in range(5)]
    for x, col, (header, body) in zip(xs, c, stages):
        ec = "#1B6B46" if "Fused" in header else "#27323A"
        lw_col = "#1B6B46" if "Fused" in header else ec
        box(ax, x, y, w, h, header, body, col, ec=lw_col)
    for i in range(4):
        arrow(ax, (xs[i] + w + 0.010, y + h / 2), (xs[i + 1] - 0.014, y + h / 2), color="#5B6268", lw=1.55)

    ax.text(
        xs[2] + w / 2, 0.085,
        "feature-level fusion + model-level fusion + uncertainty calibration",
        ha="center", va="center", fontsize=8.8, color="#1B6B46", weight="bold",
    )

    for figdir in FIGDIRS:
        for ext in ["png", "pdf"]:
            fig.savefig(figdir / f"fig_phyk_tas_framework.{ext}", bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


if __name__ == "__main__":
    main()
