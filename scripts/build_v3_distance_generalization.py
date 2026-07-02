"""PhyK-TAS v3 -- cross-regime generalization vs. distance to the training library.

Addresses the concern that group-by-cell only measures risk *within* a calibrated
regime library. Under leave-target-region-out (LTRO), each AR6 region is held out
entirely (a genuinely unseen regime) and we ask:

  1. Does degradation-prediction error grow with the held-out region's distance to
     the training regimes (physical-descriptor distance and geographic distance)?
     If so, the system generalizes to nearby regimes and degrades predictably far
     from the calibrated library.

  2. Does the split-conformal guarantee, calibrated on other regions, still cover a
     genuinely unseen region -- and does any under-coverage track distance? This is
     regime-conditional (Mondrian-style) conformal coverage under extrapolation.

Inferrer: gradient boosting on physical+shift. Operates on existing artifacts.
"""
from __future__ import annotations

import os
import warnings

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import LeaveOneGroupOut

warnings.filterwarnings("ignore")

from build_v2_meta_models import (
    PAPER, TAG, SEEDS, PHYSICAL_COLS, SHIFT_COLS, TARGET, load_seed,
)

FIG = PAPER / "figures"
FIG_DIRS = [
    PAPER / "figures",
    PAPER / "manuscript_latex" / "figures",
    PAPER / "manuscript_latex_eswa" / "figures",
    PAPER / "manuscript_latex_infofusion" / "figures",
]
for figdir in FIG_DIRS:
    figdir.mkdir(parents=True, exist_ok=True)
ALPHA = float(os.environ.get("PHYKTAS_ALPHA", "0.10"))
MODELS = ["spatial_knn_ridge", "stgcn_diffusion", "graphwavenet_transfer",
          "regional_doy_climatology"]
FEATURES = PHYSICAL_COLS + SHIFT_COLS

MODEL_LABELS = {
    "spatial_knn_ridge": "Spatial kNN-ridge",
    "stgcn_diffusion": "STGCN diffusion",
    "graphwavenet_transfer": "Graph WaveNet",
    "regional_doy_climatology": "Regional climatology",
}
MODEL_COLORS = {
    "spatial_knn_ridge": "#3B6EA8",
    "stgcn_diffusion": "#2CA25F",
    "graphwavenet_transfer": "#7B5EA7",
    "regional_doy_climatology": "#C95714",
}

OUT = PAPER / f"v3_distance_generalization_{TAG}.csv"
REPORT = PAPER / f"v3_distance_generalization_{TAG}_report.md"


def clean(df, cols):
    x = df[cols].replace([np.inf, -np.inf], np.nan)
    return x.fillna(x.median(numeric_only=True)).to_numpy()


def region_phys_distance(df):
    """Min standardized Euclidean distance of each region's mean physical
    descriptor vector to the other regions (distance in regime space)."""
    rp = df.groupby("target_region")[PHYSICAL_COLS].mean()
    z = (rp - rp.mean()) / (rp.std(ddof=0) + 1e-9)
    regions = z.index.to_numpy()
    M = z.to_numpy()
    out = {}
    for i, r in enumerate(regions):
        d = np.sqrt(((M - M[i]) ** 2).sum(axis=1))
        d[i] = np.inf
        out[r] = float(d.min())
    return out


def region_geo_distance(df):
    """Nearest-training-region geographic distance: min source->target centroid
    distance among out-of-region pairs for each target region."""
    if "region_centroid_distance_deg" not in df.columns:
        return {r: np.nan for r in df["target_region"].unique()}
    g = df.groupby("target_region")["region_centroid_distance_deg"].min()
    return g.to_dict()


def main() -> None:
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 10,
        "axes.labelsize": 11,
        "axes.titlesize": 11,
        "xtick.labelsize": 9.2,
        "ytick.labelsize": 9.2,
        "legend.fontsize": 9,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.facecolor": "#FBFBFB",
        "figure.facecolor": "white",
        "savefig.dpi": 400,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.04,
    })
    df = pd.concat([load_seed(s) for s in SEEDS], ignore_index=True)
    phys_dist = region_phys_distance(df)
    geo_dist = region_geo_distance(df)

    rows = []
    for model in MODELS:
        sub = df[df["model"] == model].reset_index(drop=True)
        if sub.empty:
            continue
        X = clean(sub, FEATURES)
        y = sub[TARGET].to_numpy()
        groups = sub["target_region"].to_numpy()
        cv = LeaveOneGroupOut()

        pred = np.full(len(y), np.nan)
        for tr, te in cv.split(X, y, groups):
            est = HistGradientBoostingRegressor(max_iter=400, learning_rate=0.05,
                                                random_state=20260524)
            est.fit(X[tr], y[tr])
            pred[te] = est.predict(X[te])
        resid = y - pred

        # regime-conditional conformal: calibrate on other regions, cover held-out
        for r in np.unique(groups):
            m = groups == r
            mae = mean_absolute_error(y[m], pred[m])
            r2 = r2_score(y[m], pred[m]) if m.sum() > 2 else np.nan
            sp = spearmanr(pred[m], y[m])[0] if m.sum() > 5 else np.nan
            cal = resid[~m]
            n = len(cal)
            k = min(max(int(np.ceil((n + 1) * (1 - ALPHA))), 1), n)
            q = np.sort(cal)[k - 1]
            coverage = float(np.mean(y[m] <= pred[m] + q))
            rows.append({
                "model": model, "held_out_region": r, "n": int(m.sum()),
                "phys_distance": phys_dist.get(r, np.nan),
                "geo_distance": geo_dist.get(r, np.nan),
                "ltro_mae": mae, "ltro_r2": r2, "ltro_spearman": sp,
                "conformal_coverage": coverage,
            })

    res = pd.DataFrame(rows)
    res.to_csv(OUT, index=False)

    # correlations of error / coverage with distance (pooled and per model)
    lines = [f"# Cross-regime generalization vs. distance ({TAG})", "",
             f"LTRO with HistGBM(physical+shift). Conformal alpha={ALPHA} "
             f"(target coverage {1-ALPHA:.2f}), calibrated on other regions.", ""]

    def corr(a, b):
        ok = np.isfinite(a) & np.isfinite(b)
        if ok.sum() < 4:
            return np.nan, np.nan
        return spearmanr(a[ok], b[ok])

    for scope, d in [("pooled", res)] + [(m, res[res.model == m]) for m in MODELS]:
        pd_ = d["phys_distance"].to_numpy()
        mae_ = d["ltro_mae"].to_numpy()
        cov_ = d["conformal_coverage"].to_numpy()
        rho_e, p_e = corr(pd_, mae_)
        rho_c, p_c = corr(pd_, cov_)
        lines.append(f"- **{scope}**: Spearman(phys-distance, LTRO MAE) = {rho_e:.3f} "
                     f"(p={p_e:.3f}); Spearman(phys-distance, coverage) = {rho_c:.3f} "
                     f"(p={p_c:.3f}); mean coverage = {np.nanmean(cov_):.3f}")
    lines += ["", res.round(3).to_markdown(index=False), ""]
    REPORT.write_text("\n".join(lines), encoding="utf-8")

    # figure: LTRO error vs regime distance
    fig, ax = plt.subplots(1, 2, figsize=(7.45, 3.45), sharex=True)
    for model in MODELS:
        d = res[res.model == model]
        ax[0].scatter(
            d["phys_distance"], d["ltro_mae"], label=MODEL_LABELS[model],
            s=50, color=MODEL_COLORS[model], alpha=0.86, edgecolor="white", linewidth=0.55,
        )
        ax[1].scatter(
            d["phys_distance"], d["conformal_coverage"], label=MODEL_LABELS[model],
            s=50, color=MODEL_COLORS[model], alpha=0.86, edgecolor="white", linewidth=0.55,
        )
    ax[0].set_xlabel("Distance to nearest training regime")
    ax[0].set_ylabel("LTRO prediction MAE")
    ax[0].set_title("Prediction error")
    ax[1].axhline(1 - ALPHA, ls="--", c="#333333", lw=1.0, label=f"Target {1-ALPHA:.2f}")
    ax[1].set_xlabel("Distance to nearest training regime")
    ax[1].set_ylabel("Held-out coverage")
    ax[1].set_title("Conformal coverage")
    ax[1].set_ylim(0, 1.04)
    for label, axis in zip(["A", "B"], ax):
        axis.text(-0.12, 1.05, label, transform=axis.transAxes, fontsize=11, fontweight="bold", va="bottom")
        axis.grid(color="#E8E8E8", linewidth=0.55)
        axis.set_axisbelow(True)
        axis.spines["left"].set_color("#666666")
        axis.spines["bottom"].set_color("#666666")
    handles, labels = ax[1].get_legend_handles_labels()
    fig.legend(handles, labels, frameon=False, ncols=3, loc="upper center", bbox_to_anchor=(0.5, 1.08))
    fig.tight_layout(rect=(0, 0, 1, 0.95), w_pad=1.2)
    for figdir in FIG_DIRS:
        fig.savefig(figdir / "fig_v3_distance_generalization.png")
        fig.savefig(figdir / "fig_v3_distance_generalization.pdf")

    print(res.round(3).to_string(index=False))
    print("\n".join(lines[:12]))
    print(f"wrote {OUT}\nwrote {REPORT}")


if __name__ == "__main__":
    main()
