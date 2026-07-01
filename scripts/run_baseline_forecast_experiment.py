from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
EXPERIMENT_TAG = os.environ.get("FORECAST_EXPERIMENT_TAG", "").strip()
SUFFIX = f"_{EXPERIMENT_TAG}" if EXPERIMENT_TAG else ""
DATA = Path(os.environ.get("FORECAST_DATA", PAPER / "forecast_dataset_operational_sample.npz"))
META = Path(os.environ.get("FORECAST_META", PAPER / "forecast_dataset_operational_sample_metadata.csv"))
OUT_STATION = PAPER / f"forecast_baseline{SUFFIX}_station_metrics.csv"
OUT_PAIR = PAPER / f"forecast_baseline{SUFFIX}_pair_summary.csv"
OUT_PERSISTENCE = PAPER / f"forecast_persistence{SUFFIX}_station_metrics.csv"
REPORT = PAPER / f"forecast_baseline{SUFFIX}_report.md"

LOOKBACK = 1


# Temporal split years (env-overridable so the later-window expansion run does
# not require editing this script; defaults reproduce the 11-region benchmark).
_TR0 = int(os.environ.get("FC_TRAIN_START_YEAR", "2005"))
_TR1 = int(os.environ.get("FC_TRAIN_END_YEAR", "2012"))
_TE0 = int(os.environ.get("FC_TEST_START_YEAR", "2020"))
_TE1 = int(os.environ.get("FC_TEST_END_YEAR", "2025"))


def date_mask(dates: np.ndarray, start: str, end: str) -> np.ndarray:
    d = pd.to_datetime(dates)
    return np.asarray((d >= start) & (d <= end))


def doy_index(dates: np.ndarray) -> np.ndarray:
    d = pd.to_datetime(dates)
    # Collapse leap day into Feb 28 bucket to keep a stable 365-day climatology.
    doy = d.dayofyear.to_numpy()
    leap_after_feb = d.is_leap_year & (d.month > 2)
    doy = doy - leap_after_feb.astype(int)
    doy[(d.month == 2) & (d.day == 29)] = 59
    return doy.astype(int) - 1


def evaluate_raw_predictions(
    rows: list[tuple[int, float, float]],
    meta: pd.DataFrame,
    source_region: str,
    model_name: str,
) -> pd.DataFrame:
    pred = pd.DataFrame(rows, columns=["station_idx", "y_raw", "pred_raw"])
    pred = pred.merge(meta[["station_idx", "ar6_region", "cell5"]], on="station_idx", how="left")
    pred["pred_raw"] = pred["pred_raw"].clip(lower=0)
    pred["abs_error"] = (pred["y_raw"] - pred["pred_raw"]).abs()
    pred["occ_y"] = (pred["y_raw"] > 1.0).astype(float)
    pred["occ_prob"] = (pred["pred_raw"] > 1.0).astype(float)
    pred["brier_occurrence"] = (pred["occ_y"] - pred["occ_prob"]) ** 2
    out = (
        pred.groupby(["station_idx", "ar6_region", "cell5"])
        .agg(mae=("abs_error", "mean"), brier_occurrence=("brier_occurrence", "mean"), n=("y_raw", "size"))
        .reset_index()
        .rename(columns={"ar6_region": "target_region"})
    )
    out["source_region"] = source_region
    out["model"] = model_name
    return out


def build_regional_climatology(
    y_raw: np.ndarray,
    mask: np.ndarray,
    dates: np.ndarray,
    train_times: np.ndarray,
    station_region: np.ndarray,
    source_idx: int,
) -> np.ndarray:
    doy = doy_index(dates)
    clim = np.full(365, np.nan, dtype=np.float32)
    source_stations = np.where(station_region == source_idx)[0]
    for d in range(365):
        t = train_times[doy[train_times] == d]
        if len(t) == 0:
            continue
        block_y = y_raw[np.ix_(source_stations, t)]
        block_m = mask[np.ix_(source_stations, t)] > 0
        vals = block_y[block_m]
        if vals.size:
            clim[d] = float(np.mean(vals))
    fallback = float(np.nanmean(y_raw[np.ix_(source_stations, train_times)][mask[np.ix_(source_stations, train_times)] > 0]))
    clim = np.where(np.isfinite(clim), clim, fallback).astype(np.float32)
    return clim


def regional_climatology_metrics(
    y_raw: np.ndarray,
    mask: np.ndarray,
    dates: np.ndarray,
    test_times: np.ndarray,
    station_region: np.ndarray,
    region_names: np.ndarray,
    meta: pd.DataFrame,
) -> pd.DataFrame:
    train_times = np.where(date_mask(dates, f"{_TR0}-01-01", f"{_TR1}-12-31"))[0]
    doy = doy_index(dates)
    rows = []
    for source_idx, source_region in enumerate(region_names):
        clim = build_regional_climatology(y_raw, mask, dates, train_times, station_region, int(source_idx))
        pred_rows = []
        for s in range(y_raw.shape[0]):
            valid_t = test_times[mask[s, test_times] > 0]
            for t in valid_t:
                pred_rows.append((s, float(y_raw[s, t]), float(clim[doy[t]])))
        rows.append(evaluate_raw_predictions(pred_rows, meta, str(source_region), "regional_doy_climatology"))
    return pd.concat(rows, ignore_index=True)


def persistence_metrics(
    y_raw: np.ndarray,
    mask: np.ndarray,
    test_times: np.ndarray,
    meta: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    for s in range(y_raw.shape[0]):
        for t in test_times:
            prev = t - LOOKBACK
            if prev < 0:
                continue
            if mask[s, t] <= 0 or mask[s, prev] <= 0:
                continue
            rows.append((s, float(y_raw[s, t]), float(y_raw[s, prev])))
    return evaluate_raw_predictions(rows, meta, "none", "station_persistence")


def add_degradation(station: pd.DataFrame) -> pd.DataFrame:
    in_region = station[station["source_region"] == station["target_region"]][
        ["station_idx", "model", "mae", "brier_occurrence"]
    ].rename(columns={"mae": "mae_in_region", "brier_occurrence": "brier_in_region"})
    station = station.merge(in_region, on=["station_idx", "model"], how="left")
    station["mae_out_minus_in"] = station["mae"] - station["mae_in_region"]
    station["brier_out_minus_in"] = station["brier_occurrence"] - station["brier_in_region"]
    return station


def pair_summary(station: pd.DataFrame) -> pd.DataFrame:
    return (
        station.groupby(["source_region", "target_region", "model"])
        .agg(
            n_stations=("station_idx", "nunique"),
            n_cells=("cell5", "nunique"),
            mae_mean=("mae", "mean"),
            brier_mean=("brier_occurrence", "mean"),
            mae_out_minus_in_mean=("mae_out_minus_in", "mean"),
            brier_out_minus_in_mean=("brier_out_minus_in", "mean"),
        )
        .reset_index()
    )


def main() -> None:
    data = np.load(DATA, allow_pickle=True)
    y_raw = data["y_raw"].astype(np.float32)
    mask = data["mask"].astype(np.float32)
    dates = data["dates"]
    station_region = data["station_region"]
    region_names = data["region_names"]
    meta = pd.read_csv(META)

    test_times = np.where(date_mask(dates, f"{_TE0}-01-01", f"{_TE1}-12-31"))[0]

    station = regional_climatology_metrics(y_raw, mask, dates, test_times, station_region, region_names, meta)
    station = add_degradation(station)
    pair = pair_summary(station)

    persistence = persistence_metrics(y_raw, mask, test_times, meta)

    station.to_csv(OUT_STATION, index=False)
    pair.to_csv(OUT_PAIR, index=False)
    persistence.to_csv(OUT_PERSISTENCE, index=False)

    persistence_summary = (
        persistence.groupby(["target_region", "model"])
        .agg(
            n_stations=("station_idx", "nunique"),
            n_cells=("cell5", "nunique"),
            mae_mean=("mae", "mean"),
            brier_mean=("brier_occurrence", "mean"),
        )
        .reset_index()
    )

    lines = [
        "# Baseline forecasting experiment",
        "",
        "Dataset:",
        "",
        f"- `{DATA.name}`;",
        "- test period 2020-2025.",
        "",
        "Models:",
        "",
        "- `regional_doy_climatology`: source-region daily climatology learned on 2005-2012 and transferred to each target region;",
        "- `station_persistence`: previous observed day at the same station, reported as a non-transfer meteorological baseline.",
        "",
        "## Regional climatology pair summary",
        "",
        pair.to_markdown(index=False),
        "",
        "## Station persistence summary",
        "",
        persistence_summary.to_markdown(index=False),
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT_STATION}")
    print(f"wrote {OUT_PAIR}")
    print(f"wrote {OUT_PERSISTENCE}")
    print(f"wrote {REPORT}")
    print(pair.to_string(index=False))
    print(persistence_summary.to_string(index=False))


if __name__ == "__main__":
    main()
