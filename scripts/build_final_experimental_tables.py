from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"

KBS_UNC = PAPER / "large_seed_kbs_uncertainty.csv"
PAIR_UNC = PAPER / "large_seed_pair_uncertainty.csv"
DECISIONS = PAPER / "large_seed_transfer_decisions.csv"
OUT_MODEL = PAPER / "final_model_kbs_summary.csv"
OUT_PAIR = PAPER / "final_pair_risk_summary.csv"
REPORT = PAPER / "final_experimental_summary_report.md"


def main() -> None:
    kbs = pd.read_csv(KBS_UNC)
    pair = pd.read_csv(PAIR_UNC)
    decisions = pd.read_csv(DECISIONS)

    focus = kbs[
        (kbs["cv_kind"] == "group_by_cell")
        & (kbs["estimator"] == "random_forest")
        & (kbs["forecast_model"].isin(["graphwavenet_transfer", "stgcn_diffusion"]))
    ].copy()
    best = (
        focus.sort_values(["forecast_model", "r2_mean"], ascending=[True, False])
        .groupby("forecast_model")
        .head(1)
        .rename(columns={"forecast_model": "model", "feature_set": "best_kbs_feature_set"})
    )

    risk = (
        pair[pair["source_region"] != pair["target_region"]]
        .groupby("model")
        .agg(
            max_degradation_mean=("degradation_mean", "max"),
            mean_degradation_mean=("degradation_mean", "mean"),
            max_degradation_sd=("degradation_sd", "max"),
        )
        .reset_index()
    )
    counts = (
        decisions.groupby(["model", "conservative_decision"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    for col in ["deploy", "adapt", "retrain"]:
        if col not in counts.columns:
            counts[col] = 0

    model_summary = (
        best[
            [
                "model",
                "best_kbs_feature_set",
                "mae_mean",
                "mae_sd",
                "r2_mean",
                "r2_sd",
                "r2_min",
                "r2_max",
            ]
        ]
        .merge(risk, on="model", how="left")
        .merge(counts[["model", "deploy", "adapt", "retrain"]], on="model", how="left")
    )
    model_summary.to_csv(OUT_MODEL, index=False)

    pair_summary = decisions[
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
    ].sort_values(["model", "degradation_mean"], ascending=[True, False])
    pair_summary.to_csv(OUT_PAIR, index=False)

    lines = [
        "# Final experimental summary",
        "",
        "This table consolidates the large multi-seed ST-GNN experiment for manuscript reporting.",
        "",
        "## Model-level KBS summary",
        "",
        model_summary.to_markdown(index=False),
        "",
        "## Pair-level transfer risk summary",
        "",
        pair_summary.to_markdown(index=False),
        "",
        "Interpretation:",
        "",
        "- `physical_plus_shift` is the best group-by-cell KBS feature set for both large ST-GNNs;",
        "- STGCN diffusion has the more permissive conservative decision profile;",
        "- Graph WaveNet is more conservative, especially for transfers involving NEU.",
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT_MODEL}")
    print(f"wrote {OUT_PAIR}")
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
