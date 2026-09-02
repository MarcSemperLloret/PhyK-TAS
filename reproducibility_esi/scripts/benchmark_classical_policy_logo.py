"""Persist nested leave-one-region-out classical policy-learner baselines."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import LeaveOneGroupOut


ROOT = Path(__file__).resolve().parents[1]
KEYS = ["model", "source_region", "target_region"]


def import_local(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


external_eval = import_local(
    "external_eval_classical", ROOT / "scripts" / "evaluate_softbudget_external5.py"
)


def main() -> None:
    data, _, features = external_eval.training_and_external_features()
    groups = data["target_region"].to_numpy()
    logo = LeaveOneGroupOut()
    rows = []
    for learner in ("extratrees", "lightgbm"):
        for fold, (train_idx, test_idx) in enumerate(
            logo.split(data[features], groups=groups), start=1
        ):
            train = data.iloc[train_idx]
            test = data.iloc[test_idx]
            held_out = str(test["target_region"].iloc[0])
            print(f"{learner} fold {fold}/11: {held_out}", flush=True)
            adapt, score = external_eval.tuned_predictions(
                train, test, features, learner
            )
            frame = test[KEYS].copy()
            frame["learner"] = learner
            frame["pred_benefit_adapt"] = np.asarray(adapt, dtype=float)
            frame["predicted_gain"] = np.asarray(score, dtype=float)
            rows.append(frame)
    predictions = pd.concat(rows, ignore_index=True)
    expected = 2 * len(data)
    if (
        len(predictions) != expected
        or predictions.duplicated(KEYS + ["learner"]).any()
        or predictions[["pred_benefit_adapt", "predicted_gain"]].isna().any().any()
    ):
        raise RuntimeError("Invalid classical development predictions")
    outcomes = data[KEYS + ["deploy", "adapt", "retrain"]]
    _, curve, auc = external_eval.curves_and_auc(predictions, outcomes)
    summary = (
        auc.groupby("learner", as_index=False)
        .agg(
            mean_budget_curve_auc=("policy", "mean"),
            mean_random_auc=("random", "mean"),
            mean_oracle_auc=("oracle", "mean"),
            mean_difference_vs_random=("difference_vs_random", "mean"),
            targets_better_than_random=(
                "difference_vs_random", lambda x: int((x < 0).sum())
            ),
            mean_gap_closed=("gap_closed", "mean"),
        )
        .sort_values("mean_budget_curve_auc")
    )
    predictions.to_csv(
        ROOT / "classical_policy_benchmark_dev_predictions.csv", index=False
    )
    curve.to_csv(ROOT / "classical_policy_benchmark_dev_budget_curve.csv", index=False)
    auc.to_csv(ROOT / "classical_policy_benchmark_dev_target_auc.csv", index=False)
    summary.to_csv(ROOT / "classical_policy_benchmark_dev_summary.csv", index=False)
    (ROOT / "classical_policy_benchmark_dev_config.json").write_text(
        json.dumps(
            {
                "outer_validation": "LeaveOneGroupOut(target_region)",
                "inner_validation": "GroupKFold over all remaining target regions",
                "scoring": "negative mean absolute error",
                "features": len(features),
                "rows": len(data),
                "learners": ["extratrees", "lightgbm"],
                "grids": "Defined in scripts/evaluate_softbudget_external5.py:tuned_predictions",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
