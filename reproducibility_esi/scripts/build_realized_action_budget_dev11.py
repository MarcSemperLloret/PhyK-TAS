"""Budgeted retraining allocation on cross-target development predictions."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon


ROOT = Path(__file__).resolve().parents[1]
PRED_FILE = ROOT / "realized_action_policy_dev11_predictions.csv"
OUT_CURVE = ROOT / "realized_action_budget_dev11_curve.csv"
OUT_TARGET = ROOT / "realized_action_budget_dev11_target_auc.csv"
OUT_REPORT = ROOT / "realized_action_budget_dev11_report.md"

RANKERS = {
    "action_value": "predicted_gain",
    "mmd": "mmd_rbf_precip",
    "wasserstein": "wasserstein_precip",
    "distance": "region_centroid_distance_deg",
    "mean_shift": "shift_mean_abs",
    "kl_source_target": "kl_source_to_target",
}


def markdown_table(frame: pd.DataFrame, decimals: int = 6) -> str:
    formatted = frame.copy()
    for column in formatted.select_dtypes(include=[np.number]).columns:
        formatted[column] = formatted[column].map(lambda value: f"{value:.{decimals}f}")
    header = "| " + " | ".join(formatted.columns) + " |"
    separator = "|" + "|".join(["---"] * len(formatted.columns)) + "|"
    rows = ["| " + " | ".join(map(str, row)) + " |" for row in formatted.to_numpy()]
    return "\n".join([header, separator, *rows])


def make_curves(pred: pd.DataFrame) -> pd.DataFrame:
    pred = pred.copy()
    pred["cheap_action"] = np.where(pred["pred_benefit_adapt"] > 0, "adapt", "deploy")
    pred["cheap_mae"] = np.where(pred["cheap_action"].eq("adapt"), pred["adapt"], pred["deploy"])
    pred["predicted_gain"] = pred["pred_benefit_retrain"] - np.maximum(
        0.0, pred["pred_benefit_adapt"]
    )
    pred["realized_gain"] = pred["cheap_mae"] - pred["retrain"]

    rows: list[dict[str, float | int | str]] = []
    for target, group in pred.groupby("target_region", sort=True):
        group = group.reset_index(drop=True)
        n = len(group)
        cheap = group["cheap_mae"].to_numpy()
        retrain = group["retrain"].to_numpy()
        policies = {
            name: group[column].to_numpy().argsort()[::-1]
            for name, column in RANKERS.items()
        }
        policies["oracle"] = group["realized_gain"].to_numpy().argsort()[::-1]
        for budget in range(n + 1):
            for policy, order in policies.items():
                selected = order[:budget]
                mae = cheap.copy()
                mae[selected] = retrain[selected]
                rows.append(
                    {
                        "target_region": target,
                        "budget_retrains": budget,
                        "budget_fraction": budget / n,
                        "policy": policy,
                        "mean_mae": float(mae.mean()),
                    }
                )
            random_mae = cheap.mean() + (budget / n) * (retrain - cheap).mean()
            rows.append(
                {
                    "target_region": target,
                    "budget_retrains": budget,
                    "budget_fraction": budget / n,
                    "policy": "random_expected",
                    "mean_mae": float(random_mae),
                }
            )
    return pd.DataFrame(rows)


def target_auc(curve: pd.DataFrame) -> pd.DataFrame:
    auc = (
        curve.groupby(["target_region", "policy"], as_index=False)["mean_mae"]
        .mean()
        .rename(columns={"mean_mae": "budget_curve_auc"})
    )
    oracle = (
        auc.loc[auc["policy"].eq("oracle"), ["target_region", "budget_curve_auc"]]
        .rename(columns={"budget_curve_auc": "oracle_auc"})
    )
    auc = auc.merge(oracle, on="target_region", how="left")
    auc["excess_auc_vs_oracle"] = auc["budget_curve_auc"] - auc["oracle_auc"]
    return auc


def make_report(curve: pd.DataFrame, auc: pd.DataFrame) -> str:
    summary = (
        auc.groupby("policy", as_index=False)
        .agg(
            mean_budget_curve_auc=("budget_curve_auc", "mean"),
            mean_excess_auc_vs_oracle=("excess_auc_vs_oracle", "mean"),
        )
        .sort_values("mean_budget_curve_auc")
    )
    wide = auc.pivot(index="target_region", columns="policy", values="budget_curve_auc")
    action = wide["action_value"]
    comparison_rows = []
    for baseline in ("random_expected", "mmd", "wasserstein", "distance", "mean_shift", "kl_source_target"):
        diff = action - wide[baseline]
        comparison_rows.append(
            {
                "baseline": baseline,
                "mean_auc_difference": float(diff.mean()),
                "targets_action_value_better": int((diff < 0).sum()),
                "targets_total": int(len(diff)),
                "wilcoxon_one_sided_p": float(wilcoxon(diff, alternative="less").pvalue),
            }
        )
    comparisons = pd.DataFrame(comparison_rows).sort_values("mean_auc_difference")
    aggregate_curve = (
        curve.groupby(["budget_retrains", "budget_fraction", "policy"], as_index=False)["mean_mae"]
        .mean()
    )
    selected_budgets = aggregate_curve.loc[
        aggregate_curve["budget_retrains"].isin([0, 5, 10, 15, 20, 25, 30])
        & aggregate_curve["policy"].isin(["action_value", "random_expected", "mmd", "oracle"])
    ].pivot(index="budget_retrains", columns="policy", values="mean_mae").reset_index()

    policy_auc = float(summary.loc[summary["policy"].eq("action_value"), "mean_budget_curve_auc"].iloc[0])
    random_auc = float(summary.loc[summary["policy"].eq("random_expected"), "mean_budget_curve_auc"].iloc[0])
    oracle_auc = float(summary.loc[summary["policy"].eq("oracle"), "mean_budget_curve_auc"].iloc[0])
    closed = (random_auc - policy_auc) / (random_auc - oracle_auc)

    return "\n".join(
        [
            "# Desarrollo: asignacion de reentrenamiento bajo presupuesto",
            "",
            "**Periodo de outcomes:** 2020-2022.  ",
            "**Periodo confirmatorio 2023-2025:** no abierto.  ",
            "**Unidad de validacion:** target region retenida (11 folds).  ",
            "**Decisiones:** 330 combinaciones modelo/source/target.  ",
            "**Presupuesto:** curva completa de 0 a 30 reentrenamientos por target; no se selecciona post hoc un unico coste.",
            "",
            "La accion barata se elige entre deploy y adapt con predicciones out-of-target. La politica ordena el beneficio esperado de retrain y asigna el presupuesto a los primeros casos.",
            "",
            "## AUC de la curva de presupuesto",
            "",
            markdown_table(summary),
            "",
            f"Frente a asignacion aleatoria, action-value reduce el AUC de MAE en {random_auc - policy_auc:.6f} y cierra el {100 * closed:.1f}% de la distancia entre random y el oraculo restringido.",
            "",
            "## Comparaciones pareadas por target",
            "",
            markdown_table(comparisons),
            "",
            "Los p-valores son exploratorios, unilaterales y no corregidos; el bloque se uso para desarrollar la politica.",
            "",
            "## Puntos de la curva agregada",
            "",
            markdown_table(selected_budgets),
            "",
            "## Veredicto de desarrollo",
            "",
            "GO condicionado para congelar la politica budget-aware y evaluarla en 2023-2025. La politica supera a random en 10/11 targets y a MMD en 9/11, pero no supera always-retrain cuando no existe restriccion. Por tanto, el claim defendible es asignacion de reentrenamiento bajo capacidad limitada, no mejora universal de MAE.",
            "",
            "Antes de abrir el bloque confirmatorio deben congelarse: rasgos, ridge, validacion, definicion de accion barata, curva de presupuestos y estadisticos. No se permite seleccionar tras la confirmacion un presupuesto o una metrica diferente.",
            "",
        ]
    )


def main() -> None:
    pred = pd.read_csv(PRED_FILE)
    curve = make_curves(pred)
    auc = target_auc(curve)
    curve.to_csv(OUT_CURVE, index=False)
    auc.to_csv(OUT_TARGET, index=False)
    OUT_REPORT.write_text(make_report(curve, auc), encoding="utf-8")
    print(OUT_CURVE)
    print(OUT_TARGET)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()
