param(
    [int]$STGCNEpochs = 5,
    [int]$GraphWaveNetEpochs = 8
)

# Eje 1: re-run the forecaster suite over the existing full datasets with
# per-(station, day) prediction export enabled, then build the label-free
# agreement features per seed and the pooled estimator comparison.
# Original artifacts are untouched: outputs use the "<source-tag>_export" tag.

$ErrorActionPreference = "Stop"
$paper = Resolve-Path "$PSScriptRoot\.."

$runs = @(
    @{ SourceTag = "all_viable_min100_full_s1"; Seed = 20260602 },
    @{ SourceTag = "all_viable_min100_full_s2"; Seed = 20260603 },
    @{ SourceTag = "all_viable_min100_full_s3"; Seed = 20260604 }
)

foreach ($run in $runs) {
    $srcTag = $run.SourceTag
    $tag = "${srcTag}_export"
    $log = Join-Path $paper "${tag}_run.log"

    function Write-Step($message) {
        $stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        "[$stamp] $message" | Tee-Object -FilePath $log -Append
    }

    $env:FORECAST_EXPERIMENT_TAG = $tag
    $env:FORECAST_DATA = Join-Path $paper "forecast_dataset_large_${srcTag}.npz"
    $env:FORECAST_META = Join-Path $paper "forecast_dataset_large_${srcTag}_metadata.csv"
    $env:FORECAST_RANDOM_SEED = "$($run.Seed)"
    $env:FORECAST_MODEL_SEED = "$($run.Seed)"
    $env:FORECAST_EXPORT_PREDICTIONS = "1"

    Write-Step "start export run tag=$tag seed=$($run.Seed) stgcn_epochs=$STGCNEpochs graphwavenet_epochs=$GraphWaveNetEpochs"

    Write-Step "run regional climatology and persistence"
    python (Join-Path $paper "scripts\run_baseline_forecast_experiment.py") *>&1 | Tee-Object -FilePath $log -Append

    Write-Step "run spatial kNN-ridge baseline"
    python (Join-Path $paper "scripts\run_spatial_baseline_experiment.py") *>&1 | Tee-Object -FilePath $log -Append

    Write-Step "run STGCN diffusion"
    $env:FORECAST_EPOCHS = "$STGCNEpochs"
    python (Join-Path $paper "scripts\run_stgnn_experiment.py") *>&1 | Tee-Object -FilePath $log -Append

    Write-Step "run Graph WaveNet transfer"
    $env:FORECAST_EPOCHS = "$GraphWaveNetEpochs"
    python (Join-Path $paper "scripts\run_graphwavenet_experiment.py") *>&1 | Tee-Object -FilePath $log -Append

    Write-Step "run linear window and PatchTST"
    python (Join-Path $paper "scripts\run_patchtst_experiment.py") *>&1 | Tee-Object -FilePath $log -Append

    Write-Step "build agreement features"
    python (Join-Path $paper "scripts\build_v2_agreement_features.py") *>&1 | Tee-Object -FilePath $log -Append

    Write-Step "done tag=$tag"
}

$finalLog = Join-Path $paper "eje1_agreement_estimators.log"
"[{0}] pooled agreement estimator comparison" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss") | Tee-Object -FilePath $finalLog -Append
python (Join-Path $paper "scripts\build_v2_agreement_estimators.py") *>&1 | Tee-Object -FilePath $finalLog -Append
"[{0}] all done" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss") | Tee-Object -FilePath $finalLog -Append
