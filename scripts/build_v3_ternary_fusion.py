"""Ternary reliability/conflict fusion: extend the Stage-1 source-level fusion
to the Stage-2 agreement stream (three evidence sources).

The manuscript currently defines reliability weights and inter-source conflict
for the two Stage-1 views only (physical, shift) and incorporates the Stage-2
agreement stream through feature-level concatenation. This script closes that
gap with existing out-of-fold artifacts (no forecaster retraining):

  - three-source inverse-variance reliability fusion
        d_hat = w_p f_phys + w_s f_shift + w_a f_agree,
    with each source's sigma^2(region) estimated leave-one-region-out;
  - ternary inter-source conflict, the maximum pairwise disagreement
        c3 = max(|f_p - f_s|, |f_p - f_a|, |f_s - f_a|),
    which reduces to the paper's |f_phys - f_shift| in the two-source case;
  - the same repeated split-conformal decision routine as
    build_v3_operational_agreement (identical thresholds, cost matrix,
    split protocol), so the new policies are directly comparable to Table 9.

Policies evaluated:
  1. reliability_fusion_2src   + binary-conflict stratification  (reference)
  2. three_source_concat       + binary-conflict stratification  (reference)
  3. reliability_fusion_3src   + global conformal
  4. reliability_fusion_3src   + ternary-conflict stratification
  5. three_source_concat       + ternary-conflict stratification

Also reports per-model mean source weights and the ternary-conflict error
analysis (correlation with fused absolute error; error by conflict tercile).
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import pearsonr
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

OUT = PAPER / f"v3_ternary_fusion_{SUFFIX}.csv"
OUT_WEIGHTS = PAPER / f"v3_ternary_fusion_weights_{SUFFIX}.csv"
OUT_CONFLICT = PAPER / f"v3_ternary_conflict_{SUFFIX}.csv"
REPORT = PAPER / f"v3_ternary_fusion_{SUFFIX}_report.md"

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
    f_agree = sub[f"label_free_agreement_cold_{CV}_pred"].to_numpy()

    s2 = {
        "phys": leave_region_out_sigma2(y - f_phys, regions),
        "shift": leave_region_out_sigma2(y - f_shift, regions),
        "agree": leave_region_out_sigma2(y - f_agree, regions),
    }
    w = {k: np.array([1.0 / s2[k][r] for r in regions]) for k in s2}
    tot3 = w["phys"] + w["shift"] + w["agree"]
    wp3, ws3, wa3 = w["phys"] / tot3, w["shift"] / tot3, w["agree"] / tot3
    tot2 = w["phys"] + w["shift"]
    wp2 = w["phys"] / tot2

    frame = sub[["source_region", "target_region"]].copy()
    frame["d_obs"] = y
    frame["three_source_concat"] = sub[
        f"physical_plus_shift_plus_agreement_cold_{CV}_pred"
    ].to_numpy()
    frame["reliability_fusion_2src"] = wp2 * f_phys + (1.0 - wp2) * f_shift
    frame["reliability_fusion_3src"] = wp3 * f_phys + ws3 * f_shift + wa3 * f_agree
    frame["conflict2"] = np.abs(f_phys - f_shift)
    frame["conflict3"] = np.maximum.reduce(
        [np.abs(f_phys - f_shift), np.abs(f_phys - f_agree), np.abs(f_shift - f_agree)]
    )
    frame["w_phys"] = wp3
    frame["w_shift"] = ws3
    frame["w_agree"] = wa3
    return frame.groupby(["source_region", "target_region"], as_index=False).mean(numeric_only=True)


def evaluate(pair: pd.DataFrame, col: str, conflict_col: str | None, alpha: float) -> dict:
    pred = pair[col].to_numpy()
    obs = pair["d_obs"].to_numpy()
    obs_decision = decision_from_value(obs)
    stratified = conflict_col is not None
    conflict = pair[conflict_col].to_numpy() if stratified else None

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
        ("reliability_fusion_2src_conflict2", "reliability_fusion_2src", "conflict2"),
        ("three_source_concat_conflict2", "three_source_concat", "conflict2"),
        ("reliability_fusion_3src_global", "reliability_fusion_3src", None),
        ("reliability_fusion_3src_conflict3", "reliability_fusion_3src", "conflict3"),
        ("three_source_concat_conflict3", "three_source_concat", "conflict3"),
    ]
    rows, weight_rows, conflict_rows = [], [], []
    for model, sub in df.groupby("model"):
        pair = pair_predictions(sub.reset_index(drop=True))

        weight_rows.append(
            {
                "forecast_model": model,
                "mean_w_phys": float(pair["w_phys"].mean()),
                "mean_w_shift": float(pair["w_shift"].mean()),
                "mean_w_agree": float(pair["w_agree"].mean()),
            }
        )

        err3 = np.abs(pair["d_obs"] - pair["reliability_fusion_3src"])
        c3 = pair["conflict3"].to_numpy()
        r, p = pearsonr(c3, err3)
        t1, t2 = np.quantile(c3, [1.0 / 3.0, 2.0 / 3.0])
        ter = np.where(c3 <= t1, 0, np.where(c3 <= t2, 1, 2))
        conflict_rows.append(
            {
                "forecast_model": model,
                "pearson_r_conflict3_abs_err": float(r),
                "pearson_p": float(p),
                "abs_err_low": float(err3[ter == 0].mean()),
                "abs_err_mid": float(err3[ter == 1].mean()),
                "abs_err_high": float(err3[ter == 2].mean()),
            }
        )

        for policy, col, conflict_col in policies:
            point_r2 = r2_score(pair["d_obs"], pair[col])
            for alpha in ALPHAS:
                rec = {
                    "forecast_model": model,
                    "policy": policy,
                    "n_pairs": len(pair),
                    "point_r2": float(point_r2),
                }
                rec.update(evaluate(pair, col, conflict_col, alpha))
                rows.append(rec)
                print(
                    f"{model:24s} {policy:36s} a={alpha:.2f} "
                    f"cov={rec['empirical_coverage']:.3f} deploy={rec['deploy_rate']:.3f} "
                    f"unsafe={rec['unsafe_deploy_rate']:.3f} cost={rec['mean_cost']:.3f}",
                    flush=True,
                )

    res = pd.DataFrame(rows)
    res.to_csv(OUT, index=False)
    pd.DataFrame(weight_rows).to_csv(OUT_WEIGHTS, index=False)
    pd.DataFrame(conflict_rows).to_csv(OUT_CONFLICT, index=False)

    main_alpha = min(ALPHAS, key=lambda x: abs(x - 0.10))
    view = res[res["alpha"].round(6) == round(main_alpha, 6)].copy()
    lines = [
        f"# Ternary reliability/conflict fusion ({SUFFIX})",
        "",
        f"Same conformal decision protocol as v3_operational_agreement ({N_SPLITS} splits, "
        f"deploy <= {DEPLOY_THR:.3f}, adapt <= {ADAPT_THR:.3f}). Shown for alpha={main_alpha:.2f}.",
        "",
        "## Policy comparison",
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
        "## Mean three-source reliability weights (leave-one-region-out)",
        "",
        pd.DataFrame(weight_rows).round(3).to_markdown(index=False),
        "",
        "## Ternary conflict as an uncertainty proxy (3-source reliability fusion)",
        "",
        pd.DataFrame(conflict_rows).round(4).to_markdown(index=False),
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nwrote {OUT}\nwrote {OUT_WEIGHTS}\nwrote {OUT_CONFLICT}\nwrote {REPORT}")


if __name__ == "__main__":
    main()
