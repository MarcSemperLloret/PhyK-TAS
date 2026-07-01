from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
LOG = PAPER / "dedup_log.csv"
STATIONS = PAPER / "stations_ar6.csv"
OUT = PAPER / "dedup_audit_sample.csv"
REPORT = PAPER / "dedup_audit_report.md"


def main() -> None:
    log = pd.read_csv(LOG)
    stations = pd.read_csv(STATIONS, dtype={"source_station_id": str}, low_memory=False)
    stations["station_uid"] = stations["source_id"] + "::" + stations["source_station_id"].astype(str)
    cols = [
        "station_uid",
        "source_id",
        "source_station_id",
        "station_name",
        "country_iso3",
        "latitude",
        "longitude",
        "elevation_m",
        "wmo_id",
        "candidate_duplicate_key",
    ]
    meta = stations[cols]
    sample = log[log["merged"] == True].sample(min(30, (log["merged"] == True).sum()), random_state=23)
    sample = sample.merge(meta.add_suffix("_a"), left_on="station_uid_a", right_on="station_uid_a", how="left")
    sample = sample.merge(meta.add_suffix("_b"), left_on="station_uid_b", right_on="station_uid_b", how="left")
    sample["manual_review"] = ""
    sample["plausible_false_positive"] = ""
    sample.to_csv(OUT, index=False)

    by_criterion = log["criterion"].value_counts().reset_index()
    by_criterion.columns = ["criterion", "n_edges"]
    lines = [
        "# Deduplication audit report",
        "",
        "This is the required 30-edge audit sample for manual inspection.",
        "",
        f"Total dedup edges: {len(log)}",
        f"Merged edges: {int((log['merged'] == True).sum())}",
        "",
        "## Criteria counts",
        "",
        by_criterion.to_markdown(index=False),
        "",
        "## Audit rule",
        "",
        "- Inspect `dedup_audit_sample.csv`.",
        "- Mark `plausible_false_positive=True` for stations that appear legitimately distinct.",
        "- If more than 3 of 30 are plausible false positives, rerun with stricter metadata identity.",
        "",
        "## Current status",
        "",
        "Pending manual inspection. The sampled rows include station names, WMO IDs, elevations and distances.",
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"wrote {REPORT}")
    print(by_criterion.to_string(index=False))


if __name__ == "__main__":
    main()

