from __future__ import annotations

from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
from scipy.stats import nct, t


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
DAILY = ROOT / "Data" / "harmonized" / "precip_daily"
ASSIGN = PAPER / "dedup_assignments_core_2005.csv"
OUT_STATIONS = PAPER / "pilot_light_stations.csv"
OUT_METRICS = PAPER / "pilot_light_degradation.csv"
OUT_POWER = PAPER / "pilot_light_power.md"

REGIONS = ["MED", "WCE", "NEU"]
REGION_THRESHOLDS = {"MED": 80, "WCE": 95, "NEU": 95}
N_PER_REGION = 300
RANDOM_SEED = 20260523


def detectable_r2(n: int, alpha: float = 0.05, power: float = 0.8) -> float:
    if n <= 4:
        return float("nan")
    df = n - 2
    tcrit = t.ppf(1 - alpha / 2, df)
    grid = np.linspace(0.001, 0.8, 5000)
    for r2 in grid:
        r = np.sqrt(r2)
        ncp = r * np.sqrt(df / (1 - r2))
        pwr = nct.sf(tcrit, df, ncp) + nct.cdf(-tcrit, df, ncp)
        if pwr >= power:
            return float(r2)
    return float("nan")


def select_stations() -> pd.DataFrame:
    assign = pd.read_csv(ASSIGN)
    parts = []
    for region in REGIONS:
        threshold = REGION_THRESHOLDS[region]
        sub = assign[
            (assign["ar6_region"] == region)
            & (assign["coverage_threshold"] == threshold)
        ].copy()
        sub = sub.drop_duplicates("canonical_station_uid")
        n = min(N_PER_REGION, len(sub))
        parts.append(sub.sample(n=n, random_state=RANDOM_SEED))
    stations = pd.concat(parts, ignore_index=True)
    stations[["source_id", "source_station_id"]] = stations["canonical_station_uid"].str.split(
        "::", n=1, expand=True
    )
    stations["station_uid"] = stations["canonical_station_uid"]
    stations.to_csv(OUT_STATIONS, index=False)
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
          AND p.precip_mm IS NOT NULL
        """
        frames.append(con.execute(q).df())
        con.unregister("selected_ids")
    daily = pd.concat(frames, ignore_index=True)
    daily["station_uid"] = daily["source_id"] + "::" + daily["source_station_id"].astype(str)
    daily = daily.merge(
        stations[["canonical_station_uid", "ar6_region", "cell5", "station_uid"]],
        on="station_uid",
        how="inner",
    )
    daily["obs_date"] = pd.to_datetime(daily["obs_date"])
    daily["doy"] = daily["obs_date"].dt.dayofyear.clip(upper=365)
    return daily


def mae(y: np.ndarray, pred: np.ndarray) -> float:
    mask = np.isfinite(y) & np.isfinite(pred)
    if mask.sum() == 0:
        return float("nan")
    return float(np.mean(np.abs(y[mask] - pred[mask])))


def main() -> None:
    stations = select_stations()
    daily = load_daily(stations)

    train = daily[(daily["obs_date"] >= "2005-01-01") & (daily["obs_date"] <= "2012-12-31")]
    test = daily[(daily["obs_date"] >= "2020-01-01") & (daily["obs_date"] <= "2025-12-31")]

    # Region-level daily climatology trained only on train period.
    clim = (
        train.groupby(["ar6_region", "doy"])["precip_mm"]
        .mean()
        .reset_index(name="pred")
    )
    clim_map = {
        region: grp.set_index("doy")["pred"].reindex(range(1, 366)).interpolate(limit_direction="both").to_numpy()
        for region, grp in clim.groupby("ar6_region")
    }

    rows = []
    for uid, g in test.groupby("canonical_station_uid"):
        target_region = str(g["ar6_region"].iloc[0])
        y = g["precip_mm"].to_numpy(dtype=float)
        doys = g["doy"].to_numpy(dtype=int)
        region_mae = {}
        for source_region in REGIONS:
            preds = clim_map[source_region][doys - 1]
            region_mae[source_region] = mae(y, preds)
        in_mae = region_mae[target_region]
        out_maes = [v for k, v in region_mae.items() if k != target_region]
        best_out = float(np.nanmin(out_maes))
        mean_out = float(np.nanmean(out_maes))
        rows.append(
            {
                "canonical_station_uid": uid,
                "ar6_region": target_region,
                "cell5": str(g["cell5"].iloc[0]),
                "n_test_days": len(g),
                "mae_in_region_climatology": in_mae,
                "mae_best_out_region_climatology": best_out,
                "mae_mean_out_region_climatology": mean_out,
                "degradation_best_out_minus_in": best_out - in_mae,
                "degradation_mean_out_minus_in": mean_out - in_mae,
                "degradation_ratio_mean_out_over_in": mean_out / in_mae if in_mae > 0 else np.nan,
            }
        )
    metrics = pd.DataFrame(rows)
    metrics.to_csv(OUT_METRICS, index=False)

    summary = (
        metrics.groupby("ar6_region")
        .agg(
            n_station=("canonical_station_uid", "nunique"),
            n_cell5=("cell5", "nunique"),
            mean_deg=("degradation_mean_out_minus_in", "mean"),
            sd_deg=("degradation_mean_out_minus_in", "std"),
            median_ratio=("degradation_ratio_mean_out_over_in", "median"),
        )
        .reset_index()
    )

    power_rows = []
    for _, r in summary.iterrows():
        power_rows.append(
            {
                "ar6_region": r["ar6_region"],
                "n_station": int(r["n_station"]),
                "n_cell5": int(r["n_cell5"]),
                "sd_degradation": float(r["sd_deg"]),
                "min_detectable_r2_station_iid": detectable_r2(int(r["n_station"])),
                "min_detectable_r2_cell_effective": detectable_r2(int(r["n_cell5"])),
            }
        )
    power = pd.DataFrame(power_rows)

    lines = [
        "# Pilot light power analysis",
        "",
        "This pilot uses post-dedup operational stations sampled from the preregistration candidate design.",
        "",
        f"Sample: up to {N_PER_REGION} stations per region.",
        "",
        "Model:",
        "",
        "- daily region-level climatology trained on 2005-2012;",
        "- evaluated on 2020-2025;",
        "- degradation per station is mean out-region climatology MAE minus in-region climatology MAE.",
        "",
        "This is not the final model comparison. It estimates variance of degradation for power planning.",
        "",
        "## Degradation summary",
        "",
        summary.to_markdown(index=False),
        "",
        "## Power bounds",
        "",
        power.to_markdown(index=False),
        "",
        "## Interpretation",
        "",
        "- The station-level sample supports detecting small associations if stations were independent.",
        "- The cell-level bound remains conservative and shows MED is the limiting region.",
        "- The preregistered analysis must therefore use hierarchical/bootstrap uncertainty and avoid claiming IID station-level power.",
        "",
    ]
    OUT_POWER.write_text("\n".join(lines), encoding="utf-8")

    print(f"wrote {OUT_STATIONS}")
    print(f"wrote {OUT_METRICS}")
    print(f"wrote {OUT_POWER}")
    print(summary.to_string(index=False))
    print(power.to_string(index=False))


if __name__ == "__main__":
    main()
