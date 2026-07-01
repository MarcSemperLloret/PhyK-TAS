# Analysis Traceability

This file maps paper-facing claims, tables, and figures to repository artifacts. It is intended for reviewers who want to audit the experiment without reading the manuscript source.

## Core Benchmark

| Claim or display | Primary script | Included outputs |
|---|---|---|
| Viable AR6 region set and station counts | `scripts/build_viability_pre_dedup.py`, `scripts/deduplicate_ar6_viability.py`, `scripts/select_viable_regions.py` | `results/all_viable_min100_full_region_audit.csv`, `results/viability_pre_dedup_all_sources.csv`, `results/viability_post_dedup_all_sources.csv`, `results/region_thresholds_all_viable_min100.csv` |
| AR6 station assignment | `scripts/assign_ar6_regions.py` | `results/stations_ar6.csv`, `results/stations_ar6_summary.csv`, `figures/fig_all_viable_region_map.png` |
| Physical descriptor layer | `scripts/build_physical_descriptors.py` | `results/physical_descriptors_station_all_viable_min100.csv`, `results/physical_descriptors_cell5_all_viable_min100.csv`, `results/physical_descriptors_region_all_viable_min100.csv` |
| Generic shift diagnostics | `scripts/build_shift_baselines.py` | `results/distribution_shift_baselines_all_viable_min100.csv`, `results/distribution_shift_baselines_report_all_viable_min100.md` |

## Forecasting And Transfer Degradation

| Claim or display | Primary script | Included outputs |
|---|---|---|
| Regional climatology transfer | `scripts/run_baseline_forecast_experiment.py` | `results/forecast_baseline_all_viable_min100_full_s*_pair_summary.csv`, `results/forecast_baseline_all_viable_min100_full_s*_report.md` |
| Spatial kNN-ridge transfer | `scripts/run_spatial_baseline_experiment.py` | `results/forecast_spatial_baseline_all_viable_min100_full_s*_pair_summary.csv`, `results/forecast_spatial_baseline_all_viable_min100_full_s*_report.md` |
| PatchTST and local linear transfer | `scripts/run_patchtst_experiment.py` | `results/forecast_patchtst_all_viable_min100_full_s*_pair_summary.csv`, `results/forecast_patchtst_all_viable_min100_full_s*_report.md` |
| STGCN diffusion transfer | `scripts/run_stgnn_experiment.py` | `results/forecast_stgnn_all_viable_min100_full_s*_pair_summary.csv`, `results/forecast_stgnn_all_viable_min100_full_s*_report.md` |
| Graph WaveNet transfer | `scripts/run_graphwavenet_experiment.py` | `results/forecast_graphwavenet_all_viable_min100_full_s*_pair_summary.csv`, `results/forecast_graphwavenet_all_viable_min100_full_s*_report.md` |
| Multi-seed aggregation | `scripts/aggregate_experiment_runs.py` | `results/all_viable_min100_full_pair_summary_all.csv`, `results/all_viable_min100_full_pair_uncertainty.csv`, `results/all_viable_min100_full_aggregate_report.md` |

## Information Fusion Analyses

| Paper-facing result | Primary script | Included outputs |
|---|---|---|
| Feature-set comparison: physical vs shift vs combined | `scripts/compare_kbs_on_forecast_models.py`, `scripts/aggregate_experiment_runs.py` | `results/all_viable_min100_full_kbs_results_all.csv`, `results/all_viable_min100_full_kbs_uncertainty.csv`, `figures/fig_all_viable_kbs_r2_by_model.png` |
| Hierarchical-bootstrap significance of physical+shift over shift | `scripts/analyze_v2_significance.py` | `results/v2_significance_all_viable_min100_full.csv`, `results/v2_significance_all_viable_min100_full_report.md` |
| Inference-model fusion and LTRO stress test | `scripts/build_v2_meta_models.py` | `results/v2_meta_models_all_viable_min100_full.csv`, `results/v2_meta_models_all_viable_min100_full_report.md` |
| Monotone shift constraints | `scripts/build_v2_monotonic.py` | `results/v2_monotonic_all_viable_min100_full.csv`, `results/v2_monotonic_all_viable_min100_full_report.md` |
| Split-conformal decision calibration | `scripts/build_v2_conformal.py` | `results/v2_conformal_all_viable_min100_full.csv`, `results/v2_conformal_all_viable_min100_full_report.md` |
| Physical descriptor group ablation | `scripts/run_physical_group_ablation.py` | `results/physical_group_ablation_results_all.csv`, `results/physical_group_ablation_summary.csv`, `figures/fig_physical_group_ablation.png` |
| Negative controls for physical descriptors | `scripts/build_v2_negative_controls.py` | `results/v2_negative_controls_all_viable_min100_full.csv`, `results/v2_negative_controls_all_viable_min100_full_report.md` |
| Compact multi-level fusion ablation | `scripts/build_v2_fusion_ablation_summary.py` | `results/v2_fusion_ablation_summary_all_viable_min100_full.csv`, `results/v2_fusion_ablation_summary_all_viable_min100_full_report.md` |
| Regional-set sensitivity | `scripts/build_v2_region_sensitivity.py` | `results/v2_region_sensitivity_all_viable_min100_full.csv`, `results/v2_region_sensitivity_all_viable_min100_full_report.md` |

## Decision And Robustness Checks

| Paper-facing result | Primary script | Included outputs |
|---|---|---|
| Deploy/adapt/retrain decision counts | `scripts/build_large_seed_decision_layer.py` | `results/large_seed_transfer_decisions.csv`, `results/large_seed_transfer_decision_report.md`, `figures/fig_all_viable_decision_counts.png` |
| Decision validation against observed classes | `scripts/build_review_response_analyses.py` | `results/all_viable_min100_full_decision_validation_pairs.csv`, `results/all_viable_min100_full_decision_validation_summary.csv` |
| Cost-sensitive decision comparison against simple policies | `scripts/build_v2_decision_costs.py` | `results/v2_decision_costs_all_viable_min100_full.csv`, `results/v2_decision_costs_all_viable_min100_full_report.md` |
| Threshold sensitivity | `scripts/run_decision_threshold_sensitivity.py` | `results/all_viable_min100_full_threshold_sensitivity.csv`, `results/all_viable_min100_full_threshold_sensitivity_details.csv`, `figures/fig_all_viable_threshold_sensitivity.png` |
| Source accuracy versus transfer degradation | `scripts/build_review_response_analyses.py` | `results/all_viable_min100_full_source_accuracy_vs_transfer.csv`, `results/all_viable_min100_full_source_accuracy_vs_transfer_summary.csv`, `figures/fig_all_viable_source_accuracy_vs_transfer.png` |
| Relative-degradation scale diagnostic | `scripts/build_review_response_analyses.py` | `results/all_viable_min100_full_relative_degradation_kbs_results.csv`, `results/all_viable_min100_full_relative_degradation_summary.csv` |
| Directional transfer heatmaps | `scripts/build_all_viable_final_artifacts.py`, `scripts/build_publication_figures.py` | `figures/fig_all_viable_degradation_heatmaps.png`, `figures/fig_all_viable_degradation_heatmap_*.png` |

## Manuscript Exclusion Check

No manuscript source is required for the traceability above. The repository should not contain `manuscript_latex/`, `manuscript_latex_eswa/`, or `manuscript_latex_infofusion/`.
