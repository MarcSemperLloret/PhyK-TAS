from __future__ import annotations

import math
import os
from dataclasses import dataclass
from pathlib import Path

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
OUT_STATION = PAPER / f"forecast_patchtst{SUFFIX}_station_metrics.csv"
OUT_PAIR = PAPER / f"forecast_patchtst{SUFFIX}_pair_summary.csv"
REPORT = PAPER / f"forecast_patchtst{SUFFIX}_report.md"

LOOKBACK = int(os.environ.get("FORECAST_LOOKBACK", "30"))
HORIZON = int(os.environ.get("FORECAST_HORIZON", "1"))
BATCH_SIZE = int(os.environ.get("PATCHTST_BATCH_SIZE", "512"))
EPOCHS = int(os.environ.get("PATCHTST_EPOCHS", "3"))
LR = float(os.environ.get("PATCHTST_LR", "1e-3"))
SEED = int(os.environ.get("FORECAST_MODEL_SEED", os.environ.get("FORECAST_RANDOM_SEED", "20260523")))
MAX_TRAIN_WINDOWS = int(os.environ.get("PATCHTST_MAX_TRAIN_WINDOWS", "90000"))
MAX_VAL_WINDOWS = int(os.environ.get("PATCHTST_MAX_VAL_WINDOWS", "25000"))
MAX_TEST_WINDOWS = int(os.environ.get("PATCHTST_MAX_TEST_WINDOWS", "180000"))


def date_mask(dates: np.ndarray, start: str, end: str) -> np.ndarray:
    d = pd.to_datetime(dates)
    return np.asarray((d >= start) & (d <= end))


class WindowDataset(Dataset):
    def __init__(
        self,
        y: np.ndarray,
        mask: np.ndarray,
        station_indices: np.ndarray,
        time_indices: np.ndarray,
        max_samples: int | None = None,
        seed: int = SEED,
    ):
        self.y = y
        self.mask = mask
        self.samples = []
        for s in station_indices:
            for t in time_indices:
                start = t - LOOKBACK
                target = t + HORIZON - 1
                if start < 0 or target >= y.shape[1]:
                    continue
                if mask[s, target] <= 0:
                    continue
                # Allow missing inputs; they are represented by a mask channel.
                self.samples.append((s, t))
        if max_samples is not None and len(self.samples) > max_samples:
            rng = np.random.default_rng(seed)
            idx = rng.choice(len(self.samples), max_samples, replace=False)
            self.samples = [self.samples[i] for i in idx]

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int):
        s, t = self.samples[idx]
        x = self.y[s, t - LOOKBACK : t]
        m = self.mask[s, t - LOOKBACK : t]
        x = np.stack([np.nan_to_num(x, nan=0.0), m], axis=0).astype(np.float32)
        y = self.y[s, t + HORIZON - 1].astype(np.float32)
        return torch.from_numpy(x), torch.tensor(y), torch.tensor(s, dtype=torch.long)


class LinearWindow(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Flatten(),
            nn.Linear(LOOKBACK * 2, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
        )

    def forward(self, x):
        return self.net(x).squeeze(-1)


class PatchTSTSmall(nn.Module):
    def __init__(self, patch_len: int = 5, d_model: int = 48, nhead: int = 4, layers: int = 1):
        super().__init__()
        self.patch_len = patch_len
        self.n_patches = LOOKBACK // patch_len
        self.proj = nn.Linear(patch_len * 2, d_model)
        enc_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=128,
            dropout=0.1,
            batch_first=True,
            activation="gelu",
        )
        self.encoder = nn.TransformerEncoder(enc_layer, num_layers=layers)
        self.head = nn.Sequential(nn.Flatten(), nn.Linear(self.n_patches * d_model, 1))

    def forward(self, x):
        # x: B, 2, LOOKBACK
        b = x.shape[0]
        x = x[:, :, : self.n_patches * self.patch_len]
        patches = x.reshape(b, 2, self.n_patches, self.patch_len).permute(0, 2, 1, 3)
        patches = patches.reshape(b, self.n_patches, 2 * self.patch_len)
        z = self.proj(patches)
        z = self.encoder(z)
        return self.head(z).squeeze(-1)


def train_model(model: nn.Module, train_loader: DataLoader, val_loader: DataLoader, device: torch.device) -> nn.Module:
    model.to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=1e-4)
    loss_fn = nn.L1Loss()
    best_state = None
    best_val = float("inf")
    for _ in range(EPOCHS):
        model.train()
        for x, y, _ in train_loader:
            x, y = x.to(device), y.to(device)
            opt.zero_grad()
            pred = model(x)
            loss = loss_fn(pred, y)
            loss.backward()
            opt.step()
        model.eval()
        vals = []
        with torch.no_grad():
            for x, y, _ in val_loader:
                x, y = x.to(device), y.to(device)
                vals.append(loss_fn(model(x), y).item())
        val = float(np.mean(vals)) if vals else float("inf")
        if val < best_val:
            best_val = val
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
    if best_state is not None:
        model.load_state_dict(best_state)
    return model


def predict(model: nn.Module, loader: DataLoader, device: torch.device) -> pd.DataFrame:
    model.eval()
    rows = []
    with torch.no_grad():
        for x, y, s in loader:
            x = x.to(device)
            pred = model(x).cpu().numpy()
            for si, yi, pi in zip(s.numpy(), y.numpy(), pred):
                rows.append((int(si), float(yi), float(pi)))
    return pd.DataFrame(rows, columns=["station_idx", "y_log1p", "pred_log1p"])


def evaluate_predictions(pred: pd.DataFrame, meta: pd.DataFrame, source_region: str, model_name: str) -> pd.DataFrame:
    pred = pred.merge(meta[["station_idx", "ar6_region", "cell5"]], on="station_idx", how="left")
    pred["y_raw"] = np.expm1(pred["y_log1p"]).clip(lower=0)
    pred["pred_raw"] = np.expm1(pred["pred_log1p"]).clip(lower=0)
    pred["abs_error"] = (pred["y_raw"] - pred["pred_raw"]).abs()
    pred["occ_y"] = (pred["y_raw"] > 1.0).astype(float)
    pred["occ_pred"] = (pred["pred_raw"] > 1.0).astype(float)
    pred["brier_occurrence"] = (pred["occ_y"] - pred["occ_pred"]) ** 2
    out = (
        pred.groupby(["station_idx", "ar6_region", "cell5"])
        .agg(mae=("abs_error", "mean"), brier_occurrence=("brier_occurrence", "mean"), n=("y_raw", "size"))
        .reset_index()
        .rename(columns={"ar6_region": "target_region"})
    )
    out["source_region"] = source_region
    out["model"] = model_name
    return out


def main() -> None:
    torch.manual_seed(SEED)
    np.random.seed(SEED)
    data = np.load(DATA, allow_pickle=True)
    y = data["y_log1p"].astype(np.float32)
    mask = data["mask"].astype(np.float32)
    dates = data["dates"]
    regions = data["region_names"]
    station_region = data["station_region"]
    meta = pd.read_csv(META)

    train_times = np.where(date_mask(dates, "2005-02-01", "2012-12-31"))[0]
    val_times = np.where(date_mask(dates, "2013-02-01", "2015-12-31"))[0]
    test_times = np.where(date_mask(dates, "2020-02-01", "2025-12-31"))[0]

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    rows = []
    for source_idx, source_region in enumerate(regions):
        station_train = np.where(station_region == source_idx)[0]
        train_ds = WindowDataset(
            y, mask, station_train, train_times, max_samples=MAX_TRAIN_WINDOWS, seed=SEED + int(source_idx)
        )
        val_ds = WindowDataset(
            y, mask, station_train, val_times, max_samples=MAX_VAL_WINDOWS, seed=SEED + 100 + int(source_idx)
        )
        train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
        val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False)

        for model_name, model in [
            ("linear_window", LinearWindow()),
            ("patchtst_small", PatchTSTSmall()),
        ]:
            trained = train_model(model, train_loader, val_loader, device)
            all_test = WindowDataset(
                y,
                mask,
                np.arange(y.shape[0]),
                test_times,
                max_samples=MAX_TEST_WINDOWS,
                seed=SEED + 200 + int(source_idx),
            )
            test_loader = DataLoader(all_test, batch_size=BATCH_SIZE, shuffle=False)
            pred = predict(trained, test_loader, device)
            eval_df = evaluate_predictions(pred, meta, source_region, model_name)
            rows.append(eval_df)
            print(source_region, model_name, len(train_ds), len(val_ds), len(all_test))

    station = pd.concat(rows, ignore_index=True)
    # Add out-minus-in per model and station.
    in_region = station[station["source_region"] == station["target_region"]][
        ["station_idx", "model", "mae", "brier_occurrence"]
    ].rename(columns={"mae": "mae_in_region", "brier_occurrence": "brier_in_region"})
    station = station.merge(in_region, on=["station_idx", "model"], how="left")
    station["mae_out_minus_in"] = station["mae"] - station["mae_in_region"]
    station["brier_out_minus_in"] = station["brier_occurrence"] - station["brier_in_region"]
    station.to_csv(OUT_STATION, index=False)

    pair = (
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
    pair.to_csv(OUT_PAIR, index=False)

    lines = [
        "# PatchTST first forecasting experiment",
        "",
        "Dataset:",
        "",
        f"- `{DATA.name}`;",
        "- lookback 30 days, horizon 1 day;",
        "- target transform: log1p precipitation.",
        "",
        "Models:",
        "",
        "- `linear_window`;",
        "- `patchtst_small`.",
        "",
        "Training:",
        "",
        "- source region only;",
        "- train 2005-2012;",
        "- validation 2013-2015;",
        "- test 2020-2025 on all target regions.",
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
