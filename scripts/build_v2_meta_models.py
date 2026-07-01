"""PhyK-TAS v2 -- Eje 3: hierarchical / partial-pooling meta-models.

Compares the current random forest degradation inferrer against estimators that
can extrapolate outside the training range (Bayesian ridge, gradient boosting)
and against a partial-pooling linear mixed model with a source-region random
intercept. The key question is whether any of these rescues the weak
leave-target-region-out (unseen-region) extrapolation where the RF collapses.

Reuses the already-computed forecast station metrics + physical descriptors +
shift baselines (no forecaster retraining). Feature set: physical_plus_shift
(the winning set from the significance analysis). R^2 is reported with a
hierarchical bootstrap CI over (seed, cell5) clusters.
"""
from __future__ import annotations

import os
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import BayesianRidge
from sklearn.metrics import r2_score
from sklearn.model_selection import GroupKFold, LeaveOneGroupOut
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"

TAG = os.environ.get("PHYKTAS_V2_TAG", "all_viable_min100_full")
SEEDS = os.environ.get("PHYKTAS_V2_SEEDS", "s1,s2,s3").split(",")
REGION_SET = os.environ.get("PHYKTAS_V2_REGION_SET", "all_viable_min100")
N_BOOT = int(os.environ.get("PHYKTAS_V2_NBOOT", "1000"))
RUN_MIXEDLM = os.environ.get("PHYKTAS_V2_MIXEDLM", "1") not in {"0", "false", "no"}
RNG = np.random.default_rng(int(os.environ.get("PHYKTAS_V2_SEED", "20260701")))

MODELS = {
    "regional_doy_climatology": "forecast_baseline",
    "spatial_knn_ridge": "forecast_spatial_baseline",
    "linear_window": "forecast_baseline",
    "patchtst_small": "forecast_patchtst",
    "stgcn_diffusion": "forecast_stgnn",
    "graphwavenet_transfer": "forecast_graphwavenet",
}
METRIC_PREFIXES = sorted(set(MODELS.values()))

PHYSICAL_COLS = [
    "wet_day_fraction_gt1mm", "wet_day_mean_intensity", "daily_precip_cv",
    "monthly_climatology_amplitude", "top3_month_precip_fraction",
    "occurrence_lag1_autocorr", "wet_intensity_lag1_autocorr",
    "dry_spell_mean_days", "dry_spell_p95_days", "wet_day_p95", "wet_day_p99",
    "extreme_tail_ratio_p99_p95",
]
SHIFT_COLS = [
    "kl_source_to_target", "kl_target_to_source", "wasserstein_precip",
    "mmd_rbf_precip", "shift_mean_abs", "shift_variance_abs",
    "shift_wet_fraction_abs", "shift_p95_abs", "shift_p99_abs",
    "shift_monthly_l2", "region_centroid_distance_deg",
]
FEATURES = PHYSICAL_COLS + SHIFT_COLS
TARGET = "mae_out_minus_in"

OUT = PAPER / f"v2_meta_models_{TAG}.csv"
REPORT = PAPER / f"v2_meta_models_{TAG}_report.md"


def load_seed(seed: str) -> pd.DataFrame:
    frames = []
    for prefix in METRIC_PREFIXES:
        path = PAPER / f"{prefix}_{TAG}_{seed}_station_metrics.csv"
        if path.exists():
            frames.append(pd.read_csv(path))
    forecast = pd.concat(frames, ignore_index=True)
    forecast = forecast[forecast["source_region"] != forecast["target_region"]].copy()
    meta = pd.read_csv(PAPER / f"forecast_dataset_large_{TAG}_{seed}_metadata.csv")
    meta = meta[["station_idx", "canonical_station_uid"]]
    forecast = forecast.merge(meta, on="station_idx", how="left")
    desc = pd.read_csv(PAPER / f"physical_descriptors_station_{REGION_SET}.csv")
    shift = pd.read_csv(PAPER / f"distribution_shift_baselines_{REGION_SET}.csv")
    df = forecast.merge(
        desc,
        left_on=["canonical_station_uid", "target_region", "cell5"],
        right_on=["canonical_station_uid", "ar6_region", "cell5"],
        how="left",
    ).merge(shift, on=["source_region", "target_region"], how="left")
    df = df[df[TARGET].notna()].copy()
    df["seed"] = seed
    return df


def clean_features(df: pd.DataFrame) -> pd.DataFrame:
    x = df[FEATURES].replace([np.inf, -np.inf], np.nan)
    return x.fillna(x.median(numeric_only=True))


def make_estimator(name: str):
    if name == "random_forest":
        return RandomForestRegressor(n_estimators=400, min_samples_leaf=10,
                                     random_state=20260524, n_jobs=-1)
    if name == "bayes_ridge":
        return make_pipeline(StandardScaler(), BayesianRidge())
    if name == "hist_gbm":
        return HistGradientBoostingRegressor(max_iter=400, learning_rate=0.05,
                                             random_state=20260524)
    raise ValueError(name)


def oof_predict_sklearn(name, X, y, splits):
    pred = np.full(len(y), np.nan)
    for tr, te in splits:
        est = make_estimator(name)
        est.fit(X[tr], y[tr])
        pred[te] = est.predict(X[te])
    return pred


def oof_predict_mixedlm(df, X, y, splits):
    """Partial pooling: y ~ physical+shift (fixed) + (1 | source_region).
    On unseen target regions the source random intercept still applies.

    Robust to the boundary case where the random-effect variance collapses to
    zero (statsmodels then refuses to predict random effects): we keep the
    fixed-effects (complete-pooling) prediction instead of discarding the fold.
    """
    import statsmodels.formula.api as smf

    Xz = StandardScaler().fit_transform(X)
    feat_names = [f"f{i}" for i in range(Xz.shape[1])]
    base = pd.DataFrame(Xz, columns=feat_names)
    base["y"] = y
    base["source_region"] = df["source_region"].to_numpy()
    formula = "y ~ " + " + ".join(feat_names)
    pred = np.full(len(y), np.nan)
    for tr, te in splits:
        tr_df = base.iloc[tr].reset_index(drop=True)
        te_df = base.iloc[te].reset_index(drop=True)
        try:
            md = smf.mixedlm(formula, tr_df, groups=tr_df["source_region"])
            res = md.fit(method="lbfgs", maxiter=200, disp=False)
            fixed = res.predict(te_df).to_numpy()
        except Exception as exc:  # only a hard fit failure falls back to mean
            print(f"  mixedlm fit failed: {exc}")
            pred[te] = float(np.mean(y[tr]))
            continue
        add = np.zeros(len(te_df))
        try:  # add source random intercept when it is estimable
            re = res.random_effects
            add = np.array([
                float(re[s].iloc[0]) if s in re else 0.0
                for s in te_df["source_region"]
            ])
        except Exception:
            pass  # singular covariance -> keep fixed-effects prediction
        pred[te] = fixed + add
    return pred


def stacked_oof(pred_dict, y, groups, cv_kind, cell5, target_region):
    """Honest non-negative stacking: learn fusion weights over base-estimator
    out-of-fold predictions with an inner group CV (weights fit on train folds
    only), so the fusion is not evaluated on rows used to weight it."""
    from scipy.optimize import nnls

    names = list(pred_dict)
    P = np.column_stack([pred_dict[n] for n in names])
    if cv_kind == "group_by_cell":
        inner = GroupKFold(n_splits=min(5, len(np.unique(cell5))))
        g = cell5
    else:
        inner = LeaveOneGroupOut()
        g = target_region
    out = np.full(len(y), np.nan)
    weights = np.zeros(len(names))
    for tr, te in inner.split(P, y, g):
        w, _ = nnls(P[tr], y[tr])
        out[te] = P[te] @ w
        weights += w
    return out, dict(zip(names, weights / max(1, inner.get_n_splits(groups=g))))


def cluster_bootstrap_r2(y, pred, cluster_ids, n_boot):
    uniq = np.unique(cluster_ids)
    order = np.argsort(cluster_ids, kind="stable")
    sorted_ids = cluster_ids[order]
    starts = np.searchsorted(sorted_ids, uniq, side="left")
    ends = np.searchsorted(sorted_ids, uniq, side="right")
    rows = [order[a:b] for a, b in zip(starts, ends)]
    n = len(uniq)
    vals = np.empty(n_boot)
    for b in range(n_boot):
        pick = RNG.integers(0, n, size=n)
        idx = np.concatenate([rows[i] for i in pick])
        vals[b] = r2_score(y[idx], pred[idx])
    return np.percentile(vals, [2.5, 97.5])


def build_splits(df, cv_kind):
    if cv_kind == "group_by_cell":
        groups = df["cell5"].to_numpy()
        cv = GroupKFold(n_splits=min(5, df["cell5"].nunique()))
    elif cv_kind == "leave_target_region_out":
        groups = df["target_region"].to_numpy()
        cv = LeaveOneGroupOut()
    else:
        raise ValueError(cv_kind)
    X_dummy = np.zeros((len(df), 1))
    return list(cv.split(X_dummy, df[TARGET].to_numpy(), groups))


def main() -> None:
    df = pd.concat([load_seed(s) for s in SEEDS], ignore_index=True)
    estimators = ["random_forest", "bayes_ridge", "hist_gbm"]
    records = []
    for cv_kind in ["group_by_cell", "leave_target_region_out"]:
        for model, sub in df.groupby("model"):
            sub = sub.reset_index(drop=True)
            X = clean_features(sub).to_numpy()
            y = sub[TARGET].to_numpy()
            cluster = (sub["seed"].astype(str) + "|" + sub["cell5"].astype(str)).to_numpy()
            splits = build_splits(sub, cv_kind)
            preds = {}
            for name in estimators:
                preds[name] = oof_predict_sklearn(name, X, y, splits)
            if RUN_MIXEDLM:
                preds["mixedlm_pool"] = oof_predict_mixedlm(sub, X, y, splits)
            # Fusion of inference models (the Information-Fusion angle): combine
            # a nonlinear in-range learner with extrapolation-capable ones.
            base_preds = dict(preds)  # snapshot before adding fusion columns
            preds["fusion_mean"] = np.mean([base_preds[n] for n in base_preds], axis=0)
            stack, wts = stacked_oof(
                base_preds, y, None, cv_kind,
                sub["cell5"].to_numpy(), sub["target_region"].to_numpy(),
            )
            preds["fusion_stack"] = stack
            print(f"  [{cv_kind}/{model}] stack weights: "
                  + ", ".join(f"{k}={v:.2f}" for k, v in wts.items()))
            for name, pred in preds.items():
                r2 = r2_score(y, pred)
                lo, hi = cluster_bootstrap_r2(y, pred, cluster, N_BOOT)
                records.append({
                    "cv_kind": cv_kind, "forecast_model": model,
                    "estimator": name, "n": len(sub),
                    "r2": r2, "r2_lo": lo, "r2_hi": hi,
                })
                print(f"{cv_kind:24s} {model:24s} {name:14s} "
                      f"R2={r2:.3f} [{lo:.3f},{hi:.3f}]")
    res = pd.DataFrame(records)
    res.to_csv(OUT, index=False)

    lines = [f"# PhyK-TAS v2 meta-model comparison ({TAG})", "",
             f"Feature set: physical_plus_shift. Hierarchical bootstrap over "
             f"(seed, cell5), N={N_BOOT}. Pooled across seeds {SEEDS}.", ""]
    for cv_kind in ["group_by_cell", "leave_target_region_out"]:
        lines += [f"## {cv_kind}", ""]
        piv = res[res.cv_kind == cv_kind].pivot_table(
            index="forecast_model", columns="estimator", values="r2")
        lines += [piv.round(3).to_markdown(), ""]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nwrote {OUT}\nwrote {REPORT}")


if __name__ == "__main__":
    main()
