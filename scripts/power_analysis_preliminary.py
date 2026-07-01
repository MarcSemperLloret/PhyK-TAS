from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import nct, t

from experiment_config import assignment_path, tagged_paper_path
from deduplicate_ar6_viability import CORE, REGIONS, dedup, prepare_base


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
OUT = tagged_paper_path("power_analysis", ".md")
ASSIGN = assignment_path()


def detectable_r2(n: int, alpha: float = 0.05, power: float = 0.8) -> float:
    if n <= 4:
        return float("nan")
    df = n - 2
    tcrit = t.ppf(1 - alpha / 2, df)
    grid = np.linspace(0.001, 0.8, 5000)
    for r2 in grid:
        r = np.sqrt(r2)
        ncp = r * np.sqrt(df / (1 - r2))
        pwr = nct.sf(tcrit, df, ncp) + nct.cdf(-tcrit, df, ncp)
        if pwr >= power:
            return float(r2)
    return float("nan")


def main() -> None:
    base = prepare_base(2005)
    rows = []
    assignments = []
    for threshold, flag_col in [(80, "all4_ge80"), (95, "all4_ge95")]:
        filt = base[base[flag_col] & base["source_id"].isin(CORE)].copy()
        for region in REGIONS:
            region_df = filt[filt["ar6_region"] == region].copy()
            deduped, _ = dedup(region_df)
            if deduped.empty:
                continue
            # Assign cell from canonical station coordinates by taking the canonical row.
            canon = deduped.sort_values(["canonical_station_uid", "source_id", "source_station_id"]).drop_duplicates(
                "canonical_station_uid"
            )
            canon["cell5_lon"] = (np.floor(canon["longitude"].astype(float) / 5) * 5).astype(int)
            canon["cell5_lat"] = (np.floor(canon["latitude"].astype(float) / 5) * 5).astype(int)
            canon["cell5"] = canon["cell5_lat"].astype(str) + "_" + canon["cell5_lon"].astype(str)
            canon["coverage_threshold"] = threshold
            assignments.append(
                canon[
                    [
                        "canonical_station_uid",
                        "ar6_region",
                        "coverage_threshold",
                        "cell5",
                        "latitude",
                        "longitude",
                        "source_id",
                    ]
                ]
            )
            n_station = canon["canonical_station_uid"].nunique()
            n_cell = canon["cell5"].nunique()
            rows.append(
                {
                    "ar6_region": region,
                    "coverage_threshold": threshold,
                    "n_station": n_station,
                    "n_cell5": n_cell,
                    "min_detectable_r2_station_iid": detectable_r2(n_station),
                    "min_detectable_r2_cell_effective": detectable_r2(n_cell),
                }
            )
    assign = pd.concat(assignments, ignore_index=True)
    assign.to_csv(ASSIGN, index=False)
    table = pd.DataFrame(rows)

    lines = [
        "# Preliminary power analysis",
        "",
        "This is a pre-model analytic power check using post-dedup AR6 counts for the configured sources and period_start=2005.",
        "",
        "It does not replace the later pilot-model power analysis. It estimates the minimum detectable R2 for a single predictor under alpha=0.05 and power=0.8 using two bounds:",
        "",
        "- station IID bound: optimistic;",
        "- cell 5 x 5 effective-n bound: conservative for spatial dependence.",
        "",
        table.to_markdown(index=False),
        "",
        "## Interpretation",
        "",
        "- WCE and NEU have enough stations and cells for inferential analysis.",
        "- MED is viable by station count but remains the limiting region by 5 x 5 cell count.",
        "- The final power analysis must use pilot degradation estimates and hierarchical/bootstrap variance, as specified in the protocol.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {ASSIGN}")
    print(f"wrote {OUT}")
    print(table.to_string(index=False))


if __name__ == "__main__":
    main()
