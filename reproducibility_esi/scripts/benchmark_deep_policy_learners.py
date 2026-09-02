"""Benchmark modern deep tabular learners for the action-value policy.

The development comparison uses leave-one-target-region-out predictions on the
2020--2022 action library.  The five-region 2023--2025 evaluation is explicitly
post hoc for the learners added by this script, because those outcomes had
already been opened before this benchmark was specified.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import importlib.util
import json
import random
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from scipy.stats import wilcoxon
from sklearn.model_selection import LeaveOneGroupOut


ROOT = Path(__file__).resolve().parents[1]
KEYS = ["model", "source_region", "target_region"]
SEED = 20260822


def import_local(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


external_eval = import_local(
    "external_eval_deep", ROOT / "scripts" / "evaluate_softbudget_external5.py"
)


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def standardize(
    x_train: np.ndarray, y_train: np.ndarray, x_test: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    x_mean = x_train.mean(axis=0)
    x_std = x_train.std(axis=0)
    x_std[x_std < 1e-6] = 1.0
    y_mean = y_train.mean(axis=0)
    y_std = y_train.std(axis=0)
    y_std[y_std < 1e-6] = 1.0
    return (
        (x_train - x_mean) / x_std,
        (y_train - y_mean) / y_std,
        (x_test - x_mean) / x_std,
        y_mean,
        y_std,
    )


def fit_torch_once(
    learner: str,
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_test: np.ndarray,
    *,
    epochs: int,
    seed: int,
) -> tuple[np.ndarray, float, float]:
    """Fit one frozen configuration and return two action-benefit outputs."""
    from rtdl_revisiting_models import FTTransformer
    from tabm import TabM

    set_seed(seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    x_train, y_train, x_test, y_mean, y_std = standardize(
        x_train, y_train, x_test
    )
    x = torch.as_tensor(x_train, dtype=torch.float32, device=device)
    y = torch.as_tensor(y_train, dtype=torch.float32, device=device)
    xt = torch.as_tensor(x_test, dtype=torch.float32, device=device)

    if learner == "tabm":
        # Official package defaults: three 512-wide blocks and k=32 efficient
        # submodels.  Only data-related arguments and d_out are supplied.
        model = TabM.make(
            n_num_features=x.shape[1], cat_cardinalities=[], d_out=2
        ).to(device)
        optimizer = torch.optim.AdamW(model.parameters(), lr=2e-3, weight_decay=3e-4)

        def forward(z: torch.Tensor) -> torch.Tensor:
            return model(z, None)

        def loss_fn(output: torch.Tensor) -> torch.Tensor:
            return torch.nn.functional.mse_loss(output, y[:, None, :].expand_as(output))

        def reduce_output(output: torch.Tensor) -> torch.Tensor:
            return output.mean(dim=1)

    elif learner == "ft_transformer":
        kwargs = FTTransformer.get_default_kwargs(n_blocks=2)
        model = FTTransformer(
            n_cont_features=x.shape[1], cat_cardinalities=[], d_out=2, **kwargs
        ).to(device)
        optimizer = model.make_default_optimizer()

        def forward(z: torch.Tensor) -> torch.Tensor:
            return model(z, None)

        def loss_fn(output: torch.Tensor) -> torch.Tensor:
            return torch.nn.functional.mse_loss(output, y)

        def reduce_output(output: torch.Tensor) -> torch.Tensor:
            return output

    else:
        raise ValueError(learner)

    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=max(1, epochs)
    )
    fit_start = time.perf_counter()
    for _ in range(epochs):
        model.train()
        optimizer.zero_grad(set_to_none=True)
        loss = loss_fn(forward(x))
        if not torch.isfinite(loss):
            raise RuntimeError(f"Non-finite {learner} loss")
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
        optimizer.step()
        scheduler.step()
    fit_seconds = time.perf_counter() - fit_start

    pred_start = time.perf_counter()
    model.eval()
    with torch.inference_mode():
        prediction = reduce_output(forward(xt)).cpu().numpy()
    predict_seconds = time.perf_counter() - pred_start
    prediction = prediction * y_std + y_mean
    del model, optimizer, scheduler, x, y, xt
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return prediction.astype(np.float64), fit_seconds, predict_seconds


def fit_torch_ensemble(
    learner: str,
    train: pd.DataFrame,
    test: pd.DataFrame,
    features: list[str],
    *,
    epochs: int,
    repetitions: int,
    seed: int,
) -> tuple[np.ndarray, dict[str, float]]:
    x_train = train[features].to_numpy(dtype=np.float32)
    y_train = train[["benefit_adapt", "benefit_retrain"]].to_numpy(dtype=np.float32)
    x_test = test[features].to_numpy(dtype=np.float32)
    predictions = []
    fit_seconds = 0.0
    predict_seconds = 0.0
    for repetition in range(repetitions):
        pred, fit_time, pred_time = fit_torch_once(
            learner,
            x_train,
            y_train,
            x_test,
            epochs=epochs,
            seed=seed + 1009 * repetition,
        )
        predictions.append(pred)
        fit_seconds += fit_time
        predict_seconds += pred_time
    return np.mean(predictions, axis=0), {
        "fit_seconds": fit_seconds,
        "predict_seconds": predict_seconds,
    }


def fit_tabdpt(
    train: pd.DataFrame,
    test: pd.DataFrame,
    features: list[str],
    *,
    seed: int,
) -> tuple[np.ndarray, dict[str, float]]:
    from tabdpt import TabDPTRegressor

    x_train = train[features].to_numpy(dtype=np.float32)
    x_test = test[features].to_numpy(dtype=np.float32)
    output = []
    fit_seconds = 0.0
    predict_seconds = 0.0
    model = TabDPTRegressor(
        device="cuda" if torch.cuda.is_available() else "cpu",
        use_flash=False,
        compile=False,
        verbose=False,
    )
    for offset, outcome in enumerate(("benefit_adapt", "benefit_retrain")):
        start = time.perf_counter()
        model.fit(x_train, train[outcome].to_numpy(dtype=np.float32))
        fit_seconds += time.perf_counter() - start
        start = time.perf_counter()
        pred = model.predict(
            x_test,
            n_ensembles=8,
            context_size=min(128, len(train)),
            seed=seed + offset,
        )
        predict_seconds += time.perf_counter() - start
        output.append(np.asarray(pred, dtype=np.float64))
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return np.column_stack(output), {
        "fit_seconds": fit_seconds,
        "predict_seconds": predict_seconds,
    }


def predict_one(
    learner: str,
    train: pd.DataFrame,
    test: pd.DataFrame,
    features: list[str],
    *,
    epochs: int,
    repetitions: int,
    seed: int,
) -> tuple[pd.DataFrame, dict[str, float]]:
    if learner == "tabdpt_v1_2":
        raw, timing = fit_tabdpt(train, test, features, seed=seed)
    else:
        raw, timing = fit_torch_ensemble(
            learner,
            train,
            test,
            features,
            epochs=epochs,
            repetitions=repetitions,
            seed=seed,
        )
    frame = test[KEYS].copy()
    frame["learner"] = learner
    frame["pred_benefit_adapt"] = raw[:, 0]
    frame["pred_benefit_retrain"] = raw[:, 1]
    frame["predicted_gain"] = raw[:, 1] - np.maximum(0.0, raw[:, 0])
    return frame, timing


def development_predictions(
    learner: str,
    train: pd.DataFrame,
    features: list[str],
    *,
    epochs: int,
    repetitions: int,
) -> tuple[pd.DataFrame, list[dict[str, float | int | str]]]:
    logo = LeaveOneGroupOut()
    rows = []
    timings = []
    groups = train["target_region"].to_numpy()
    for fold, (train_idx, test_idx) in enumerate(
        logo.split(train[features], groups=groups), start=1
    ):
        held_out = str(train.iloc[test_idx]["target_region"].iloc[0])
        print(f"{learner} development fold {fold}/11: {held_out}", flush=True)
        pred, timing = predict_one(
            learner,
            train.iloc[train_idx],
            train.iloc[test_idx],
            features,
            epochs=epochs,
            repetitions=repetitions,
            seed=SEED + 100 * fold,
        )
        rows.append(pred)
        timings.append(
            {"learner": learner, "stage": "development", "fold": fold,
             "held_out_region": held_out, **timing}
        )
    result = pd.concat(rows, ignore_index=True)
    if len(result) != len(train) or result.duplicated(KEYS).any():
        raise RuntimeError(f"Invalid development predictions for {learner}")
    return result, timings


def external_predictions(
    learner: str,
    train: pd.DataFrame,
    external: pd.DataFrame,
    features: list[str],
    *,
    epochs: int,
    repetitions: int,
) -> tuple[pd.DataFrame, list[dict[str, float | int | str]]]:
    print(f"{learner} external post-hoc stress test", flush=True)
    pred, timing = predict_one(
        learner,
        train,
        external,
        features,
        epochs=epochs,
        repetitions=repetitions,
        seed=SEED + 9000,
    )
    if len(pred) != 165 or pred.duplicated(KEYS).any():
        raise RuntimeError(f"Invalid external predictions for {learner}")
    return pred, [
        {"learner": learner, "stage": "external_posthoc", "fold": 0,
         "held_out_region": "CAU,NAU,NEN,ESB,RFE", **timing}
    ]


def summarize(auc: pd.DataFrame, stage: str) -> pd.DataFrame:
    return (
        auc.groupby("learner", as_index=False)
        .agg(
            mean_budget_curve_auc=("policy", "mean"),
            mean_random_auc=("random", "mean"),
            mean_oracle_auc=("oracle", "mean"),
            mean_difference_vs_random=("difference_vs_random", "mean"),
            targets_better_than_random=("difference_vs_random", lambda x: int((x < 0).sum())),
            targets_total=("target_region", "nunique"),
            mean_gap_closed=("gap_closed", "mean"),
        )
        .assign(stage=stage)
        .sort_values("mean_budget_curve_auc")
    )


def compare_external_to_baselines(new_auc: pd.DataFrame) -> pd.DataFrame:
    baseline = pd.read_csv(ROOT / "softbudget_external5_target_auc.csv")
    combined = pd.concat([baseline, new_auc], ignore_index=True)
    pivot = combined.pivot(index="target_region", columns="learner", values="policy")
    rows = []
    for learner in sorted(new_auc["learner"].unique()):
        for reference in ("ridge", "extratrees", "pointwise", "tabicl_v2"):
            diff = pivot[learner] - pivot[reference]
            rows.append(
                {
                    "learner": learner,
                    "reference": reference,
                    "mean_auc_difference": float(diff.mean()),
                    "median_auc_difference": float(diff.median()),
                    "targets_learner_better": int((diff < 0).sum()),
                    "targets_total": int(len(diff)),
                    "wilcoxon_one_sided_p": float(
                        wilcoxon(diff, alternative="less").pvalue
                    ),
                }
            )
    return pd.DataFrame(rows)


def make_report(
    dev_summary: pd.DataFrame,
    external_summary: pd.DataFrame,
    comparisons: pd.DataFrame,
    timings: pd.DataFrame,
    config: dict,
) -> str:
    lines = [
        "# Modern deep policy-learner benchmark",
        "",
        "Development uses leave-one-target-region-out on 2020--2022. The five-region",
        "2023--2025 results are post hoc for these newly added learners and are not an",
        "independent confirmation.",
        "",
        "## Frozen configurations",
        "",
        "```json",
        json.dumps(config, indent=2),
        "```",
        "",
        "## Development LOGO",
        "",
        dev_summary.to_markdown(index=False, floatfmt=".6f"),
        "",
        "## External five-region stress test (post hoc)",
        "",
        external_summary.to_markdown(index=False, floatfmt=".6f"),
        "",
        "## Paired external comparisons",
        "",
        comparisons.to_markdown(index=False, floatfmt=".6f"),
        "",
        "## Computational cost",
        "",
        timings.groupby(["learner", "stage"], as_index=False)[
            ["fit_seconds", "predict_seconds"]
        ].sum().to_markdown(index=False, floatfmt=".3f"),
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--models",
        default="tabm,ft_transformer,tabdpt_v1_2",
        help="Comma-separated subset of tabm,ft_transformer,tabdpt_v1_2",
    )
    parser.add_argument("--epochs", type=int, default=300)
    parser.add_argument("--repetitions", type=int, default=3)
    args = parser.parse_args()
    models = [x.strip() for x in args.models.split(",") if x.strip()]
    allowed = {"tabm", "ft_transformer", "tabdpt_v1_2"}
    if not models or not set(models).issubset(allowed):
        raise ValueError(f"Models must be a subset of {sorted(allowed)}")

    train, external, features = external_eval.training_and_external_features()
    dev_outcomes = train[KEYS + ["deploy", "adapt", "retrain"]].copy()
    ext_outcomes = external_eval.load_outcomes()
    timings: list[dict[str, float | int | str]] = []
    dev_predictions = []
    ext_predictions = []
    for learner in models:
        repetitions = 1 if learner in {"tabm", "tabdpt_v1_2"} else args.repetitions
        dev, timing = development_predictions(
            learner,
            train,
            features,
            epochs=args.epochs,
            repetitions=repetitions,
        )
        dev.to_csv(ROOT / f"deep_policy_{learner}_dev_predictions.csv", index=False)
        dev_predictions.append(dev)
        timings.extend(timing)
        ext, timing = external_predictions(
            learner,
            train,
            external,
            features,
            epochs=args.epochs,
            repetitions=repetitions,
        )
        ext.to_csv(ROOT / f"deep_policy_{learner}_external5_predictions.csv", index=False)
        ext_predictions.append(ext)
        timings.extend(timing)

    dev_pred = pd.concat(dev_predictions, ignore_index=True)
    ext_pred = pd.concat(ext_predictions, ignore_index=True)
    _, dev_curve, dev_auc = external_eval.curves_and_auc(dev_pred, dev_outcomes)
    _, ext_curve, ext_auc = external_eval.curves_and_auc(ext_pred, ext_outcomes)
    dev_summary = summarize(dev_auc, "development_logo")
    ext_summary = summarize(ext_auc, "external5_posthoc")
    comparisons = compare_external_to_baselines(ext_auc)
    timing_frame = pd.DataFrame(timings)

    config = {
        "date": "2026-08-22",
        "models": models,
        "features": len(features),
        "development_rows": len(train),
        "external_rows": len(external),
        "epochs": args.epochs,
        "ft_transformer_repetitions": args.repetitions,
        "tabm": "package defaults (3x512, k=32), AdamW lr=2e-3 wd=3e-4",
        "ft_transformer": "official two-block default, AdamW lr=1e-4 wd=1e-5",
        "tabdpt": "v1.2.0, context=128, ensembles=8, no task-specific tuning",
        "versions": {
            package: importlib.metadata.version(package)
            for package in ("tabm", "rtdl-revisiting-models", "tabdpt", "torch")
        },
        "device": str(torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu"),
        "external_status": "post hoc for the new learners",
    }

    dev_curve.to_csv(ROOT / "deep_policy_benchmark_dev_budget_curve.csv", index=False)
    dev_auc.to_csv(ROOT / "deep_policy_benchmark_dev_target_auc.csv", index=False)
    dev_summary.to_csv(ROOT / "deep_policy_benchmark_dev_summary.csv", index=False)
    ext_curve.to_csv(ROOT / "deep_policy_benchmark_external5_budget_curve.csv", index=False)
    ext_auc.to_csv(ROOT / "deep_policy_benchmark_external5_target_auc.csv", index=False)
    ext_summary.to_csv(ROOT / "deep_policy_benchmark_external5_summary.csv", index=False)
    comparisons.to_csv(ROOT / "deep_policy_benchmark_external5_comparisons.csv", index=False)
    timing_frame.to_csv(ROOT / "deep_policy_benchmark_timings.csv", index=False)
    (ROOT / "deep_policy_benchmark_config.json").write_text(
        json.dumps(config, indent=2), encoding="utf-8"
    )
    report = make_report(dev_summary, ext_summary, comparisons, timing_frame, config)
    (ROOT / "deep_policy_benchmark_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
