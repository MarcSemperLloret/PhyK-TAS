"""Cost-matrix sensitivity of the operational policy ranking.

The asymmetric cost matrix of the main policy comparison is illustrative, so
this script tests whether the headline ranking (the three-source predictor
with conflict-stratified calibration is cheapest for five of six families)
depends on that particular matrix. The three Table-9 policies are re-evaluated
at alpha=0.10 under three preference profiles:

  C1 baseline   : deploy (0,5,10);  adapt (1,0,4); retrain (3,1,0)  [Table 2]
  C2 safety     : deploy (0,10,20); adapt (1,0,4); retrain (3,1,0)
                  (unsafe deployment twice as costly)
  C3 throughput : deploy (0,5,10);  adapt (2,0,4); retrain (6,2,0)
                  (unnecessary conservatism twice as costly)

All matrices are evaluated on identical calibration/test splits and identical
decision sequences, so differences reflect only the preference profile.
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd

from build_v3_fusion import leave_region_out_sigma2

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
SUFFIX = os.environ.get("AGREEMENT_OUT_SUFFIX", "all_viable_min100_full").strip()
PRED_FILE = PAPER / f"v2_agreement_estimators_{SUFFIX}_predictions.csv"

DEPLOY_THR = float(os.environ.get("PHYKTAS_DEPLOY_THR", "0.010"))
ADAPT_THR = float(os.environ.get("PHYKTAS_ADAPT_THR", "0.025"))
ALPHA = float(os.environ.get("PHYKTAS_POLICY_ALPHA", "0.10"))
N_SPLITS = int(os.environ.get("PHYKTAS_POLICY_SPLITS", "300"))
RNG = np.random.default_rng(int(os.environ.get("PHYKTAS_POLICY_SEED", "20260702")))

OUT = PAPER / f"v3_cost_sensitivity_{SUFFIX}.csv"
REPORT = PAPER / f"v3_cost_sensitivity_{SUFFIX}_report.md"

CV = "group_by_cell"

MATRICES = {
    "C1_baseline": {
        ("deploy", "deploy"): 0, ("deploy", "adapt"): 5, ("deploy", "retrain"): 10,
        ("adapt", "deploy"): 1, ("adapt", "adapt"): 0, ("adapt", "retrain"): 4,
        ("retrain", "deploy"): 3, ("retrain", "adapt"): 1, ("retrain", "retrain"): 0,
    },
    "C2_safety": {
        ("deploy", "deploy"): 0, ("deploy", "adapt"): 10, ("deploy", "retrain"): 20,
        ("adapt", "deploy"): 1, ("adapt", "adapt"): 0, ("adapt", "retrain"): 4,
        ("retrain", "deploy"): 3, ("retrain", "adapt"): 1, ("retrain", "retrain"): 0,
    },
    "C3_throughput": {
        ("deploy", "deploy"): 0, ("deploy", "adapt"): 5, ("deploy", "retrain"): 10,
        ("adapt", "deploy"): 2, ("adapt", "adapt"): 0, ("adapt", "retrain"): 4,
        ("retrain", "deploy"): 6, ("retrain", "adapt"): 2, ("retrain", "retrain"): 0,
    },
}


def q_upper(resid: np.ndarray, alpha: float) -> float:
    n = len(resid)
    k = min(max(int(np.ceil((n + 1) * (1 - alpha))), 1), n)
    return float(np.sort(resid)[k - 1])


def decision_from_value(x: np.ndarray) -> np.ndarray:
    return np.where(x <= DEPLOY_THR, "deploy", np.where(x <= ADAPT_THR, "adapt", "retrain"))


def pair_predictions(sub: pd.DataFrame) -> pd.DataFrame:
    y = sub["mae_out_minus_in"].to_numpy()
    regions = sub["target_region"].to_numpy()
    f_phys = sub[f"physical_knowledge_{CV}_pred"].to_numpy()
    f_shift = sub[f"generic_shift_{CV}_pred"].to_numpy()

    s2_phys = leave_region_out_sigma2(y - f_phys, regions)
    s2_shift = leave_region_out_sigma2(y - f_shift, regions)
    wp = np.array([1.0 / s2_phys[r] for r in regions])
    ws = np.array([1.0 / s2_shift[r] for r in regions])
    wp = wp / (wp + ws)

    frame = sub[["source_region", "target_region"]].copy()
    frame["d_obs"] = y
    frame["concat"] = sub[f"physical_plus_shift_{CV}_pred"].to_numpy()
    frame["reliability_fusion"] = wp * f_phys + (1.0 - wp) * f_shift
    frame["three_source_excl_local"] = sub[
        f"physical_plus_shift_plus_agreement_cold_{CV}_pred"
    ].to_numpy()
    frame["conflict"] = np.abs(f_phys - f_shift)
    return frame.groupby(["source_region", "target_region"], as_index=False).mean(numeric_only=True)


def evaluate(pair: pd.DataFrame, col: str, stratified: bool) -> dict:
    pred = pair[col].to_numpy()
    obs = pair["d_obs"].to_numpy()
    conflict = pair["conflict"].to_numpy()
    obs_decision = decision_from_value(obs)

    idx = np.arange(len(pair))
    costs = {name: [] for name in MATRICES}
    for _ in range(N_SPLITS):
        RNG.shuffle(idx)
        half = len(idx) // 2
        cal, tst = idx[:half], idx[half:]
        q_global = q_upper(obs[cal] - pred[cal], ALPHA)
        if stratified:
            c1, c2 = np.quantile(conflict[cal], [1.0 / 3.0, 2.0 / 3.0])
            ter_cal = np.where(conflict[cal] <= c1, 0, np.where(conflict[cal] <= c2, 1, 2))
            ter_tst = np.where(conflict[tst] <= c1, 0, np.where(conflict[tst] <= c2, 1, 2))
            q_by_t = {}
            for t in (0, 1, 2):
                m = cal[ter_cal == t]
                q_by_t[t] = q_upper(obs[m] - pred[m], ALPHA) if len(m) >= 5 else q_global
            q = np.array([q_by_t[int(t)] for t in ter_tst])
        else:
            q = np.full(len(tst), q_global)

        pred_decision = decision_from_value(pred[tst] + q)
        obs_t = obs_decision[tst]
        for name, C in MATRICES.items():
            costs[name].append(float(np.mean([C[(p, o)] for p, o in zip(pred_decision, obs_t)])))

    return {name: float(np.mean(v)) for name, v in costs.items()}


def main() -> None:
    df = pd.read_csv(PRED_FILE)
    policies = [
        ("concat_global", "concat", False),
        ("reliability_fusion_conflict_stratified", "reliability_fusion", True),
        ("three_source_excl_local_conflict_stratified", "three_source_excl_local", True),
    ]
    rows = []
    for model, sub in df.groupby("model"):
        pair = pair_predictions(sub.reset_index(drop=True))
        for policy, col, stratified in policies:
            rec = {"forecast_model": model, "policy": policy}
            rec.update(evaluate(pair, col, stratified))
            rows.append(rec)
            print(f"{model:24s} {policy:44s} " + " ".join(
                f"{k}={rec[k]:.3f}" for k in MATRICES), flush=True)

    res = pd.DataFrame(rows)
    res.to_csv(OUT, index=False)

    lines = [
        f"# Cost-matrix sensitivity of the policy ranking ({SUFFIX})",
        "",
        f"alpha={ALPHA:.2f}, {N_SPLITS} splits, deploy <= {DEPLOY_THR:.3f}, adapt <= "
        f"{ADAPT_THR:.3f}. All matrices share identical splits and decisions.",
        "",
        res.round(3).to_markdown(index=False),
        "",
        "## Winner per model per matrix",
        "",
    ]
    for name in MATRICES:
        winners = res.loc[res.groupby("forecast_model")[name].idxmin()]
        n_three = (winners["policy"] == "three_source_excl_local_conflict_stratified").sum()
        lines.append(f"- {name}: three-source+conflict cheapest for {n_three} of "
                     f"{winners.shape[0]} families "
                     f"(exceptions: "
                     + (", ".join(winners.loc[winners['policy'] != 'three_source_excl_local_conflict_stratified', 'forecast_model']) or "none")
                     + ")")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nwrote {OUT}\nwrote {REPORT}")


if __name__ == "__main__":
    main()
