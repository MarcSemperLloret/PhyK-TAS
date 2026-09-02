"""Exploratory action-value policy on the locked 2020--2022 development block.

The script deliberately uses only source/target descriptors computed from the
pre-deployment training period.  It never reads the reserved 2023--2025
outcomes.  Performance is estimated by leaving one target region out.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV, GroupKFold, LeaveOneGroupOut
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]

ACTION_FILES = (
    ROOT / "realized_actions_dev11_spatial_s1.csv",
    ROOT / "realized_actions_dev11_patchtst_head_s1.csv",
    ROOT / "realized_actions_dev11_graphwavenet_head_s1.csv",
)
SHIFT_FILE = ROOT / "distribution_shift_baselines_all_viable_min100.csv"
PHYSICAL_FILE = ROOT / "physical_descriptors_region_all_viable_min100.csv"
OUT_PRED = ROOT / "realized_action_policy_dev11_predictions.csv"
OUT_FOLDS = ROOT / "realized_action_policy_dev11_folds.csv"
OUT_REPORT = ROOT / "realized_action_policy_dev11_report.md"

ACTIONS = ("deploy", "adapt", "retrain")
PHYSICAL_BASES = (
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
)
ALPHAS = np.logspace(-3, 4, 15)


def load_action_outcomes() -> pd.DataFrame:
    frames = [pd.read_csv(path) for path in ACTION_FILES]
    long = pd.concat(frames, ignore_index=True)
    duplicates = long.duplicated(["model", "source_region", "target_region", "action"])
    if duplicates.any():
        raise ValueError("Duplicate model/source/target/action rows in action outcomes")
    wide = (
        long.pivot(
            index=["model", "source_region", "target_region"],
            columns="action",
            values="mae_2020_2022",
        )
        .reset_index()
        .rename_axis(columns=None)
    )
    missing = [action for action in ACTIONS if action not in wide]
    if missing:
        raise ValueError(f"Missing action outcomes: {missing}")
    if wide[list(ACTIONS)].isna().any().any():
        raise ValueError("Incomplete action outcome table")
    wide["benefit_adapt"] = wide["deploy"] - wide["adapt"]
    wide["benefit_retrain"] = wide["deploy"] - wide["retrain"]
    wide["oracle_action"] = wide[list(ACTIONS)].idxmin(axis=1)
    wide["oracle_mae"] = wide[list(ACTIONS)].min(axis=1)
    return wide


def physical_pair_features(pairs: pd.DataFrame) -> pd.DataFrame:
    physical = pd.read_csv(PHYSICAL_FILE).set_index("ar6_region")
    columns = [f"{base}_mean" for base in PHYSICAL_BASES]
    absent = [column for column in columns if column not in physical]
    if absent:
        raise ValueError(f"Missing physical descriptors: {absent}")

    records: list[dict[str, float | str]] = []
    for pair in pairs[["source_region", "target_region"]].drop_duplicates().itertuples(index=False):
        source = physical.loc[pair.source_region, columns]
        target = physical.loc[pair.target_region, columns]
        record: dict[str, float | str] = {
            "source_region": pair.source_region,
            "target_region": pair.target_region,
        }
        for base, column in zip(PHYSICAL_BASES, columns):
            record[f"phys_source_{base}"] = float(source[column])
            record[f"phys_target_{base}"] = float(target[column])
            delta = float(target[column] - source[column])
            record[f"phys_delta_{base}"] = delta
            record[f"phys_abs_delta_{base}"] = abs(delta)
        records.append(record)
    return pd.DataFrame.from_records(records)


def build_feature_table(outcomes: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    shift = pd.read_csv(SHIFT_FILE)
    physical = physical_pair_features(outcomes)
    data = outcomes.merge(shift, on=["source_region", "target_region"], how="left")
    data = data.merge(physical, on=["source_region", "target_region"], how="left")
    model_dummies = pd.get_dummies(data["model"], prefix="model", dtype=float)
    data = pd.concat([data, model_dummies], axis=1)

    excluded = {
        "model",
        "source_region",
        "target_region",
        *ACTIONS,
        "benefit_adapt",
        "benefit_retrain",
        "oracle_action",
        "oracle_mae",
    }
    features = [column for column in data.columns if column not in excluded]
    if data[features].isna().any().any():
        missing = data[features].columns[data[features].isna().any()].tolist()
        raise ValueError(f"Missing feature values: {missing}")
    return data, features


def fit_predict_logo(data: pd.DataFrame, features: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    logo = LeaveOneGroupOut()
    predictions: list[pd.DataFrame] = []
    fold_rows: list[dict[str, float | str]] = []

    x = data[features].astype(float)
    groups = data["target_region"]
    for train_idx, test_idx in logo.split(x, groups=groups):
        train = data.iloc[train_idx]
        test = data.iloc[test_idx].copy()
        train_groups = train["target_region"]
        held_out = str(test["target_region"].iloc[0])
        inner_cv = GroupKFold(n_splits=train_groups.nunique())

        for outcome in ("benefit_adapt", "benefit_retrain"):
            pipeline = Pipeline(
                [("scale", StandardScaler()), ("ridge", Ridge())]
            )
            search = GridSearchCV(
                pipeline,
                {"ridge__alpha": ALPHAS},
                scoring="neg_mean_absolute_error",
                cv=inner_cv,
                n_jobs=-1,
            )
            search.fit(
                train[features].astype(float),
                train[outcome],
                groups=train_groups,
            )
            test[f"pred_{outcome}"] = search.predict(test[features].astype(float))
            fold_rows.append(
                {
                    "held_out_target": held_out,
                    "outcome": outcome,
                    "best_alpha": float(search.best_params_["ridge__alpha"]),
                    "inner_cv_mae": float(-search.best_score_),
                }
            )
        predictions.append(test)

    pred = pd.concat(predictions, ignore_index=True)
    predicted_benefits = np.column_stack(
        [
            np.zeros(len(pred)),
            pred["pred_benefit_adapt"].to_numpy(),
            pred["pred_benefit_retrain"].to_numpy(),
        ]
    )
    chosen_idx = predicted_benefits.argmax(axis=1)
    pred["policy_action"] = np.asarray(ACTIONS, dtype=object)[chosen_idx]
    action_mae = pred[list(ACTIONS)].to_numpy()
    pred["policy_mae"] = action_mae[np.arange(len(pred)), chosen_idx]
    pred["policy_regret"] = pred["policy_mae"] - pred["oracle_mae"]
    pred["policy_normalized_regret"] = pred["policy_regret"] / pred["oracle_mae"].clip(lower=1e-12)
    pred["policy_correct"] = pred["policy_action"] == pred["oracle_action"]
    return pred, pd.DataFrame(fold_rows)


def policy_metrics(pred: pd.DataFrame, label: str, mae_column: str, action_column: str | None = None) -> dict[str, float | str]:
    regret = pred[mae_column] - pred["oracle_mae"]
    normalized = regret / pred["oracle_mae"].clip(lower=1e-12)
    if action_column is None:
        correct = pred["oracle_action"].eq(label).mean()
    else:
        correct = pred[action_column].eq(pred["oracle_action"]).mean()
    return {
        "policy": label,
        "mean_mae": float(pred[mae_column].mean()),
        "mean_regret": float(regret.mean()),
        "median_regret": float(regret.median()),
        "mean_normalized_regret": float(normalized.mean()),
        "oracle_action_accuracy": float(correct),
    }


def make_report(pred: pd.DataFrame, folds: pd.DataFrame, features: list[str]) -> str:
    policies = [
        policy_metrics(pred, "action-value ridge", "policy_mae", "policy_action"),
        *(policy_metrics(pred, action, action) for action in ACTIONS),
    ]
    metrics = pd.DataFrame(policies).sort_values("mean_regret")
    counts = pred["policy_action"].value_counts().reindex(ACTIONS, fill_value=0)
    oracle_counts = pred["oracle_action"].value_counts().reindex(ACTIONS, fill_value=0)
    by_target = (
        pred.groupby("target_region", as_index=False)
        .agg(
            n_pairs=("model", "size"),
            mean_policy_regret=("policy_regret", "mean"),
            median_policy_regret=("policy_regret", "median"),
            action_accuracy=("policy_correct", "mean"),
        )
        .sort_values("target_region")
    )

    def md_table(frame: pd.DataFrame, decimals: int = 6) -> str:
        formatted = frame.copy()
        for column in formatted.select_dtypes(include=[np.number]).columns:
            formatted[column] = formatted[column].map(lambda value: f"{value:.{decimals}f}")
        header = "| " + " | ".join(formatted.columns) + " |"
        separator = "|" + "|".join(["---"] * len(formatted.columns)) + "|"
        rows = ["| " + " | ".join(map(str, row)) + " |" for row in formatted.to_numpy()]
        return "\n".join([header, separator, *rows])

    lines = [
        "# Desarrollo de la politica de acciones realizadas",
        "",
        "**Bloque evaluado:** 2020-2022 (desarrollo).  ",
        "**Bloque confirmatorio:** 2023-2025 no abierto.  ",
        f"**Validacion externa interna:** leave-one-target-region-out ({pred['target_region'].nunique()} folds).  ",
        f"**Muestra:** {len(pred)} combinaciones modelo/source/target.  ",
        f"**Predictores:** {len(features)} rasgos pre-deployment de shift fisico/climatico y familia de modelo.",
        "",
        "## Comparacion de politicas",
        "",
        md_table(metrics),
        "",
        "El regret es la diferencia de MAE respecto a la mejor accion realizada para cada par. Un valor menor es mejor.",
        "",
        "## Acciones elegidas",
        "",
        f"Politica ridge: deploy={counts['deploy']}, adapt={counts['adapt']}, retrain={counts['retrain']}.  ",
        f"Oraculo observado: deploy={oracle_counts['deploy']}, adapt={oracle_counts['adapt']}, retrain={oracle_counts['retrain']}.",
        "",
        "## Resultado por target retenido",
        "",
        md_table(by_target),
        "",
        "## Diagnostico",
        "",
    ]
    ridge = metrics.loc[metrics["policy"] == "action-value ridge"].iloc[0]
    retrain = metrics.loc[metrics["policy"] == "retrain"].iloc[0]
    delta = float(ridge["mean_regret"] - retrain["mean_regret"])
    if delta < 0:
        lines.append(
            f"La politica action-value reduce el regret medio frente a always-retrain en {-delta:.6f} MAE. "
            "Es una senal exploratoria favorable para congelar el sistema y pasar al bloque confirmatorio."
        )
    else:
        lines.append(
            f"La politica action-value no supera always-retrain: su regret medio es {delta:.6f} MAE mayor. "
            "No hay base para abrir el bloque confirmatorio con esta politica; primero debe revisarse el diseno sin usar 2023-2025."
        )
    lines.extend(
        [
            "",
            "Esta prueba no incorpora costes elegidos post hoc. Evalua solo calidad predictiva y utiliza rasgos calculados antes del periodo de despliegue. No constituye evidencia confirmatoria ni debe presentarse como resultado principal sin la evaluacion 2023-2025 previamente congelada.",
            "",
            "## Hiperparametros por fold",
            "",
            md_table(folds),
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    outcomes = load_action_outcomes()
    data, features = build_feature_table(outcomes)
    predictions, folds = fit_predict_logo(data, features)
    predictions.to_csv(OUT_PRED, index=False)
    folds.to_csv(OUT_FOLDS, index=False)
    OUT_REPORT.write_text(make_report(predictions, folds, features), encoding="utf-8")
    print(OUT_PRED)
    print(OUT_FOLDS)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()
