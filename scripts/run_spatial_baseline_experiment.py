from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import RidgeCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
EXPERIMENT_TAG = os.environ.get("FORECAST_EXPERIMENT_TAG", "").strip()
SUFFIX = f"_{EXPERIMENT_TAG}" if EXPERIMENT_TAG else ""
DATA = Path(os.environ.get("FORECAST_DATA", PAPER / "forecast_dataset_operational_sample.npz"))
META = Path(os.environ.get("FORECAST_META", PAPER / "forecast_dataset_operational_sample_metadata.csv"))
OUT_STATION = PAPER / f"forecast_spatial_baseline{SUFFIX}_station_metrics.csv"
OUT_PAIR = PAPER / f"forecast_spatial_baseline{SUFFIX}_pair_summary.csv"
REPORT = PAPER / f"forecast_spatial_baseline{SUFFIX}_report.md"

K_NEIGHBORS = int(os.environ.get("SPATIAL_BASELINE_K_NEIGHBORS", "5"))
MAX_TRAIN_SAMPLES = int(os.environ.get("SPATIAL_BASELINE_MAX_TRAIN_SAMPLES", "120000"))
SEED = int(os.environ.get("FORECAST_MODEL_SEED", os.environ.get("FORECAST_RANDOM_SEED", "20260524")))


# Temporal split years (env-overridable so the later-window expansion run does
# not require editing this script; defaults reproduce the 11-region benchmark).
_TR0 = int(os.environ.get("FC_TRAIN_START_YEAR", "2005"))
_TR1 = int(os.environ.get("FC_TRAIN_END_YEAR", "2012"))
_TE0 = int(os.environ.get("FC_TEST_START_YEAR", "2020"))
_TE1 = int(os.environ.get("FC_TEST_END_YEAR", "2025"))


def date_mask(dates: np.ndarray, start: str, end: str) -> np.ndarray:
    d = pd.to_datetime(dates)
    return np.asarray((d >= start) & (d <= end))


def build_knn(meta: pd.DataFrame, station_region: np.ndarray) -> list[np.ndarray]:
    lat = meta.sort_values("station_idx")["latitude"].to_numpy(dtype=float)
    lon = meta.sort_values("station_idx")["longitude"].to_numpy(dtype=float)
    coords = np.column_stack([lat, lon])
    neighbors: list[np.ndarray] = []
    for i in range(len(meta)):
        same = np.where(station_region == station_region[i])[0]
        same = same[same != i]
        if len(same) == 0:
            neighbors.append(np.array([i], dtype=int))
            continue
        # Euclidean degrees are sufficient for local kNN ordering at this diagnostic scale.
        dist = np.sum((coords[same] - coords[i]) ** 2, axis=1)
        nn = same[np.argsort(dist)[: min(K_NEIGHBORS, len(same))]]
        neighbors.append(nn.astype(int))
    return neighbors


def neighbor_lag_features(
    y_log: np.ndarray,
    mask: np.ndarray,
    neighbors: list[np.ndarray],
    time_indices: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    lag_t = time_indices - 1
    own = y_log[:, lag_t].copy()
    own_mask = mask[:, lag_t] > 0
    own = np.where(own_mask, own, 0.0)
    neigh_mean = np.zeros_like(own, dtype=np.float32)
    neigh_wet = np.zeros_like(own, dtype=np.float32)
    for s, nn in enumerate(neighbors):
        vals = y_log[np.ix_(nn, lag_t)]
        m = mask[np.ix_(nn, lag_t)] > 0
        counts = np.maximum(m.sum(axis=0), 1)
        neigh_mean[s] = np.where(m.any(axis=0), (vals * m).sum(axis=0) / counts, own[s])
        wet = (np.expm1(vals).clip(min=0) > 1.0) & m
        neigh_wet[s] = np.where(m.any(axis=0), wet.sum(axis=0) / counts, 0.0)
    return own.astype(np.float32), neigh_mean.astype(np.float32), neigh_wet.astype(np.float32)


def sample_training_matrix(
    y_log: np.ndarray,
    mask: np.ndarray,
    station_indices: np.ndarray,
    train_times: np.ndarray,
    own: np.ndarray,
    neigh_mean: np.ndarray,
    neigh_wet: np.ndarray,
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    valid_pairs = []
    for s in station_indices:
        valid_t_pos = np.where(mask[s, train_times] > 0)[0]
        for pos in valid_t_pos:
            valid_pairs.append((s, pos))
    rng = np.random.default_rng(seed)
    if len(valid_pairs) > MAX_TRAIN_SAMPLES:
        idx = rng.choice(len(valid_pairs), MAX_TRAIN_SAMPLES, replace=False)
        valid_pairs = [valid_pairs[i] for i in idx]
    x = np.zeros((len(valid_pairs), 3), dtype=np.float32)
    y = np.zeros(len(valid_pairs), dtype=np.float32)
    for j, (s, pos) in enumerate(valid_pairs):
        x[j] = [own[s, pos], neigh_mean[s, pos], neigh_wet[s, pos]]
        y[j] = y_log[s, train_times[pos]]
    return x, y


def evaluate_source_model(
    model,
    y_raw: np.ndarray,
    y_log: np.ndarray,
    mask: np.ndarray,
    test_times: np.ndarray,
    own: np.ndarray,
    neigh_mean: np.ndarray,
    neigh_wet: np.ndarray,
    meta: pd.DataFrame,
    source_region: str,
) -> pd.DataFrame:
    rows = []
    x_all = np.stack([own, neigh_mean, neigh_wet], axis=2).reshape(-1, 3)
    pred_log = model.predict(x_all).reshape(own.shape)
    pred_raw = np.expm1(pred_log).clip(min=0)
    for s in range(y_raw.shape[0]):
        valid = mask[s, test_times] > 0
        if not valid.any():
            continue
        yt = y_raw[s, test_times][valid]
        yp = pred_raw[s][valid]
        abs_error = np.abs(yt - yp)
        brier = ((yt > 1.0).astype(float) - (yp > 1.0).astype(float)) ** 2
        rows.append(
            {
                "station_idx": s,
                "mae": float(abs_error.mean()),
                "brier_occurrence": float(brier.mean()),
                "n": int(valid.sum()),
            }
        )
    out = pd.DataFrame(rows)
    out = out.merge(meta[["station_idx", "ar6_region", "cell5"]], on="station_idx", how="left")
    out = out.rename(columns={"ar6_region": "target_region"})
    out["source_region"] = source_region
    out["model"] = "spatial_knn_ridge"
    return out


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
    y_log = data["y_log1p"].astype(np.float32)
    mask = data["mask"].astype(np.float32)
    dates = data["dates"]
    station_region = data["station_region"]
    region_names = data["region_names"]
    meta = pd.read_csv(META).sort_values("station_idx").reset_index(drop=True)

    train_times = np.where(date_mask(dates, f"{_TR0}-01-02", f"{_TR1}-12-31"))[0]
    test_times = np.where(date_mask(dates, f"{_TE0}-01-02", f"{_TE1}-12-31"))[0]

    neighbors = build_knn(meta, station_region)
    train_own, train_neigh, train_wet = neighbor_lag_features(y_log, mask, neighbors, train_times)
    test_own, test_neigh, test_wet = neighbor_lag_features(y_log, mask, neighbors, test_times)

    rows = []
    for source_idx, source_region in enumerate(region_names):
        station_train = np.where(station_region == source_idx)[0]
        x_train, y_train = sample_training_matrix(
            y_log,
            mask,
            station_train,
            train_times,
            train_own,
            train_neigh,
            train_wet,
            seed=SEED + int(source_idx),
        )
        model = make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-3, 3, 13)))
        model.fit(x_train, y_train)
        eval_df = evaluate_source_model(
            model,
            y_raw,
            y_log,
            mask,
            test_times,
            test_own,
            test_neigh,
            test_wet,
            meta,
            str(source_region),
        )
        rows.append(eval_df)
        print(source_region, x_train.shape)

    station = add_degradation(pd.concat(rows, ignore_index=True))
    pair = pair_summary(station)
    station.to_csv(OUT_STATION, index=False)
    pair.to_csv(OUT_PAIR, index=False)

    lines = [
        "# Spatial baseline forecasting experiment",
        "",
        f"Dataset: `{DATA.name}`.",
        "",
        "Model:",
        "",
        "- `spatial_knn_ridge`: ridge regression trained on source-region stations;",
        "- features: own previous-day log precipitation, local kNN previous-day mean, local kNN wet fraction;",
        f"- kNN graph: {K_NEIGHBORS} nearest stations within each target/source AR6 region.",
        "",
        "Interpretation:",
        "",
        "- this is a lightweight spatial model, not a full ST-GNN;",
        "- it tests whether a transferable local spatial-lag rule adds value before training Graph WaveNet or AGCRN.",
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
