"""Selective deployment in the WITHIN-LIBRARY (group-by-cell) operational setting.

Complements the leave-target-region-out analysis: here the target regime is
represented during calibration, so deployment is actually viable. We compare a
global split-conformal deploy rule against a conflict-conditioned one and ask,
at a capped unsafe-deploy rate, how many safe transfers each deploys. Support
distance is ~0 in-library, so only global vs. conflict are compared.
"""
from __future__ import annotations

import os
import warnings

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import GroupKFold

warnings.filterwarnings("ignore")

from build_v2_meta_models import (
    PAPER, TAG, SEEDS, PHYSICAL_COLS, SHIFT_COLS, TARGET, load_seed,
)

DEPLOY_THR = float(os.environ.get("PHYKTAS_DEPLOY_THR", "0.010"))
MODELS = ["spatial_knn_ridge", "regional_doy_climatology",
          "stgcn_diffusion", "graphwavenet_transfer"]
FEAT = PHYSICAL_COLS + SHIFT_COLS
ALPHAS = np.round(np.arange(0.02, 0.61, 0.02), 3)
N_SPLITS = 200
RNG = np.random.default_rng(20260701)
REPORT = PAPER / f"v3_selective_gbc_{TAG}_report.md"


def clean(df, cols):
    x = df[cols].replace([np.inf, -np.inf], np.nan)
    return x.fillna(x.median(numeric_only=True)).to_numpy()


def gbc_oof(sub, cols):
    y = sub[TARGET].to_numpy(); X = clean(sub, cols); g = sub["cell5"].to_numpy()
    cv = GroupKFold(n_splits=min(5, sub["cell5"].nunique()))
    pred = np.full(len(y), np.nan)
    for tr, te in cv.split(X, y, g):
        est = HistGradientBoostingRegressor(max_iter=400, learning_rate=0.05,
                                            random_state=20260524)
        est.fit(X[tr], y[tr]); pred[te] = est.predict(X[te])
    return pred


def q_upper(res, alpha):
    if len(res) < 3:
        return np.inf
    n = len(res); k = min(max(int(np.ceil((n + 1) * (1 - alpha))), 1), n)
    return np.sort(res)[k - 1]


def main() -> None:
    df = pd.concat([load_seed(s) for s in SEEDS], ignore_index=True)
    lines = [f"# Within-library selective deployment ({TAG})", "",
             f"Group-by-cell, deploy threshold {DEPLOY_THR}, {N_SPLITS} split-conformal "
             "repetitions. Max safe deployments at a capped unsafe-deploy rate.", ""]
    summary = {0.05: {}, 0.10: {}}
    for model in MODELS:
        sub = df[df["model"] == model].reset_index(drop=True)
        y = sub[TARGET].to_numpy()
        d_pred = gbc_oof(sub, FEAT); f_p = gbc_oof(sub, PHYSICAL_COLS); f_s = gbc_oof(sub, SHIFT_COLS)
        t = sub[["source_region", "target_region"]].copy()
        t["d_pred"] = d_pred; t["d_obs"] = y; t["conflict"] = np.abs(f_p - f_s)
        pair = t.groupby(["source_region", "target_region"]).mean().reset_index()
        dpred = pair["d_pred"].to_numpy(); dobs = pair["d_obs"].to_numpy()
        conf = pair["conflict"].to_numpy(); safe = dobs <= DEPLOY_THR
        ct = np.quantile(conf, [1/3, 2/3]); cter = np.digitize(conf, ct)
        idx = np.arange(len(pair))
        # accumulate per (policy, alpha): unsafe_rate, safe_deploy
        acc = {p: {a: {"nd": [], "un": [], "sd": []} for a in ALPHAS}
               for p in ["global", "conflict"]}
        for _ in range(N_SPLITS):
            RNG.shuffle(idx); half = len(idx) // 2
            cal, tst = idx[:half], idx[half:]
            res = dobs[cal] - dpred[cal]
            for a in ALPHAS:
                qg = q_upper(res, a)
                for policy in ["global", "conflict"]:
                    if policy == "global":
                        up = dpred[tst] + qg
                    else:
                        up = np.empty(len(tst))
                        for j, i in enumerate(tst):
                            m = cter[cal] == cter[i]
                            qq = q_upper(res[m], a) if m.sum() >= 5 else qg
                            up[j] = dpred[i] + qq
                    dep = up <= DEPLOY_THR
                    nd = int(dep.sum())
                    un = float(np.mean(dobs[tst][dep] > DEPLOY_THR)) if nd else 0.0
                    sd = int(np.sum(dep & safe[tst]))
                    acc[policy][a]["nd"].append(nd)
                    acc[policy][a]["un"].append(un)
                    acc[policy][a]["sd"].append(sd)
        for cap in (0.05, 0.10):
            row = {}
            for policy in ["global", "conflict"]:
                best = 0
                for a in ALPHAS:
                    un = float(np.mean(acc[policy][a]["un"]))
                    sd = float(np.mean(acc[policy][a]["sd"]))
                    if un <= cap:
                        best = max(best, sd)
                row[policy] = round(best, 1)
            row["n_safe(of 55/split)"] = round(float(np.mean(safe) * (len(pair) / 2)), 1)
            summary[cap][model] = row
        print(f"{model}: done")
    for cap in (0.05, 0.10):
        lines.append(f"## Mean safe deployments/split at unsafe-rate <= {cap}")
        lines.append(pd.DataFrame(summary[cap]).T.to_markdown())
        lines.append("")
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
