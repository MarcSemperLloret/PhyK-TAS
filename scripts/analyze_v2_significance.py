"""PhyK-TAS v2 statistical-significance analysis.

Turns the fragile "3 station samples -> t with 2 dof" uncertainty into a
defensible hierarchical bootstrap over spatial cells, pooled across the three
station-sample seeds. For each forecasting model it reports:

  * R^2 of each feature set (group-by-cell and leave-target-region-out),
    with a 95% hierarchical-bootstrap confidence interval;
  * the paired gain of physical+shift over generic-shift (Delta R^2), its
    bootstrap CI and one-sided p-value (H1: combined > shift);
  * Holm-Bonferroni-corrected p-values across the six forecasting models.

Uses only the already-computed cross-validated predictions, so it does NOT
re-train any forecaster. Bootstrap resampling unit is (seed, cell5), which
respects the nesting of stations within cells within station-sample seeds.
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import r2_score

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"

TAG = os.environ.get("PHYKTAS_V2_TAG", "all_viable_min100_full")
SEEDS = os.environ.get("PHYKTAS_V2_SEEDS", "s1,s2,s3").split(",")
N_BOOT = int(os.environ.get("PHYKTAS_V2_NBOOT", "2000"))
RNG = np.random.default_rng(int(os.environ.get("PHYKTAS_V2_SEED", "20260701")))

ESTIMATOR = "random_forest"
FEATURE_SETS = ["physical_knowledge", "generic_shift", "physical_plus_shift"]
CV_KINDS = ["group_by_cell", "leave_target_region_out"]
TARGET = "mae_out_minus_in"

OUT = PAPER / f"v2_significance_{TAG}.csv"
REPORT = PAPER / f"v2_significance_{TAG}_report.md"


def load_predictions() -> pd.DataFrame:
    frames = []
    for seed in SEEDS:
        path = PAPER / f"kbs_forecast_model_comparison_{TAG}_{seed}_predictions.csv"
        if not path.exists():
            raise FileNotFoundError(path)
        df = pd.read_csv(path)
        df["seed"] = seed
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def pred_col(feature_set: str, cv_kind: str) -> str:
    return f"{feature_set}_{cv_kind}_{ESTIMATOR}_pred"


def bootstrap_cluster_indices(cluster_ids: np.ndarray, n_boot: int):
    """Yield row-index arrays formed by resampling whole clusters with
    replacement (hierarchical bootstrap: stations nested in (seed, cell))."""
    uniq = np.unique(cluster_ids)
    # Pre-index rows by cluster once for speed.
    order = np.argsort(cluster_ids, kind="stable")
    sorted_ids = cluster_ids[order]
    boundaries = np.searchsorted(sorted_ids, uniq, side="left")
    ends = np.searchsorted(sorted_ids, uniq, side="right")
    rows_by_cluster = [order[b:e] for b, e in zip(boundaries, ends)]
    n = len(uniq)
    for _ in range(n_boot):
        pick = RNG.integers(0, n, size=n)
        yield np.concatenate([rows_by_cluster[i] for i in pick])


def analyze(df: pd.DataFrame) -> pd.DataFrame:
    records = []
    for cv_kind in CV_KINDS:
        for model, sub in df.groupby("model"):
            sub = sub.reset_index(drop=True)
            y = sub[TARGET].to_numpy()
            cluster = (sub["seed"].astype(str) + "|" + sub["cell5"].astype(str)).to_numpy()
            preds = {fs: sub[pred_col(fs, cv_kind)].to_numpy() for fs in FEATURE_SETS}

            point = {fs: r2_score(y, preds[fs]) for fs in FEATURE_SETS}

            # One shared set of bootstrap resamples -> paired comparisons.
            boot_r2 = {fs: np.empty(N_BOOT) for fs in FEATURE_SETS}
            for b, idx in enumerate(bootstrap_cluster_indices(cluster, N_BOOT)):
                yb = y[idx]
                for fs in FEATURE_SETS:
                    boot_r2[fs][b] = r2_score(yb, preds[fs][idx])

            delta = boot_r2["physical_plus_shift"] - boot_r2["generic_shift"]
            delta_phys = boot_r2["physical_plus_shift"] - boot_r2["physical_knowledge"]
            # One-sided p (H1: combined > shift): fraction of resamples not improving.
            p_vs_shift = float((delta <= 0).mean())
            p_vs_phys = float((delta_phys <= 0).mean())

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
            rec["delta_combined_minus_shift"] = point["physical_plus_shift"] - point["generic_shift"]
            rec["delta_cvs_lo"], rec["delta_cvs_hi"] = np.percentile(delta, [2.5, 97.5])
            rec["p_combined_gt_shift"] = p_vs_shift
            rec["delta_combined_minus_physical"] = point["physical_plus_shift"] - point["physical_knowledge"]
            rec["delta_cvp_lo"], rec["delta_cvp_hi"] = np.percentile(delta_phys, [2.5, 97.5])
            rec["p_combined_gt_physical"] = p_vs_phys
            records.append(rec)
    res = pd.DataFrame(records)
    # Holm-Bonferroni across the six models, within each cv_kind, for the
    # primary hypothesis (combined > shift).
    res["p_combined_gt_shift_holm"] = np.nan
    for cv_kind, grp in res.groupby("cv_kind"):
        p = grp["p_combined_gt_shift"].to_numpy()
        order = np.argsort(p)
        m = len(p)
        adj = np.empty(m)
        running = 0.0
        for rank, i in enumerate(order):
            val = (m - rank) * p[i]
            running = max(running, val)
            adj[i] = min(running, 1.0)
        res.loc[grp.index, "p_combined_gt_shift_holm"] = adj
    return res


def main() -> None:
    df = load_predictions()
    res = analyze(df)
    res.to_csv(OUT, index=False)

    def fmt(row, fs):
        return f"{row[f'r2_{fs}']:.3f} [{row[f'r2_{fs}_lo']:.3f}, {row[f'r2_{fs}_hi']:.3f}]"

    lines = [
        f"# PhyK-TAS v2 significance analysis ({TAG})",
        "",
        f"Hierarchical bootstrap over (seed, cell5) clusters, N={N_BOOT}, "
        f"pooled across seeds {SEEDS}. Estimator: {ESTIMATOR}.",
        "",
        "R^2 [95% bootstrap CI]. Delta = physical+shift minus generic-shift; "
        "p is one-sided (H1: combined > shift), Holm-corrected across the six models.",
        "",
    ]
    for cv_kind in CV_KINDS:
        sub = res[res["cv_kind"] == cv_kind].copy()
        lines += [f"## {cv_kind}", ""]
        tbl = pd.DataFrame({
            "model": sub["forecast_model"],
            "physical": [fmt(r, "physical_knowledge") for _, r in sub.iterrows()],
            "shift": [fmt(r, "generic_shift") for _, r in sub.iterrows()],
            "phys+shift": [fmt(r, "physical_plus_shift") for _, r in sub.iterrows()],
            "dR2(comb-shift)": [f"{r['delta_combined_minus_shift']:.3f} "
                                 f"[{r['delta_cvs_lo']:.3f}, {r['delta_cvs_hi']:.3f}]"
                                 for _, r in sub.iterrows()],
            "p_holm": [f"{r['p_combined_gt_shift_holm']:.4f}" for _, r in sub.iterrows()],
        })
        lines += [tbl.to_markdown(index=False), ""]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"wrote {REPORT}")
    print(res.to_string(index=False))


if __name__ == "__main__":
    main()
