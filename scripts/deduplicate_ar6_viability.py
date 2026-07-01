from __future__ import annotations

import math
import os
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

from experiment_config import daily_sources, regions, tag_suffix, tagged_paper_path


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
STATIONS_AR6 = PAPER / "stations_ar6.csv"
FLAGS_DIR = PAPER / "coverage_flags_by_source"
OUT_LOG = tagged_paper_path("dedup_log", ".csv")
OUT_VIABILITY = tagged_paper_path("viability_post_dedup", ".csv")
OUT_COMPARE = tagged_paper_path("viability_dedup_comparison", ".md")

DEFAULT_CORE = ["global_ghcnd_01", "eur_ecad_01"]
DEFAULT_VALIDATION = ["deu_dwd_cdc_01", "che_meteoswiss_01", "esp_aemet_daily_hist_01"]
CORE = daily_sources(DEFAULT_CORE)
VALIDATION = [] if CORE != DEFAULT_CORE else DEFAULT_VALIDATION
SOURCES = CORE + VALIDATION
REGIONS = regions()
PERIOD_STARTS = [
    int(x.strip())
    for x in os.environ.get("PHYKTAS_PERIOD_STARTS", "2000,2005").split(",")
    if x.strip()
]
THRESHOLDS = [(80, "all4_ge80"), (95, "all4_ge95")]


class DSU:
    def __init__(self, n: int) -> None:
        self.p = list(range(n))
        self.r = [0] * n

    def find(self, x: int) -> int:
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.r[ra] < self.r[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        if self.r[ra] == self.r[rb]:
            self.r[ra] += 1
        return True


def norm_name(x: object) -> str:
    if pd.isna(x):
        return ""
    return re.sub(r"[^A-Z0-9]+", "", str(x).upper())


def canonical_uid(group: pd.DataFrame) -> str:
    priority = {sid: i for i, sid in enumerate(CORE + VALIDATION)}
    g = group.copy()
    g["_priority"] = g["source_id"].map(priority).fillna(999)
    g = g.sort_values(["_priority", "source_id", "source_station_id"])
    return str(g.iloc[0]["station_uid"])


def load_flags(period_start: int) -> pd.DataFrame:
    path = FLAGS_DIR / f"all_sources_{period_start}{tag_suffix()}.csv"
    if not path.exists():
        path = FLAGS_DIR / f"all_sources_{period_start}.csv"
    if not path.exists():
        raise FileNotFoundError(path)
    flags = pd.read_csv(path, dtype={"source_station_id": str})
    return flags[flags["source_id"].isin(SOURCES)].copy()


def prepare_base(period_start: int) -> pd.DataFrame:
    ar6 = pd.read_csv(STATIONS_AR6, dtype={"source_station_id": str}, low_memory=False)
    flags = load_flags(period_start)
    df = ar6.merge(flags, on=["source_id", "source_station_id"], how="inner")
    df = df[df["source_id"].isin(SOURCES) & df["ar6_region"].isin(REGIONS)].copy()
    for col in ["latitude", "longitude", "elevation_m"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["norm_name"] = df["station_name"].map(norm_name)
    df["wmo_norm"] = df["wmo_id"].fillna("").astype(str).str.replace(r"\.0$", "", regex=True)
    df.loc[df["wmo_norm"].isin(["", "nan", "None", "<NA>"]), "wmo_norm"] = ""
    df["candidate_duplicate_key"] = df["candidate_duplicate_key"].fillna("")
    df["station_uid"] = df["source_id"] + "::" + df["source_station_id"].astype(str)
    return df


def add_edge(
    edges: list[dict],
    dsu: DSU,
    df: pd.DataFrame,
    i: int,
    j: int,
    criterion: str,
    distance_km: float | None = None,
) -> None:
    if df.at[i, "source_id"] == df.at[j, "source_id"]:
        return
    merged = dsu.union(i, j)
    edges.append(
        {
            "station_uid_a": df.at[i, "station_uid"],
            "station_uid_b": df.at[j, "station_uid"],
            "ar6_region": df.at[i, "ar6_region"],
            "distance_km": distance_km,
            "correlation": "",
            "criterion": criterion,
            "merged": merged,
        }
    )


def dedup(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = df.reset_index(drop=True).copy()
    dsu = DSU(len(df))
    edges: list[dict] = []

    for col, criterion in [
        ("wmo_norm", "same_wmo_id"),
        ("candidate_duplicate_key", "same_candidate_duplicate_key"),
    ]:
        vals = df[col].fillna("")
        for _, idx in vals[vals != ""].groupby(vals).groups.items():
            idx = list(idx)
            for j in idx[1:]:
                add_edge(edges, dsu, df, idx[0], j, criterion)

    if len(df):
        lat = np.radians(df["latitude"].astype(float).to_numpy())
        lon = np.radians(df["longitude"].astype(float).to_numpy())
        xyz = np.column_stack(
            [np.cos(lat) * np.cos(lon), np.cos(lat) * np.sin(lon), np.sin(lat)]
        )
        tree = cKDTree(xyz)
        radius = 2 * math.sin((1.0 / 6371.0088) / 2)
        for i, j in tree.query_pairs(radius):
            if df.at[i, "source_id"] == df.at[j, "source_id"]:
                continue
            same_wmo = df.at[i, "wmo_norm"] and df.at[i, "wmo_norm"] == df.at[j, "wmo_norm"]
            same_name = df.at[i, "norm_name"] and df.at[i, "norm_name"] == df.at[j, "norm_name"]
            ei, ej = df.at[i, "elevation_m"], df.at[j, "elevation_m"]
            elev_close = pd.notna(ei) and pd.notna(ej) and abs(float(ei) - float(ej)) <= 10
            if same_wmo or same_name or elev_close:
                dist = float(np.linalg.norm(xyz[i] - xyz[j]) * 6371.0088)
                reasons = []
                if same_wmo:
                    reasons.append("wmo")
                if same_name:
                    reasons.append("name")
                if elev_close:
                    reasons.append("elev10m")
                add_edge(edges, dsu, df, i, j, "spatial_1km_plus_" + "_".join(reasons), dist)

    roots = [dsu.find(i) for i in range(len(df))]
    df["dedup_root"] = roots
    canon = (
        df.groupby("dedup_root", group_keys=False)
        .apply(lambda g: canonical_uid(g), include_groups=True)
        .to_dict()
    )
    df["canonical_station_uid"] = df["dedup_root"].map(canon)
    return df, pd.DataFrame(edges)


def main() -> None:
    log_frames = []
    viability_rows = []
    comparison_rows = []

    for period_start in PERIOD_STARTS:
        base = prepare_base(period_start)
        for threshold, flag_col in THRESHOLDS:
            filt = base[base[flag_col]].copy()
            for region in REGIONS:
                region_df = filt[filt["ar6_region"] == region].copy()
                pre_core = region_df[region_df["source_id"].isin(CORE)]["station_uid"].nunique()
                pre_all = region_df["station_uid"].nunique()

                for scope, scope_sources in [
                    ("core_ghcnd_ecad", CORE),
                    ("core_plus_validation", SOURCES),
                ]:
                    scoped = region_df[region_df["source_id"].isin(scope_sources)].copy()
                    if scoped.empty:
                        post = 0
                        edge_log = pd.DataFrame()
                        deduped = scoped
                    else:
                        deduped, edge_log = dedup(scoped)
                        post = deduped["canonical_station_uid"].nunique()
                        if not edge_log.empty:
                            edge_log["period_start"] = period_start
                            edge_log["coverage_threshold"] = threshold
                            edge_log["scope"] = scope
                            log_frames.append(edge_log)

                    viability_rows.append(
                        {
                            "ar6_region": region,
                            "scope": scope,
                            "coverage_threshold": threshold,
                            "period_start": period_start,
                            "n_unique_post_dedup": int(post),
                            "n_source_rows_pre_dedup": int(scoped["station_uid"].nunique()),
                        }
                    )

                comparison_rows.append(
                    {
                        "period_start": period_start,
                        "coverage_threshold": threshold,
                        "ar6_region": region,
                        "pre_core": int(pre_core),
                        "pre_all_sources": int(pre_all),
                    }
                )

    log = pd.concat(log_frames, ignore_index=True) if log_frames else pd.DataFrame()
    log.to_csv(OUT_LOG, index=False)
    viability = pd.DataFrame(viability_rows)
    viability.to_csv(OUT_VIABILITY, index=False)

    comp = pd.DataFrame(comparison_rows).merge(
        viability,
        on=["period_start", "coverage_threshold", "ar6_region"],
        how="left",
    )
    lines = [
        "# Post-dedup viability comparison",
        "",
        "Deduplication is metadata-first and spatial <=1 km with compatible metadata.",
        "Series-correlation confirmation is deferred to audit candidates because full daily pair correlation is expensive.",
        "",
        comp.sort_values(["period_start", "coverage_threshold", "ar6_region", "scope"]).to_markdown(index=False),
        "",
    ]
    OUT_COMPARE.write_text("\n".join(lines), encoding="utf-8")

    print(f"wrote {OUT_LOG}")
    print(f"wrote {OUT_VIABILITY}")
    print(f"wrote {OUT_COMPARE}")
    print(viability.to_string(index=False))


if __name__ == "__main__":
    main()
