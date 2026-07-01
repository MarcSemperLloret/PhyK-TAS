from __future__ import annotations

import os
from pathlib import Path

import pandas as pd

from experiment_config import PAPER, assignment_path


MIN_STATIONS = int(os.environ.get("PHYKTAS_MIN_REGION_STATIONS", "100"))
SELECTED_TAG = os.environ.get("PHYKTAS_SELECTED_REGION_TAG", f"all_viable_min{MIN_STATIONS}")
ASSIGN = assignment_path()
OUT = PAPER / f"region_thresholds_{SELECTED_TAG}.csv"
REPORT = PAPER / f"region_thresholds_{SELECTED_TAG}_report.md"


def choose_threshold(group: pd.DataFrame) -> pd.Series | None:
    counts = (
        group.groupby("coverage_threshold")
        .agg(
            n_stations=("canonical_station_uid", "nunique"),
            n_cell5=("cell5", "nunique"),
        )
        .reset_index()
    )
    for threshold in [95, 80]:
        row = counts[counts["coverage_threshold"] == threshold]
        if not row.empty and int(row.iloc[0]["n_stations"]) >= MIN_STATIONS:
            return row.iloc[0]
    return None


def main() -> None:
    if not ASSIGN.exists():
        raise FileNotFoundError(ASSIGN)
    assign = pd.read_csv(ASSIGN)
    selected_rows = []
    for region, group in assign.groupby("ar6_region"):
        choice = choose_threshold(group)
        if choice is None:
            continue
        selected_rows.append(
            {
                "ar6_region": region,
                "coverage_threshold": int(choice["coverage_threshold"]),
                "n_stations": int(choice["n_stations"]),
                "n_cell5": int(choice["n_cell5"]),
            }
        )

    selected = pd.DataFrame(selected_rows).sort_values(
        ["n_stations", "ar6_region"], ascending=[False, True]
    )
    selected.to_csv(OUT, index=False)

    counts = (
        assign.groupby(["ar6_region", "coverage_threshold"])
        .agg(
            n_stations=("canonical_station_uid", "nunique"),
            n_cell5=("cell5", "nunique"),
        )
        .reset_index()
        .sort_values(["coverage_threshold", "n_stations"], ascending=[False, False])
    )
    rejected = counts[
        (counts["coverage_threshold"] == 80)
        & (~counts["ar6_region"].isin(selected["ar6_region"]))
        & (counts["n_stations"] > 0)
    ].sort_values("n_stations", ascending=False)

    lines = [
        f"# Viable AR6 region selection: {SELECTED_TAG}",
        "",
        f"Assignment file: `{ASSIGN.name}`.",
        f"Minimum stations per region: {MIN_STATIONS}.",
        "",
        "Selection rule: prefer 95% coverage when it has enough stations; otherwise use 80%.",
        "",
        "## Selected regions",
        "",
        selected.to_markdown(index=False),
        "",
        "## Rejected regions with some 80% coverage",
        "",
        rejected.to_markdown(index=False),
        "",
        "## All counts",
        "",
        counts.to_markdown(index=False),
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"wrote {REPORT}")
    print(selected.to_string(index=False))


if __name__ == "__main__":
    main()
