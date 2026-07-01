from __future__ import annotations

from itertools import product
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from scipy.stats import wasserstein_distance

from experiment_config import assignment_path, region_thresholds, shift_baseline_paths


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
DAILY = ROOT / "Data" / "harmonized" / "precip_daily"
ASSIGN = assignment_path()
OUT, REPORT = shift_baseline_paths()

REGION_THRESHOLDS = region_thresholds()
REGIONS = list(REGION_THRESHOLDS)
TRAIN_START = "2005-01-01"
TRAIN_END = "2012-12-31"
MAX_VALUES_PER_REGION = 300000
RANDOM_SEED = 20260523


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
        stations[["canonical_station_uid", "ar6_region", "cell5", "latitude", "longitude"]],
        on="canonical_station_uid",
        how="inner",
    )
    daily["obs_date"] = pd.to_datetime(daily["obs_date"])
    daily["month"] = daily["obs_date"].dt.month
    return daily


def hist_prob(values: np.ndarray, bins: np.ndarray) -> np.ndarray:
    h, _ = np.histogram(values, bins=bins)
    p = h.astype(float) + 1e-9
    return p / p.sum()


def kl(p: np.ndarray, q: np.ndarray) -> float:
    return float(np.sum(p * np.log(p / q)))


def mmd_rbf(x: np.ndarray, y: np.ndarray, gamma: float | None = None, max_n: int = 3000) -> float:
    rng = np.random.default_rng(RANDOM_SEED)
    if len(x) > max_n:
        x = rng.choice(x, max_n, replace=False)
    if len(y) > max_n:
        y = rng.choice(y, max_n, replace=False)
    x = x.reshape(-1, 1)
    y = y.reshape(-1, 1)
    if gamma is None:
        z = np.vstack([x, y])
        d = cdist(z[: min(len(z), 1000)], z[: min(len(z), 1000)], "sqeuclidean")
        med = np.median(d[d > 0]) if np.any(d > 0) else 1.0
        gamma = 1.0 / med
    kxx = np.exp(-gamma * cdist(x, x, "sqeuclidean")).mean()
    kyy = np.exp(-gamma * cdist(y, y, "sqeuclidean")).mean()
    kxy = np.exp(-gamma * cdist(x, y, "sqeuclidean")).mean()
    return float(kxx + kyy - 2 * kxy)


def region_features(daily: pd.DataFrame) -> dict[str, dict]:
    rng = np.random.default_rng(RANDOM_SEED)
    out = {}
    for region, g in daily.groupby("ar6_region"):
        vals = g["precip_mm"].to_numpy(dtype=float)
        if len(vals) > MAX_VALUES_PER_REGION:
            vals = rng.choice(vals, MAX_VALUES_PER_REGION, replace=False)
        wet = vals > 1.0
        monthly = g.groupby("month")["precip_mm"].mean().reindex(range(1, 13), fill_value=0.0).to_numpy()
        out[region] = {
            "values": vals,
            "wet_fraction": float(np.mean(wet)),
            "mean": float(np.mean(vals)),
            "variance": float(np.var(vals)),
            "p95": float(np.percentile(vals, 95)),
            "p99": float(np.percentile(vals, 99)),
            "monthly_mean": monthly,
            "lat_mean": float(g["latitude"].mean()),
            "lon_mean": float(g["longitude"].mean()),
        }
    return out


def main() -> None:
    stations = operational_stations()
    daily = load_daily(stations)
    feats = region_features(daily)
    all_values = np.concatenate([f["values"] for f in feats.values()])
    bins = np.unique(np.quantile(all_values, np.linspace(0, 1, 51)))
    if len(bins) < 5:
        bins = np.linspace(float(all_values.min()), float(all_values.max()), 50)

    rows = []
    for src, dst in product(REGIONS, REGIONS):
        fs, fd = feats[src], feats[dst]
        ps = hist_prob(fs["values"], bins)
        pdst = hist_prob(fd["values"], bins)
        geo_dist = float(np.sqrt((fs["lat_mean"] - fd["lat_mean"]) ** 2 + (fs["lon_mean"] - fd["lon_mean"]) ** 2))
        rows.append(
            {
                "source_region": src,
                "target_region": dst,
                "kl_source_to_target": kl(ps, pdst),
                "kl_target_to_source": kl(pdst, ps),
                "wasserstein_precip": float(wasserstein_distance(fs["values"], fd["values"])),
                "mmd_rbf_precip": mmd_rbf(fs["values"], fd["values"]),
                "shift_mean_abs": abs(fs["mean"] - fd["mean"]),
                "shift_variance_abs": abs(fs["variance"] - fd["variance"]),
                "shift_wet_fraction_abs": abs(fs["wet_fraction"] - fd["wet_fraction"]),
                "shift_p95_abs": abs(fs["p95"] - fd["p95"]),
                "shift_p99_abs": abs(fs["p99"] - fd["p99"]),
                "shift_monthly_l2": float(np.linalg.norm(fs["monthly_mean"] - fd["monthly_mean"])),
                "region_centroid_distance_deg": geo_dist,
            }
        )
    out = pd.DataFrame(rows)
    out.to_csv(OUT, index=False)

    lines = [
        "# Distribution shift baselines report",
        "",
        "Operational design:",
        "",
        f"- Assignment file: `{ASSIGN.name}`.",
        f"- Region thresholds: {', '.join(f'{r}:{t}' for r, t in REGION_THRESHOLDS.items())}.",
        "- Training period for shift calculation: 2005-2012.",
        "",
        "Output:",
        "",
        "- `distribution_shift_baselines.csv`",
        "",
        "## Pairwise shift table",
        "",
        out.to_markdown(index=False),
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"wrote {REPORT}")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
