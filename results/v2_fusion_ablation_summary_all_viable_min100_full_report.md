# PhyK-TAS v2 fusion-ablation summary (all_viable_min100_full)

This compact table is intended for reviewer-facing synthesis. It does not introduce new model training; it collates the v2 feature-fusion, model-fusion, monotonicity, and conformal-decision analyses.

| forecast_model           | stage                | metric                                   |   value | context                                     |
|:-------------------------|:---------------------|:-----------------------------------------|--------:|:--------------------------------------------|
| graphwavenet_transfer    | feature_fusion       | delta_r2_physical_plus_shift_minus_shift |  0.2428 | group_by_cell random_forest                 |
| linear_window            | feature_fusion       | delta_r2_physical_plus_shift_minus_shift | -0.1292 | group_by_cell random_forest                 |
| patchtst_small           | feature_fusion       | delta_r2_physical_plus_shift_minus_shift | -0.128  | group_by_cell random_forest                 |
| regional_doy_climatology | feature_fusion       | delta_r2_physical_plus_shift_minus_shift | -0.1396 | group_by_cell random_forest                 |
| spatial_knn_ridge        | feature_fusion       | delta_r2_physical_plus_shift_minus_shift |  0.1765 | group_by_cell random_forest                 |
| stgcn_diffusion          | feature_fusion       | delta_r2_physical_plus_shift_minus_shift |  0.2873 | group_by_cell random_forest                 |
| graphwavenet_transfer    | inference_model      | r2_random_forest                         |  0.1363 | leave_target_region_out physical_plus_shift |
| graphwavenet_transfer    | inference_model      | r2_mixedlm_pool                          | -1.2295 | leave_target_region_out physical_plus_shift |
| graphwavenet_transfer    | inference_model      | r2_fusion_stack                          |  0.1292 | leave_target_region_out physical_plus_shift |
| linear_window            | inference_model      | r2_random_forest                         | -0.0461 | leave_target_region_out physical_plus_shift |
| linear_window            | inference_model      | r2_mixedlm_pool                          | -0.0027 | leave_target_region_out physical_plus_shift |
| linear_window            | inference_model      | r2_fusion_stack                          | -0      | leave_target_region_out physical_plus_shift |
| patchtst_small           | inference_model      | r2_random_forest                         | -0.0526 | leave_target_region_out physical_plus_shift |
| patchtst_small           | inference_model      | r2_mixedlm_pool                          | -0.0032 | leave_target_region_out physical_plus_shift |
| patchtst_small           | inference_model      | r2_fusion_stack                          |  0.0001 | leave_target_region_out physical_plus_shift |
| regional_doy_climatology | inference_model      | r2_random_forest                         | -0.6955 | leave_target_region_out physical_plus_shift |
| regional_doy_climatology | inference_model      | r2_mixedlm_pool                          |  0.8593 | leave_target_region_out physical_plus_shift |
| regional_doy_climatology | inference_model      | r2_fusion_stack                          |  0.857  | leave_target_region_out physical_plus_shift |
| spatial_knn_ridge        | inference_model      | r2_random_forest                         | -0.9695 | leave_target_region_out physical_plus_shift |
| spatial_knn_ridge        | inference_model      | r2_mixedlm_pool                          |  0.2642 | leave_target_region_out physical_plus_shift |
| spatial_knn_ridge        | inference_model      | r2_fusion_stack                          |  0.3155 | leave_target_region_out physical_plus_shift |
| stgcn_diffusion          | inference_model      | r2_random_forest                         |  0.0023 | leave_target_region_out physical_plus_shift |
| stgcn_diffusion          | inference_model      | r2_mixedlm_pool                          | -0.0635 | leave_target_region_out physical_plus_shift |
| stgcn_diffusion          | inference_model      | r2_fusion_stack                          |  0.1136 | leave_target_region_out physical_plus_shift |
| graphwavenet_transfer    | monotone_prior       | r2_hist_gbm                              |  0.1984 | leave_target_region_out physical_plus_shift |
| graphwavenet_transfer    | monotone_prior       | r2_hist_gbm_mono                         |  0.1522 | leave_target_region_out physical_plus_shift |
| linear_window            | monotone_prior       | r2_hist_gbm                              | -0.0196 | leave_target_region_out physical_plus_shift |
| linear_window            | monotone_prior       | r2_hist_gbm_mono                         | -0.0185 | leave_target_region_out physical_plus_shift |
| patchtst_small           | monotone_prior       | r2_hist_gbm                              | -0.0265 | leave_target_region_out physical_plus_shift |
| patchtst_small           | monotone_prior       | r2_hist_gbm_mono                         | -0.0236 | leave_target_region_out physical_plus_shift |
| regional_doy_climatology | monotone_prior       | r2_hist_gbm                              | -0.416  | leave_target_region_out physical_plus_shift |
| regional_doy_climatology | monotone_prior       | r2_hist_gbm_mono                         |  0.124  | leave_target_region_out physical_plus_shift |
| spatial_knn_ridge        | monotone_prior       | r2_hist_gbm                              | -0.4041 | leave_target_region_out physical_plus_shift |
| spatial_knn_ridge        | monotone_prior       | r2_hist_gbm_mono                         | -0.3242 | leave_target_region_out physical_plus_shift |
| stgcn_diffusion          | monotone_prior       | r2_hist_gbm                              |  0.0225 | leave_target_region_out physical_plus_shift |
| stgcn_diffusion          | monotone_prior       | r2_hist_gbm_mono                         |  0.09   | leave_target_region_out physical_plus_shift |
| graphwavenet_transfer    | decision_calibration | unsafe_deploy_rate_alpha_0.10            |  0      | coverage=0.908; deploy/split=0.00           |
| linear_window            | decision_calibration | unsafe_deploy_rate_alpha_0.10            |  0      | coverage=0.906; deploy/split=0.00           |
| patchtst_small           | decision_calibration | unsafe_deploy_rate_alpha_0.10            |  0      | coverage=0.908; deploy/split=0.00           |
| regional_doy_climatology | decision_calibration | unsafe_deploy_rate_alpha_0.10            |  0.0136 | coverage=0.916; deploy/split=5.78           |
| spatial_knn_ridge        | decision_calibration | unsafe_deploy_rate_alpha_0.10            |  0      | coverage=0.910; deploy/split=3.20           |
| stgcn_diffusion          | decision_calibration | unsafe_deploy_rate_alpha_0.10            |  0      | coverage=0.908; deploy/split=0.00           |
