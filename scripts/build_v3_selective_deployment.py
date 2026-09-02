"""PhyK-TAS v3 -- risk-controlled selective deployment under regime shift.

Cross-regime (leave-target-region-out) deployment decision at the source-target
pair level. A pair is *deployable* only if a conformal upper bound on its
degradation lies below the deploy threshold; otherwise the system abstains
(adapt/retrain). We compare four decision policies that differ in how the bound
is calibrated / when the system abstains:

  1. global      : one leave-region-out residual quantile for all pairs;
  2. conflict    : quantile conditioned on the inter-source conflict tercile;
  3. distance    : quantile conditioned on the target region's support-distance;
  4. reject-OOS  : global bound, but hard-abstain pairs whose target region is
                   out-of-support (top support-distance tercile).

The unifying metric is a risk--coverage (selective-deployment) curve: sweeping
the tolerance, how many transfers are deployed versus the unsafe-deploy rate
among deployed. A better policy deploys more safe transfers at the same risk.
Support-distance and conflict are the fusion signals from earlier sections.
"""
from __future__ import annotations

import os
import warnings

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import LeaveOneGroupOut

warnings.filterwarnings("ignore")

from build_v2_meta_models import (
    PAPER, TAG, SEEDS, PHYSICAL_COLS, SHIFT_COLS, TARGET, load_seed,
)
from build_v3_distance_generalization import region_phys_distance

FIG_DIRS = [PAPER / "figures", PAPER / "manuscript_latex_infofusion" / "figures"]
for d in FIG_DIRS:
    d.mkdir(parents=True, exist_ok=True)

DEPLOY_THR = float(os.environ.get("PHYKTAS_DEPLOY_THR", "0.010"))
MODELS = ["spatial_knn_ridge", "stgcn_diffusion", "graphwavenet_transfer"]
FEAT = PHYSICAL_COLS + SHIFT_COLS
ALPHAS = np.round(np.arange(0.02, 0.61, 0.02), 3)
OUT = PAPER / f"v3_selective_deployment_{TAG}.csv"
REPORT = PAPER / f"v3_selective_deployment_{TAG}_report.md"


def clean(df, cols):
    x = df[cols].replace([np.inf, -np.inf], np.nan)
    return x.fillna(x.median(numeric_only=True)).to_numpy()


def ltro_oof(sub, cols):
    y = sub[TARGET].to_numpy()
    X = clean(sub, cols)
    g = sub["target_region"].to_numpy()
    pred = np.full(len(y), np.nan)
    for tr, te in LeaveOneGroupOut().split(X, y, g):
        est = HistGradientBoostingRegressor(max_iter=400, learning_rate=0.05,
                                            random_state=20260524)
        est.fit(X[tr], y[tr])
        pred[te] = est.predict(X[te])
    return pred


def q_upper(res, alpha):
    if len(res) < 3:
        return np.inf
    n = len(res)
    k = min(max(int(np.ceil((n + 1) * (1 - alpha))), 1), n)
    return np.sort(res)[k - 1]


def pair_table(sub, dist):
    """Aggregate LTRO station predictions to source-target pairs."""
    y = sub[TARGET].to_numpy()
    d_pred = ltro_oof(sub, FEAT)
    f_p = ltro_oof(sub, PHYSICAL_COLS)
    f_s = ltro_oof(sub, SHIFT_COLS)
    t = sub[["source_region", "target_region"]].copy()
    t["d_pred"] = d_pred; t["d_obs"] = y; t["conflict"] = np.abs(f_p - f_s)
    pair = t.groupby(["source_region", "target_region"]).mean().reset_index()
    pair["dist"] = pair["target_region"].map(dist)
    return pair


def decisions(pair, alpha, policy, ct, dt, oos_cut):
    """Return boolean deploy mask for all pairs under a policy at tolerance alpha.
    Calibration is leave-region-out (a pair's own target region is excluded)."""
    reg = pair["target_region"].to_numpy()
    resid = (pair["d_obs"] - pair["d_pred"]).to_numpy()
    conf = pair["conflict"].to_numpy()
    dist = pair["dist"].to_numpy()
    dpred = pair["d_pred"].to_numpy()
    c_ter = np.digitize(conf, ct)   # 0/1/2
    d_ter = np.digitize(dist, dt)
    deploy = np.zeros(len(pair), bool)
    for i in range(len(pair)):
        cal = reg != reg[i]
        if policy == "global" or policy == "reject":
            q = q_upper(resid[cal], alpha)
        elif policy == "conflict":
            m = cal & (c_ter == c_ter[i])
            q = q_upper(resid[m], alpha) if m.sum() >= 5 else q_upper(resid[cal], alpha)
        elif policy == "distance":
            m = cal & (d_ter == d_ter[i])
            q = q_upper(resid[m], alpha) if m.sum() >= 5 else q_upper(resid[cal], alpha)
        else:
            raise ValueError(policy)
        if policy == "reject" and dist[i] > oos_cut:
            deploy[i] = False
            continue
        deploy[i] = (dpred[i] + q) <= DEPLOY_THR
    return deploy


def main() -> None:
    df = pd.concat([load_seed(s) for s in SEEDS], ignore_index=True)
    dist = region_phys_distance(df)
    rows = []
    fig, axes = plt.subplots(1, len(MODELS), figsize=(11, 3.4), sharey=True)
    for ax, model in zip(np.atleast_1d(axes), MODELS):
        sub = df[df["model"] == model].reset_index(drop=True)
        pair = pair_table(sub, dist)
        safe = (pair["d_obs"] <= DEPLOY_THR).to_numpy()
        n_safe = int(safe.sum()); n_pairs = len(pair)
        ct = np.quantile(pair["conflict"], [1/3, 2/3])
        dt = np.quantile(pair["dist"], [1/3, 2/3])
        oos_cut = float(np.quantile(pair["dist"], 2/3))  # top distance tercile
        for policy in ["global", "conflict", "distance", "reject"]:
            for a in ALPHAS:
                dep = decisions(pair, a, policy, ct, dt, oos_cut)
                nd = int(dep.sum())
                unsafe = float(np.mean(pair["d_obs"].to_numpy()[dep] > DEPLOY_THR)) if nd else 0.0
                safe_dep = int(np.sum(dep & safe))
                rows.append({"model": model, "policy": policy, "alpha": a,
                             "n_deploy": nd, "unsafe_rate": unsafe,
                             "safe_deploy": safe_dep, "n_safe": n_safe, "n_pairs": n_pairs})
        # plot risk-coverage (safe_deploy vs unsafe_rate) per policy
        subrows = pd.DataFrame([r for r in rows if r["model"] == model])
        for policy in ["global", "conflict", "distance", "reject"]:
            p = subrows[subrows.policy == policy].sort_values("unsafe_rate")
            ax.plot(p["unsafe_rate"], p["safe_deploy"], marker="o", ms=3, label=policy)
        ax.set_title(model, fontsize=9)
        ax.set_xlabel("unsafe-deploy rate")
        ax.axhline(n_safe, ls=":", c="gray", lw=0.8)
    axes[0].set_ylabel("safe transfers deployed")
    axes[-1].legend(fontsize=7)
    fig.tight_layout()
    for d in FIG_DIRS:
        fig.savefig(d / "fig_v3_selective_deployment.png", dpi=200, bbox_inches="tight")
        fig.savefig(d / "fig_v3_selective_deployment.pdf", bbox_inches="tight")

    res = pd.DataFrame(rows)
    res.to_csv(OUT, index=False)

    # headline: at unsafe_rate <= 0.10, max safe deployments per policy per model
    lines = [f"# Risk-controlled selective deployment ({TAG})", "",
             f"LTRO, pair-level, deploy threshold {DEPLOY_THR}. "
             "At a capped unsafe-deploy rate, how many safe transfers each policy deploys.", ""]
    for cap in [0.05, 0.10]:
        lines.append(f"## Max safe deployments at unsafe-rate <= {cap}")
        tab = {}
        for model in MODELS:
            row = {}
            for policy in ["global", "conflict", "distance", "reject"]:
                d = res[(res.model == model) & (res.policy == policy) & (res.unsafe_rate <= cap)]
                row[policy] = int(d["safe_deploy"].max()) if len(d) else 0
            row["n_safe"] = int(res[res.model == model]["n_safe"].iloc[0])
            tab[model] = row
        lines.append(pd.DataFrame(tab).T.to_markdown())
        lines.append("")
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"wrote {OUT}\nwrote {REPORT}")


if __name__ == "__main__":
    main()
