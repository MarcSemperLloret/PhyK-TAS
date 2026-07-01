import os
from datetime import date
from pathlib import Path

import duckdb
import pandas as pd

from experiment_config import daily_sources, regions, tag_suffix, tagged_paper_path


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
DAILY = ROOT / "Data" / "harmonized" / "precip_daily"
STATIONS_AR6 = PAPER / "stations_ar6.csv"
OUT = tagged_paper_path("viability_pre_dedup", ".csv")
SUMMARY = tagged_paper_path("viability_pre_dedup_summary", ".md")

DEFAULT_SOURCES = [
    "global_ghcnd_01",
    "eur_ecad_01",
    "deu_dwd_cdc_01",
    "che_meteoswiss_01",
    "esp_aemet_daily_hist_01",
    "esp_avamet_01",
    "can_eccc_climate_stations_01",
]
SOURCES = daily_sources(DEFAULT_SOURCES)

PERIOD_SCHEMES = {
    2000: [
        ("train", date(2000, 1, 1), date(2012, 12, 31)),
        ("val", date(2013, 1, 1), date(2015, 12, 31)),
        ("mid", date(2016, 1, 1), date(2019, 12, 31)),
        ("test", date(2020, 1, 1), date(2025, 12, 31)),
    ],
    2005: [
        ("train", date(2005, 1, 1), date(2012, 12, 31)),
        ("val", date(2013, 1, 1), date(2015, 12, 31)),
        ("mid", date(2016, 1, 1), date(2019, 12, 31)),
        ("test", date(2020, 1, 1), date(2025, 12, 31)),
    ],
    # Later common window (Option B): unlocks recently-densified networks
    # (e.g. INMET/Brazil, weather2k/China) that lack pre-2010 coverage.
    2015: [
        ("train", date(2015, 1, 1), date(2018, 12, 31)),
        ("val", date(2019, 1, 1), date(2019, 12, 31)),
        ("test", date(2020, 1, 1), date(2025, 12, 31)),
    ],
}

REGIONS = regions()


def station_flags_for_source(con: duckdb.DuckDBPyConnection, source_id: str, period_start: int) -> pd.DataFrame:
    periods = PERIOD_SCHEMES[period_start]
    glob = str((DAILY / f"source_id={source_id}" / "**" / "*.parquet")).replace("\\", "/")
    ctes = []
    for name, start, end in periods:
        days = (end - start).days + 1
        ge80 = int(days * 0.8 + 0.999999)
        ge95 = int(days * 0.95 + 0.999999)
        ctes.append(
            f"""
            {name}_p AS (
              SELECT source_station_id,
                     count(DISTINCT CAST(obs_date AS DATE)) >= {ge80} AS {name}_ge80,
                     count(DISTINCT CAST(obs_date AS DATE)) >= {ge95} AS {name}_ge95
              FROM read_parquet('{glob}', hive_partitioning=true)
              WHERE year BETWEEN {start.year} AND {end.year}
                AND CAST(obs_date AS DATE) BETWEEN DATE '{start.isoformat()}' AND DATE '{end.isoformat()}'
                AND precip_mm IS NOT NULL
              GROUP BY source_station_id
            )
            """
        )
    names = [name for name, _, _ in periods]
    union = " UNION ".join(f"SELECT source_station_id FROM {n}_p" for n in names)
    joins = "\n".join(f"LEFT JOIN {n}_p USING(source_station_id)" for n in names)
    # Column names ({name}_ge80/95) are unique per period, so they can be
    # referenced unqualified after the joins. Output columns keep the historical
    # `all4_*` names for downstream compatibility regardless of period count.
    and80 = " AND ".join(f"coalesce({n}_ge80,false)" for n in names)
    and95 = " AND ".join(f"coalesce({n}_ge95,false)" for n in names)
    q = f"""
    WITH {",".join(ctes)},
    all_ids AS ({union})
    SELECT
      '{source_id}' AS source_id,
      a.source_station_id,
      {and80} AS all4_ge80,
      {and95} AS all4_ge95
    FROM all_ids a
    {joins}
    """
    return con.execute(q).df()


def main() -> None:
    ar6 = pd.read_csv(STATIONS_AR6, dtype={"source_station_id": str})
    ar6 = ar6[ar6["ar6_region"].notna()].copy()
    rows = []
    flags_dir = PAPER / "coverage_flags_by_source"
    flags_dir.mkdir(exist_ok=True)
    con = duckdb.connect()

    wanted = os.environ.get("PHYKTAS_PERIOD_STARTS", "").strip()
    schemes = [int(x) for x in wanted.split(",") if x.strip()] if wanted else list(PERIOD_SCHEMES)
    for period_start in schemes:
        frames = []
        for source_id in SOURCES:
            source_dir = DAILY / f"source_id={source_id}"
            if not source_dir.exists():
                continue
            flags = station_flags_for_source(con, source_id, period_start)
            flags["period_start"] = period_start
            frames.append(flags)
            flags.to_csv(flags_dir / f"{source_id}_{period_start}.csv", index=False)
        all_flags = pd.concat(frames, ignore_index=True)
        all_flags.to_csv(flags_dir / f"all_sources_{period_start}{tag_suffix()}.csv", index=False)
        merged = ar6.merge(all_flags, on=["source_id", "source_station_id"], how="inner")
        for threshold, col in [(80, "all4_ge80"), (95, "all4_ge95")]:
            filt = merged[merged[col]]
            grouped = (
                filt.groupby(["ar6_region", "source_id"], dropna=False)
                .size()
                .reset_index(name="n_stations")
            )
            for _, r in grouped.iterrows():
                rows.append(
                    {
                        "ar6_region": r["ar6_region"],
                        "source_id": r["source_id"],
                        "coverage_threshold": threshold,
                        "period_start": period_start,
                        "n_stations": int(r["n_stations"]),
                    }
                )

    out = pd.DataFrame(rows).sort_values(
        ["period_start", "coverage_threshold", "ar6_region", "source_id"]
    )
    out.to_csv(OUT, index=False)

    core = out[out["source_id"].isin(SOURCES)]
    agg = (
        core.groupby(["period_start", "coverage_threshold", "ar6_region"])["n_stations"]
        .sum()
        .reset_index()
    )
    candidates = agg[agg["ar6_region"].isin(REGIONS)].copy()

    lines = [
        "# Pre-dedup viability summary",
        "",
        "Counts are AR6-assigned and temporally stable, but not deduplicated.",
        "",
        "## Configured sources",
        "",
        ", ".join(SOURCES),
        "",
        candidates.to_markdown(index=False),
        "",
        "## Regions below 500 pre-dedup",
        "",
        candidates[candidates["n_stations"] < 500].to_markdown(index=False),
        "",
    ]
    SUMMARY.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"wrote {SUMMARY}")
    print(candidates.to_string(index=False))


if __name__ == "__main__":
    main()
