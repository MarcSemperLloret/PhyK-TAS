from __future__ import annotations

from pathlib import Path

import duckdb
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
DAILY = ROOT / "Data" / "harmonized" / "precip_daily"
ASSIGN = PAPER / "dedup_assignments_core_2005.csv"
OUT_STATION = PAPER / "light_degradation_station.csv"
OUT_PAIR = PAPER / "light_degradation_pair_summary.csv"
REPORT = PAPER / "light_degradation_matrix_report.md"

REGIONS = ["MED", "WCE", "NEU"]
REGION_THRESHOLDS = {"MED": 80, "WCE": 95, "NEU": 95}
TRAIN_START = "2005-01-01"
TRAIN_END = "2012-12-31"
TEST_START = "2020-01-01"
TEST_END = "2025-12-31"


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
    stations["station_uid"] = stations["canonical_station_uid"]
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
          AND CAST(p.obs_date AS DATE) BETWEEN DATE '{TRAIN_START}' AND DATE '{TEST_END}'
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
    daily["doy"] = daily["obs_date"].dt.dayofyear.clip(upper=365)
    return daily


def mae(y: np.ndarray, pred: np.ndarray) -> float:
    mask = np.isfinite(y) & np.isfinite(pred)
    return float(np.mean(np.abs(y[mask] - pred[mask]))) if mask.any() else np.nan


def brier_occurrence(y: np.ndarray, prob: np.ndarray, threshold: float = 1.0) -> float:
    obs = (y > threshold).astype(float)
    mask = np.isfinite(obs) & np.isfinite(prob)
    return float(np.mean((obs[mask] - prob[mask]) ** 2)) if mask.any() else np.nan


def build_climatologies(train: pd.DataFrame) -> dict[str, dict[str, np.ndarray]]:
    out = {}
    for region, g in train.groupby("ar6_region"):
        by_doy = g.groupby("doy")["precip_mm"]
        amount = by_doy.mean().reindex(range(1, 366)).interpolate(limit_direction="both").to_numpy()
        occurrence = (
            g.assign(wet=(g["precip_mm"] > 1.0).astype(float))
            .groupby("doy")["wet"]
            .mean()
            .reindex(range(1, 366))
            .interpolate(limit_direction="both")
            .to_numpy()
        )
        out[region] = {"amount": amount, "occurrence": occurrence}
    return out


def build_station_persistence(train: pd.DataFrame) -> pd.DataFrame:
    # Station-level monthly mean acts as a local lightweight baseline when daily persistence is unavailable.
    monthly = (
        train.assign(month=train["obs_date"].dt.month)
        .groupby(["canonical_station_uid", "month"])["precip_mm"]
        .mean()
        .reset_index(name="station_monthly_mean")
    )
    return monthly


def main() -> None:
    stations = operational_stations()
    daily = load_daily(stations)
    train = daily[(daily["obs_date"] >= TRAIN_START) & (daily["obs_date"] <= TRAIN_END)].copy()
    test = daily[(daily["obs_date"] >= TEST_START) & (daily["obs_date"] <= TEST_END)].copy()
    test["month"] = test["obs_date"].dt.month

    clim = build_climatologies(train)
    station_monthly = build_station_persistence(train)
    test = test.merge(station_monthly, on=["canonical_station_uid", "month"], how="left")
    global_train_mean = float(train["precip_mm"].mean())
    test["station_monthly_mean"] = test["station_monthly_mean"].fillna(global_train_mean)

    rows = []
    for uid, g in test.groupby("canonical_station_uid", sort=False):
        target = str(g["ar6_region"].iloc[0])
        y = g["precip_mm"].to_numpy(dtype=float)
        doys = g["doy"].to_numpy(dtype=int)
        local_pred = g["station_monthly_mean"].to_numpy(dtype=float)
        local_mae = mae(y, local_pred)

        for source in REGIONS:
            amount_pred = clim[source]["amount"][doys - 1]
            occ_prob = clim[source]["occurrence"][doys - 1]
            rows.append(
                {
                    "canonical_station_uid": uid,
                    "target_region": target,
                    "source_region": source,
                    "cell5": str(g["cell5"].iloc[0]),
                    "n_test_days": len(g),
                    "model": "region_daily_climatology",
                    "mae": mae(y, amount_pred),
                    "brier_occurrence": brier_occurrence(y, occ_prob),
                    "local_station_monthly_mae": local_mae,
                    "degradation_vs_local_monthly": mae(y, amount_pred) - local_mae,
                    "is_in_region": source == target,
                }
            )
    station = pd.DataFrame(rows)
    station.to_csv(OUT_STATION, index=False)

    pair = (
        station.groupby(["source_region", "target_region", "model"])
        .agg(
            n_stations=("canonical_station_uid", "nunique"),
            n_cells=("cell5", "nunique"),
            mae_mean=("mae", "mean"),
            mae_median=("mae", "median"),
            brier_mean=("brier_occurrence", "mean"),
            degradation_vs_local_mean=("degradation_vs_local_monthly", "mean"),
            degradation_vs_local_median=("degradation_vs_local_monthly", "median"),
        )
        .reset_index()
    )

    # Add out-minus-in degradation per target/source by comparing each target station to its in-region MAE.
    in_region = station[station["is_in_region"]][
        ["canonical_station_uid", "mae", "brier_occurrence"]
    ].rename(columns={"mae": "mae_in_region", "brier_occurrence": "brier_in_region"})
    station2 = station.merge(in_region, on="canonical_station_uid", how="left")
    station2["mae_out_minus_in"] = station2["mae"] - station2["mae_in_region"]
    station2["brier_out_minus_in"] = station2["brier_occurrence"] - station2["brier_in_region"]
    station2.to_csv(OUT_STATION, index=False)
    pair_shift = (
        station2.groupby(["source_region", "target_region", "model"])
        .agg(
            mae_out_minus_in_mean=("mae_out_minus_in", "mean"),
            mae_out_minus_in_median=("mae_out_minus_in", "median"),
            brier_out_minus_in_mean=("brier_out_minus_in", "mean"),
        )
        .reset_index()
    )
    pair = pair.merge(pair_shift, on=["source_region", "target_region", "model"], how="left")
    pair.to_csv(OUT_PAIR, index=False)

    lines = [
        "# Light degradation matrix report",
        "",
        "Model layer:",
        "",
        "- region daily climatology trained on 2005-2012;",
        "- local station monthly climatology as lightweight local baseline;",
        "- evaluated on 2020-2025.",
        "",
        "Outputs:",
        "",
        "- `light_degradation_station.csv`",
        "- `light_degradation_pair_summary.csv`",
        "",
        "## Pair summary",
        "",
        pair.to_markdown(index=False),
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT_STATION}")
    print(f"wrote {OUT_PAIR}")
    print(f"wrote {REPORT}")
    print(pair.to_string(index=False))


if __name__ == "__main__":
    main()
