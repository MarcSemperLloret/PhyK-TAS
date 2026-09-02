"""Apply the frozen budget-aware policy to 2023--2025 outcomes."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon


ROOT = Path(__file__).resolve().parents[1]
DEV_PRED = ROOT / "realized_action_policy_dev11_predictions.csv"
CONFIRM_FILES = (
    ROOT / "realized_actions_confirm_spatial_s1.csv",
    ROOT / "realized_actions_confirm_patchtst_head_s1.csv",
    ROOT / "realized_actions_confirm_graphwavenet_head_s1.csv",
)
OUT_MERGED = ROOT / "realized_action_confirmatory_predictions_outcomes.csv"
OUT_CURVE = ROOT / "realized_action_confirmatory_budget_curve.csv"
OUT_TARGET = ROOT / "realized_action_confirmatory_target_auc.csv"
OUT_REPORT = ROOT / "realized_action_confirmatory_report.md"

KEYS = ["model", "source_region", "target_region"]
RANKERS = {
    "action_value": "predicted_gain",
    "mmd": "mmd_rbf_precip",
    "wasserstein": "wasserstein_precip",
    "distance": "region_centroid_distance_deg",
    "mean_shift": "shift_mean_abs",
    "kl_source_target": "kl_source_to_target",
}


def md_table(frame: pd.DataFrame, decimals: int = 6) -> str:
    formatted = frame.copy()
    for column in formatted.select_dtypes(include=[np.number]).columns:
        formatted[column] = formatted[column].map(lambda value: f"{value:.{decimals}f}")
    header = "| " + " | ".join(formatted.columns) + " |"
    separator = "|" + "|".join(["---"] * len(formatted.columns)) + "|"
    rows = ["| " + " | ".join(map(str, row)) + " |" for row in formatted.to_numpy()]
    return "\n".join([header, separator, *rows])


def holm_adjust(pvalues: pd.Series) -> pd.Series:
    order = np.argsort(pvalues.to_numpy())
    adjusted = np.empty(len(pvalues), dtype=float)
    running = 0.0
    m = len(pvalues)
    raw = pvalues.to_numpy()
    for rank, idx in enumerate(order):
        candidate = min(1.0, (m - rank) * raw[idx])
        running = max(running, candidate)
        adjusted[idx] = running
    return pd.Series(adjusted, index=pvalues.index)


def load_confirmatory() -> pd.DataFrame:
    long = pd.concat([pd.read_csv(path) for path in CONFIRM_FILES], ignore_index=True)
    if len(long) != 990:
        raise ValueError(f"Expected 990 action rows, found {len(long)}")
    if long.duplicated(KEYS + ["action"]).any():
        raise ValueError("Duplicate confirmatory action row")
    if "mae_2023_2025" not in long or long["mae_2023_2025"].isna().any():
        raise ValueError("Missing confirmatory MAE")
    wide = (
        long.pivot(index=KEYS, columns="action", values="mae_2023_2025")
        .reset_index()
        .rename_axis(columns=None)
    )
    if len(wide) != 330 or wide[["deploy", "adapt", "retrain"]].isna().any().any():
        raise ValueError("Incomplete confirmatory decision table")
    return wide


def merge_frozen_predictions(confirm: pd.DataFrame) -> pd.DataFrame:
    dev = pd.read_csv(DEV_PRED)
    if len(dev) != 330 or dev.duplicated(KEYS).any():
        raise ValueError("Invalid frozen development predictions")
    overlap = {"deploy", "adapt", "retrain", "oracle_action", "oracle_mae"}
    keep = [column for column in dev.columns if column not in overlap]
    merged = dev[keep].merge(confirm, on=KEYS, how="outer", validate="one_to_one", indicator=True)
    if not merged["_merge"].eq("both").all():
        raise ValueError("Development/confirmation IDs do not match exactly")
    merged = merged.drop(columns="_merge")
    merged["cheap_action"] = np.where(merged["pred_benefit_adapt"] > 0, "adapt", "deploy")
    merged["cheap_mae"] = np.where(
        merged["cheap_action"].eq("adapt"), merged["adapt"], merged["deploy"]
    )
    merged["predicted_gain"] = merged["pred_benefit_retrain"] - np.maximum(
        0.0, merged["pred_benefit_adapt"]
    )
    merged["realized_gain"] = merged["cheap_mae"] - merged["retrain"]
    merged["oracle_action_confirm"] = merged[["deploy", "adapt", "retrain"]].idxmin(axis=1)
    merged["oracle_mae_confirm"] = merged[["deploy", "adapt", "retrain"]].min(axis=1)
    return merged


def make_curves(data: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, float | int | str]] = []
    for target, group in data.groupby("target_region", sort=True):
        group = group.reset_index(drop=True)
        n = len(group)
        if n != 30:
            raise ValueError(f"Expected 30 decisions for {target}, found {n}")
        cheap = group["cheap_mae"].to_numpy()
        retrain = group["retrain"].to_numpy()
        policies = {
            name: group[column].to_numpy().argsort()[::-1]
            for name, column in RANKERS.items()
        }
        policies["oracle"] = group["realized_gain"].to_numpy().argsort()[::-1]
        for budget in range(n + 1):
            for policy, order in policies.items():
                mae = cheap.copy()
                mae[order[:budget]] = retrain[order[:budget]]
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
    oracle = auc.loc[auc["policy"].eq("oracle"), ["target_region", "budget_curve_auc"]].rename(
        columns={"budget_curve_auc": "oracle_auc"}
    )
    auc = auc.merge(oracle, on="target_region", how="left")
    auc["excess_auc_vs_oracle"] = auc["budget_curve_auc"] - auc["oracle_auc"]
    return auc


def family_diagnostics(data: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (model, target), group in data.groupby(["model", "target_region"], sort=True):
        group = group.reset_index(drop=True)
        n = len(group)
        cheap = group["cheap_mae"].to_numpy()
        retrain = group["retrain"].to_numpy()
        order = group["predicted_gain"].to_numpy().argsort()[::-1]
        policy_auc = np.mean(
            [
                np.where(np.isin(np.arange(n), order[:budget]), retrain, cheap).mean()
                for budget in range(n + 1)
            ]
        )
        random_auc = np.mean(
            [cheap.mean() + (budget / n) * (retrain - cheap).mean() for budget in range(n + 1)]
        )
        rows.append(
            {
                "model": model,
                "target_region": target,
                "action_value_auc": float(policy_auc),
                "random_auc": float(random_auc),
                "difference": float(policy_auc - random_auc),
            }
        )
    detail = pd.DataFrame(rows)
    return (
        detail.groupby("model", as_index=False)
        .agg(
            mean_auc_difference=("difference", "mean"),
            targets_better=("difference", lambda values: int((values < 0).sum())),
            targets_total=("difference", "size"),
            worst_target_difference=("difference", "max"),
        )
        .sort_values("model")
    )


def make_report(data: pd.DataFrame, curve: pd.DataFrame, auc: pd.DataFrame) -> str:
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
    comparisons = []
    baselines = ["random_expected", "mmd", "wasserstein", "distance", "mean_shift", "kl_source_target"]
    for baseline in baselines:
        diff = action - wide[baseline]
        comparisons.append(
            {
                "baseline": baseline,
                "mean_auc_difference": float(diff.mean()),
                "median_auc_difference": float(diff.median()),
                "targets_action_value_better": int((diff < 0).sum()),
                "targets_total": len(diff),
                "wilcoxon_one_sided_p": float(wilcoxon(diff, alternative="less").pvalue),
                "wilcoxon_two_sided_p": float(wilcoxon(diff, alternative="two-sided").pvalue),
            }
        )
    comparisons = pd.DataFrame(comparisons)
    secondary_mask = comparisons["baseline"].ne("random_expected")
    comparisons["holm_adjusted_p"] = np.nan
    comparisons.loc[secondary_mask, "holm_adjusted_p"] = holm_adjust(
        comparisons.loc[secondary_mask, "wilcoxon_one_sided_p"]
    )
    comparisons = comparisons.sort_values("mean_auc_difference")
    # Prespecified primary test is one-sided; the two-sided p-value is reported
    # only as a post-confirmation robustness column and never redefines the
    # GO/NO-GO rule below.

    primary = comparisons.loc[comparisons["baseline"].eq("random_expected")].iloc[0]
    family = family_diagnostics(data)
    no_family_collapse = bool((family["mean_auc_difference"] <= 0).all())
    go = bool(
        primary["wilcoxon_one_sided_p"] < 0.05
        and primary["mean_auc_difference"] < 0
        and primary["targets_action_value_better"] >= 8
        and no_family_collapse
    )

    oracle_counts = data["oracle_action_confirm"].value_counts().reindex(
        ["deploy", "adapt", "retrain"], fill_value=0
    )
    action_summary = []
    for model, group in data.groupby("model"):
        best = group["oracle_action_confirm"].value_counts().reindex(
            ["deploy", "adapt", "retrain"], fill_value=0
        )
        action_summary.append(
            {
                "model": model,
                "adapt_improves_deploy": int((group["adapt"] < group["deploy"]).sum()),
                "n": len(group),
                "best_deploy": int(best["deploy"]),
                "best_adapt": int(best["adapt"]),
                "best_retrain": int(best["retrain"]),
                "mean_adapt_minus_deploy": float((group["adapt"] - group["deploy"]).mean()),
                "mean_retrain_minus_deploy": float((group["retrain"] - group["deploy"]).mean()),
            }
        )
    action_summary = pd.DataFrame(action_summary)

    aggregate_curve = curve.groupby(["budget_retrains", "policy"], as_index=False)["mean_mae"].mean()
    points = aggregate_curve.loc[
        aggregate_curve["budget_retrains"].isin([0, 5, 10, 15, 20, 25, 30])
        & aggregate_curve["policy"].isin(["action_value", "random_expected", "mmd", "oracle"])
    ].pivot(index="budget_retrains", columns="policy", values="mean_mae").reset_index()

    policy_auc = float(summary.loc[summary["policy"].eq("action_value"), "mean_budget_curve_auc"].iloc[0])
    random_auc = float(summary.loc[summary["policy"].eq("random_expected"), "mean_budget_curve_auc"].iloc[0])
    oracle_auc = float(summary.loc[summary["policy"].eq("oracle"), "mean_budget_curve_auc"].iloc[0])
    gap_closed = (random_auc - policy_auc) / (random_auc - oracle_auc)

    verdict = "GO CONFIRMATORIO" if go else "NO-GO CONFIRMATORIO"
    reasons = (
        f"p primario={primary['wilcoxon_one_sided_p']:.6f}; diferencia media={primary['mean_auc_difference']:.6f}; "
        f"targets favorables={int(primary['targets_action_value_better'])}/11; "
        f"sin deterioro medio por familia={no_family_collapse}."
    )
    return "\n".join(
        [
            "# Evaluacion confirmatoria de acciones realizadas",
            "",
            "**Outcomes:** 2023-2025.  ",
            "**Predicciones/rankings:** congelados desde desarrollo 2020-2022.  ",
            "**Targets:** 11; **decisiones:** 330; **acciones realizadas:** 990.  ",
            "**Metrica primaria:** AUC discreto de MAE sobre presupuestos 0-30.",
            "",
            f"## Veredicto: {verdict}",
            "",
            reasons,
            "",
            "## AUC de la curva de presupuesto",
            "",
            md_table(summary),
            "",
            f"Action-value cambia el AUC frente a random en {policy_auc - random_auc:.6f} MAE-AUC y cierra el {100 * gap_closed:.1f}% del gap random-oracle.",
            "",
            "## Test primario y comparaciones secundarias",
            "",
            md_table(comparisons),
            "",
            "El test frente a random es el unico primario. Los p-valores Holm corresponden solo a los cinco baselines shift-only secundarios.",
            "",
            "El test primario preespecificado es unilateral. La columna `wilcoxon_two_sided_p` es una comprobacion de robustez posterior a la confirmacion: no redefine el estimando, no entra en la regla GO/NO-GO y no se corrige por multiplicidad.",
            "",
            "## Diagnostico por familia",
            "",
            md_table(family),
            "",
            "## Heterogeneidad de acciones confirmatorias",
            "",
            md_table(action_summary),
            "",
            f"Oraculo global: deploy={oracle_counts['deploy']}, adapt={oracle_counts['adapt']}, retrain={oracle_counts['retrain']}.",
            "",
            "## Puntos de la curva agregada",
            "",
            md_table(points),
            "",
            "## Interpretacion permitida",
            "",
            "El resultado solo respalda asignacion de capacidad limitada de reentrenamiento si el veredicto es GO. No respalda superioridad frente a always-retrain sin restriccion, mejora universal del forecaster ni novedad arquitectonica.",
            "",
        ]
    )


def main() -> None:
    confirm = load_confirmatory()
    data = merge_frozen_predictions(confirm)
    curve = make_curves(data)
    auc = target_auc(curve)
    data.to_csv(OUT_MERGED, index=False)
    curve.to_csv(OUT_CURVE, index=False)
    auc.to_csv(OUT_TARGET, index=False)
    OUT_REPORT.write_text(make_report(data, curve, auc), encoding="utf-8")
    print(OUT_MERGED)
    print(OUT_CURVE)
    print(OUT_TARGET)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()
