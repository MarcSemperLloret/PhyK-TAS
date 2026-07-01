"""PhyK-TAS v2: compact fusion-ablation summary.

Collects existing v2 outputs into a reviewer-facing table showing what is gained
by feature-level fusion, inference-model fusion, monotone constraints, and the
split-conformal decision layer.
"""
from __future__ import annotations

import os
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
TAG = os.environ.get("PHYKTAS_V2_TAG", "all_viable_min100_full")

OUT = PAPER / f"v2_fusion_ablation_summary_{TAG}.csv"
REPORT = PAPER / f"v2_fusion_ablation_summary_{TAG}_report.md"


def main() -> None:
    sig = pd.read_csv(PAPER / f"v2_significance_{TAG}.csv")
    meta = pd.read_csv(PAPER / f"v2_meta_models_{TAG}.csv")
    mono = pd.read_csv(PAPER / f"v2_monotonic_{TAG}.csv")
    conf = pd.read_csv(PAPER / f"v2_conformal_{TAG}.csv")

    rows = []
    for _, r in sig[sig.cv_kind == "group_by_cell"].iterrows():
        rows.append({
            "forecast_model": r.forecast_model,
            "stage": "feature_fusion",
            "metric": "delta_r2_physical_plus_shift_minus_shift",
            "value": r.delta_combined_minus_shift,
            "context": "group_by_cell random_forest",
        })
    for _, r in meta[(meta.cv_kind == "leave_target_region_out") &
                     (meta.estimator.isin(["random_forest", "fusion_stack", "mixedlm_pool"]))].iterrows():
        rows.append({
            "forecast_model": r.forecast_model,
            "stage": "inference_model",
            "metric": f"r2_{r.estimator}",
            "value": r.r2,
            "context": "leave_target_region_out physical_plus_shift",
        })
    for _, r in mono[(mono.cv_kind == "leave_target_region_out") &
                     (mono.estimator.isin(["hist_gbm", "hist_gbm_mono"]))].iterrows():
        rows.append({
            "forecast_model": r.forecast_model,
            "stage": "monotone_prior",
            "metric": f"r2_{r.estimator}",
            "value": r.r2,
            "context": "leave_target_region_out physical_plus_shift",
        })
    for _, r in conf[conf.alpha == 0.10].iterrows():
        rows.append({
            "forecast_model": r.forecast_model,
            "stage": "decision_calibration",
            "metric": "unsafe_deploy_rate_alpha_0.10",
            "value": r.unsafe_deploy_rate,
            "context": f"coverage={r.empirical_coverage:.3f}; deploy/split={r.mean_deploy_per_split:.2f}",
        })

    out = pd.DataFrame(rows)
    out.to_csv(OUT, index=False)

    lines = [
        f"# PhyK-TAS v2 fusion-ablation summary ({TAG})",
        "",
        "This compact table is intended for reviewer-facing synthesis. It does "
        "not introduce new model training; it collates the v2 feature-fusion, "
        "model-fusion, monotonicity, and conformal-decision analyses.",
        "",
        out.round(4).to_markdown(index=False),
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
