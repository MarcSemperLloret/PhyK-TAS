"""Operational integration of the agreement evidence source (Stage 3).

Re-runs the operational policy comparison of build_v3_operational_policy_comparison
on the agreement-run out-of-fold predictions, so that the three-source predictor
(physical + shift + target-model-excluded agreement) is evaluated inside the
same conformal decision routine as the descriptor-only policies:

  1. concatenation (phys+shift) + global conformal;
  2. fixed-weight physical/shift source fusion + global conformal;
  3. reliability-weighted source fusion + global conformal;
  4. reliability-weighted source fusion + conflict-stratified conformal;
  5. three-source concatenation (phys+shift+agreement, excl. local model) + global;
  6. three-source concatenation + conflict-stratified conformal.

All policies use the same seed-pooled group-by-cell out-of-fold predictions
aggregated to source-target pairs, the same repeated calibration/test splits,
and the same asymmetric cost matrix.
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import r2_score

from build_v2_conformal_utility import COST
from build_v3_fusion import leave_region_out_sigma2

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
SUFFIX = os.environ.get("AGREEMENT_OUT_SUFFIX", "all_viable_min100_full").strip()
PRED_FILE = PAPER / f"v2_agreement_estimators_{SUFFIX}_predictions.csv"

DEPLOY_THR = float(os.environ.get("PHYKTAS_DEPLOY_THR", "0.010"))
ADAPT_THR = float(os.environ.get("PHYKTAS_ADAPT_THR", "0.025"))
ALPHAS = [float(x) for x in os.environ.get("PHYKTAS_POLICY_ALPHAS", "0.20,0.10,0.05").split(",")]
N_SPLITS = int(os.environ.get("PHYKTAS_POLICY_SPLITS", "300"))
RNG = np.random.default_rng(int(os.environ.get("PHYKTAS_POLICY_SEED", "20260702")))

OUT = PAPER / f"v3_operational_agreement_{SUFFIX}.csv"
REPORT = PAPER / f"v3_operational_agreement_{SUFFIX}_report.md"

CV = "group_by_cell"


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
    frame["fixed_source_fusion"] = 0.5 * f_phys + 0.5 * f_shift
    frame["reliability_fusion"] = wp * f_phys + (1.0 - wp) * f_shift
    frame["three_source_excl_local"] = sub[
        f"physical_plus_shift_plus_agreement_cold_{CV}_pred"
    ].to_numpy()
    frame["agreement_excl_local"] = sub[f"label_free_agreement_cold_{CV}_pred"].to_numpy()
    frame["conflict"] = np.abs(f_phys - f_shift)
    return frame.groupby(["source_region", "target_region"], as_index=False).mean(numeric_only=True)


def evaluate(pair: pd.DataFrame, col: str, alpha: float, stratified: bool) -> dict:
    pred = pair[col].to_numpy()
    obs = pair["d_obs"].to_numpy()
    conflict = pair["conflict"].to_numpy()
    obs_decision = decision_from_value(obs)

    idx = np.arange(len(pair))
    cover, width, deploy, adapt, retrain, unsafe, costs = [], [], [], [], [], [], []
    for _ in range(N_SPLITS):
        RNG.shuffle(idx)
        half = len(idx) // 2
        cal, tst = idx[:half], idx[half:]
        q_global = q_upper(obs[cal] - pred[cal], alpha)
        if stratified:
            c1, c2 = np.quantile(conflict[cal], [1.0 / 3.0, 2.0 / 3.0])
            ter_cal = np.where(conflict[cal] <= c1, 0, np.where(conflict[cal] <= c2, 1, 2))
            ter_tst = np.where(conflict[tst] <= c1, 0, np.where(conflict[tst] <= c2, 1, 2))
            q_by_t = {}
            for t in (0, 1, 2):
                m = cal[ter_cal == t]
                q_by_t[t] = q_upper(obs[m] - pred[m], alpha) if len(m) >= 5 else q_global
            q = np.array([q_by_t[int(t)] for t in ter_tst])
        else:
            q = np.full(len(tst), q_global)

        upper = pred[tst] + q
        pred_decision = decision_from_value(upper)
        obs_t = obs_decision[tst]
        deploy_mask = pred_decision == "deploy"

        cover.append(float(np.mean(obs[tst] <= upper)))
        width.append(float(np.mean(q)))
        deploy.append(float(np.mean(pred_decision == "deploy")))
        adapt.append(float(np.mean(pred_decision == "adapt")))
        retrain.append(float(np.mean(pred_decision == "retrain")))
        unsafe.append(float(np.mean(obs_t[deploy_mask] != "deploy")) if deploy_mask.any() else np.nan)
        costs.append(float(np.mean([COST[(p, o)] for p, o in zip(pred_decision, obs_t)])))

    return {
        "alpha": alpha,
        "target_coverage": 1.0 - alpha,
        "empirical_coverage": float(np.mean(cover)),
        "mean_bound_width": float(np.mean(width)),
        "deploy_rate": float(np.mean(deploy)),
        "adapt_rate": float(np.mean(adapt)),
        "retrain_rate": float(np.mean(retrain)),
        "unsafe_deploy_rate": float(np.nanmean(unsafe)) if np.isfinite(unsafe).any() else 0.0,
        "mean_cost": float(np.mean(costs)),
    }


def main() -> None:
    df = pd.read_csv(PRED_FILE)
    policies = [
        ("concat_global", "concat", False),
        ("fixed_source_fusion_global", "fixed_source_fusion", False),
        ("reliability_fusion_global", "reliability_fusion", False),
        ("reliability_fusion_conflict_stratified", "reliability_fusion", True),
        ("three_source_excl_local_global", "three_source_excl_local", False),
        ("three_source_excl_local_conflict_stratified", "three_source_excl_local", True),
    ]
    rows = []
    for model, sub in df.groupby("model"):
        pair = pair_predictions(sub.reset_index(drop=True))
        for policy, col, stratified in policies:
            point_r2 = r2_score(pair["d_obs"], pair[col])
            for alpha in ALPHAS:
                rec = {
                    "forecast_model": model,
                    "policy": policy,
                    "n_pairs": len(pair),
                    "point_r2": float(point_r2),
                }
                rec.update(evaluate(pair, col, alpha, stratified))
                rows.append(rec)
                print(
                    f"{model:24s} {policy:44s} a={alpha:.2f} "
                    f"cov={rec['empirical_coverage']:.3f} deploy={rec['deploy_rate']:.3f} "
                    f"unsafe={rec['unsafe_deploy_rate']:.3f} cost={rec['mean_cost']:.3f}",
                    flush=True,
                )

    res = pd.DataFrame(rows)
    res.to_csv(OUT, index=False)

    main_alpha = min(ALPHAS, key=lambda x: abs(x - 0.10))
    view = res[res["alpha"].round(6) == round(main_alpha, 6)].copy()
    lines = [
        f"# Operational policy comparison with the agreement source ({SUFFIX})",
        "",
        f"Same protocol as v3_operational_policy_comparison ({N_SPLITS} splits, deploy <= "
        f"{DEPLOY_THR:.3f}, adapt <= {ADAPT_THR:.3f}), on the agreement-run out-of-fold "
        f"predictions so all six policies share identical targets. Shown for alpha={main_alpha:.2f}.",
        "",
        view[
            [
                "forecast_model",
                "policy",
                "point_r2",
                "empirical_coverage",
                "mean_bound_width",
                "deploy_rate",
                "unsafe_deploy_rate",
                "mean_cost",
            ]
        ].round(4).to_markdown(index=False),
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nwrote {OUT}\nwrote {REPORT}")


if __name__ == "__main__":
    main()
