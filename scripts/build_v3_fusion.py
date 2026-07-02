"""PhyK-TAS v3 -- reliability-aware information fusion (upgrades A, B, C).

Moves beyond feature concatenation + stacking to genuine evidence fusion:

  B (complementarity): per target region, which single evidence source
    (physical-only vs shift-only degradation predictor) is more reliable, showing
    that different sources dominate in different regimes.

  A (precision-weighted fusion): each source is a separate degradation predictor
    with a context-dependent reliability sigma_s(region), estimated leave-one-
    region-out from its residual variance; sources are fused at the estimate level
    by inverse-variance weighting d_hat = sum_s w_s(r) f_s(x),
    w_s(r) = (1/sigma_s^2(r)) / sum. Compared against physical-only, shift-only,
    and concatenation-RF.

  C (conflict -> uncertainty): inter-source disagreement |f_phys - f_shift| is
    tested as an epistemic-uncertainty signal that predicts larger fusion error.

Operates on group-by-cell out-of-fold predictions from the existing artifacts;
no forecaster retraining.
"""
from __future__ import annotations

import os
import warnings

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import r2_score

warnings.filterwarnings("ignore")

from build_v2_meta_models import (
    PAPER, TAG, SEEDS, PHYSICAL_COLS, SHIFT_COLS, TARGET,
    load_seed, build_splits, oof_predict_sklearn,
)

MODELS = ["spatial_knn_ridge", "stgcn_diffusion", "graphwavenet_transfer",
          "regional_doy_climatology"]
MIN_REGION_ROWS = 30

OUT_A = PAPER / f"v3_fusion_scores_{TAG}.csv"
OUT_B = PAPER / f"v3_complementarity_{TAG}.csv"
OUT_C = PAPER / f"v3_conflict_{TAG}.csv"
REPORT = PAPER / f"v3_fusion_{TAG}_report.md"


def clean(df, cols):
    x = df[cols].replace([np.inf, -np.inf], np.nan)
    return x.fillna(x.median(numeric_only=True)).to_numpy()


def source_oof(sub, cols, splits, y):
    return oof_predict_sklearn("random_forest", clean(sub, cols), y, splits)


def leave_region_out_sigma2(resid, regions):
    """sigma_s^2 for each region estimated from residuals of all OTHER regions,
    so a region's fusion weights never use its own residuals."""
    uniq = np.unique(regions)
    global_var = float(np.var(resid)) + 1e-9
    out = {}
    for r in uniq:
        other = resid[regions != r]
        out[r] = float(np.var(other)) + 1e-9 if len(other) > 5 else global_var
    return out


def main() -> None:
    df = pd.concat([load_seed(s) for s in SEEDS], ignore_index=True)
    scores, comp_rows, conflict_rows = [], [], []
    report = [f"# PhyK-TAS v3 reliability-aware fusion ({TAG})", ""]

    for model in MODELS:
        sub = df[df["model"] == model].reset_index(drop=True)
        if sub.empty:
            continue
        y = sub[TARGET].to_numpy()
        regions = sub["target_region"].to_numpy()
        splits = build_splits(sub, "group_by_cell")

        f_phys = source_oof(sub, PHYSICAL_COLS, splits, y)
        f_shift = source_oof(sub, SHIFT_COLS, splits, y)
        f_concat = source_oof(sub, PHYSICAL_COLS + SHIFT_COLS, splits, y)

        # --- B: per-region reliability of each single source -----------------
        n_phys_win = n_shift_win = 0
        for r in np.unique(regions):
            m = regions == r
            if m.sum() < MIN_REGION_ROWS:
                continue
            r2p = r2_score(y[m], f_phys[m])
            r2s = r2_score(y[m], f_shift[m])
            winner = "physical" if r2p > r2s else "shift"
            n_phys_win += winner == "physical"
            n_shift_win += winner == "shift"
            comp_rows.append({"model": model, "target_region": r, "n": int(m.sum()),
                              "r2_physical": r2p, "r2_shift": r2s, "winner": winner})

        # --- A: inverse-variance, region-conditional precision fusion --------
        s2_phys = leave_region_out_sigma2(y - f_phys, regions)
        s2_shift = leave_region_out_sigma2(y - f_shift, regions)
        wp = np.array([1.0 / s2_phys[r] for r in regions])
        ws = np.array([1.0 / s2_shift[r] for r in regions])
        wsum = wp + ws
        wp, ws = wp / wsum, ws / wsum
        f_fused = wp * f_phys + ws * f_shift

        r2_scores = {
            "physical_only": r2_score(y, f_phys),
            "shift_only": r2_score(y, f_shift),
            "concatenation_rf": r2_score(y, f_concat),
            "precision_fusion": r2_score(y, f_fused),
        }
        scores.append({"model": model, "mean_weight_physical": float(wp.mean()),
                       **r2_scores})
        report.append(f"## {model}")
        report.append(f"- source wins across regions: physical={n_phys_win}, shift={n_shift_win}")
        report.append(f"- R2: physical={r2_scores['physical_only']:.3f}, "
                      f"shift={r2_scores['shift_only']:.3f}, "
                      f"concat={r2_scores['concatenation_rf']:.3f}, "
                      f"precision-fusion={r2_scores['precision_fusion']:.3f} "
                      f"(mean physical weight {wp.mean():.2f})")

        # --- C: conflict (source disagreement) as an uncertainty signal ------
        conflict = np.abs(f_phys - f_shift)
        fused_err = np.abs(y - f_fused)
        pr = pearsonr(conflict, fused_err)[0]
        sr = spearmanr(conflict, fused_err)[0]
        # error by conflict tertile
        q1, q2 = np.quantile(conflict, [1 / 3, 2 / 3])
        lo = fused_err[conflict <= q1].mean()
        mid = fused_err[(conflict > q1) & (conflict <= q2)].mean()
        hi = fused_err[conflict > q2].mean()
        conflict_rows.append({"model": model, "pearson_conflict_err": pr,
                              "spearman_conflict_err": sr,
                              "err_low_conflict": lo, "err_mid_conflict": mid,
                              "err_high_conflict": hi})
        report.append(f"- conflict vs fusion error: Pearson={pr:.3f}, Spearman={sr:.3f}; "
                      f"mean |err| low/mid/high conflict = {lo:.3f}/{mid:.3f}/{hi:.3f}")
        report.append("")
        print(report[-3]); print(report[-2])

    pd.DataFrame(scores).to_csv(OUT_A, index=False)
    pd.DataFrame(comp_rows).to_csv(OUT_B, index=False)
    pd.DataFrame(conflict_rows).to_csv(OUT_C, index=False)
    REPORT.write_text("\n".join(report), encoding="utf-8")
    print(f"\nwrote {OUT_A}\nwrote {OUT_B}\nwrote {OUT_C}\nwrote {REPORT}")


if __name__ == "__main__":
    main()
