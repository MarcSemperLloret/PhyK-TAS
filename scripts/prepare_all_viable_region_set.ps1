param(
    [int]$MinStations = 100,
    [string]$SourceTag = "all_sources",
    [string]$SelectedTag = "",
    [string]$PeriodStarts = "2005"
)

$ErrorActionPreference = "Stop"
$paper = Resolve-Path "$PSScriptRoot\.."

if (-not $SelectedTag) {
    $SelectedTag = "all_viable_min$MinStations"
}

$env:PHYKTAS_REGION_SET = "all"
$env:PHYKTAS_REGION_TAG = $SourceTag
$env:PHYKTAS_USE_ALL_DAILY_SOURCES = "1"
$env:PHYKTAS_PERIOD_STARTS = $PeriodStarts

python (Join-Path $paper "scripts\build_viability_pre_dedup.py")
python (Join-Path $paper "scripts\deduplicate_ar6_viability.py")
python (Join-Path $paper "scripts\power_analysis_preliminary.py")

$env:PHYKTAS_MIN_REGION_STATIONS = "$MinStations"
$env:PHYKTAS_SELECTED_REGION_TAG = $SelectedTag
python (Join-Path $paper "scripts\select_viable_regions.py")

$assignments = Join-Path $paper "dedup_assignments_core_2005_${SourceTag}.csv"
$thresholds = Join-Path $paper "region_thresholds_${SelectedTag}.csv"

$env:PHYKTAS_REGION_TAG = $SelectedTag
$env:PHYKTAS_ASSIGNMENTS = $assignments
$env:PHYKTAS_REGION_THRESHOLDS_FILE = $thresholds
python (Join-Path $paper "scripts\build_physical_descriptors.py")
python (Join-Path $paper "scripts\build_shift_baselines.py")

Write-Host "Prepared region set $SelectedTag"
Write-Host "Assignments: $assignments"
Write-Host "Thresholds: $thresholds"
