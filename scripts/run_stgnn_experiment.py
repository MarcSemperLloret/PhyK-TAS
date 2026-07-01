from __future__ import annotations

from pathlib import Path
import os

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
EXPERIMENT_TAG = os.environ.get("FORECAST_EXPERIMENT_TAG", "").strip()
SUFFIX = f"_{EXPERIMENT_TAG}" if EXPERIMENT_TAG else ""
DATA = Path(os.environ.get("FORECAST_DATA", PAPER / "forecast_dataset_operational_sample.npz"))
META = Path(os.environ.get("FORECAST_META", PAPER / "forecast_dataset_operational_sample_metadata.csv"))
OUT_STATION = PAPER / f"forecast_stgnn{SUFFIX}_station_metrics.csv"
OUT_PAIR = PAPER / f"forecast_stgnn{SUFFIX}_pair_summary.csv"
REPORT = PAPER / f"forecast_stgnn{SUFFIX}_report.md"

LOOKBACK = int(os.environ.get("FORECAST_LOOKBACK", "30"))
HORIZON = int(os.environ.get("FORECAST_HORIZON", "1"))
K_NEIGHBORS = int(os.environ.get("FORECAST_K_NEIGHBORS", "8"))
HIDDEN = int(os.environ.get("STGNN_HIDDEN", "48"))
BATCH_SIZE = int(os.environ.get("FORECAST_BATCH_SIZE", "16"))
EPOCHS = int(os.environ.get("FORECAST_EPOCHS", "5"))
LR = float(os.environ.get("FORECAST_LR", "1e-3"))
SEED = int(os.environ.get("FORECAST_MODEL_SEED", os.environ.get("FORECAST_RANDOM_SEED", "20260524")))


# Temporal split years (env-overridable so the later-window expansion run does
# not require editing this script; defaults reproduce the 11-region benchmark).
_TR0 = int(os.environ.get("FC_TRAIN_START_YEAR", "2005"))
_TR1 = int(os.environ.get("FC_TRAIN_END_YEAR", "2012"))
_VA0 = int(os.environ.get("FC_VAL_START_YEAR", "2013"))
_VA1 = int(os.environ.get("FC_VAL_END_YEAR", "2015"))
_TE0 = int(os.environ.get("FC_TEST_START_YEAR", "2020"))
_TE1 = int(os.environ.get("FC_TEST_END_YEAR", "2025"))


def date_mask(dates: np.ndarray, start: str, end: str) -> np.ndarray:
    d = pd.to_datetime(dates)
    return np.asarray((d >= start) & (d <= end))


def build_region_indices(station_region: np.ndarray, region_names: np.ndarray) -> dict[str, np.ndarray]:
    return {str(name): np.where(station_region == i)[0] for i, name in enumerate(region_names)}


def build_adjacency(meta: pd.DataFrame, indices: np.ndarray) -> torch.Tensor:
    sub = meta.sort_values("station_idx").set_index("station_idx").loc[indices]
    lat = np.deg2rad(sub["latitude"].to_numpy(dtype=float))
    lon = np.deg2rad(sub["longitude"].to_numpy(dtype=float))
    coords = np.column_stack([lat, lon])
    n = len(indices)
    dist = np.zeros((n, n), dtype=np.float32)
    for i in range(n):
        dlat = coords[:, 0] - coords[i, 0]
        dlon = coords[:, 1] - coords[i, 1]
        a = np.sin(dlat / 2) ** 2 + np.cos(coords[i, 0]) * np.cos(coords[:, 0]) * np.sin(dlon / 2) ** 2
        dist[i] = 2 * 6371.0 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))
    adj = np.zeros((n, n), dtype=np.float32)
    for i in range(n):
        order = np.argsort(dist[i])
        nn = order[1 : min(K_NEIGHBORS + 1, n)]
        sigma = float(np.median(dist[i, nn])) if len(nn) else 1.0
        sigma = max(sigma, 1e-3)
        adj[i, i] = 1.0
        adj[i, nn] = np.exp(-(dist[i, nn] ** 2) / (2 * sigma**2))
    adj = np.maximum(adj, adj.T)
    deg = adj.sum(axis=1)
    deg[deg == 0] = 1.0
    norm = adj / deg[:, None]
    return torch.tensor(norm, dtype=torch.float32)


class GraphWindowDataset(Dataset):
    def __init__(self, y_log: np.ndarray, mask: np.ndarray, indices: np.ndarray, time_indices: np.ndarray):
        self.y_log = y_log
        self.mask = mask
        self.indices = indices
        self.samples = []
        for t in time_indices:
            start = t - LOOKBACK
            target = t + HORIZON - 1
            if start < 0 or target >= y_log.shape[1]:
                continue
            if mask[indices, target].sum() == 0:
                continue
            self.samples.append(t)

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int):
        t = self.samples[idx]
        target = t + HORIZON - 1
        x = self.y_log[np.ix_(self.indices, np.arange(t - LOOKBACK, t))]
        m = self.mask[np.ix_(self.indices, np.arange(t - LOOKBACK, t))]
        y = self.y_log[self.indices, target]
        ym = self.mask[self.indices, target]
        x = np.stack([np.nan_to_num(x, nan=0.0), m], axis=-1).astype(np.float32)
        return (
            torch.from_numpy(x),
            torch.from_numpy(np.nan_to_num(y, nan=0.0).astype(np.float32)),
            torch.from_numpy(ym.astype(np.float32)),
            torch.tensor(target, dtype=torch.long),
        )


class DiffusionLayer(nn.Module):
    def __init__(self, hidden: int):
        super().__init__()
        self.lin = nn.Linear(hidden * 3, hidden)

    def forward(self, h: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        ah = torch.einsum("ij,bjh->bih", adj, h)
        a2h = torch.einsum("ij,bjh->bih", adj, ah)
        return torch.relu(self.lin(torch.cat([h, ah, a2h], dim=-1)))


class STGCNDiffusion(nn.Module):
    def __init__(self, hidden: int = HIDDEN):
        super().__init__()
        self.temporal = nn.Sequential(
            nn.Conv1d(2, hidden, kernel_size=5, padding=2),
            nn.GELU(),
            nn.Conv1d(hidden, hidden, kernel_size=3, padding=1),
            nn.GELU(),
        )
        self.g1 = DiffusionLayer(hidden)
        self.g2 = DiffusionLayer(hidden)
        self.head = nn.Linear(hidden, 1)

    def forward(self, x: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        # x: B, N, L, 2
        b, n, l, c = x.shape
        z = x.reshape(b * n, l, c).permute(0, 2, 1)
        h = self.temporal(z)[:, :, -1].reshape(b, n, -1)
        h = self.g1(h, adj)
        h = self.g2(h, adj)
        return self.head(h).squeeze(-1)


def masked_l1(pred: torch.Tensor, y: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    denom = mask.sum().clamp_min(1.0)
    return (torch.abs(pred - y) * mask).sum() / denom


def train_model(model: nn.Module, train_loader: DataLoader, val_loader: DataLoader, adj: torch.Tensor, device: torch.device):
    model.to(device)
    adj = adj.to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=1e-4)
    best_state = None
    best_val = float("inf")
    for _ in range(EPOCHS):
        model.train()
        for x, y, ym, _ in train_loader:
            x, y, ym = x.to(device), y.to(device), ym.to(device)
            opt.zero_grad()
            loss = masked_l1(model(x, adj), y, ym)
            loss.backward()
            opt.step()
        model.eval()
        vals = []
        with torch.no_grad():
            for x, y, ym, _ in val_loader:
                x, y, ym = x.to(device), y.to(device), ym.to(device)
                vals.append(masked_l1(model(x, adj), y, ym).item())
        val = float(np.mean(vals)) if vals else float("inf")
        if val < best_val:
            best_val = val
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
    if best_state is not None:
        model.load_state_dict(best_state)
    return model


def evaluate_model(
    model: nn.Module,
    loader: DataLoader,
    adj: torch.Tensor,
    indices: np.ndarray,
    y_raw: np.ndarray,
    meta: pd.DataFrame,
    source_region: str,
    device: torch.device,
) -> pd.DataFrame:
    model.eval()
    adj = adj.to(device)
    rows = []
    with torch.no_grad():
        for x, _, ym, target_t in loader:
            x = x.to(device)
            pred = np.expm1(model(x, adj).cpu().numpy()).clip(min=0)
            ym_np = ym.numpy()
            for b in range(pred.shape[0]):
                t = int(target_t[b].item())
                valid = ym_np[b] > 0
                for local_i in np.where(valid)[0]:
                    s = int(indices[local_i])
                    rows.append((s, float(y_raw[s, t]), float(pred[b, local_i])))
    pred_df = pd.DataFrame(rows, columns=["station_idx", "y_raw", "pred_raw"])
    pred_df = pred_df.merge(meta[["station_idx", "ar6_region", "cell5"]], on="station_idx", how="left")
    pred_df["abs_error"] = (pred_df["y_raw"] - pred_df["pred_raw"]).abs()
    pred_df["occ_y"] = (pred_df["y_raw"] > 1.0).astype(float)
    pred_df["occ_pred"] = (pred_df["pred_raw"] > 1.0).astype(float)
    pred_df["brier_occurrence"] = (pred_df["occ_y"] - pred_df["occ_pred"]) ** 2
    out = (
        pred_df.groupby(["station_idx", "ar6_region", "cell5"])
        .agg(mae=("abs_error", "mean"), brier_occurrence=("brier_occurrence", "mean"), n=("y_raw", "size"))
        .reset_index()
        .rename(columns={"ar6_region": "target_region"})
    )
    out["source_region"] = source_region
    out["model"] = "stgcn_diffusion"
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
    torch.manual_seed(SEED)
    np.random.seed(SEED)
    data = np.load(DATA, allow_pickle=True)
    y_raw = data["y_raw"].astype(np.float32)
    y_log = data["y_log1p"].astype(np.float32)
    mask = data["mask"].astype(np.float32)
    dates = data["dates"]
    station_region = data["station_region"]
    region_names = data["region_names"]
    meta = pd.read_csv(META).sort_values("station_idx").reset_index(drop=True)

    train_times = np.where(date_mask(dates, f"{_TR0}-02-01", f"{_TR1}-12-31"))[0]
    val_times = np.where(date_mask(dates, f"{_VA0}-02-01", f"{_VA1}-12-31"))[0]
    test_times = np.where(date_mask(dates, f"{_TE0}-02-01", f"{_TE1}-12-31"))[0]

    region_indices = build_region_indices(station_region, region_names)
    adjs = {region: build_adjacency(meta, idx) for region, idx in region_indices.items()}

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    rows = []
    for source_region, source_indices in region_indices.items():
        train_ds = GraphWindowDataset(y_log, mask, source_indices, train_times)
        val_ds = GraphWindowDataset(y_log, mask, source_indices, val_times)
        train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
        val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False)
        model = train_model(STGCNDiffusion(), train_loader, val_loader, adjs[source_region], device)

        for target_region, target_indices in region_indices.items():
            test_ds = GraphWindowDataset(y_log, mask, target_indices, test_times)
            test_loader = DataLoader(test_ds, batch_size=BATCH_SIZE, shuffle=False)
            rows.append(
                evaluate_model(
                    model,
                    test_loader,
                    adjs[target_region],
                    target_indices,
                    y_raw,
                    meta,
                    source_region,
                    device,
                )
            )
        print(source_region, len(train_ds), len(val_ds))

    station = add_degradation(pd.concat(rows, ignore_index=True))
    pair = pair_summary(station)
    station.to_csv(OUT_STATION, index=False)
    pair.to_csv(OUT_PAIR, index=False)
    lines = [
        "# ST-GNN forecasting experiment",
        "",
        "Model:",
        "",
        "- `stgcn_diffusion`: temporal convolution plus two fixed-graph diffusion layers;",
        "- graph: symmetric kNN adjacency within each AR6 region;",
        "- no node-specific embeddings, so weights can transfer across regions with different station identities.",
        "",
        "Training:",
        "",
        "- source region only;",
        "- train 2005-2012;",
        "- validation 2013-2015;",
        "- test 2020-2025 on each target-region graph.",
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
