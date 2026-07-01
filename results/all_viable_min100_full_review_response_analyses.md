# Review-response analyses

## Decision validation

| model                    | reference    |   n_pairs |   accuracy |   balanced_accuracy |   predicted_deploy |   unsafe_deploy |   unsafe_deploy_rate_among_predicted_deploy |   predicted_retrain |   unnecessary_retrain |   unnecessary_retrain_rate_among_predicted_retrain | confusion_matrix_deploy_adapt_retrain   |
|:-------------------------|:-------------|----------:|-----------:|--------------------:|-------------------:|----------------:|--------------------------------------------:|--------------------:|----------------------:|---------------------------------------------------:|:----------------------------------------|
| regional_doy_climatology | expected     |       110 |   0.963636 |            0.743197 |                 48 |               0 |                                   0         |                  61 |                     1 |                                          0.0163934 | [[48, 0, 1], [0, 1, 3], [0, 0, 57]]     |
| regional_doy_climatology | conservative |       110 |   0.981818 |            0.827957 |                 48 |               2 |                                   0.0416667 |                  61 |                     0 |                                          0         | [[46, 0, 0], [1, 1, 0], [1, 0, 61]]     |
| spatial_knn_ridge        | expected     |       110 |   0.863636 |            0.800595 |                 37 |               0 |                                   0         |                  62 |                     6 |                                          0.0967742 | [[37, 5, 6], [0, 4, 2], [0, 2, 54]]     |
| spatial_knn_ridge        | conservative |       110 |   0.836364 |            0.710576 |                 37 |               5 |                                   0.135135  |                  62 |                     4 |                                          0.0645161 | [[32, 1, 4], [5, 4, 2], [0, 6, 56]]     |
| linear_window            | expected     |       110 |   0.590909 |            0.359649 |                  3 |               0 |                                   0         |                 107 |                    35 |                                          0.327103  | [[3, 0, 35], [0, 0, 10], [0, 0, 62]]    |
| linear_window            | conservative |       110 |   0.972727 |            0.972727 |                  3 |               3 |                                   1         |                 107 |                     0 |                                          0         | [[0, 0, 0], [0, 0, 0], [3, 0, 107]]     |
| patchtst_small           | expected     |       110 |   0.572727 |            0.351852 |                  2 |               0 |                                   0         |                 107 |                    33 |                                          0.308411  | [[2, 1, 33], [0, 0, 13], [0, 0, 61]]    |
| patchtst_small           | conservative |       110 |   0.972727 |            0.972727 |                  2 |               2 |                                   1         |                 107 |                     0 |                                          0         | [[0, 0, 0], [0, 0, 0], [2, 1, 107]]     |
| stgcn_diffusion          | expected     |       110 |   0.654545 |            0.362319 |                  2 |               0 |                                   0         |                  98 |                    11 |                                          0.112245  | [[2, 10, 11], [0, 0, 17], [0, 0, 70]]   |
| stgcn_diffusion          | conservative |       110 |   0.9      |            0.774359 |                  2 |               1 |                                   0.5       |                  98 |                     0 |                                          0         | [[1, 0, 0], [1, 2, 2], [0, 8, 96]]      |
| graphwavenet_transfer    | expected     |       110 |   0.672727 |            0.333333 |                  0 |               0 |                                   0         |                 101 |                    11 |                                          0.108911  | [[0, 9, 11], [0, 0, 16], [0, 0, 74]]    |
| graphwavenet_transfer    | conservative |       110 |   0.963636 |            0.914008 |                  0 |               0 |                                   0         |                 101 |                     0 |                                          0         | [[0, 0, 0], [0, 6, 1], [0, 3, 100]]     |

## Best relative-degradation KBS results

| forecast_model           | feature_set         | cv_kind                 | estimator     |   n_runs |   mae_mean |      mae_sd |    r2_mean |     r2_sd |       r2_min |     r2_max |
|:-------------------------|:--------------------|:------------------------|:--------------|---------:|-----------:|------------:|-----------:|----------:|-------------:|-----------:|
| graphwavenet_transfer    | physical_knowledge  | leave_target_region_out | random_forest |        3 |  0.025498  | 0.00128027  | -0.190478  | 0.110643  | -0.28251     | -0.0677199 |
| linear_window            | physical_plus_shift | leave_target_region_out | random_forest |        3 |  0.0376904 | 0.00187788  | -0.1121    | 0.124253  | -0.254961    | -0.0291834 |
| patchtst_small           | generic_shift       | leave_target_region_out | random_forest |        3 |  0.0380082 | 0.00236941  | -0.139943  | 0.0206511 | -0.161128    | -0.11987   |
| regional_doy_climatology | physical_knowledge  | leave_target_region_out | random_forest |        3 |  0.243553  | 0.00187669  |  0.0122568 | 0.0112747 |  0.000484339 |  0.0229572 |
| spatial_knn_ridge        | physical_knowledge  | leave_target_region_out | random_forest |        3 |  0.0367906 | 7.75974e-05 |  0.0660287 | 0.0125552 |  0.0537097   |  0.0788074 |
| stgcn_diffusion          | distance_only       | leave_target_region_out | random_forest |        3 |  0.01581   | 0.000640193 |  0.327703  | 0.0810538 |  0.234386    |  0.380576  |

Outputs:

- `all_viable_min100_full_decision_validation_pairs.csv`
- `all_viable_min100_full_decision_validation_summary.csv`
- `all_viable_min100_full_relative_degradation_kbs_results.csv`
- `all_viable_min100_full_relative_degradation_summary.csv`
