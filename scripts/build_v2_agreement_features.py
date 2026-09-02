from __future__ import annotations

"""Label-free agreement features from exported per-(station, day) predictions.

Reads the prediction stacks written by the forecaster scripts when
FORECAST_EXPORT_PREDICTIONS=1 and computes, per (forecast model, source
region, station), evidence about the transfer that uses NO target labels:

- agree_cross_source_l1: mean |pred_s - pred_s'| against the same family
  trained on the other source regions, on common valid (station, day) points
  (agreement/disagreement estimators, Baek et al. 2022 flavor);
- agree_cross_source_excl_target_l1: the same, additionally excluding the
  model trained on the station's own region (genuine cold-start variant: no
  target-trained model is available for comparison);
- agree_cross_family_l1: mean |pred^m_s - pred^m'_s| against the other
  forecasting families trained on the same source;
- pred_mean / pred_wet_rate / pred_p95: prediction-distribution statistics at
  the target station;
- pred_mean_shift / pred_wet_rate_shift / pred_p95_shift: absolute difference
  between the target-station statistic and the source-region in-region mean of
  the same statistic (an output-distribution shift signal, Deng & Zheng 2021 /
  Guillory et al. 2021 flavor).
"""

import os
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
EXPERIMENT_TAG = os.environ.get("FORECAST_EXPERIMENT_TAG", "").strip()
SUFFIX = f"_{EXPERIMENT_TAG}" if EXPERIMENT_TAG else ""
META = Path(os.environ.get("FORECAST_META", PAPER / "forecast_dataset_operational_sample_metadata.csv"))
OUT = PAPER / f"v2_agreement_features{SUFFIX}.csv"
REPORT = PAPER / f"v2_agreement_features{SUFFIX}_report.md"

WET_THRESHOLD = 1.0

FAMILIES = {
    "regional_doy_climatology": (f"forecast_baseline{SUFFIX}_predictions.npz", "pred"),
    "spatial_knn_ridge": (f"forecast_spatial_baseline{SUFFIX}_predictions.npz", "pred"),
    "linear_window": (f"forecast_patchtst{SUFFIX}_predictions.npz", "pred_linear_window"),
    "patchtst_small": (f"forecast_patchtst{SUFFIX}_predictions.npz", "pred_patchtst_small"),
    "stgcn_diffusion": (f"forecast_stgnn{SUFFIX}_predictions.npz", "pred"),
    "graphwavenet_transfer": (f"forecast_graphwavenet{SUFFIX}_predictions.npz", "pred"),
}


def load_family(name: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    fname, key = FAMILIES[name]
    data = np.load(PAPER / fname, allow_pickle=True)
    return data[key], data["time_idx"].astype(np.int64), np.asarray([str(r) for r in data["source_regions"]])


def cross_source_disagreement(
    pred: np.ndarray, station_region_pos: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Mean |pred_i - pred_j| against the other sources, per (source, station).

    Returns the full-ensemble variant and a cold-start variant that also
    excludes the source trained on the station's own region.
    """
    n_sources, n_stations, _ = pred.shape
    sum_pair = np.zeros((n_sources, n_sources, n_stations), dtype=np.float64)
    cnt_pair = np.zeros((n_sources, n_sources, n_stations), dtype=np.int64)
    for i in range(n_sources):
        p_i = pred[i].astype(np.float32)
        for j in range(i + 1, n_sources):
            d = np.abs(p_i - pred[j].astype(np.float32))
            valid = ~np.isnan(d)
            s_ij = np.where(valid, d, 0.0).sum(axis=1)
            c_ij = valid.sum(axis=1)
            sum_pair[i, j] = s_ij
            sum_pair[j, i] = s_ij
            cnt_pair[i, j] = c_ij
            cnt_pair[j, i] = c_ij
    total_sum = sum_pair.sum(axis=1)
    total_cnt = cnt_pair.sum(axis=1)
    station_ax = np.arange(n_stations)
    with np.errstate(invalid="ignore"):
        full = np.where(total_cnt > 0, total_sum / np.maximum(total_cnt, 1), np.nan)
        excl = np.full_like(full, np.nan)
        for i in range(n_sources):
            minus_sum = np.where(station_region_pos != i, sum_pair[i, station_region_pos, station_ax], 0.0)
            minus_cnt = np.where(station_region_pos != i, cnt_pair[i, station_region_pos, station_ax], 0)
            e_sum = total_sum[i] - minus_sum
            e_cnt = total_cnt[i] - minus_cnt
            excl[i] = np.where(e_cnt > 0, e_sum / np.maximum(e_cnt, 1), np.nan)
    return full, excl


def cross_family_disagreement(
    name: str,
    preds: dict[str, np.ndarray],
    tidx: dict[str, np.ndarray],
) -> np.ndarray:
    """Mean |pred^m - pred^m'| against the other families, per (source, station)."""
    pred_m = preds[name]
    n_sources, n_stations, _ = pred_m.shape
    sum_abs = np.zeros((n_sources, n_stations), dtype=np.float64)
    cnt = np.zeros((n_sources, n_stations), dtype=np.int64)
    for other, pred_o in preds.items():
        if other == name:
            continue
        _, cols_m, cols_o = np.intersect1d(tidx[name], tidx[other], return_indices=True)
        if len(cols_m) == 0:
            continue
        for r in range(n_sources):
            d = np.abs(pred_m[r][:, cols_m].astype(np.float32) - pred_o[r][:, cols_o].astype(np.float32))
            valid = ~np.isnan(d)
            sum_abs[r] += np.where(valid, d, 0.0).sum(axis=1)
            cnt[r] += valid.sum(axis=1)
    with np.errstate(invalid="ignore"):
        return np.where(cnt > 0, sum_abs / np.maximum(cnt, 1), np.nan)


def prediction_stats(pred: np.ndarray) -> dict[str, np.ndarray]:
    """Per-(source, station) prediction-distribution statistics."""
    n_sources = pred.shape[0]
    mean = np.full(pred.shape[:2], np.nan, dtype=np.float64)
    wet = np.full(pred.shape[:2], np.nan, dtype=np.float64)
    p95 = np.full(pred.shape[:2], np.nan, dtype=np.float64)
    n_valid = np.zeros(pred.shape[:2], dtype=np.int64)
    for r in range(n_sources):
        p = pred[r].astype(np.float32)
        valid = ~np.isnan(p)
        n = valid.sum(axis=1)
        n_valid[r] = n
        with np.errstate(invalid="ignore"):
            mean[r] = np.where(n > 0, np.where(valid, p, 0.0).sum(axis=1) / np.maximum(n, 1), np.nan)
            wet[r] = np.where(n > 0, ((p > WET_THRESHOLD) & valid).sum(axis=1) / np.maximum(n, 1), np.nan)
        has = n > 0
        if has.any():
            p95[r, has] = np.nanpercentile(p[has], 95, axis=1)
    return {"pred_mean": mean, "pred_wet_rate": wet, "pred_p95": p95, "n_days_valid": n_valid}


def main() -> None:
    meta = pd.read_csv(META).sort_values("station_idx").reset_index(drop=True)
    station_region = meta["ar6_region"].to_numpy()

    preds: dict[str, np.ndarray] = {}
    tidx: dict[str, np.ndarray] = {}
    source_regions: np.ndarray | None = None
    for name in FAMILIES:
        pred, t, regions = load_family(name)
        if source_regions is None:
            source_regions = regions
        elif not np.array_equal(source_regions, regions):
            raise ValueError(f"source-region order mismatch for {name}")
        preds[name] = pred
        tidx[name] = t

    region_pos = {region: i for i, region in enumerate(source_regions)}
    station_region_pos = np.asarray([region_pos.get(r, -1) for r in station_region])

    frames = []
    for name in FAMILIES:
        pred = preds[name]
        stats = prediction_stats(pred)
        agree_src, agree_src_excl = cross_source_disagreement(pred, station_region_pos)
        agree_fam = cross_family_disagreement(name, preds, tidx)

        n_sources, n_stations = agree_src.shape
        for r, source_region in enumerate(source_regions):
            in_region = station_region == source_region
            src_ref = {
                key: float(np.nanmean(stats[key][r, in_region])) if in_region.any() else np.nan
                for key in ("pred_mean", "pred_wet_rate", "pred_p95")
            }
            frame = pd.DataFrame(
                {
                    "model": name,
                    "source_region": source_region,
                    "target_region": station_region,
                    "station_idx": np.arange(n_stations),
                    "agree_cross_source_l1": agree_src[r],
                    "agree_cross_source_excl_target_l1": agree_src_excl[r],
                    "agree_cross_family_l1": agree_fam[r],
                    "pred_mean": stats["pred_mean"][r],
                    "pred_wet_rate": stats["pred_wet_rate"][r],
                    "pred_p95": stats["pred_p95"][r],
                    "pred_mean_shift": np.abs(stats["pred_mean"][r] - src_ref["pred_mean"]),
                    "pred_wet_rate_shift": np.abs(stats["pred_wet_rate"][r] - src_ref["pred_wet_rate"]),
                    "pred_p95_shift": np.abs(stats["pred_p95"][r] - src_ref["pred_p95"]),
                    "n_days_valid": stats["n_days_valid"][r],
                }
            )
            frames.append(frame[frame["n_days_valid"] > 0])
        print(name, "done")

    out = pd.concat(frames, ignore_index=True)
    out.to_csv(OUT, index=False)

    summary = (
        out.groupby("model")
        .agg(
            n_rows=("station_idx", "size"),
            mean_days=("n_days_valid", "mean"),
            mean_agree_src=("agree_cross_source_l1", "mean"),
            mean_agree_fam=("agree_cross_family_l1", "mean"),
        )
        .reset_index()
    )
    lines = [
        "# Label-free agreement features",
        "",
        f"Tag: `{EXPERIMENT_TAG}`; predictions from FORECAST_EXPORT_PREDICTIONS=1 runs.",
        "",
        "Features per (model, source region, station): cross-source and cross-family",
        "L1 disagreement, prediction-distribution statistics, and their shift against",
        "the source-region in-region reference. No target labels are used.",
        "",
        summary.to_markdown(index=False),
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"wrote {REPORT}")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
