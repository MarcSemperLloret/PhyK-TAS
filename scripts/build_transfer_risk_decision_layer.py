from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    balanced_accuracy_score,
    brier_score_loss,
    f1_score,
    log_loss,
)
from sklearn.model_selection import GroupKFold, LeaveOneGroupOut, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
DESC = PAPER / "physical_descriptors_station.csv"
SHIFT = PAPER / "distribution_shift_baselines.csv"
MATRIX = PAPER / "light_degradation_station.csv"
OUT_METRICS = PAPER / "transfer_risk_classifier_results.csv"
OUT_PRED = PAPER / "transfer_risk_predictions.csv"
OUT_DECISIONS = PAPER / "transfer_risk_decisions.csv"
REPORT = PAPER / "transfer_risk_decision_layer_report.md"


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

LABEL_ORDER = ["safe", "moderate", "high"]


def risk_labels(values: pd.Series) -> pd.Series:
    positive = values[values > 0]
    high_cut = float(positive.quantile(0.75)) if len(positive) else 0.0
    labels = pd.Series(index=values.index, dtype=object)
    labels[values <= 0] = "safe"
    labels[(values > 0) & (values <= high_cut)] = "moderate"
    labels[values > high_cut] = "high"
    return labels


def prepare_data() -> pd.DataFrame:
    desc = pd.read_csv(DESC)
    shift = pd.read_csv(SHIFT)
    matrix = pd.read_csv(MATRIX)
    matrix = matrix[~matrix["is_in_region"]].copy()
    df = matrix.merge(
        desc,
        left_on=["canonical_station_uid", "target_region", "cell5"],
        right_on=["canonical_station_uid", "ar6_region", "cell5"],
        how="left",
    )
    df = df.merge(shift, on=["source_region", "target_region"], how="left")
    df = df[df["mae_out_minus_in"].notna()].copy()
    df["risk_class"] = risk_labels(df["mae_out_minus_in"])
    return df


def feature_matrix(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    x = df[cols].replace([np.inf, -np.inf], np.nan)
    return x.fillna(x.median(numeric_only=True))


def evaluate(df: pd.DataFrame, cols: list[str], feature_set: str, cv_kind: str) -> tuple[list[dict], pd.DataFrame]:
    x = feature_matrix(df, cols)
    y = pd.Categorical(df["risk_class"], categories=LABEL_ORDER, ordered=True)
    y_codes = y.codes
    y_labels = np.array(y.astype(str))

    if cv_kind == "leave_target_region_out":
        cv = LeaveOneGroupOut()
        groups = df["target_region"].to_numpy()
    elif cv_kind == "group_by_cell":
        n_splits = min(5, df["cell5"].nunique())
        cv = GroupKFold(n_splits=n_splits)
        groups = df["cell5"].to_numpy()
    else:
        raise ValueError(cv_kind)

    logreg = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=2000, class_weight="balanced", multi_class="auto"),
    )
    rf = RandomForestClassifier(
        n_estimators=500,
        min_samples_leaf=20,
        class_weight="balanced_subsample",
        random_state=20260523,
        n_jobs=-1,
    )

    rows = []
    pred_out = df[
        [
            "canonical_station_uid",
            "source_region",
            "target_region",
            "cell5",
            "mae_out_minus_in",
            "risk_class",
        ]
    ].copy()

    for model_name, model in [("logistic", logreg), ("random_forest", rf)]:
        proba = cross_val_predict(model, x, y_codes, cv=cv, groups=groups, method="predict_proba")
        # Some folds can miss a class in pathological settings; align if needed.
        if proba.shape[1] != len(LABEL_ORDER):
            aligned = np.zeros((len(df), len(LABEL_ORDER)))
            aligned[:, : proba.shape[1]] = proba
            proba = aligned
        pred_code = np.argmax(proba, axis=1)
        pred_label = np.array(LABEL_ORDER)[pred_code]
        rows.append(
            {
                "feature_set": feature_set,
                "cv_kind": cv_kind,
                "model": model_name,
                "n": len(df),
                "n_features": len(cols),
                "log_loss": log_loss(y_codes, proba, labels=[0, 1, 2]),
                "balanced_accuracy": balanced_accuracy_score(y_labels, pred_label),
                "macro_f1": f1_score(y_labels, pred_label, average="macro"),
                "brier_high": brier_score_loss((y_labels == "high").astype(int), proba[:, 2]),
            }
        )
        prefix = f"{feature_set}_{cv_kind}_{model_name}"
        for i, lab in enumerate(LABEL_ORDER):
            pred_out[f"{prefix}_p_{lab}"] = proba[:, i]
        pred_out[f"{prefix}_pred"] = pred_label

    return rows, pred_out


def recommendation(row: pd.Series) -> str:
    p_high = row["p_high"]
    p_safe = row["p_safe"]
    if p_high >= 0.5:
        return "retrain"
    if p_high >= 0.25 or p_safe < 0.4:
        return "adapt"
    return "deploy"


def main() -> None:
    df = prepare_data()
    feature_sets = {
        "physical_knowledge": PHYSICAL_COLS,
        "generic_shift": SHIFT_COLS,
        "physical_plus_shift": PHYSICAL_COLS + SHIFT_COLS,
    }
    metric_rows = []
    pred_parts = []
    for cv_kind in ["leave_target_region_out", "group_by_cell"]:
        for label, cols in feature_sets.items():
            rows, preds = evaluate(df, cols, label, cv_kind)
            metric_rows.extend(rows)
            pred_parts.append(preds)

    metrics = pd.DataFrame(metric_rows)
    metrics.to_csv(OUT_METRICS, index=False)

    key = [
        "canonical_station_uid",
        "source_region",
        "target_region",
        "cell5",
        "mae_out_minus_in",
        "risk_class",
    ]
    pred = pred_parts[0]
    for part in pred_parts[1:]:
        pred = pred.merge(part, on=key, how="left")
    pred.to_csv(OUT_PRED, index=False)

    # Decision layer uses the strongest KBS setting from the light full-matrix comparison:
    # combined features, group-by-cell, random forest.
    prefix = "physical_plus_shift_group_by_cell_random_forest"
    decision = pred[
        [
            "canonical_station_uid",
            "source_region",
            "target_region",
            "cell5",
            "mae_out_minus_in",
            "risk_class",
            f"{prefix}_p_safe",
            f"{prefix}_p_moderate",
            f"{prefix}_p_high",
            f"{prefix}_pred",
        ]
    ].rename(
        columns={
            f"{prefix}_p_safe": "p_safe",
            f"{prefix}_p_moderate": "p_moderate",
            f"{prefix}_p_high": "p_high",
            f"{prefix}_pred": "predicted_risk_class",
        }
    )
    decision["recommendation"] = decision.apply(recommendation, axis=1)
    decision.to_csv(OUT_DECISIONS, index=False)

    decision_pair = (
        decision.groupby(["source_region", "target_region"])
        .agg(
            n=("canonical_station_uid", "nunique"),
            mean_p_safe=("p_safe", "mean"),
            mean_p_moderate=("p_moderate", "mean"),
            mean_p_high=("p_high", "mean"),
            retrain_rate=("recommendation", lambda s: float(np.mean(s == "retrain"))),
            adapt_rate=("recommendation", lambda s: float(np.mean(s == "adapt"))),
            deploy_rate=("recommendation", lambda s: float(np.mean(s == "deploy"))),
            mean_observed_degradation=("mae_out_minus_in", "mean"),
        )
        .reset_index()
    )

    risk_counts = (
        decision.groupby(["source_region", "target_region", "recommendation"])
        .size()
        .reset_index(name="count")
    )

    lines = [
        "# Transfer risk decision layer report",
        "",
        "Target:",
        "",
        "- risk classes derived from `mae_out_minus_in`.",
        "- safe: degradation <= 0.",
        "- moderate: positive degradation up to the 75th percentile of positive degradation.",
        "- high: above that threshold.",
        "",
        "Feature sets:",
        "",
        "- physical knowledge;",
        "- generic shift;",
        "- physical plus shift.",
        "",
        "Validation:",
        "",
        "- leave-target-region-out;",
        "- group-by-cell.",
        "",
        "Decision policy:",
        "",
        "- `retrain` if p_high >= 0.5.",
        "- `adapt` if p_high >= 0.25 or p_safe < 0.4.",
        "- `deploy` otherwise.",
        "",
        "The current decision table uses physical_plus_shift + random forest + group-by-cell.",
        "",
        "## Classifier metrics",
        "",
        metrics.to_markdown(index=False),
        "",
        "## Pair-level decision summary",
        "",
        decision_pair.to_markdown(index=False),
        "",
        "## Recommendation counts",
        "",
        risk_counts.to_markdown(index=False),
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")

    print(f"wrote {OUT_METRICS}")
    print(f"wrote {OUT_PRED}")
    print(f"wrote {OUT_DECISIONS}")
    print(f"wrote {REPORT}")
    print(metrics.to_string(index=False))
    print(decision_pair.to_string(index=False))


if __name__ == "__main__":
    main()

