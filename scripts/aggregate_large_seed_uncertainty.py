from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
FIG = PAPER / "figures"
FIG.mkdir(exist_ok=True)

SEEDS = {
    "large_s1": "large",
    "large_s2": "large_s2",
    "large_s3": "large_s3",
}
MODELS = {
    "graphwavenet_transfer": "forecast_graphwavenet",
    "stgcn_diffusion": "forecast_stgnn",
}

OUT_PAIR_ALL = PAPER / "large_seed_pair_summary_all.csv"
OUT_PAIR_UNC = PAPER / "large_seed_pair_uncertainty.csv"
OUT_KBS_ALL = PAPER / "large_seed_kbs_results_all.csv"
OUT_KBS_UNC = PAPER / "large_seed_kbs_uncertainty.csv"
REPORT = PAPER / "large_seed_uncertainty_report.md"


def suffix_for(tag: str) -> str:
    return "large" if tag == "large" else tag


def load_pair_summaries() -> pd.DataFrame:
    frames = []
    for seed_label, tag in SEEDS.items():
        suffix = suffix_for(tag)
        for _, prefix in MODELS.items():
            path = PAPER / f"{prefix}_{suffix}_pair_summary.csv"
            df = pd.read_csv(path)
            df["seed_label"] = seed_label
            frames.append(df)
    return pd.concat(frames, ignore_index=True)


def load_kbs_results() -> pd.DataFrame:
    frames = []
    for seed_label, tag in SEEDS.items():
        suffix = suffix_for(tag)
        path = PAPER / f"kbs_forecast_model_comparison_{suffix}_results.csv"
        df = pd.read_csv(path)
        df["seed_label"] = seed_label
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def summarize_pair(pair: pd.DataFrame) -> pd.DataFrame:
    out = (
        pair.groupby(["model", "source_region", "target_region"])
        .agg(
            n_seeds=("seed_label", "nunique"),
            degradation_mean=("mae_out_minus_in_mean", "mean"),
            degradation_sd=("mae_out_minus_in_mean", "std"),
            degradation_min=("mae_out_minus_in_mean", "min"),
            degradation_max=("mae_out_minus_in_mean", "max"),
            mae_mean=("mae_mean", "mean"),
            brier_mean=("brier_mean", "mean"),
        )
        .reset_index()
    )
    out["degradation_se"] = out["degradation_sd"] / np.sqrt(out["n_seeds"])
    out["degradation_ci95_halfwidth"] = 1.96 * out["degradation_se"]
    return out


def summarize_kbs(kbs: pd.DataFrame) -> pd.DataFrame:
    out = (
        kbs.groupby(["forecast_model", "feature_set", "cv_kind", "estimator"])
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
    out["r2_se"] = out["r2_sd"] / np.sqrt(out["n_seeds"])
    out["r2_ci95_halfwidth"] = 1.96 * out["r2_se"]
    return out


def heatmap_for_model(pair_unc: pd.DataFrame, model: str, out_path: Path) -> None:
    regions = ["MED", "WCE", "NEU"]
    sub = pair_unc[pair_unc["model"] == model]
    mat = np.full((len(regions), len(regions)), np.nan)
    ann = [["" for _ in regions] for _ in regions]
    for i, src in enumerate(regions):
        for j, dst in enumerate(regions):
            row = sub[(sub["source_region"] == src) & (sub["target_region"] == dst)]
            if row.empty:
                continue
            r = row.iloc[0]
            mat[i, j] = r["degradation_mean"]
            ann[i][j] = f"{r['degradation_mean']:.3f}\n+/-{r['degradation_sd']:.3f}"
    fig, ax = plt.subplots(figsize=(6.2, 5.2), dpi=180)
    vmax = np.nanmax(np.abs(mat))
    vmax = max(vmax, 0.04)
    im = ax.imshow(mat, cmap="coolwarm", vmin=-vmax, vmax=vmax)
    ax.set_xticks(range(len(regions)), labels=regions)
    ax.set_yticks(range(len(regions)), labels=regions)
    ax.set_xlabel("Target region")
    ax.set_ylabel("Source region")
    ax.set_title(f"Out-of-region MAE degradation: {model}")
    for i in range(len(regions)):
        for j in range(len(regions)):
            ax.text(j, i, ann[i][j], ha="center", va="center", fontsize=8)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="MAE out-minus-in")
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def degradation_errorbar(pair_unc: pd.DataFrame, out_path: Path) -> None:
    sub = pair_unc[pair_unc["source_region"] != pair_unc["target_region"]].copy()
    sub["pair"] = sub["source_region"] + "->" + sub["target_region"]
    order = ["MED->WCE", "MED->NEU", "WCE->MED", "WCE->NEU", "NEU->MED", "NEU->WCE"]
    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=180)
    offsets = {"graphwavenet_transfer": -0.12, "stgcn_diffusion": 0.12}
    xbase = np.arange(len(order))
    for model, offset in offsets.items():
        rows = sub[sub["model"] == model].set_index("pair").loc[order]
        ax.errorbar(
            xbase + offset,
            rows["degradation_mean"],
            yerr=rows["degradation_sd"].fillna(0),
            fmt="o",
            capsize=4,
            label=model,
        )
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(xbase, labels=order, rotation=25, ha="right")
    ax.set_ylabel("MAE out-minus-in")
    ax.set_title("Transfer degradation across large-seed runs")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def kbs_r2_bar(kbs_unc: pd.DataFrame, out_path: Path) -> None:
    sub = kbs_unc[
        (kbs_unc["cv_kind"] == "group_by_cell")
        & (kbs_unc["estimator"] == "random_forest")
        & (kbs_unc["feature_set"].isin(["physical_knowledge", "generic_shift", "physical_plus_shift"]))
    ].copy()
    models = ["graphwavenet_transfer", "stgcn_diffusion"]
    feature_sets = ["physical_knowledge", "generic_shift", "physical_plus_shift"]
    colors = {"physical_knowledge": "#4C78A8", "generic_shift": "#F58518", "physical_plus_shift": "#54A24B"}
    fig, ax = plt.subplots(figsize=(8, 4.8), dpi=180)
    xbase = np.arange(len(models))
    width = 0.22
    for k, fs in enumerate(feature_sets):
        rows = sub[sub["feature_set"] == fs].set_index("forecast_model").loc[models]
        x = xbase + (k - 1) * width
        ax.bar(x, rows["r2_mean"], width=width, yerr=rows["r2_sd"].fillna(0), capsize=4, label=fs, color=colors[fs])
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(xbase, labels=models)
    ax.set_ylabel("R2 predicting degradation")
    ax.set_title("KBS feature-set comparison across large seeds")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def main() -> None:
    pair = load_pair_summaries()
    kbs = load_kbs_results()
    pair_unc = summarize_pair(pair)
    kbs_unc = summarize_kbs(kbs)
    pair.to_csv(OUT_PAIR_ALL, index=False)
    pair_unc.to_csv(OUT_PAIR_UNC, index=False)
    kbs.to_csv(OUT_KBS_ALL, index=False)
    kbs_unc.to_csv(OUT_KBS_UNC, index=False)

    heatmap_for_model(pair_unc, "graphwavenet_transfer", FIG / "fig_large_degradation_heatmap_graphwavenet.png")
    heatmap_for_model(pair_unc, "stgcn_diffusion", FIG / "fig_large_degradation_heatmap_stgcn.png")
    degradation_errorbar(pair_unc, FIG / "fig_large_degradation_uncertainty.png")
    kbs_r2_bar(kbs_unc, FIG / "fig_large_kbs_r2_group_by_cell.png")

    best = kbs_unc[
        (kbs_unc["cv_kind"] == "group_by_cell")
        & (kbs_unc["estimator"] == "random_forest")
    ].sort_values(["forecast_model", "r2_mean"], ascending=[True, False])
    best = best.groupby("forecast_model").head(3)

    lines = [
        "# Large-seed uncertainty report",
        "",
        "Seeds:",
        "",
        "- `large_s1`: seed 20260524;",
        "- `large_s2`: seed 20260525;",
        "- `large_s3`: seed 20260526.",
        "",
        "Scale per run:",
        "",
        "- MED: 913 stations;",
        "- WCE: 1000 stations;",
        "- NEU: 1000 stations.",
        "",
        "## Degradation uncertainty",
        "",
        pair_unc[pair_unc["source_region"] != pair_unc["target_region"]]
        .sort_values(["model", "source_region", "target_region"])
        .to_markdown(index=False),
        "",
        "## KBS uncertainty, group-by-cell random forest",
        "",
        best.to_markdown(index=False),
        "",
        "## Figures",
        "",
        "- `figures/fig_large_degradation_heatmap_graphwavenet.png`",
        "- `figures/fig_large_degradation_heatmap_stgcn.png`",
        "- `figures/fig_large_degradation_uncertainty.png`",
        "- `figures/fig_large_kbs_r2_group_by_cell.png`",
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT_PAIR_ALL}")
    print(f"wrote {OUT_PAIR_UNC}")
    print(f"wrote {OUT_KBS_ALL}")
    print(f"wrote {OUT_KBS_UNC}")
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
