from __future__ import annotations

import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
DAILY = ROOT / "Data" / "harmonized" / "precip_daily"

DEFAULT_REGION_THRESHOLDS = {
    "MED": 80,
    "WCE": 95,
    "NEU": 95,
}

EXPANDED8_REGION_THRESHOLDS = {
    "MED": 80,
    "WCE": 95,
    "NEU": 95,
    "WNA": 80,
    "ENA": 80,
    "CNA": 80,
    "SAU": 80,
    "EAU": 80,
}


def parse_region_thresholds(text: str | None, default: dict[str, int] | None = None) -> dict[str, int]:
    if not text:
        return dict(default or DEFAULT_REGION_THRESHOLDS)
    out: dict[str, int] = {}
    for item in text.split(","):
        item = item.strip()
        if not item:
            continue
        if ":" not in item:
            raise ValueError(f"Region threshold entry must be REGION:THRESHOLD, got {item!r}")
        region, threshold = item.split(":", 1)
        out[region.strip().upper()] = int(threshold)
    if not out:
        raise ValueError("No region thresholds parsed.")
    return out


def region_thresholds() -> dict[str, int]:
    thresholds_file = os.environ.get("PHYKTAS_REGION_THRESHOLDS_FILE", "").strip()
    if thresholds_file:
        import pandas as pd

        df = pd.read_csv(thresholds_file)
        return {
            str(row.ar6_region).upper(): int(row.coverage_threshold)
            for row in df.itertuples(index=False)
        }

    named = os.environ.get("PHYKTAS_REGION_SET", "").strip().lower()
    if named == "expanded8":
        default = EXPANDED8_REGION_THRESHOLDS
    elif named in {"all", "all80", "all_viable"}:
        default = {region: 80 for region in all_ar6_regions()}
    elif named == "all95":
        default = {region: 95 for region in all_ar6_regions()}
    else:
        default = DEFAULT_REGION_THRESHOLDS
    return parse_region_thresholds(os.environ.get("PHYKTAS_REGION_THRESHOLDS"), default)


def regions() -> list[str]:
    return list(region_thresholds())


def all_ar6_regions() -> list[str]:
    summary = PAPER / "stations_ar6_summary.csv"
    if summary.exists():
        import pandas as pd

        df = pd.read_csv(summary)
        values = [
            str(x)
            for x in df["ar6_region"].dropna().tolist()
            if str(x) != "EXCLUDED"
        ]
        return values
    return list(EXPANDED8_REGION_THRESHOLDS)


def region_tag() -> str:
    return os.environ.get("PHYKTAS_REGION_TAG", "").strip()


def tag_suffix(tag: str | None = None) -> str:
    value = region_tag() if tag is None else tag.strip()
    return "" if not value else f"_{value}"


def tagged_paper_path(stem: str, suffix: str, tag: str | None = None) -> Path:
    return PAPER / f"{stem}{tag_suffix(tag)}{suffix}"


def assignment_path() -> Path:
    return Path(
        os.environ.get(
            "PHYKTAS_ASSIGNMENTS",
            str(tagged_paper_path("dedup_assignments_core_2005", ".csv")),
        )
    )


def discovered_daily_sources() -> list[str]:
    if not DAILY.exists():
        return []
    out = []
    for path in DAILY.iterdir():
        if path.is_dir() and path.name.startswith("source_id="):
            out.append(path.name.split("=", 1)[1])
    return sorted(out)


def daily_sources(default: list[str]) -> list[str]:
    explicit = os.environ.get("PHYKTAS_DAILY_SOURCES", "").strip()
    if explicit:
        return [x.strip() for x in explicit.split(",") if x.strip()]
    if os.environ.get("PHYKTAS_USE_ALL_DAILY_SOURCES", "").strip() in {"1", "true", "yes"}:
        return discovered_daily_sources()
    return list(default)


def physical_descriptor_paths() -> tuple[Path, Path, Path, Path]:
    return (
        tagged_paper_path("physical_descriptors_station", ".csv"),
        tagged_paper_path("physical_descriptors_cell5", ".csv"),
        tagged_paper_path("physical_descriptors_region", ".csv"),
        tagged_paper_path("physical_descriptors_report", ".md"),
    )


def shift_baseline_paths() -> tuple[Path, Path]:
    return (
        tagged_paper_path("distribution_shift_baselines", ".csv"),
        tagged_paper_path("distribution_shift_baselines_report", ".md"),
    )
