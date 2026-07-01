from __future__ import annotations

from pathlib import Path
import os

import duckdb
import numpy as np
import pandas as pd

from experiment_config import assignment_path, region_thresholds


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
DAILY = ROOT / "Data" / "harmonized" / "precip_daily"
ASSIGN = assignment_path()
EXPERIMENT_TAG = os.environ.get("FORECAST_EXPERIMENT_TAG", "large").strip()
SUFFIX = "" if EXPERIMENT_TAG == "large" else f"_{EXPERIMENT_TAG}"
OUT = PAPER / f"forecast_dataset_large{SUFFIX}.npz"
META = PAPER / f"forecast_dataset_large{SUFFIX}_metadata.csv"
REPORT = PAPER / f"forecast_dataset_large{SUFFIX}_report.md"

REGION_THRESHOLDS = region_thresholds()
REGIONS = list(REGION_THRESHOLDS)
N_PER_REGION_TARGET = int(os.environ.get("FORECAST_N_PER_REGION", "1000"))
RANDOM_SEED = int(os.environ.get("FORECAST_RANDOM_SEED", "20260524"))
START = "2005-01-01"
END = "2025-12-31"


def select_stations() -> pd.DataFrame:
    assign = pd.read_csv(ASSIGN)
    parts = []
    for region, threshold in REGION_THRESHOLDS.items():
        sub = assign[
            (assign["ar6_region"] == region)
            & (assign["coverage_threshold"] == threshold)
        ].drop_duplicates("canonical_station_uid")
        n = min(N_PER_REGION_TARGET, len(sub))
        parts.append(sub.sample(n=n, random_state=RANDOM_SEED))
    stations = pd.concat(parts, ignore_index=True)
    stations[["source_id", "source_station_id"]] = stations["canonical_station_uid"].str.split(
        "::", n=1, expand=True
    )
    return stations


def load_daily(stations: pd.DataFrame) -> pd.DataFrame:
    con = duckdb.connect()
    frames = []
    for source_id, group in stations.groupby("source_id"):
        ids = pd.DataFrame({"source_station_id": group["source_station_id"].astype(str).unique()})
        con.register("selected_ids", ids)
        glob = str((DAILY / f"source_id={source_id}" / "**" / "*.parquet")).replace("\\", "/")
        q = f"""
        SELECT
          p.source_id,
          p.source_station_id,
          CAST(p.obs_date AS DATE) AS obs_date,
          p.precip_mm
        FROM read_parquet('{glob}', hive_partitioning=true) p
        INNER JOIN selected_ids s USING(source_station_id)
        WHERE p.year BETWEEN 2005 AND 2025
          AND CAST(p.obs_date AS DATE) BETWEEN DATE '{START}' AND DATE '{END}'
        """
        frames.append(con.execute(q).df())
        con.unregister("selected_ids")
    daily = pd.concat(frames, ignore_index=True)
    daily["canonical_station_uid"] = daily["source_id"] + "::" + daily["source_station_id"].astype(str)
    return daily


def main() -> None:
    stations = select_stations()
    daily = load_daily(stations)
    dates = pd.date_range(START, END, freq="D")
    station_ids = stations["canonical_station_uid"].tolist()
    station_index = {sid: i for i, sid in enumerate(station_ids)}
    date_index = {d: i for i, d in enumerate(dates)}

    y = np.full((len(station_ids), len(dates)), np.nan, dtype=np.float32)
    for row in daily.itertuples(index=False):
        sid = row.canonical_station_uid
        d = pd.Timestamp(row.obs_date)
        if sid in station_index and d in date_index:
            y[station_index[sid], date_index[d]] = row.precip_mm
    mask = np.isfinite(y).astype(np.float32)
    y_filled = np.nan_to_num(y, nan=0.0)
    y_log1p = np.log1p(np.clip(y_filled, 0, None)).astype(np.float32)

    meta = stations[
        [
            "canonical_station_uid",
            "ar6_region",
            "coverage_threshold",
            "cell5",
            "latitude",
            "longitude",
            "source_id",
        ]
    ].copy()
    meta["station_idx"] = np.arange(len(meta))
    meta.to_csv(META, index=False)

    region_codes = {r: i for i, r in enumerate(REGIONS)}
    station_region = meta["ar6_region"].map(region_codes).to_numpy(dtype=np.int64)
    np.savez_compressed(
        OUT,
        y_raw=y.astype(np.float32),
        y_log1p=y_log1p,
        mask=mask,
        dates=np.array([d.strftime("%Y-%m-%d") for d in dates]),
        station_ids=np.array(station_ids),
        station_region=station_region,
        region_names=np.array(REGIONS),
    )

    summary = meta.groupby("ar6_region").agg(
        n_stations=("canonical_station_uid", "nunique"),
        n_cells=("cell5", "nunique"),
    )
    coverage = pd.DataFrame(
        {"ar6_region": meta["ar6_region"], "coverage": mask.mean(axis=1)}
    ).groupby("ar6_region")["coverage"].agg(["mean", "min", "median"])
    lines = [
        "# Forecast dataset large report",
        "",
        "Large dataset for expensive forecasting experiments.",
        "",
        f"- Stations per region target: {N_PER_REGION_TARGET}",
        f"- Random seed: {RANDOM_SEED}",
        f"- Date range: {START} to {END}",
        f"- Assignment file: `{ASSIGN.name}`",
        f"- Region thresholds: {', '.join(f'{r}:{t}' for r, t in REGION_THRESHOLDS.items())}",
        "",
        "## Station summary",
        "",
        summary.reset_index().to_markdown(index=False),
        "",
        "## Coverage summary",
        "",
        coverage.reset_index().to_markdown(index=False),
        "",
        "Outputs:",
        "",
        f"- `{OUT.name}`",
        f"- `{META.name}`",
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"wrote {META}")
    print(f"wrote {REPORT}")
    print(summary.to_string())
    print(coverage.to_string())


if __name__ == "__main__":
    main()
