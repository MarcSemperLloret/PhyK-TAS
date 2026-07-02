"""Control analysis for conflict as uncertainty signal.

Tests whether physical/statistical disagreement predicts fusion error after
controlling for predicted degradation severity, generic shift magnitude, target
region, and forecast model. This guards against interpreting conflict as
epistemic uncertainty when it is only a proxy for hard or distant transfers.
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from analyze_v2_significance import ESTIMATOR, PAPER, SEEDS, TAG, TARGET, load_predictions
from build_v2_meta_models import SHIFT_COLS
from build_v3_fusion import leave_region_out_sigma2

OUT = PAPER / f"v3_conflict_confound_control_{TAG}.csv"
REPORT = PAPER / f"v3_conflict_confound_control_{TAG}_report.md"
REGION_SET = os.environ.get("PHYKTAS_V2_REGION_SET", "all_viable_min100")


def zscore(x: pd.Series) -> pd.Series:
    sd = float(x.std(ddof=0))
    if sd == 0 or not np.isfinite(sd):
        return x * 0.0
    return (x - float(x.mean())) / sd


def pair_frame(sub: pd.DataFrame) -> pd.DataFrame:
    y = sub[TARGET].to_numpy()
    regions = sub["target_region"].to_numpy()
    f_phys = sub[f"physical_knowledge_group_by_cell_{ESTIMATOR}_pred"].to_numpy()
    f_shift = sub[f"generic_shift_group_by_cell_{ESTIMATOR}_pred"].to_numpy()

    s2_phys = leave_region_out_sigma2(y - f_phys, regions)
    s2_shift = leave_region_out_sigma2(y - f_shift, regions)
    wp = np.array([1.0 / s2_phys[r] for r in regions])
    ws = np.array([1.0 / s2_shift[r] for r in regions])
    wp = wp / (wp + ws)
    pred = wp * f_phys + (1.0 - wp) * f_shift

    d = sub[["source_region", "target_region"]].copy()
    d["d_obs"] = y
    d["d_pred"] = pred
    d["conflict"] = np.abs(f_phys - f_shift)
    return d.groupby(["source_region", "target_region"], as_index=False).mean(numeric_only=True)


def main() -> None:
    df = load_predictions()
    shift = pd.read_csv(PAPER / f"distribution_shift_baselines_{REGION_SET}.csv")
    frames = []
    for model, sub in df.groupby("model"):
        p = pair_frame(sub.reset_index(drop=True))
        p = p.merge(shift[["source_region", "target_region"] + SHIFT_COLS], on=["source_region", "target_region"], how="left")
        p["forecast_model"] = model
        frames.append(p)
    data = pd.concat(frames, ignore_index=True)
    data["abs_error"] = np.abs(data["d_obs"] - data["d_pred"])
    data["predicted_severity"] = np.abs(data["d_pred"])

    shift_rank_cols = []
    for col in SHIFT_COLS:
        rcol = f"{col}_rank"
        data[rcol] = data[col].rank(pct=True)
        shift_rank_cols.append(rcol)
    data["shift_magnitude"] = data[shift_rank_cols].mean(axis=1)

    for col in ["abs_error", "conflict", "predicted_severity", "shift_magnitude"]:
        data[f"{col}_z"] = zscore(data[col])

    formula = (
        "abs_error_z ~ conflict_z + predicted_severity_z + shift_magnitude_z "
        "+ C(target_region) + C(forecast_model)"
    )
    fit = smf.ols(formula, data=data).fit(cov_type="HC3")
    terms = ["conflict_z", "predicted_severity_z", "shift_magnitude_z"]
    rows = []
    for term in terms:
        rows.append(
            {
                "term": term,
                "coef_standardized": float(fit.params[term]),
                "robust_se": float(fit.bse[term]),
                "p_value": float(fit.pvalues[term]),
                "ci_low": float(fit.conf_int().loc[term, 0]),
                "ci_high": float(fit.conf_int().loc[term, 1]),
                "n": int(fit.nobs),
                "r2": float(fit.rsquared),
            }
        )
    out = pd.DataFrame(rows)
    out.to_csv(OUT, index=False)

    lines = [
        f"# Conflict confound-control analysis ({TAG})",
        "",
        "Pair-level OLS with HC3 robust standard errors. Outcome is standardized absolute "
        "error of reliability-weighted source fusion. Predictors are standardized; fixed "
        "effects are target region and forecast model.",
        "",
        out.round(4).to_markdown(index=False),
        "",
        "Model formula:",
        "",
        f"`{formula}`",
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(out.to_string(index=False))
    print(f"\nwrote {OUT}\nwrote {REPORT}")


if __name__ == "__main__":
    main()
