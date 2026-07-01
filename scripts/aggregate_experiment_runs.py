from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"

RUN_TAGS = [x.strip() for x in os.environ.get("PHYKTAS_RUN_TAGS", "").split(",") if x.strip()]
OUT_PREFIX = os.environ.get("PHYKTAS_AGGREGATE_PREFIX", "experiment").strip()

PAIR_PREFIXES = [
    "forecast_baseline",
    "forecast_spatial_baseline",
    "forecast_stgnn",
    "forecast_graphwavenet",
    "forecast_patchtst",
]

T_CRITICAL_95 = {
    2: 12.706204736432095,
    3: 4.302652729911275,
    4: 3.182446305284263,
    5: 2.7764451051977987,
    6: 2.570581835636314,
    7: 2.4469118511449692,
    8: 2.3646242510102993,
    9: 2.306004135204166,
    10: 2.2621571627409915,
}


def t_halfwidth_multiplier(n: pd.Series) -> pd.Series:
    """Two-sided 95% t multiplier for small repeated-sample summaries."""
    df = (n.astype(int) - 1).clip(lower=1)
    return df.map(T_CRITICAL_95).fillna(1.96)


def require_tags() -> list[str]:
    if not RUN_TAGS:
        raise ValueError("Set PHYKTAS_RUN_TAGS to a comma-separated list of experiment tags.")
    return RUN_TAGS


def load_pair_summaries(tags: list[str]) -> pd.DataFrame:
    frames = []
    for seed_idx, tag in enumerate(tags, start=1):
        for prefix in PAIR_PREFIXES:
            path = PAPER / f"{prefix}_{tag}_pair_summary.csv"
            if not path.exists():
                continue
            df = pd.read_csv(path)
            df["run_tag"] = tag
            df["seed_index"] = seed_idx
            frames.append(df)
    if not frames:
        raise FileNotFoundError("No pair summary files found for configured tags.")
    return pd.concat(frames, ignore_index=True)


def load_kbs_results(tags: list[str]) -> pd.DataFrame:
    frames = []
    for seed_idx, tag in enumerate(tags, start=1):
        path = PAPER / f"kbs_forecast_model_comparison_{tag}_results.csv"
        if not path.exists():
            continue
        df = pd.read_csv(path)
        df["run_tag"] = tag
        df["seed_index"] = seed_idx
        frames.append(df)
    if not frames:
        raise FileNotFoundError("No KBS comparison files found for configured tags.")
    return pd.concat(frames, ignore_index=True)


def summarize_pair(pair: pd.DataFrame) -> pd.DataFrame:
    out = (
        pair.groupby(["model", "source_region", "target_region"])
        .agg(
            n_runs=("run_tag", "nunique"),
            degradation_mean=("mae_out_minus_in_mean", "mean"),
            degradation_sd=("mae_out_minus_in_mean", "std"),
            degradation_min=("mae_out_minus_in_mean", "min"),
            degradation_max=("mae_out_minus_in_mean", "max"),
            mae_mean=("mae_mean", "mean"),
            brier_mean=("brier_mean", "mean"),
        )
        .reset_index()
    )
    out["degradation_sd"] = out["degradation_sd"].fillna(0.0)
    out["degradation_se"] = out["degradation_sd"] / np.sqrt(out["n_runs"].clip(lower=1))
    out["degradation_ci95_halfwidth"] = t_halfwidth_multiplier(out["n_runs"]) * out["degradation_se"]
    return out


def summarize_kbs(kbs: pd.DataFrame) -> pd.DataFrame:
    out = (
        kbs.groupby(["forecast_model", "feature_set", "cv_kind", "estimator"])
        .agg(
            n_runs=("run_tag", "nunique"),
            mae_mean=("mae", "mean"),
            mae_sd=("mae", "std"),
            r2_mean=("r2", "mean"),
            r2_sd=("r2", "std"),
            r2_min=("r2", "min"),
            r2_max=("r2", "max"),
        )
        .reset_index()
    )
    out["mae_sd"] = out["mae_sd"].fillna(0.0)
    out["r2_sd"] = out["r2_sd"].fillna(0.0)
    out["r2_se"] = out["r2_sd"] / np.sqrt(out["n_runs"].clip(lower=1))
    out["r2_ci95_halfwidth"] = t_halfwidth_multiplier(out["n_runs"]) * out["r2_se"]
    return out


def classify(score: float, deploy_t: float = 0.010, adapt_t: float = 0.025) -> str:
    if score <= deploy_t:
        return "deploy"
    if score <= adapt_t:
        return "adapt"
    return "retrain"


def build_decisions(pair_unc: pd.DataFrame) -> pd.DataFrame:
    decisions = pair_unc[pair_unc["source_region"] != pair_unc["target_region"]].copy()
    decisions["risk_score"] = decisions["degradation_mean"] + decisions["degradation_ci95_halfwidth"]
    decisions["expected_decision"] = decisions["degradation_mean"].map(classify)
    decisions["conservative_decision"] = decisions["risk_score"].map(classify)
    decisions = decisions.sort_values(["model", "risk_score"], ascending=[True, False])
    return decisions


def main() -> None:
    tags = require_tags()
    pair = load_pair_summaries(tags)
    kbs = load_kbs_results(tags)
    pair_unc = summarize_pair(pair)
    kbs_unc = summarize_kbs(kbs)
    decisions = build_decisions(pair_unc)

    pair_all_path = PAPER / f"{OUT_PREFIX}_pair_summary_all.csv"
    pair_unc_path = PAPER / f"{OUT_PREFIX}_pair_uncertainty.csv"
    kbs_all_path = PAPER / f"{OUT_PREFIX}_kbs_results_all.csv"
    kbs_unc_path = PAPER / f"{OUT_PREFIX}_kbs_uncertainty.csv"
    decisions_path = PAPER / f"{OUT_PREFIX}_transfer_decisions.csv"
    report_path = PAPER / f"{OUT_PREFIX}_aggregate_report.md"

    pair.to_csv(pair_all_path, index=False)
    pair_unc.to_csv(pair_unc_path, index=False)
    kbs.to_csv(kbs_all_path, index=False)
    kbs_unc.to_csv(kbs_unc_path, index=False)
    decisions.to_csv(decisions_path, index=False)

    best = (
        kbs_unc[
            (kbs_unc["cv_kind"] == "group_by_cell")
            & (kbs_unc["estimator"] == "random_forest")
        ]
        .sort_values(["forecast_model", "r2_mean"], ascending=[True, False])
        .groupby("forecast_model")
        .head(3)
    )
    decision_counts = (
        decisions.groupby(["model", "conservative_decision"])
        .size()
        .reset_index(name="n_pairs")
        .sort_values(["model", "conservative_decision"])
    )

    lines = [
        f"# Aggregate experiment report: {OUT_PREFIX}",
        "",
        "Run tags:",
        "",
        *[f"- `{tag}`" for tag in tags],
        "",
        "## Best group-by-cell random-forest PhyK-TAS results",
        "",
        best.to_markdown(index=False),
        "",
        "## Conservative decision counts",
        "",
        decision_counts.to_markdown(index=False),
        "",
        "## Outputs",
        "",
        f"- `{pair_all_path.name}`",
        f"- `{pair_unc_path.name}`",
        f"- `{kbs_all_path.name}`",
        f"- `{kbs_unc_path.name}`",
        f"- `{decisions_path.name}`",
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"wrote {pair_all_path}")
    print(f"wrote {pair_unc_path}")
    print(f"wrote {kbs_all_path}")
    print(f"wrote {kbs_unc_path}")
    print(f"wrote {decisions_path}")
    print(f"wrote {report_path}")
    print(best.to_string(index=False))


if __name__ == "__main__":
    main()
