# Reproducibility Guide

This repository is designed to let reviewers inspect the PhyK-TAS experiment without the LaTeX manuscript. It contains the analysis code, aggregate result tables, figures, and protocol notes. It does not contain raw station archives or large generated forecasting tensors.

## Scope

There are three reproducibility levels.

1. **Audit the reported results from included artifacts.** This can be done directly from `results/` and `figures/` and is the intended reviewer path.
2. **Regenerate final aggregate tables and figures.** This can be done if the included intermediate result tables are present.
3. **Rebuild the complete forecasting benchmark from raw station archives.** This requires external public station archives and the local harmonization pipeline, which are not bundled here because of size and source-specific distribution constraints.

## Environment Setup

Use Python 3.11 or newer. The original run used Python 3.13 on Windows.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

GPU support is only needed for the neural forecasting scripts (`run_patchtst_experiment.py`, `run_stgnn_experiment.py`, and `run_graphwavenet_experiment.py`). The audit and final-analysis scripts run on CPU once their CSV inputs exist.

## Quick Audit

Run the release validator:

```powershell
python scripts/validate_release_artifacts.py
```

This checks that the expected core result files, figures, and documentation are present, and that excluded manuscript folders are absent.

## Regenerating Final Analyses From Included Tables

The following commands rebuild the final v2 analysis summaries when their input tables are present in `results/`:

```powershell
python scripts/analyze_v2_significance.py
python scripts/build_v2_meta_models.py
python scripts/build_v2_monotonic.py
python scripts/build_v2_conformal.py
python scripts/build_v2_negative_controls.py
python scripts/build_v2_decision_costs.py
python scripts/build_v2_fusion_ablation_summary.py
python scripts/build_v2_region_sensitivity.py
python scripts/build_all_viable_final_artifacts.py
python scripts/build_publication_figures.py
```

Some scripts were originally written to run from the `Paper1` project root and may expect outputs in the current directory. If running them from this repository, either run from the repository root and keep the included `results/` files in place, or copy the needed inputs to the script's expected working directory. `TRACEABILITY.md` lists the specific input and output files for each paper-facing result.

The negative-control script defaults to the primary group-by-cell setting for the spatial and graph-based forecasters and uses aggregated source-target-cell-seed rows to keep the permutation test tractable. Its behavior can be changed with `PHYKTAS_NEG_REPEATS`, `PHYKTAS_NEG_TREES`, `PHYKTAS_NEG_CV`, and `PHYKTAS_NEG_MODELS`.

## Regenerating Forecasting Outputs

The expensive forecasting pipeline requires the harmonized station dataset and generated `.npz` tensors, which are not included in GitHub. The original high-level order was:

```powershell
python scripts/build_viability_pre_dedup.py
python scripts/deduplicate_ar6_viability.py
python scripts/assign_ar6_regions.py
python scripts/build_physical_descriptors.py
python scripts/build_shift_baselines.py
python scripts/build_forecasting_dataset_large.py
.\scripts\run_all_viable_seed.ps1
python scripts/aggregate_experiment_runs.py
```

The forecast-model scripts are:

- `scripts/run_baseline_forecast_experiment.py`
- `scripts/run_spatial_baseline_experiment.py`
- `scripts/run_patchtst_experiment.py`
- `scripts/run_stgnn_experiment.py`
- `scripts/run_graphwavenet_experiment.py`

These scripts produce the model-level pair summaries and station metrics that are already represented in aggregate form under `results/`.

## Excluded Large Artifacts

The following classes of files are intentionally excluded:

- Raw station archives and harmonized source databases.
- Generated `.npz` tensors used for neural forecasting.
- Console logs and Python caches.
- Prediction-level CSV files near or above GitHub's single-file size limit.
- All manuscript folders.

The included aggregate tables are sufficient to inspect the reported feature-set comparisons, hierarchical bootstrap results, model-fusion results, monotonicity analyses, conformal decision summaries, source-accuracy diagnostics, and threshold sensitivity analyses.
