"""PhyK-TAS v2: cost-sensitive decision evaluation.

Compares PhyK-TAS deploy/adapt/retrain recommendations against simple decision
policies. The goal is not to define universal operational costs, but to check
whether the decision layer improves under asymmetric costs where unsafe deploys
are more expensive than unnecessary adaptation or retraining.
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
TAG = os.environ.get("PHYKTAS_V2_TAG", "all_viable_min100_full")

DEPLOY_THR = 0.010
ADAPT_THR = 0.025

OUT = PAPER / f"v2_decision_costs_{TAG}.csv"
REPORT = PAPER / f"v2_decision_costs_{TAG}_report.md"

COST = {
    ("deploy", "deploy"): 0.0,
    ("deploy", "adapt"): 5.0,
    ("deploy", "retrain"): 10.0,
    ("adapt", "deploy"): 1.0,
    ("adapt", "adapt"): 0.0,
    ("adapt", "retrain"): 4.0,
    ("retrain", "deploy"): 3.0,
    ("retrain", "adapt"): 1.0,
    ("retrain", "retrain"): 0.0,
}


def decision_from_value(x: float) -> str:
    if x <= DEPLOY_THR:
        return "deploy"
    if x <= ADAPT_THR:
        return "adapt"
    return "retrain"


def rank_policy(values: pd.Series, low: float = 0.25, mid: float = 0.50) -> pd.Series:
    """Low values are better: bottom quartile deploys, next quartile adapts."""
    pct = values.rank(method="average", pct=True)
    return pd.Series(
        np.where(pct <= low, "deploy", np.where(pct <= mid, "adapt", "retrain")),
        index=values.index,
    )


def load_inputs() -> pd.DataFrame:
    pairs = pd.read_csv(PAPER / f"{TAG}_decision_validation_pairs.csv")
    src = pd.read_csv(PAPER / f"{TAG}_source_accuracy_vs_transfer.csv")
    src = (
        src.groupby(["model", "source_region", "target_region"], as_index=False)
        .agg(source_in_region_mae=("source_in_region_mae", "mean"))
    )
    shift = pd.read_csv(PAPER / "distribution_shift_baselines_all_viable_min100.csv")
    shift["shift_rank_score"] = (
        shift["wasserstein_precip"].rank(pct=True)
        + shift["shift_monthly_l2"].rank(pct=True)
        + shift["region_centroid_distance_deg"].rank(pct=True)
    ) / 3.0
    out = pairs.merge(src, on=["model", "source_region", "target_region"], how="left")
    out = out.merge(shift[["source_region", "target_region", "shift_rank_score"]],
                    on=["source_region", "target_region"], how="left")
    return out


def add_policies(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["policy_phyk_tas_conservative"] = out["predicted_conservative_decision"]
    out["policy_phyk_tas_expected"] = out["predicted_expected_decision"]
    out["policy_predicted_mean"] = out["predicted_degradation_mean"].map(decision_from_value)
    out["policy_always_deploy"] = "deploy"
    out["policy_always_adapt"] = "adapt"
    out["policy_always_retrain"] = "retrain"
    out["policy_source_accuracy_rank"] = (
        out.groupby("model", group_keys=False)["source_in_region_mae"].apply(rank_policy)
    )
    out["policy_shift_rank"] = (
        out.groupby("model", group_keys=False)["shift_rank_score"].apply(rank_policy)
    )
    return out


def evaluate(df: pd.DataFrame, observed_col: str) -> pd.DataFrame:
    policies = [c for c in df.columns if c.startswith("policy_")]
    rows = []
    for model, sub in df.groupby("model"):
        obs = sub[observed_col]
        for policy in policies:
            pred = sub[policy]
            costs = [COST[(p, o)] for p, o in zip(pred, obs)]
            unsafe = ((pred == "deploy") & (obs != "deploy")).mean()
            unnecessary_retrain = ((pred == "retrain") & (obs == "deploy")).mean()
            rows.append({
                "forecast_model": model,
                "observed_reference": observed_col,
                "policy": policy.replace("policy_", ""),
                "mean_cost": float(np.mean(costs)),
                "unsafe_deploy_rate": float(unsafe),
                "unnecessary_retrain_rate": float(unnecessary_retrain),
                "deploy_rate": float((pred == "deploy").mean()),
                "adapt_rate": float((pred == "adapt").mean()),
                "retrain_rate": float((pred == "retrain").mean()),
                "n_pairs": len(sub),
            })
    return pd.DataFrame(rows)


def main() -> None:
    df = add_policies(load_inputs())
    res = pd.concat([
        evaluate(df, "observed_expected_decision"),
        evaluate(df, "observed_conservative_decision"),
    ], ignore_index=True)
    res.to_csv(OUT, index=False)

    lines = [
        f"# PhyK-TAS v2 cost-sensitive decision evaluation ({TAG})",
        "",
        "Cost matrix: unsafe deploy to an adapt case = 5; unsafe deploy to a "
        "retrain case = 10; unnecessary retrain of a deploy case = 3; adapt "
        "instead of deploy = 1; retrain instead of adapt = 1; adapt instead of "
        "retrain = 4. These costs are illustrative and test decision asymmetry.",
        "",
    ]
    for ref in ["observed_expected_decision", "observed_conservative_decision"]:
        sub = res[res["observed_reference"] == ref].copy()
        best = sub.sort_values(["forecast_model", "mean_cost"]).groupby("forecast_model").head(3)
        lines += [f"## {ref}", "", best.round(4).to_markdown(index=False), ""]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
