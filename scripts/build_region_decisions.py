from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
VIABILITY = PAPER / "viability_post_dedup.csv"
OUT = PAPER / "region_decisions.md"


def classify(n95: int, n80: int) -> str:
    if n95 >= 500:
        return "principal_95"
    if n95 >= 300 or n80 >= 500:
        return "principal_80_mask_sensitivity_95"
    if n80 >= 300:
        return "limited_power_or_grouping_needed"
    return "not_main_region"


def main() -> None:
    v = pd.read_csv(VIABILITY)
    core = v[v["scope"] == "core_ghcnd_ecad"].copy()
    rows = []
    for period_start in sorted(core["period_start"].unique()):
        sub = core[core["period_start"] == period_start]
        for region in ["MED", "WCE", "NEU"]:
            n80 = int(
                sub[(sub["ar6_region"] == region) & (sub["coverage_threshold"] == 80)][
                    "n_unique_post_dedup"
                ].max()
            )
            n95 = int(
                sub[(sub["ar6_region"] == region) & (sub["coverage_threshold"] == 95)][
                    "n_unique_post_dedup"
                ].max()
            )
            rows.append(
                {
                    "period_start": period_start,
                    "ar6_region": region,
                    "n80_post_dedup": n80,
                    "n95_post_dedup": n95,
                    "decision": classify(n95, n80),
                }
            )
    table = pd.DataFrame(rows)
    selected = table[table["period_start"] == 2005].copy()
    lines = [
        "# Region decisions v1",
        "",
        "Decisions are based on `viability_post_dedup.csv` using the core sources `global_ghcnd_01` + `eur_ecad_01`.",
        "",
        "## Candidate starts",
        "",
        table.to_markdown(index=False),
        "",
        "## Selected operational design",
        "",
        "Use `period_start=2005` for the preregistration candidate.",
        "",
        "Reason:",
        "",
        "- `MED` fails the 300-station 95% rule with start 2000 (`n95=192`).",
        "- `MED` passes the 300-station 95% rule with start 2005 (`n95=311`).",
        "- `WCE` and `NEU` are strong under both starts.",
        "- Starting in 2005 improves stability without changing the core design qualitatively.",
        "",
        "## Decisions for period_start=2005",
        "",
        selected.to_markdown(index=False),
        "",
        "## MED contingency",
        "",
        "If manual deduplication audit or AR6 boundary review reduces `MED` below 300 at 95%, use 80% with explicit missingness mask as the main MED analysis and retain 95% as strict sensitivity.",
        "",
        "## Caveat",
        "",
        "This decision is not a frozen preregistration. It becomes preregistrable only after deduplication audit and power analysis.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")
    print(selected.to_string(index=False))


if __name__ == "__main__":
    main()

