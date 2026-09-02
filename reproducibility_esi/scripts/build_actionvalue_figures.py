"""Publication figures for the executed-action benchmark."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "manuscript_latex_earth_science_informatics" / "figures"
CURVE = ROOT / "realized_action_confirmatory_budget_curve.csv"
TARGET_AUC = ROOT / "realized_action_confirmatory_target_auc.csv"
OUTCOMES = ROOT / "realized_action_confirmatory_predictions_outcomes.csv"

INK = "#26323f"
MUTED = "#66727f"
GRID = "#d8dde3"
BLUE = "#1769aa"
ORANGE = "#d97904"
GREEN = "#238b57"
PURPLE = "#6f51a1"
RED = "#b64747"


def configure() -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
            "font.size": 8,
            "axes.labelsize": 8.5,
            "xtick.labelsize": 7.5,
            "ytick.labelsize": 7.5,
            "legend.fontsize": 7.4,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def save(fig: plt.Figure, stem: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"{stem}.{ext}", dpi=400, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def framework_figure() -> None:
    fig, ax = plt.subplots(figsize=(7.1, 2.65))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    boxes = [
        (0.015, 0.27, 0.205, 0.52, "Pre-deployment\nevidence", "12 physical descriptors\n11 shift / distance metrics\n3 model indicators", BLUE, "#eaf2f8"),
        (0.265, 0.27, 0.205, 0.52, "Held-target\naction-value learning", "adapt and retrain benefit\nnested group validation\n2020–2022 outcomes", PURPLE, "#f0ecf6"),
        (0.515, 0.27, 0.205, 0.52, "Budget-aware\naction policy", "choose deploy or adapt\nrank retraining benefit\nallocate budget B", ORANGE, "#fbf1e4"),
        (0.765, 0.27, 0.22, 0.52, "Frozen confirmation\nand decision output", "2023–2025 untouched\n330 decisions · 990 actions\nbudget–MAE audit curve", GREEN, "#e8f4ee"),
    ]

    for x, y, w, h, title, body, color, fill in boxes:
        ax.add_patch(
            FancyBboxPatch(
                (x, y),
                w,
                h,
                boxstyle="round,pad=0.008,rounding_size=0.015",
                linewidth=1.0,
                edgecolor=color,
                facecolor=fill,
            )
        )
        ax.text(x + w / 2, y + h * 0.71, title, ha="center", va="center", weight="bold", color=INK, fontsize=8.2)
        ax.text(x + w / 2, y + h * 0.32, body, ha="center", va="center", color=MUTED, fontsize=7.0, linespacing=1.35)

    for first, second in zip(boxes[:-1], boxes[1:]):
        x1, y1, w1, h1 = first[:4]
        x2, y2, _, h2 = second[:4]
        ax.add_patch(
            FancyArrowPatch(
                (x1 + w1 + 0.006, y1 + h1 / 2),
                (x2 - 0.006, y2 + h2 / 2),
                arrowstyle="-|>",
                mutation_scale=10,
                linewidth=1.2,
                color="#89939d",
            )
        )

    ax.text(0.5, 0.92, "PhyK-TAS as a resource-constrained model-reuse decision system", ha="center", va="center", fontsize=9.5, weight="bold", color=INK)
    ax.text(0.49, 0.16, "Development", ha="center", va="center", fontsize=7.4, color=PURPLE, weight="bold")
    ax.plot([0.265, 0.720], [0.12, 0.12], color=PURPLE, lw=1.2)
    ax.text(0.875, 0.16, "Confirmation", ha="center", va="center", fontsize=7.4, color=GREEN, weight="bold")
    ax.plot([0.765, 0.985], [0.12, 0.12], color=GREEN, lw=1.2)
    ax.text(0.5, 0.035, "No 2023–2025 outcome, action choice, or target-specific development row enters policy fitting.", ha="center", va="center", fontsize=7.1, color=MUTED)
    save(fig, "fig_actionvalue_framework")


def family_detail(data: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for (model, target), group in data.groupby(["model", "target_region"], sort=True):
        group = group.reset_index(drop=True)
        n = len(group)
        cheap = group["cheap_mae"].to_numpy()
        retrain = group["retrain"].to_numpy()
        order = group["predicted_gain"].to_numpy().argsort()[::-1]
        policy = np.mean(
            [np.where(np.isin(np.arange(n), order[:b]), retrain, cheap).mean() for b in range(n + 1)]
        )
        random = np.mean([cheap.mean() + (b / n) * (retrain - cheap).mean() for b in range(n + 1)])
        rows.append({"model": model, "target_region": target, "difference": policy - random})
    return pd.DataFrame(rows)


def results_figure() -> None:
    curve = pd.read_csv(CURVE)
    auc = pd.read_csv(TARGET_AUC)
    data = pd.read_csv(OUTCOMES)
    aggregate = curve.groupby(["budget_retrains", "policy"], as_index=False)["mean_mae"].mean()
    wide = auc.pivot(index="target_region", columns="policy", values="budget_curve_auc")
    paired = (wide["action_value"] - wide["random_expected"]).sort_values()
    families = family_detail(data)

    fig, axes = plt.subplots(1, 3, figsize=(7.1, 2.7), gridspec_kw={"width_ratios": [1.22, 0.95, 0.95]})

    styles = {
        "action_value": (BLUE, "-", "Action-value"),
        "random_expected": (MUTED, "--", "Random expected"),
        "mmd": (ORANGE, "-.", "MMD"),
        "oracle": (GREEN, ":", "Restricted oracle"),
    }
    ax = axes[0]
    for policy, (color, ls, label) in styles.items():
        part = aggregate[aggregate["policy"].eq(policy)]
        ax.plot(part["budget_retrains"], part["mean_mae"], color=color, ls=ls, lw=1.7, label=label)
    ax.set_xlabel("Retraining budget per target")
    ax.set_ylabel("Mean confirmatory MAE")
    ax.set_xticks(np.arange(0, 31, 5))
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.legend(frameon=False, loc="upper right", handlelength=2.4)
    ax.text(-0.16, 1.03, "a", transform=ax.transAxes, weight="bold", fontsize=10)

    ax = axes[1]
    colors = [BLUE if value < 0 else RED for value in paired]
    ax.barh(np.arange(len(paired)), paired.values, color=colors, height=0.68)
    ax.axvline(0, color=INK, lw=0.8)
    ax.set_yticks(np.arange(len(paired)), paired.index)
    ax.set_xlabel("AUC difference\n(action-value − random)")
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.text(-0.20, 1.03, "b", transform=ax.transAxes, weight="bold", fontsize=10)
    ax.text(0.03, 0.98, "10/11 targets favorable", transform=ax.transAxes, ha="left", va="top", fontsize=7.1, color=BLUE, weight="bold")

    ax = axes[2]
    order = ["spatial_knn_ridge", "patchtst_small", "graphwavenet_transfer"]
    labels = ["Spatial", "PatchTST", "Graph WaveNet"]
    rng = np.random.default_rng(11)
    for i, model in enumerate(order):
        vals = families.loc[families["model"].eq(model), "difference"].to_numpy()
        jitter = rng.uniform(-0.10, 0.10, size=len(vals))
        ax.scatter(np.full(len(vals), i) + jitter, vals, s=17, color="#91b9d7", edgecolor="white", linewidth=0.35, zorder=2)
        ax.scatter(i, vals.mean(), s=42, marker="D", color=BLUE, edgecolor="white", linewidth=0.6, zorder=3)
    ax.axhline(0, color=INK, lw=0.8)
    ax.set_xticks(range(3), labels, rotation=24, ha="right")
    ax.set_ylabel("AUC difference vs random")
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.text(-0.21, 1.03, "c", transform=ax.transAxes, weight="bold", fontsize=10)

    fig.subplots_adjust(wspace=0.47, bottom=0.24, top=0.93, left=0.075, right=0.99)
    save(fig, "fig_confirmatory_budget_allocation")


def main() -> None:
    configure()
    framework_figure()
    results_figure()
    print(OUT / "fig_actionvalue_framework.pdf")
    print(OUT / "fig_confirmatory_budget_allocation.pdf")


if __name__ == "__main__":
    main()
