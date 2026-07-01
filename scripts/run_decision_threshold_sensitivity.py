from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
FIG = PAPER / "figures"
FIG.mkdir(exist_ok=True)

THRESHOLDS = [
    ("strict", 0.005, 0.020),
    ("main", 0.010, 0.025),
    ("lenient", 0.015, 0.030),
]

DECISION_ORDER = ["deploy", "adapt", "retrain"]
COLORS = {"deploy": "#54A24B", "adapt": "#F2C94C", "retrain": "#D9534F"}


def classify(score: float, deploy_t: float, adapt_t: float) -> str:
    if score <= deploy_t:
        return "deploy"
    if score <= adapt_t:
        return "adapt"
    return "retrain"


def slug_for_prefix(prefix: str) -> str:
    if prefix == "all_viable_min100_full":
        return "all_viable"
    return prefix


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prefix",
        default="all_viable_min100_full",
        help="Experiment prefix, e.g. all_viable_min100_full.",
    )
    args = parser.parse_args()

    prefix = args.prefix
    slug = slug_for_prefix(prefix)
    pair_unc = PAPER / f"{prefix}_pair_uncertainty.csv"
    counts_out = PAPER / f"{prefix}_threshold_sensitivity.csv"
    details_out = PAPER / f"{prefix}_threshold_sensitivity_details.csv"
    report = PAPER / f"{prefix}_threshold_sensitivity_report.md"
    figure = FIG / f"fig_{slug}_threshold_sensitivity.png"

    pair = pd.read_csv(pair_unc)
    pair = pair[pair["source_region"] != pair["target_region"]].copy()
    rows = []
    detail_rows = []
    for label, deploy_t, adapt_t in THRESHOLDS:
        tmp = pair.copy()
        tmp["risk_score"] = tmp["degradation_mean"] + tmp["degradation_ci95_halfwidth"]
        tmp["threshold_profile"] = label
        tmp["deploy_threshold"] = deploy_t
        tmp["adapt_threshold"] = adapt_t
        tmp["decision"] = tmp["risk_score"].apply(lambda v: classify(float(v), deploy_t, adapt_t))
        detail_rows.append(
            tmp[
                [
                    "threshold_profile",
                    "deploy_threshold",
                    "adapt_threshold",
                    "model",
                    "source_region",
                    "target_region",
                    "degradation_mean",
                    "degradation_ci95_halfwidth",
                    "risk_score",
                    "decision",
                ]
            ]
        )
        counts = tmp.groupby(["model", "decision"]).size().reset_index(name="n_pairs")
        counts["threshold_profile"] = label
        counts["deploy_threshold"] = deploy_t
        counts["adapt_threshold"] = adapt_t
        rows.append(counts)
    counts_all = pd.concat(rows, ignore_index=True)
    details = pd.concat(detail_rows, ignore_index=True)
    counts_all.to_csv(counts_out, index=False)
    details.to_csv(details_out, index=False)

    pivot = counts_all.pivot_table(
        index=["threshold_profile", "model"],
        columns="decision",
        values="n_pairs",
        fill_value=0,
    ).reset_index()
    for col in DECISION_ORDER:
        if col not in pivot:
            pivot[col] = 0

    models = sorted(pivot["model"].unique())
    ncols = 3
    nrows = (len(models) + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(12, 3.4 * nrows), dpi=180, sharey=True)
    axes_flat = axes.ravel() if hasattr(axes, "ravel") else [axes]
    for ax, model in zip(axes_flat, models):
        sub = pivot[pivot["model"] == model].set_index("threshold_profile").loc[[x[0] for x in THRESHOLDS]]
        bottom = None
        x = range(len(sub))
        for decision in DECISION_ORDER:
            ax.bar(x, sub[decision], bottom=bottom, label=decision, color=COLORS[decision])
            bottom = sub[decision] if bottom is None else bottom + sub[decision]
        ax.set_xticks(list(x), labels=sub.index)
        ax.set_title(model.replace("_", " "))
        ax.set_ylabel("Number of source-target pairs")
        ax.set_ylim(0, pair.groupby("model").size().max())
    for ax in axes_flat[len(models) :]:
        ax.axis("off")
    axes_flat[min(len(models) - 1, len(axes_flat) - 1)].legend(frameon=False, loc="upper right")
    fig.suptitle("Decision sensitivity to deploy/adapt thresholds")
    fig.tight_layout()
    fig.savefig(figure)
    plt.close(fig)

    lines = [
        "# Decision threshold sensitivity report",
        "",
        f"Experiment prefix: `{prefix}`.",
        "",
        "Decisions use conservative risk score: mean degradation + 95% half-width across seeds.",
        "",
        "Threshold profiles:",
        "",
        "- strict: deploy <= 0.005, adapt <= 0.020;",
        "- main: deploy <= 0.010, adapt <= 0.025;",
        "- lenient: deploy <= 0.015, adapt <= 0.030.",
        "",
        "## Decision counts",
        "",
        pivot.to_markdown(index=False),
        "",
        "Figure:",
        "",
        f"- `figures/{figure.name}`",
        "",
    ]
    report.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {counts_out}")
    print(f"wrote {details_out}")
    print(f"wrote {report}")
    print(f"wrote {figure}")


if __name__ == "__main__":
    main()
