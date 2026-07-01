from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
FIG = PAPER / "figures"
FIG.mkdir(exist_ok=True)

PAIR_UNC = PAPER / "large_seed_pair_uncertainty.csv"
OUT = PAPER / "large_seed_transfer_decisions.csv"
REPORT = PAPER / "large_seed_transfer_decision_report.md"


def classify(value: float) -> str:
    if value <= 0.01:
        return "deploy"
    if value <= 0.025:
        return "adapt"
    return "retrain"


def conservative_class(row: pd.Series) -> str:
    upper = row["degradation_mean"] + row["degradation_ci95_halfwidth"]
    return classify(float(upper))


def expected_class(row: pd.Series) -> str:
    return classify(float(row["degradation_mean"]))


def uncertainty_flag(row: pd.Series) -> str:
    lower = row["degradation_mean"] - row["degradation_ci95_halfwidth"]
    upper = row["degradation_mean"] + row["degradation_ci95_halfwidth"]
    low_class = classify(float(lower))
    high_class = classify(float(upper))
    if low_class == high_class:
        return "stable"
    return f"boundary_{low_class}_to_{high_class}"


def decision_heatmap(decisions: pd.DataFrame, model: str, out_path: Path) -> None:
    regions = ["MED", "WCE", "NEU"]
    code = {"deploy": 0, "adapt": 1, "retrain": 2}
    labels = {0: "deploy", 1: "adapt", 2: "retrain"}
    mat = np.full((len(regions), len(regions)), np.nan)
    ann = [["" for _ in regions] for _ in regions]
    sub = decisions[decisions["model"] == model]
    for i, src in enumerate(regions):
        for j, dst in enumerate(regions):
            row = sub[(sub["source_region"] == src) & (sub["target_region"] == dst)]
            if row.empty:
                continue
            r = row.iloc[0]
            mat[i, j] = code[r["conservative_decision"]]
            ann[i][j] = f"{r['conservative_decision']}\n{r['degradation_mean']:.3f}+/-{r['degradation_sd']:.3f}"
    cmap = ListedColormap(["#54A24B", "#F2C94C", "#D9534F"])
    fig, ax = plt.subplots(figsize=(6.2, 5.2), dpi=180)
    im = ax.imshow(mat, cmap=cmap, vmin=0, vmax=2)
    ax.set_xticks(range(len(regions)), labels=regions)
    ax.set_yticks(range(len(regions)), labels=regions)
    ax.set_xlabel("Target region")
    ax.set_ylabel("Source region")
    ax.set_title(f"Conservative transfer decision: {model}")
    for i in range(len(regions)):
        for j in range(len(regions)):
            ax.text(j, i, ann[i][j], ha="center", va="center", fontsize=8)
    cbar = fig.colorbar(im, ax=ax, ticks=[0, 1, 2], fraction=0.046, pad=0.04)
    cbar.ax.set_yticklabels([labels[i] for i in [0, 1, 2]])
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def main() -> None:
    pair = pd.read_csv(PAIR_UNC)
    decisions = pair[pair["source_region"] != pair["target_region"]].copy()
    decisions["expected_decision"] = decisions.apply(expected_class, axis=1)
    decisions["conservative_decision"] = decisions.apply(conservative_class, axis=1)
    decisions["uncertainty_flag"] = decisions.apply(uncertainty_flag, axis=1)
    decisions["risk_score"] = decisions["degradation_mean"] + decisions["degradation_ci95_halfwidth"]
    decisions = decisions.sort_values(["model", "risk_score"], ascending=[True, False])
    decisions.to_csv(OUT, index=False)

    for model in decisions["model"].unique():
        decision_heatmap(decisions, model, FIG / f"fig_large_transfer_decision_{model}.png")

    counts = (
        decisions.groupby(["model", "conservative_decision"])
        .size()
        .reset_index(name="n_pairs")
        .sort_values(["model", "conservative_decision"])
    )
    lines = [
        "# Large-seed transfer decision report",
        "",
        "Decision thresholds use MAE out-minus-in degradation:",
        "",
        "- deploy: upper 95% seed interval <= 0.010;",
        "- adapt: upper 95% seed interval <= 0.025;",
        "- retrain: upper 95% seed interval > 0.025.",
        "",
        "The decision is conservative: it uses mean + 95% half-width across large seeds.",
        "",
        "## Decision counts",
        "",
        counts.to_markdown(index=False),
        "",
        "## Pair-level decisions",
        "",
        decisions[
            [
                "model",
                "source_region",
                "target_region",
                "degradation_mean",
                "degradation_sd",
                "degradation_ci95_halfwidth",
                "expected_decision",
                "conservative_decision",
                "uncertainty_flag",
            ]
        ].to_markdown(index=False),
        "",
        "## Figures",
        "",
    ]
    for model in decisions["model"].unique():
        lines.append(f"- `figures/fig_large_transfer_decision_{model}.png`")
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
