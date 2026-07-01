# PhyK-TAS

PhyK-TAS is an experimental decision-support pipeline for assessing transferability risk in spatiotemporal precipitation forecasters. It fuses physical precipitation-regime descriptors, generic distribution-shift diagnostics, and complementary degradation-inference models to estimate whether a source-trained forecaster should be deployed, adapted, or retrained in a target climate regime.

This repository contains the experiment code and derived result artifacts. It intentionally does not contain the LaTeX manuscript.

For reviewer-facing reproduction details, see `REPRODUCIBILITY.md`. For a direct mapping from paper-facing claims and figures to scripts and files, see `TRACEABILITY.md`.

## Repository Contents

- `scripts/`: experiment, aggregation, inference, conformal calibration, and figure-generation scripts.
- `results/`: derived descriptors, shift metrics, transfer-degradation summaries, decision-layer outputs, bootstrap/significance analyses, model-fusion analyses, monotonicity analyses, and conformal decision summaries.
- `figures/`: generated figures used to inspect and summarize the experiment.
- `docs/`: local protocol notes, benchmark design notes, and audit summaries.
- `REPRODUCIBILITY.md`: quick audit path, environment setup, and rebuild scope.
- `TRACEABILITY.md`: mapping from paper-facing results to scripts and artifacts.

Large raw station archives, generated `.npz` forecasting tensors, console logs, Python caches, and manuscript folders are excluded from this repository. Several large prediction-level CSV files are also excluded because they are close to or above GitHub's single-file size limit; the aggregate tables needed to inspect the reported results are included in `results/`.

## Main Experiment Artifacts

The current Information Fusion version is centered on the all-viable 11-region benchmark:

- `results/all_viable_min100_full_aggregate_report.md`
- `results/all_viable_min100_full_sanity_report.md`
- `results/all_viable_min100_full_kbs_results_all.csv`
- `results/all_viable_min100_full_pair_summary_all.csv`
- `results/v2_significance_all_viable_min100_full_report.md`
- `results/v2_meta_models_all_viable_min100_full_report.md`
- `results/v2_monotonic_all_viable_min100_full_report.md`
- `results/v2_conformal_all_viable_min100_full_report.md`

The principal scripts for rebuilding the final analysis tables are:

- `scripts/aggregate_experiment_runs.py`
- `scripts/build_all_viable_final_artifacts.py`
- `scripts/analyze_v2_significance.py`
- `scripts/build_v2_meta_models.py`
- `scripts/build_v2_monotonic.py`
- `scripts/build_v2_conformal.py`
- `scripts/build_publication_figures.py`

## Quick Validation

After cloning the repository, run:

```powershell
python scripts/validate_release_artifacts.py
```

The validator checks that core outputs are present, that manuscript folders are absent, and that no included file is near GitHub's 100 MB single-file limit.

## Environment

The scripts were developed with Python 3.13 on Windows. Core dependencies are listed in `requirements.txt`. GPU acceleration is optional for the neural forecasting scripts, but the final aggregation and analysis scripts run on CPU once their input tables exist.

## Data Notes

The benchmark is derived from public daily precipitation archives, harmonized outside this repository. The included `results/` tables are derived artifacts for the experiment. Rebuilding the complete forecasting pipeline from raw data requires the external station archives and the local harmonization pipeline.

The repository is therefore a reproducibility package for the analysis and derived results, not a mirror of the raw meteorological archives.

## Citation And License

Code is released under the MIT License. Citation metadata are provided in `CITATION.cff`.

## Manuscript Exclusion

The manuscript folders are deliberately not included:

- `manuscript_latex/`
- `manuscript_latex_eswa/`
- `manuscript_latex_infofusion/`

This repository is intended to hold the experiment code and derived artifacts only.
