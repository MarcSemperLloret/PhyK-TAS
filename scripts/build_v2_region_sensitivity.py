"""PhyK-TAS v2: regional-set sensitivity.

Recomputes the primary feature-fusion comparison on subsets of the viable
regions, using already-computed out-of-fold predictions. This checks whether
the physical+shift gain is driven by the lower-coverage 80% regions.
"""
from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from sklearn.metrics import r2_score

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
TAG = os.environ.get("PHYKTAS_V2_TAG", "all_viable_min100_full")
SEEDS = os.environ.get("PHYKTAS_V2_SEEDS", "s1,s2,s3").split(",")
TARGET = "mae_out_minus_in"

OUT = PAPER / f"v2_region_sensitivity_{TAG}.csv"
REPORT = PAPER / f"v2_region_sensitivity_{TAG}_report.md"


def pred_col(feature_set: str) -> str:
    return f"{feature_set}_group_by_cell_random_forest_pred"


def load_predictions() -> pd.DataFrame:
    frames = []
    for seed in SEEDS:
        df = pd.read_csv(PAPER / f"kbs_forecast_model_comparison_{TAG}_{seed}_predictions.csv")
        df["seed"] = seed
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def region_sets() -> dict[str, set[str]]:
    audit = pd.read_csv(PAPER / f"{TAG}_region_audit.csv")
    all_regions = set(audit["ar6_region"])
    strict95 = set(audit.loc[audit["coverage_threshold"] == 95, "ar6_region"])
    strict95_ge300 = set(
        audit.loc[
            (audit["coverage_threshold"] == 95) & (audit["n_stations"] >= 300),
            "ar6_region",
        ]
    )
    return {
        "all_11": all_regions,
        "coverage95_only": strict95,
        "coverage95_ge300": strict95_ge300,
    }


def main() -> None:
    df = load_predictions()
    rows = []
    for set_name, regions in region_sets().items():
        sub0 = df[df["source_region"].isin(regions) & df["target_region"].isin(regions)].copy()
        for model, sub in sub0.groupby("model"):
            y = sub[TARGET].to_numpy()
            r2_phys = r2_score(y, sub[pred_col("physical_knowledge")].to_numpy())
            r2_shift = r2_score(y, sub[pred_col("generic_shift")].to_numpy())
            r2_comb = r2_score(y, sub[pred_col("physical_plus_shift")].to_numpy())
            rows.append({
                "region_set": set_name,
                "n_regions": len(regions),
                "forecast_model": model,
                "n_rows": len(sub),
                "n_pairs": sub[["source_region", "target_region"]].drop_duplicates().shape[0],
                "r2_physical": r2_phys,
                "r2_shift": r2_shift,
                "r2_physical_plus_shift": r2_comb,
                "delta_combined_minus_shift": r2_comb - r2_shift,
            })
    res = pd.DataFrame(rows)
    res.to_csv(OUT, index=False)

    lines = [
        f"# PhyK-TAS v2 regional-set sensitivity ({TAG})",
        "",
        "Primary group-by-cell random-forest feature comparison recomputed on "
        "region subsets. The stricter subsets remove the 80% coverage regions "
        "and then require at least 300 stations.",
        "",
        res.round(4).to_markdown(index=False),
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
