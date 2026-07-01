param(
    [Parameter(Mandatory=$true)][string]$Tag,
    [Parameter(Mandatory=$true)][int]$Seed,
    [string]$RegionSetTag = "all_viable_min100",
    [string]$AssignmentSourceTag = "all_sources",
    [int]$NPerRegion = 100,
    [int]$STGCNEpochs = 5,
    [int]$GraphWaveNetEpochs = 8,
    [switch]$SkipSTGCN,
    [switch]$SkipGraphWaveNet
)

$ErrorActionPreference = "Stop"
$paper = Resolve-Path "$PSScriptRoot\.."
$log = Join-Path $paper "${Tag}_run.log"

function Write-Step($message) {
    $stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[$stamp] $message" | Tee-Object -FilePath $log -Append
}

$assignments = Join-Path $paper "dedup_assignments_core_2005_${AssignmentSourceTag}.csv"
$thresholds = Join-Path $paper "region_thresholds_${RegionSetTag}.csv"
$descriptors = Join-Path $paper "physical_descriptors_station_${RegionSetTag}.csv"
$shift = Join-Path $paper "distribution_shift_baselines_${RegionSetTag}.csv"

$env:PHYKTAS_REGION_TAG = $RegionSetTag
$env:PHYKTAS_ASSIGNMENTS = $assignments
$env:PHYKTAS_REGION_THRESHOLDS_FILE = $thresholds
$env:PHYKTAS_PHYSICAL_DESCRIPTORS = $descriptors
$env:PHYKTAS_SHIFT_BASELINES = $shift

$env:FORECAST_EXPERIMENT_TAG = $Tag
$env:FORECAST_RANDOM_SEED = "$Seed"
$env:FORECAST_MODEL_SEED = "$Seed"
$env:FORECAST_N_PER_REGION = "$NPerRegion"

Write-Step "start tag=$Tag seed=$Seed region_set=$RegionSetTag n_per_region=$NPerRegion stgcn_epochs=$STGCNEpochs graphwavenet_epochs=$GraphWaveNetEpochs"

python (Join-Path $paper "scripts\build_forecasting_dataset_large.py") *>&1 | Tee-Object -FilePath $log -Append

$dataset = Join-Path $paper "forecast_dataset_large_${Tag}.npz"
$meta = Join-Path $paper "forecast_dataset_large_${Tag}_metadata.csv"
$env:FORECAST_DATA = $dataset
$env:FORECAST_META = $meta

Write-Step "run regional climatology and persistence"
python (Join-Path $paper "scripts\run_baseline_forecast_experiment.py") *>&1 | Tee-Object -FilePath $log -Append

Write-Step "run spatial kNN-ridge baseline"
python (Join-Path $paper "scripts\run_spatial_baseline_experiment.py") *>&1 | Tee-Object -FilePath $log -Append

$metricFiles = @(
    (Join-Path $paper "forecast_baseline_${Tag}_station_metrics.csv"),
    (Join-Path $paper "forecast_spatial_baseline_${Tag}_station_metrics.csv")
)

if (-not $SkipSTGCN) {
    Write-Step "run STGCN diffusion"
    $env:FORECAST_EPOCHS = "$STGCNEpochs"
    python (Join-Path $paper "scripts\run_stgnn_experiment.py") *>&1 | Tee-Object -FilePath $log -Append
    $metricFiles += Join-Path $paper "forecast_stgnn_${Tag}_station_metrics.csv"
}

if (-not $SkipGraphWaveNet) {
    Write-Step "run Graph WaveNet transfer"
    $env:FORECAST_EPOCHS = "$GraphWaveNetEpochs"
    python (Join-Path $paper "scripts\run_graphwavenet_experiment.py") *>&1 | Tee-Object -FilePath $log -Append
    $metricFiles += Join-Path $paper "forecast_graphwavenet_${Tag}_station_metrics.csv"
}

$env:FORECAST_METRICS = ($metricFiles -join ";")
Write-Step "run PhyK-TAS feature comparison"
python (Join-Path $paper "scripts\compare_kbs_on_forecast_models.py") *>&1 | Tee-Object -FilePath $log -Append

Write-Step "done"
