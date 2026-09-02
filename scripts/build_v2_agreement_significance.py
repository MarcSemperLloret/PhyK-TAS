"""Significance analysis for the label-free agreement evidence source.

Hierarchical bootstrap over (seed, cell5) clusters on the out-of-fold
predictions saved by build_v2_agreement_estimators.py. For each forecasting
model and validation regime it reports:

  * R^2 with 95% bootstrap CI for the agreement (full and cold-start),
    physical+shift, and physical+shift+agreement feature sets;
  * the paired gain of physical+shift+agreement over physical+shift
    (does agreement add on top of the fused descriptor layer?), full and
    cold-start, with one-sided p-values Holm-corrected across models;
  * the paired difference of physical+shift versus agreement alone
    (two-sided characterization of the SOTA-comparator baseline).
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import r2_score

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"

SUFFIX = os.environ.get("AGREEMENT_OUT_SUFFIX", "all_viable_min100_full").strip()
N_BOOT = int(os.environ.get("PHYKTAS_V2_NBOOT", "2000"))
RNG = np.random.default_rng(int(os.environ.get("PHYKTAS_V2_SEED", "20260701")))

FEATURE_SETS = [
    "label_free_agreement",
    "label_free_agreement_cold",
    "physical_plus_shift",
    "physical_plus_shift_plus_agreement",
    "physical_plus_shift_plus_agreement_cold",
]
CV_KINDS = ["group_by_cell", "leave_target_region_out"]
TARGET = "mae_out_minus_in"

PRED_FILE = PAPER / f"v2_agreement_estimators_{SUFFIX}_predictions.csv"
OUT = PAPER / f"v2_agreement_significance_{SUFFIX}.csv"
REPORT = PAPER / f"v2_agreement_significance_{SUFFIX}_report.md"


def pred_col(feature_set: str, cv_kind: str) -> str:
    return f"{feature_set}_{cv_kind}_pred"


def bootstrap_cluster_indices(cluster_ids: np.ndarray, n_boot: int):
    uniq = np.unique(cluster_ids)
    order = np.argsort(cluster_ids, kind="stable")
    sorted_ids = cluster_ids[order]
    boundaries = np.searchsorted(sorted_ids, uniq, side="left")
    ends = np.searchsorted(sorted_ids, uniq, side="right")
    rows_by_cluster = [order[b:e] for b, e in zip(boundaries, ends)]
    n = len(uniq)
    for _ in range(n_boot):
        pick = RNG.integers(0, n, size=n)
        yield np.concatenate([rows_by_cluster[i] for i in pick])


def holm(pvals: np.ndarray) -> np.ndarray:
    order = np.argsort(pvals)
    m = len(pvals)
    adj = np.empty(m)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, (m - rank) * pvals[i])
        adj[i] = min(running, 1.0)
    return adj


def analyze(df: pd.DataFrame) -> pd.DataFrame:
    records = []
    for cv_kind in CV_KINDS:
        for model, sub in df.groupby("model"):
            sub = sub.reset_index(drop=True)
            y = sub[TARGET].to_numpy()
            cluster = (sub["seed"].astype(str) + "|" + sub["cell5"].astype(str)).to_numpy()
            preds = {fs: sub[pred_col(fs, cv_kind)].to_numpy() for fs in FEATURE_SETS}
            point = {fs: r2_score(y, preds[fs]) for fs in FEATURE_SETS}

            boot_r2 = {fs: np.empty(N_BOOT) for fs in FEATURE_SETS}
            for b, idx in enumerate(bootstrap_cluster_indices(cluster, N_BOOT)):
                yb = y[idx]
                for fs in FEATURE_SETS:
                    boot_r2[fs][b] = r2_score(yb, preds[fs][idx])

            delta_add = boot_r2["physical_plus_shift_plus_agreement"] - boot_r2["physical_plus_shift"]
            delta_add_cold = (
                boot_r2["physical_plus_shift_plus_agreement_cold"] - boot_r2["physical_plus_shift"]
            )
            delta_vs_agree = boot_r2["physical_plus_shift"] - boot_r2["label_free_agreement"]

            rec = {
                "cv_kind": cv_kind,
                "forecast_model": model,
                "n": len(sub),
                "n_clusters": len(np.unique(cluster)),
            }
            for fs in FEATURE_SETS:
                lo, hi = np.percentile(boot_r2[fs], [2.5, 97.5])
                rec[f"r2_{fs}"] = point[fs]
                rec[f"r2_{fs}_lo"] = lo
                rec[f"r2_{fs}_hi"] = hi
            rec["delta_add"] = (
                point["physical_plus_shift_plus_agreement"] - point["physical_plus_shift"]
            )
            rec["delta_add_lo"], rec["delta_add_hi"] = np.percentile(delta_add, [2.5, 97.5])
            rec["p_add"] = float((delta_add <= 0).mean())
            rec["delta_add_cold"] = (
                point["physical_plus_shift_plus_agreement_cold"] - point["physical_plus_shift"]
            )
            rec["delta_add_cold_lo"], rec["delta_add_cold_hi"] = np.percentile(delta_add_cold, [2.5, 97.5])
            rec["p_add_cold"] = float((delta_add_cold <= 0).mean())
            rec["delta_fused_minus_agree"] = point["physical_plus_shift"] - point["label_free_agreement"]
            rec["delta_fma_lo"], rec["delta_fma_hi"] = np.percentile(delta_vs_agree, [2.5, 97.5])
            records.append(rec)
            print(cv_kind, model, "done", flush=True)
    res = pd.DataFrame(records)
    for col in ["p_add", "p_add_cold"]:
        res[f"{col}_holm"] = np.nan
        for cv_kind, grp in res.groupby("cv_kind"):
            res.loc[grp.index, f"{col}_holm"] = holm(grp[col].to_numpy())
    return res


def main() -> None:
    df = pd.read_csv(PRED_FILE)
    res = analyze(df)
    res.to_csv(OUT, index=False)

    def fmt(row, fs):
        return f"{row[f'r2_{fs}']:.3f} [{row[f'r2_{fs}_lo']:.3f}, {row[f'r2_{fs}_hi']:.3f}]"

    lines = [
        f"# Agreement-source significance analysis ({SUFFIX})",
        "",
        f"Hierarchical bootstrap over (seed, cell5) clusters, N={N_BOOT}, seed-pooled.",
        "",
        "delta_add = (phys+shift+agreement) - (phys+shift); p one-sided, Holm across models.",
        "delta_fused_minus_agree = (phys+shift) - agreement-alone (two-sided CI).",
        "",
    ]
    for cv_kind in CV_KINDS:
        sub = res[res["cv_kind"] == cv_kind]
        lines += [f"## {cv_kind}", ""]
        tbl = pd.DataFrame({
            "model": sub["forecast_model"],
            "agree": [fmt(r, "label_free_agreement") for _, r in sub.iterrows()],
            "agree_cold": [fmt(r, "label_free_agreement_cold") for _, r in sub.iterrows()],
            "phys+shift": [fmt(r, "physical_plus_shift") for _, r in sub.iterrows()],
            "dR2 add [CI], p_holm": [
                f"{r['delta_add']:.3f} [{r['delta_add_lo']:.3f}, {r['delta_add_hi']:.3f}], p={r['p_add_holm']:.4f}"
                for _, r in sub.iterrows()
            ],
            "dR2 add cold [CI], p_holm": [
                f"{r['delta_add_cold']:.3f} [{r['delta_add_cold_lo']:.3f}, {r['delta_add_cold_hi']:.3f}], p={r['p_add_cold_holm']:.4f}"
                for _, r in sub.iterrows()
            ],
            "fused-agree [CI]": [
                f"{r['delta_fused_minus_agree']:.3f} [{r['delta_fma_lo']:.3f}, {r['delta_fma_hi']:.3f}]"
                for _, r in sub.iterrows()
            ],
        })
        lines += [tbl.to_markdown(index=False), ""]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
