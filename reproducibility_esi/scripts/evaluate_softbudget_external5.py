"""Evaluate the frozen Soft-Budget learner on five untouched external regions."""

from __future__ import annotations

import importlib.util
import json
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd
from lightgbm import LGBMRegressor
from scipy.stats import wilcoxon
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV, GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]
SOURCE_REGIONS = ("NEU", "WCE", "WNA", "ENA", "CNA", "SAU", "MED", "EAU", "NWN", "NCA", "EAS")
TARGET_REGIONS = ("CAU", "NAU", "NEN", "ESB", "RFE")
MODELS = ("spatial_knn_ridge", "patchtst_small", "graphwavenet_transfer")
ACTION_FILES = (
    ROOT / "realized_actions_softbudget_external5_spatial_s1.csv",
    ROOT / "realized_actions_softbudget_external5_patchtst_head_s1.csv",
    ROOT / "realized_actions_softbudget_external5_graphwavenet_head_s1.csv",
)
SHIFT_FILE = ROOT / "distribution_shift_baselines_softbudget_external16.csv"
PHYSICAL_FILE = ROOT / "physical_descriptors_region_softbudget_external16.csv"


def import_local(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def training_and_external_features():
    policy = import_local("action_policy", ROOT / "scripts" / "build_realized_action_policy_dev.py")
    train, features = policy.build_feature_table(policy.load_action_outcomes())
    keys = pd.DataFrame(
        product(MODELS, SOURCE_REGIONS, TARGET_REGIONS),
        columns=["model", "source_region", "target_region"],
    )
    shift = pd.read_csv(SHIFT_FILE)
    policy.PHYSICAL_FILE = PHYSICAL_FILE
    physical = policy.physical_pair_features(keys)
    external = keys.merge(shift, on=["source_region", "target_region"], how="left")
    external = external.merge(physical, on=["source_region", "target_region"], how="left")
    dummies = pd.get_dummies(external["model"], prefix="model", dtype=float)
    external = pd.concat([external, dummies], axis=1)
    missing = [column for column in features if column not in external]
    if missing:
        raise ValueError(f"External feature columns missing: {missing}")
    if external[features].isna().any().any() or len(external) != 165:
        raise ValueError("Invalid external feature table")
    return train, external, features


def neural_predictions(train, external, features, kind: str):
    ranker = import_local(
        f"ranker_{kind}", ROOT / "scripts" / "build_budget_integrated_action_ranker.py"
    )
    gain = train["benefit_retrain"].to_numpy(dtype=np.float32) - np.maximum(
        0.0, train["benefit_adapt"].to_numpy(dtype=np.float32)
    )
    rank_weight = 0.0 if kind == "pointwise" else 1.0
    members = []
    for member in range(3):
        members.append(
            ranker.fit_member(
                train[features].to_numpy(dtype=np.float32),
                train["benefit_adapt"].to_numpy(dtype=np.float32),
                gain,
                train["target_region"].to_numpy(),
                external[features].to_numpy(dtype=np.float32),
                rank_kind=kind,
                rank_weight=rank_weight,
                temperature=0.5,
                seed=2026 + member,
                epochs=300,
                hidden=128,
                dropout=0.10,
            )
        )
    stack = np.stack(members, axis=0)
    return stack[:, :, 0].mean(axis=0), stack[:, :, 1].mean(axis=0)


def tabicl_predictions(train, external, features):
    from tabicl import TabICLRegressor

    output = {}
    for offset, outcome in enumerate(("benefit_adapt", "benefit_retrain")):
        model = TabICLRegressor(
            n_estimators=4,
            checkpoint_version="tabicl-regressor-v2-20260212.ckpt",
            device="cuda",
            random_state=2026 + offset,
            verbose=False,
        )
        model.fit(
            train[features].to_numpy(dtype=np.float32),
            train[outcome].to_numpy(dtype=np.float32),
        )
        output[outcome] = model.predict(external[features].to_numpy(dtype=np.float32))
    score = output["benefit_retrain"] - np.maximum(0.0, output["benefit_adapt"])
    return output["benefit_adapt"], score


def tuned_predictions(train, external, features, learner: str):
    groups = train["target_region"]
    cv = GroupKFold(n_splits=groups.nunique())
    output = {}
    for outcome in ("benefit_adapt", "benefit_retrain"):
        if learner == "ridge":
            estimator = Pipeline([("scale", StandardScaler()), ("model", Ridge())])
            grid = {"model__alpha": np.logspace(-3, 4, 15)}
        elif learner == "extratrees":
            estimator = ExtraTreesRegressor(random_state=2026, n_jobs=1)
            grid = {
                "n_estimators": [300],
                "min_samples_leaf": [2, 5, 10],
                "max_features": [0.5, 1.0],
            }
        elif learner == "lightgbm":
            estimator = LGBMRegressor(
                random_state=2026,
                n_jobs=1,
                verbosity=-1,
                deterministic=True,
                force_col_wise=True,
            )
            grid = {
                "n_estimators": [100, 250],
                "num_leaves": [5, 10],
                "learning_rate": [0.03, 0.08],
                "min_child_samples": [10, 30],
                "reg_lambda": [1.0],
            }
        else:
            raise ValueError(learner)
        search = GridSearchCV(
            estimator,
            grid,
            scoring="neg_mean_absolute_error",
            cv=cv,
            n_jobs=-1,
        )
        search.fit(train[features], train[outcome], groups=groups)
        output[outcome] = search.predict(external[features])
    score = output["benefit_retrain"] - np.maximum(0.0, output["benefit_adapt"])
    return output["benefit_adapt"], score


def all_predictions(train, external, features):
    rows = []
    configs = {}
    for kind in ("pointwise", "pairwise", "softbudget"):
        configs[kind] = neural_predictions(train, external, features, kind)
        print(f"fit {kind}", flush=True)
    configs["tabicl_v2"] = tabicl_predictions(train, external, features)
    print("fit tabicl_v2", flush=True)
    for learner in ("ridge", "extratrees", "lightgbm"):
        configs[learner] = tuned_predictions(train, external, features, learner)
        print(f"fit {learner}", flush=True)
    for learner, (adapt, score) in configs.items():
        frame = external[["model", "source_region", "target_region"]].copy()
        frame["learner"] = learner
        frame["pred_benefit_adapt"] = adapt
        frame["predicted_gain"] = score
        rows.append(frame)
    pred = pd.concat(rows, ignore_index=True)
    ridge = pred[pred["learner"].eq("ridge")][
        ["model", "source_region", "target_region", "pred_benefit_adapt"]
    ].rename(columns={"pred_benefit_adapt": "ridge_adapt"})
    shift = external[[
        "model", "source_region", "target_region", "mmd_rbf_precip",
        "wasserstein_precip", "region_centroid_distance_deg", "shift_mean_abs",
        "kl_source_to_target",
    ]].merge(ridge, on=["model", "source_region", "target_region"])
    for label, column in {
        "mmd": "mmd_rbf_precip",
        "wasserstein": "wasserstein_precip",
        "distance": "region_centroid_distance_deg",
        "mean_shift": "shift_mean_abs",
        "kl_source_target": "kl_source_to_target",
    }.items():
        frame = shift[["model", "source_region", "target_region"]].copy()
        frame["learner"] = label
        frame["pred_benefit_adapt"] = shift["ridge_adapt"].to_numpy()
        frame["predicted_gain"] = shift[column].to_numpy()
        pred = pd.concat([pred, frame], ignore_index=True)
    return pred


def load_outcomes():
    long = pd.concat([pd.read_csv(path) for path in ACTION_FILES], ignore_index=True)
    keys = ["model", "source_region", "target_region"]
    if len(long) != 495 or long.duplicated(keys + ["action"]).any():
        raise ValueError(f"Expected 495 unique action rows, found {len(long)}")
    if long["mae_2023_2025"].isna().any():
        raise ValueError("Missing external MAE")
    wide = (
        long.pivot(index=keys, columns="action", values="mae_2023_2025")
        .reset_index()
        .rename_axis(columns=None)
    )
    if len(wide) != 165 or wide[["deploy", "adapt", "retrain"]].isna().any().any():
        raise ValueError("Incomplete external action triplets")
    return wide


def curves_and_auc(pred, outcomes):
    keys = ["model", "source_region", "target_region"]
    data = pred.merge(outcomes, on=keys, validate="many_to_one")
    data["cheap_mae"] = np.where(
        data["pred_benefit_adapt"] > 0, data["adapt"], data["deploy"]
    )
    data["realized_gain"] = data["cheap_mae"] - data["retrain"]
    rows = []
    for (learner, target), group in data.groupby(["learner", "target_region"], sort=True):
        group = group.reset_index(drop=True)
        n = len(group)
        cheap = group["cheap_mae"].to_numpy()
        retrain = group["retrain"].to_numpy()
        orders = {
            "policy": group["predicted_gain"].to_numpy().argsort()[::-1],
            "oracle": group["realized_gain"].to_numpy().argsort()[::-1],
        }
        for budget in range(n + 1):
            for policy, order in orders.items():
                mae = cheap.copy()
                mae[order[:budget]] = retrain[order[:budget]]
                rows.append({
                    "learner": learner, "target_region": target,
                    "budget_retrains": budget, "policy": policy,
                    "mean_mae": float(mae.mean()),
                })
            rows.append({
                "learner": learner, "target_region": target,
                "budget_retrains": budget, "policy": "random",
                "mean_mae": float(cheap.mean() + (budget / n) * (retrain - cheap).mean()),
            })
    curve = pd.DataFrame(rows)
    auc = (
        curve.groupby(["learner", "target_region", "policy"], as_index=False)["mean_mae"]
        .mean().rename(columns={"mean_mae": "budget_curve_auc"})
    )
    wide = auc.pivot(index=["learner", "target_region"], columns="policy", values="budget_curve_auc").reset_index()
    wide["difference_vs_random"] = wide["policy"] - wide["random"]
    wide["gap_closed"] = (wide["random"] - wide["policy"]) / (wide["random"] - wide["oracle"])
    return data, curve, wide


def family_differences(data):
    rows = []
    subset = data[data["learner"].isin(["softbudget", "pointwise"])]
    for (learner, target, model), group in subset.groupby(["learner", "target_region", "model"]):
        group = group.reset_index(drop=True)
        n = len(group); cheap = group["cheap_mae"].to_numpy(); retrain = group["retrain"].to_numpy()
        order = group["predicted_gain"].to_numpy().argsort()[::-1]
        values = []
        for budget in range(n + 1):
            mae = cheap.copy(); mae[order[:budget]] = retrain[order[:budget]]; values.append(mae.mean())
        rows.append({"learner": learner, "target_region": target, "model": model, "auc": float(np.mean(values))})
    frame = pd.DataFrame(rows)
    wide = frame.pivot(index=["target_region", "model"], columns="learner", values="auc").reset_index()
    wide["soft_minus_pointwise"] = wide["softbudget"] - wide["pointwise"]
    return wide


def report_and_summary(auc, family):
    summary = auc.groupby("learner", as_index=False).agg(
        mean_budget_curve_auc=("policy", "mean"),
        mean_random_auc=("random", "mean"),
        mean_oracle_auc=("oracle", "mean"),
        mean_difference_vs_random=("difference_vs_random", "mean"),
        targets_better_than_random=("difference_vs_random", lambda x: int((x < 0).sum())),
        mean_gap_closed=("gap_closed", "mean"),
    ).sort_values("mean_budget_curve_auc")
    target = auc.pivot(index="target_region", columns="learner", values="policy")
    diff = target["softbudget"] - target["pointwise"]
    p_value = float(wilcoxon(diff, alternative="less").pvalue)
    family_summary = family.groupby("model", as_index=False).agg(
        mean_soft_minus_pointwise=("soft_minus_pointwise", "mean"),
        targets_soft_better=("soft_minus_pointwise", lambda x: int((x < 0).sum())),
        worst_difference=("soft_minus_pointwise", "max"),
    )
    tabicl_mean = float(summary.loc[summary["learner"].eq("tabicl_v2"), "mean_budget_curve_auc"].iloc[0])
    soft_mean = float(summary.loc[summary["learner"].eq("softbudget"), "mean_budget_curve_auc"].iloc[0])
    conditions = {
        "favorable_mean": bool(diff.mean() < 0),
        "favorable_median": bool(diff.median() < 0),
        "all_5_targets": bool((diff < 0).all()),
        "wilcoxon_p_equals_0_03125": bool(np.isclose(p_value, 0.03125)),
        "all_family_means_favorable": bool((family_summary["mean_soft_minus_pointwise"] < 0).all()),
        "not_worse_than_tabicl_mean": bool(soft_mean <= tabicl_mean),
        "complete_495_actions": True,
    }
    go = bool(all(conditions.values()))
    result = {
        "verdict": "GO" if go else "NO-GO",
        "softbudget_minus_pointwise_mean": float(diff.mean()),
        "softbudget_minus_pointwise_median": float(diff.median()),
        "targets_softbudget_better": int((diff < 0).sum()),
        "targets_total": 5,
        "wilcoxon_one_sided_p": p_value,
        "conditions": conditions,
    }
    lines = [
        "# Soft-Budget external-region validation", "",
        "**Protocol:** `SOFT_BUDGET_EXTERNAL5_PROTOCOL.md`.",
        "**Targets:** CAU, NAU, NEN, ESB, RFE.",
        "**Actions:** 495 complete deploy/adapt/retrain rows.", "",
        f"## Verdict: {result['verdict']}", "",
        f"Soft-Budget minus matched pointwise mean AUC: {diff.mean():.6f}.",
        f"Median paired difference: {diff.median():.6f}.",
        f"Targets favorable: {(diff < 0).sum()}/5.",
        f"Exact one-sided paired Wilcoxon p={p_value:.5f}.", "",
        "## Learner summary", "", summary.to_markdown(index=False, floatfmt=".6f"), "",
        "## Target AUC", "", target.reset_index().to_markdown(index=False, floatfmt=".6f"), "",
        "## Matched family ablation", "", family_summary.to_markdown(index=False, floatfmt=".6f"), "",
        "## Frozen success conditions", "",
        *[f"- {'PASS' if value else 'FAIL'}: {key}" for key, value in conditions.items()], "",
    ]
    return summary, family_summary, result, "\n".join(lines)


def main():
    train, external, features = training_and_external_features()
    pred = all_predictions(train, external, features)
    outcomes = load_outcomes()
    data, curve, auc = curves_and_auc(pred, outcomes)
    family = family_differences(data)
    summary, family_summary, result, report = report_and_summary(auc, family)
    pred.to_csv(ROOT / "softbudget_external5_predictions.csv", index=False)
    curve.to_csv(ROOT / "softbudget_external5_budget_curve.csv", index=False)
    auc.to_csv(ROOT / "softbudget_external5_target_auc.csv", index=False)
    family.to_csv(ROOT / "softbudget_external5_family_auc.csv", index=False)
    summary.to_csv(ROOT / "softbudget_external5_summary.csv", index=False)
    (ROOT / "softbudget_external5_result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    (ROOT / "softbudget_external5_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
