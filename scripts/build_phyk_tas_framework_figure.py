from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT = ROOT / "Paper1" / "manuscript_latex"
FIGDIR = MANUSCRIPT / "figures"
FIGDIR.mkdir(parents=True, exist_ok=True)


def box(ax, xy, wh, text, fc, ec="#2F3437", fontsize=9.5, weight="normal"):
    x, y = xy
    w, h = wh
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.018,rounding_size=0.018",
        linewidth=1.1,
        edgecolor=ec,
        facecolor=fc,
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        weight=weight,
        color="#172026",
        linespacing=1.18,
    )
    return patch


def arrow(ax, start, end, color="#4A4F55", lw=1.3, rad=0.0):
    arr = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=12,
        linewidth=lw,
        color=color,
        connectionstyle=f"arc3,rad={rad}",
    )
    ax.add_patch(arr)


def main() -> None:
    fig, ax = plt.subplots(figsize=(13.2, 7.2), dpi=180)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    colors = {
        "data": "#D8EAF7",
        "curation": "#E7E2F3",
        "physical": "#DCEEDC",
        "shift": "#FCE6C8",
        "models": "#F8D7DA",
        "inference": "#D7E7F5",
        "decision": "#E8E8E8",
        "output": "#DDF3F0",
    }

    box(
        ax,
        (0.035, 0.58),
        (0.18, 0.22),
        "Station archives\nGHCN-D, ECA\\&D\nnational networks",
        colors["data"],
        weight="bold",
    )
    box(
        ax,
        (0.275, 0.58),
        (0.22, 0.22),
        "Benchmark curation\nAR6 regions\ncross-source dedup\ncoverage masks\ntime splits",
        colors["curation"],
        weight="bold",
    )

    box(
        ax,
        (0.56, 0.72),
        (0.22, 0.18),
        "Physical knowledge layer\noccurrence, intensity\nseasonality, intermittency\nextremes",
        colors["physical"],
        weight="bold",
    )
    box(
        ax,
        (0.56, 0.48),
        (0.22, 0.18),
        "Generic shift layer\nKL, Wasserstein, MMD\nmoment and percentile shifts\ngeographic controls",
        colors["shift"],
        weight="bold",
    )
    box(
        ax,
        (0.56, 0.24),
        (0.22, 0.18),
        "Model evaluation layer\nSTGCN diffusion\nGraph WaveNet transfer\nout-minus-in degradation",
        colors["models"],
        weight="bold",
    )

    box(
        ax,
        (0.82, 0.50),
        (0.15, 0.22),
        "Degradation\ninference\nblocked CV\nseed uncertainty\nrisk score",
        colors["inference"],
        weight="bold",
    )
    box(
        ax,
        (0.82, 0.18),
        (0.15, 0.20),
        "Decision layer\nDEPLOY\nADAPT\nRETRAIN",
        colors["decision"],
        weight="bold",
    )

    box(
        ax,
        (0.305, 0.12),
        (0.16, 0.16),
        "Knowledge base\npreregistered descriptors\nfixed feature groups\nno post-hoc selection",
        colors["output"],
        fontsize=8.8,
        weight="bold",
    )

    arrow(ax, (0.215, 0.69), (0.275, 0.69))
    arrow(ax, (0.495, 0.69), (0.56, 0.81))
    arrow(ax, (0.495, 0.69), (0.56, 0.57))
    arrow(ax, (0.495, 0.63), (0.56, 0.33))
    arrow(ax, (0.78, 0.81), (0.82, 0.64))
    arrow(ax, (0.78, 0.57), (0.82, 0.61))
    arrow(ax, (0.78, 0.33), (0.82, 0.54))
    arrow(ax, (0.895, 0.50), (0.895, 0.38))
    arrow(ax, (0.385, 0.58), (0.385, 0.28), rad=0.0)
    arrow(ax, (0.465, 0.20), (0.56, 0.78), color="#2F6F48", rad=-0.15)
    arrow(ax, (0.465, 0.20), (0.56, 0.54), color="#2F6F48", rad=-0.05)

    ax.text(
        0.035,
        0.925,
        "PhyK-TAS: physically informed knowledge-based transferability assessment",
        fontsize=15,
        weight="bold",
        color="#172026",
    )
    ax.text(
        0.035,
        0.885,
        "The system estimates model degradation before deployment and converts it into uncertainty-aware operational decisions.",
        fontsize=10.5,
        color="#3A4148",
    )

    ax.text(
        0.835,
        0.105,
        "Output: transfer-risk table\nand interpretable decision rationale",
        fontsize=9,
        color="#3A4148",
        ha="center",
    )

    for ext in ["png", "pdf"]:
        fig.savefig(FIGDIR / f"fig_phyk_tas_framework.{ext}", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
