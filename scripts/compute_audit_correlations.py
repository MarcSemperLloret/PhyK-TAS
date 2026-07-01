from pathlib import Path

import duckdb
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
DAILY = ROOT / "Data" / "harmonized" / "precip_daily"
AUDIT = PAPER / "dedup_audit_sample.csv"
OUT = PAPER / "dedup_audit_sample_with_correlations.csv"


def split_uid(uid: str) -> tuple[str, str]:
    source, station = uid.split("::", 1)
    return source, station


def corr_for_pair(con: duckdb.DuckDBPyConnection, uid_a: str, uid_b: str) -> tuple[float | None, int]:
    source_a, station_a = split_uid(uid_a)
    source_b, station_b = split_uid(uid_b)
    glob_a = str((DAILY / f"source_id={source_a}" / "**" / "*.parquet")).replace("\\", "/")
    glob_b = str((DAILY / f"source_id={source_b}" / "**" / "*.parquet")).replace("\\", "/")
    q = f"""
    WITH a AS (
      SELECT CAST(obs_date AS DATE) AS d, precip_mm AS pa
      FROM read_parquet('{glob_a}', hive_partitioning=true)
      WHERE source_station_id = '{station_a.replace("'", "''")}'
        AND year BETWEEN 2005 AND 2025
        AND precip_mm IS NOT NULL
    ),
    b AS (
      SELECT CAST(obs_date AS DATE) AS d, precip_mm AS pb
      FROM read_parquet('{glob_b}', hive_partitioning=true)
      WHERE source_station_id = '{station_b.replace("'", "''")}'
        AND year BETWEEN 2005 AND 2025
        AND precip_mm IS NOT NULL
    )
    SELECT corr(pa, pb) AS r, count(*) AS n_overlap
    FROM a INNER JOIN b USING(d)
    """
    r, n = con.execute(q).fetchone()
    return r, int(n or 0)


def main() -> None:
    audit = pd.read_csv(AUDIT)
    con = duckdb.connect()
    corrs = []
    overlaps = []
    for _, row in audit.iterrows():
        try:
            r, n = corr_for_pair(con, row["station_uid_a"], row["station_uid_b"])
        except Exception:
            r, n = None, 0
        corrs.append(r)
        overlaps.append(n)
    audit["daily_corr_2005_2025"] = corrs
    audit["daily_overlap_days"] = overlaps
    audit.to_csv(OUT, index=False)
    print(f"wrote {OUT}")
    print(audit[["station_uid_a", "station_uid_b", "criterion", "distance_km", "daily_corr_2005_2025", "daily_overlap_days"]].to_string(index=False))


if __name__ == "__main__":
    main()

