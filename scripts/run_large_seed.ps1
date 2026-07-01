param(
    [Parameter(Mandatory=$true)][string]$Tag,
    [Parameter(Mandatory=$true)][int]$Seed
)

$ErrorActionPreference = "Stop"
$root = Resolve-Path "$PSScriptRoot\..\.."
$paper = Join-Path $root "Paper1"
$log = Join-Path $paper "large_${Tag}_run.log"

function Write-Step($message) {
    $stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[$stamp] $message" | Tee-Object -FilePath $log -Append
}

Write-Step "start tag=$Tag seed=$Seed"

$env:FORECAST_EXPERIMENT_TAG = $Tag
$env:FORECAST_RANDOM_SEED = "$Seed"
$env:FORECAST_N_PER_REGION = "1000"
python (Join-Path $paper "scripts\build_forecasting_dataset_large.py") *>&1 | Tee-Object -FilePath $log -Append

$dataset = Join-Path $paper "forecast_dataset_large_${Tag}.npz"
$meta = Join-Path $paper "forecast_dataset_large_${Tag}_metadata.csv"

$env:FORECAST_DATA = $dataset
$env:FORECAST_META = $meta
Write-Step "run graphwavenet"
python (Join-Path $paper "scripts\run_graphwavenet_experiment.py") *>&1 | Tee-Object -FilePath $log -Append

Write-Step "run stgcn"
python (Join-Path $paper "scripts\run_stgnn_experiment.py") *>&1 | Tee-Object -FilePath $log -Append

$env:FORECAST_METRICS = "$(Join-Path $paper "forecast_graphwavenet_${Tag}_station_metrics.csv");$(Join-Path $paper "forecast_stgnn_${Tag}_station_metrics.csv")"
Write-Step "run kbs comparison"
python (Join-Path $paper "scripts\compare_kbs_on_forecast_models.py") *>&1 | Tee-Object -FilePath $log -Append

Write-Step "done"
