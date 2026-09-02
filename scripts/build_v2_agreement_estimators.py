from __future__ import annotations

"""Evaluate label-free agreement estimators against the PhyK-TAS evidence layers.

Pools the export-run seeds and compares, per forecast model and validation
regime (group-by-cell, leave-target-region-out), the degradation-inference R2
of: label-free agreement features alone (the SOTA-comparator baseline), the
generic-shift and physical layers, their fusion, and the fusion augmented with
the agreement source. Protocol mirrors compare_kbs_on_forecast_models.py
(RF 400 trees / min leaf 10 / fixed seed, median imputation, grouped CV).
"""

import os
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import GroupKFold, LeaveOneGroupOut, cross_val_predict


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"

TAGS = [
    t.strip()
    for t in os.environ.get(
        "AGREEMENT_TAGS",
        "all_viable_min100_full_s1_export;all_viable_min100_full_s2_export;all_viable_min100_full_s3_export",
    ).split(";")
    if t.strip()
]
DATASET_TAGS = [
    t.strip()
    for t in os.environ.get(
        "AGREEMENT_DATASET_TAGS",
        "all_viable_min100_full_s1;all_viable_min100_full_s2;all_viable_min100_full_s3",
    ).split(";")
    if t.strip()
]
DESC = Path(
    os.environ.get("PHYKTAS_PHYSICAL_DESCRIPTORS", PAPER / "physical_descriptors_station_all_viable_min100.csv")
)
SHIFT = Path(
    os.environ.get("PHYKTAS_SHIFT_BASELINES", PAPER / "distribution_shift_baselines_all_viable_min100.csv")
)
OUT_SUFFIX = os.environ.get("AGREEMENT_OUT_SUFFIX", "all_viable_min100_full").strip()
OUT = PAPER / f"v2_agreement_estimators_{OUT_SUFFIX}.csv"
PRED = PAPER / f"v2_agreement_estimators_{OUT_SUFFIX}_predictions.csv"
REPORT = PAPER / f"v2_agreement_estimators_{OUT_SUFFIX}_report.md"

METRIC_FILES = [
    "forecast_baseline_{tag}_station_metrics.csv",
    "forecast_spatial_baseline_{tag}_station_metrics.csv",
    "forecast_patchtst_{tag}_station_metrics.csv",
    "forecast_stgnn_{tag}_station_metrics.csv",
    "forecast_graphwavenet_{tag}_station_metrics.csv",
]

PHYSICAL_COLS = [
    "wet_day_fraction_gt1mm",
    "wet_day_mean_intensity",
    "daily_precip_cv",
    "monthly_climatology_amplitude",
    "top3_month_precip_fraction",
    "occurrence_lag1_autocorr",
    "wet_intensity_lag1_autocorr",
    "dry_spell_mean_days",
    "dry_spell_p95_days",
    "wet_day_p95",
    "wet_day_p99",
    "extreme_tail_ratio_p99_p95",
]

SHIFT_COLS = [
    "kl_source_to_target",
    "kl_target_to_source",
    "wasserstein_precip",
    "mmd_rbf_precip",
    "shift_mean_abs",
    "shift_variance_abs",
    "shift_wet_fraction_abs",
    "shift_p95_abs",
    "shift_p99_abs",
    "shift_monthly_l2",
    "region_centroid_distance_deg",
]

AGREE_COLS = [
    "agree_cross_source_l1",
    "agree_cross_family_l1",
    "pred_mean",
    "pred_wet_rate",
    "pred_p95",
    "pred_mean_shift",
    "pred_wet_rate_shift",
    "pred_p95_shift",
]

# Cold-start variant: the cross-source ensemble excludes the model trained on
# the station's own region, so no target-trained forecaster is assumed.
AGREE_COLD_COLS = ["agree_cross_source_excl_target_l1"] + AGREE_COLS[1:]

FEATURE_SETS = {
    "label_free_agreement": AGREE_COLS,
    "label_free_agreement_cold": AGREE_COLD_COLS,
    "generic_shift": SHIFT_COLS,
    "physical_knowledge": PHYSICAL_COLS,
    "physical_plus_shift": PHYSICAL_COLS + SHIFT_COLS,
    "shift_plus_agreement": SHIFT_COLS + AGREE_COLS,
    "physical_plus_shift_plus_agreement": PHYSICAL_COLS + SHIFT_COLS + AGREE_COLS,
    "physical_plus_shift_plus_agreement_cold": PHYSICAL_COLS + SHIFT_COLS + AGREE_COLD_COLS,
}


def load_seed(tag: str, dataset_tag: str, seed_label: str) -> pd.DataFrame:
    frames = [
        pd.read_csv(PAPER / name.format(tag=tag))
        for name in METRIC_FILES
        if (PAPER / name.format(tag=tag)).exists()
    ]
    if not frames:
        raise FileNotFoundError(f"No station metrics for tag {tag}")
    forecast = pd.concat(frames, ignore_index=True)
    forecast = forecast[forecast["source_region"] != forecast["target_region"]].copy()

    meta = pd.read_csv(PAPER / f"forecast_dataset_large_{dataset_tag}_metadata.csv")[
        ["station_idx", "canonical_station_uid"]
    ]
    forecast = forecast.merge(meta, on="station_idx", how="left")

    agree = pd.read_csv(PAPER / f"v2_agreement_features_{tag}.csv")
    forecast = forecast.merge(
        agree.drop(columns=["target_region"]),
        on=["model", "source_region", "station_idx"],
        how="left",
    )

    desc = pd.read_csv(DESC)
    shift = pd.read_csv(SHIFT)
    df = forecast.merge(
        desc,
        left_on=["canonical_station_uid", "target_region", "cell5"],
        right_on=["canonical_station_uid", "ar6_region", "cell5"],
        how="left",
    ).merge(shift, on=["source_region", "target_region"], how="left")
    df = df[df["mae_out_minus_in"].notna()].copy()
    df["seed"] = seed_label
    return df


def evaluate(
    df: pd.DataFrame, cols: list[str], feature_set: str, cv_kind: str, model_name: str
) -> tuple[dict, np.ndarray]:
    y = df["mae_out_minus_in"].to_numpy()
    x = df[cols].replace([np.inf, -np.inf], np.nan)
    x = x.fillna(x.median(numeric_only=True))
    if cv_kind == "leave_target_region_out":
        cv = LeaveOneGroupOut()
        groups = df["target_region"].to_numpy()
    elif cv_kind == "group_by_cell":
        cv = GroupKFold(n_splits=min(5, df["cell5"].nunique()))
        groups = df["cell5"].to_numpy()
    else:
        raise ValueError(cv_kind)
    rf = RandomForestRegressor(n_estimators=400, min_samples_leaf=10, random_state=20260524, n_jobs=-1)
    pred = cross_val_predict(rf, x, y, cv=cv, groups=groups)
    row = {
        "forecast_model": model_name,
        "feature_set": feature_set,
        "cv_kind": cv_kind,
        "n": len(df),
        "n_features": len(cols),
        "mae": mean_absolute_error(y, pred),
        "r2": r2_score(y, pred),
    }
    return row, pred


def main() -> None:
    if len(TAGS) != len(DATASET_TAGS):
        raise ValueError("AGREEMENT_TAGS and AGREEMENT_DATASET_TAGS must align")
    df = pd.concat(
        [load_seed(tag, ds, f"s{i+1}") for i, (tag, ds) in enumerate(zip(TAGS, DATASET_TAGS))],
        ignore_index=True,
    )
    print("pooled rows:", len(df))

    rows = []
    pred_frames = []
    for forecast_model, sub in df.groupby("model"):
        pred_df = sub[
            ["seed", "station_idx", "source_region", "target_region", "cell5", "mae_out_minus_in", "model"]
        ].copy()
        for cv_kind in ["group_by_cell", "leave_target_region_out"]:
            for label, cols in FEATURE_SETS.items():
                row, pred = evaluate(sub, cols, label, cv_kind, forecast_model)
                rows.append(row)
                pred_df[f"{label}_{cv_kind}_pred"] = pred
                print(forecast_model, cv_kind, label, f"r2={row['r2']:.3f}", flush=True)
        pred_frames.append(pred_df)
    results = pd.DataFrame(rows)
    results.to_csv(OUT, index=False)
    pd.concat(pred_frames, ignore_index=True).to_csv(PRED, index=False)

    wide = results.pivot_table(index=["forecast_model", "cv_kind"], columns="feature_set", values="r2")
    wide["delta_agree_over_fused"] = (
        wide["physical_plus_shift_plus_agreement"] - wide["physical_plus_shift"]
    )
    wide["delta_fused_over_agree"] = wide["physical_plus_shift"] - wide["label_free_agreement"]
    wide["delta_agree_cold_over_fused"] = (
        wide["physical_plus_shift_plus_agreement_cold"] - wide["physical_plus_shift"]
    )
    wide["delta_fused_over_agree_cold"] = wide["physical_plus_shift"] - wide["label_free_agreement_cold"]

    lines = [
        "# Label-free agreement estimators vs PhyK-TAS evidence layers",
        "",
        f"Seed-pooled over tags: {', '.join(TAGS)}.",
        "",
        "`label_free_agreement` is the SOTA-comparator baseline (cross-source and",
        "cross-family disagreement plus output-distribution shift, no target labels).",
        "`delta_fused_over_agree` > 0 means the PhyK-TAS fused layer beats the",
        "label-free baseline; `delta_agree_over_fused` > 0 means agreement adds",
        "information on top of the fused layer.",
        "",
        wide.round(3).to_markdown(),
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"wrote {PRED}")
    print(f"wrote {REPORT}")
    print(wide.round(3).to_string())


if __name__ == "__main__":
    main()
