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
OUT_STATION = PAPER / f"forecast_graphwavenet{SUFFIX}_station_metrics.csv"
OUT_PAIR = PAPER / f"forecast_graphwavenet{SUFFIX}_pair_summary.csv"
REPORT = PAPER / f"forecast_graphwavenet{SUFFIX}_report.md"

LOOKBACK = int(os.environ.get("FORECAST_LOOKBACK", "30"))
HORIZON = int(os.environ.get("FORECAST_HORIZON", "1"))
K_NEIGHBORS = int(os.environ.get("FORECAST_K_NEIGHBORS", "8"))
RESIDUAL_CHANNELS = int(os.environ.get("GRAPHWAVENET_RESIDUAL_CHANNELS", "32"))
SKIP_CHANNELS = int(os.environ.get("GRAPHWAVENET_SKIP_CHANNELS", "64"))
DILATIONS = [int(x) for x in os.environ.get("GRAPHWAVENET_DILATIONS", "1,2,4,8").split(",")]
BATCH_SIZE = int(os.environ.get("FORECAST_BATCH_SIZE", "16"))
EPOCHS = int(os.environ.get("FORECAST_EPOCHS", "8"))
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
    forward = adj / deg[:, None]
    backward = forward.T
    supports = np.stack([forward, backward], axis=0)
    return torch.tensor(supports, dtype=torch.float32)


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
        times = np.arange(t - LOOKBACK, t)
        x = self.y_log[np.ix_(self.indices, times)]
        m = self.mask[np.ix_(self.indices, times)]
        y = self.y_log[self.indices, target]
        ym = self.mask[self.indices, target]
        x = np.stack([np.nan_to_num(x, nan=0.0), m], axis=0).astype(np.float32)
        # x: C, N, T
        return (
            torch.from_numpy(x),
            torch.from_numpy(np.nan_to_num(y, nan=0.0).astype(np.float32)),
            torch.from_numpy(ym.astype(np.float32)),
            torch.tensor(target, dtype=torch.long),
        )


class GraphConv(nn.Module):
    def __init__(self, channels: int):
        super().__init__()
        self.proj = nn.Conv2d(channels * 3, channels, kernel_size=(1, 1))

    def forward(self, x: torch.Tensor, supports: torch.Tensor) -> torch.Tensor:
        # x: B, C, N, T; supports: S, N, N.
        out = [x]
        for s in supports:
            out.append(torch.einsum("nm,bcmt->bcnt", s, x))
        return self.proj(torch.cat(out, dim=1))


class WaveBlock(nn.Module):
    def __init__(self, channels: int, skip_channels: int, dilation: int):
        super().__init__()
        pad = dilation
        self.filter_conv = nn.Conv2d(channels, channels, kernel_size=(1, 2), dilation=(1, dilation), padding=(0, pad))
        self.gate_conv = nn.Conv2d(channels, channels, kernel_size=(1, 2), dilation=(1, dilation), padding=(0, pad))
        self.graph_conv = GraphConv(channels)
        self.residual_conv = nn.Conv2d(channels, channels, kernel_size=(1, 1))
        self.skip_conv = nn.Conv2d(channels, skip_channels, kernel_size=(1, 1))
        self.norm = nn.BatchNorm2d(channels)

    def forward(self, x: torch.Tensor, supports: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        residual = x
        f = torch.tanh(self.filter_conv(x))[..., : x.shape[-1]]
        g = torch.sigmoid(self.gate_conv(x))[..., : x.shape[-1]]
        z = f * g
        z = self.graph_conv(z, supports)
        skip = self.skip_conv(z)
        z = self.residual_conv(z)
        z = self.norm(z + residual)
        return z, skip


class TransferableGraphWaveNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.start = nn.Conv2d(2, RESIDUAL_CHANNELS, kernel_size=(1, 1))
        self.blocks = nn.ModuleList(
            [WaveBlock(RESIDUAL_CHANNELS, SKIP_CHANNELS, dilation=d) for d in DILATIONS]
        )
        self.end = nn.Sequential(
            nn.ReLU(),
            nn.Conv2d(SKIP_CHANNELS, SKIP_CHANNELS, kernel_size=(1, 1)),
            nn.ReLU(),
            nn.Conv2d(SKIP_CHANNELS, 1, kernel_size=(1, 1)),
        )

    def forward(self, x: torch.Tensor, supports: torch.Tensor) -> torch.Tensor:
        # x: B, 2, N, T
        h = self.start(x)
        skip_total = None
        for block in self.blocks:
            h, skip = block(h, supports)
            skip_total = skip if skip_total is None else skip_total + skip
        out = self.end(skip_total)
        return out[..., -1].squeeze(1)


def masked_l1(pred: torch.Tensor, y: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    denom = mask.sum().clamp_min(1.0)
    return (torch.abs(pred - y) * mask).sum() / denom


def train_model(model: nn.Module, train_loader: DataLoader, val_loader: DataLoader, supports: torch.Tensor, device: torch.device):
    model.to(device)
    supports = supports.to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=1e-4)
    best_state = None
    best_val = float("inf")
    patience = 3
    no_improve = 0
    for _ in range(EPOCHS):
        model.train()
        for x, y, ym, _ in train_loader:
            x, y, ym = x.to(device), y.to(device), ym.to(device)
            opt.zero_grad()
            loss = masked_l1(model(x, supports), y, ym)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
            opt.step()
        model.eval()
        vals = []
        with torch.no_grad():
            for x, y, ym, _ in val_loader:
                x, y, ym = x.to(device), y.to(device), ym.to(device)
                vals.append(masked_l1(model(x, supports), y, ym).item())
        val = float(np.mean(vals)) if vals else float("inf")
        if val < best_val:
            best_val = val
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
            no_improve = 0
        else:
            no_improve += 1
            if no_improve >= patience:
                break
    if best_state is not None:
        model.load_state_dict(best_state)
    return model


def evaluate_model(
    model: nn.Module,
    loader: DataLoader,
    supports: torch.Tensor,
    indices: np.ndarray,
    y_raw: np.ndarray,
    meta: pd.DataFrame,
    source_region: str,
    device: torch.device,
) -> pd.DataFrame:
    model.eval()
    supports = supports.to(device)
    rows = []
    with torch.no_grad():
        for x, _, ym, target_t in loader:
            pred = np.expm1(model(x.to(device), supports).cpu().numpy()).clip(min=0)
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
    out["model"] = "graphwavenet_transfer"
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

    train_times = np.where(date_mask(dates, "2005-02-01", "2012-12-31"))[0]
    val_times = np.where(date_mask(dates, "2013-02-01", "2015-12-31"))[0]
    test_times = np.where(date_mask(dates, "2020-02-01", "2025-12-31"))[0]
    region_indices = build_region_indices(station_region, region_names)
    supports_by_region = {region: build_adjacency(meta, idx) for region, idx in region_indices.items()}

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    rows = []
    for source_region, source_indices in region_indices.items():
        train_ds = GraphWindowDataset(y_log, mask, source_indices, train_times)
        val_ds = GraphWindowDataset(y_log, mask, source_indices, val_times)
        train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
        val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False)
        model = train_model(
            TransferableGraphWaveNet(),
            train_loader,
            val_loader,
            supports_by_region[source_region],
            device,
        )
        for target_region, target_indices in region_indices.items():
            test_ds = GraphWindowDataset(y_log, mask, target_indices, test_times)
            test_loader = DataLoader(test_ds, batch_size=BATCH_SIZE, shuffle=False)
            rows.append(
                evaluate_model(
                    model,
                    test_loader,
                    supports_by_region[target_region],
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
        "# Transferable Graph WaveNet experiment",
        "",
        "Model:",
        "",
        "- `graphwavenet_transfer`: Graph WaveNet-style dilated gated temporal convolutions plus graph diffusion;",
        "- fixed source/target kNN supports, forward and backward random-walk matrices;",
        "- no node-specific embeddings, so the model is transferable across station sets.",
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
