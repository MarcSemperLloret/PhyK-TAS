from __future__ import annotations

from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

from experiment_config import assignment_path, physical_descriptor_paths, region_thresholds


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
DAILY = ROOT / "Data" / "harmonized" / "precip_daily"
ASSIGN = assignment_path()
OUT_STATION, OUT_CELL, OUT_REGION, REPORT = physical_descriptor_paths()

TRAIN_START = "2005-01-01"
TRAIN_END = "2012-12-31"
REGION_THRESHOLDS = region_thresholds()


def operational_stations() -> pd.DataFrame:
    assign = pd.read_csv(ASSIGN)
    parts = []
    for region, threshold in REGION_THRESHOLDS.items():
        sub = assign[
            (assign["ar6_region"] == region)
            & (assign["coverage_threshold"] == threshold)
        ].copy()
        parts.append(sub)
    stations = pd.concat(parts, ignore_index=True).drop_duplicates("canonical_station_uid")
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
        WHERE p.year BETWEEN 2005 AND 2012
          AND CAST(p.obs_date AS DATE) BETWEEN DATE '{TRAIN_START}' AND DATE '{TRAIN_END}'
          AND p.precip_mm IS NOT NULL
        """
        frames.append(con.execute(q).df())
        con.unregister("selected_ids")
    daily = pd.concat(frames, ignore_index=True)
    daily["canonical_station_uid"] = daily["source_id"] + "::" + daily["source_station_id"].astype(str)
    daily = daily.merge(
        stations[
            [
                "canonical_station_uid",
                "ar6_region",
                "cell5",
                "latitude",
                "longitude",
            ]
        ],
        on="canonical_station_uid",
        how="inner",
    )
    daily["obs_date"] = pd.to_datetime(daily["obs_date"])
    daily["month"] = daily["obs_date"].dt.month
    return daily


def lag1_autocorr(values: np.ndarray) -> float:
    values = values.astype(float)
    if len(values) < 3:
        return float("nan")
    x = values[:-1]
    y = values[1:]
    if np.nanstd(x) == 0 or np.nanstd(y) == 0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def dry_spell_stats(dates: pd.Series, precip: np.ndarray) -> tuple[float, float]:
    df = pd.DataFrame({"date": pd.to_datetime(dates), "precip": precip}).sort_values("date")
    full = pd.DataFrame({"date": pd.date_range(TRAIN_START, TRAIN_END, freq="D")})
    df = full.merge(df, on="date", how="left")
    dry = (df["precip"].fillna(np.nan) <= 1.0).to_numpy()
    observed = df["precip"].notna().to_numpy()
    runs = []
    current = 0
    for is_dry, is_obs in zip(dry, observed):
        if not is_obs:
            if current:
                runs.append(current)
                current = 0
            continue
        if is_dry:
            current += 1
        else:
            if current:
                runs.append(current)
                current = 0
    if current:
        runs.append(current)
    if not runs:
        return float("nan"), float("nan")
    return float(np.mean(runs)), float(np.percentile(runs, 95))


def station_descriptors(daily: pd.DataFrame, stations: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for uid, g in daily.groupby("canonical_station_uid", sort=False):
        p = g["precip_mm"].to_numpy(dtype=float)
        wet = p > 1.0
        wet_vals = p[wet]
        monthly = g.groupby("month")["precip_mm"].sum().reindex(range(1, 13), fill_value=0.0)
        total = float(monthly.sum())
        top3_frac = float(monthly.sort_values(ascending=False).head(3).sum() / total) if total > 0 else np.nan
        dry_mean, dry_p95 = dry_spell_stats(g["obs_date"], p)
        occurrence = wet.astype(float)
        intensity = np.where(wet, p, np.nan)
        intensity_valid = intensity[np.isfinite(intensity)]
        row = {
            "canonical_station_uid": uid,
            "ar6_region": g["ar6_region"].iloc[0],
            "cell5": g["cell5"].iloc[0],
            "latitude": float(g["latitude"].iloc[0]),
            "longitude": float(g["longitude"].iloc[0]),
            "n_obs_train": int(len(g)),
            "wet_day_fraction_gt1mm": float(np.mean(wet)),
            "wet_day_mean_intensity": float(np.mean(wet_vals)) if len(wet_vals) else np.nan,
            "daily_precip_cv": float(np.std(p) / np.mean(p)) if np.mean(p) > 0 else np.nan,
            "monthly_climatology_amplitude": float(monthly.max() - monthly.min()),
            "top3_month_precip_fraction": top3_frac,
            "occurrence_lag1_autocorr": lag1_autocorr(occurrence),
            "wet_intensity_lag1_autocorr": lag1_autocorr(intensity_valid) if len(intensity_valid) > 3 else np.nan,
            "dry_spell_mean_days": dry_mean,
            "dry_spell_p95_days": dry_p95,
            "wet_day_p95": float(np.percentile(wet_vals, 95)) if len(wet_vals) else np.nan,
            "wet_day_p99": float(np.percentile(wet_vals, 99)) if len(wet_vals) else np.nan,
            "extreme_tail_ratio_p99_p95": float(np.percentile(wet_vals, 99) / np.percentile(wet_vals, 95))
            if len(wet_vals) and np.percentile(wet_vals, 95) > 0
            else np.nan,
        }
        rows.append(row)
    desc = pd.DataFrame(rows)
    # Preserve source metadata through the canonical id.
    return desc.merge(
        stations[["canonical_station_uid", "source_id", "source_station_id", "coverage_threshold"]],
        on="canonical_station_uid",
        how="left",
    )


def aggregate_descriptors(desc: pd.DataFrame, by: list[str]) -> pd.DataFrame:
    numeric_cols = [
        c
        for c in desc.columns
        if c
        not in {
            "canonical_station_uid",
            "source_id",
            "source_station_id",
            "ar6_region",
            "cell5",
        }
        and pd.api.types.is_numeric_dtype(desc[c])
    ]
    agg = desc.groupby(by)[numeric_cols].agg(["mean", "std", "median"]).reset_index()
    agg.columns = ["_".join([x for x in col if x]) for col in agg.columns.to_flat_index()]
    counts = desc.groupby(by)["canonical_station_uid"].nunique().reset_index(name="n_stations")
    return counts.merge(agg, on=by, how="left")


def main() -> None:
    stations = operational_stations()
    daily = load_daily(stations)
    desc = station_descriptors(daily, stations)
    cell = aggregate_descriptors(desc, ["ar6_region", "cell5"])
    region = aggregate_descriptors(desc, ["ar6_region"])

    desc.to_csv(OUT_STATION, index=False)
    cell.to_csv(OUT_CELL, index=False)
    region.to_csv(OUT_REGION, index=False)

    summary = desc.groupby("ar6_region").agg(
        n_stations=("canonical_station_uid", "nunique"),
        wet_day_fraction=("wet_day_fraction_gt1mm", "mean"),
        wet_intensity=("wet_day_mean_intensity", "mean"),
        dry_spell_p95=("dry_spell_p95_days", "median"),
        wet_p99=("wet_day_p99", "median"),
        top3_fraction=("top3_month_precip_fraction", "mean"),
    )
    lines = [
        "# Physical descriptors report",
        "",
        "Operational design:",
        "",
        f"- Assignment file: `{ASSIGN.name}`.",
        f"- Region thresholds: {', '.join(f'{r}:{t}' for r, t in REGION_THRESHOLDS.items())}.",
        "- Training period for descriptor calculation: 2005-2012.",
        "",
        "Outputs:",
        "",
        "- `physical_descriptors_station.csv`",
        "- `physical_descriptors_cell5.csv`",
        "- `physical_descriptors_region.csv`",
        "",
        "## Regional descriptor summary",
        "",
        summary.reset_index().to_markdown(index=False),
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT_STATION}")
    print(f"wrote {OUT_CELL}")
    print(f"wrote {OUT_REGION}")
    print(f"wrote {REPORT}")
    print(summary.to_string())


if __name__ == "__main__":
    main()
