# Aggregate experiment report: all_viable_min100_full

Run tags:

- `all_viable_min100_full_s1`
- `all_viable_min100_full_s2`
- `all_viable_min100_full_s3`

## Best group-by-cell random-forest PhyK-TAS results

| forecast_model           | feature_set         | cv_kind       | estimator     |   n_runs |   mae_mean |      mae_sd |    r2_mean |      r2_sd |     r2_min |      r2_max |       r2_se |   r2_ci95_halfwidth |
|:-------------------------|:--------------------|:--------------|:--------------|---------:|-----------:|------------:|-----------:|-----------:|-----------:|------------:|------------:|--------------------:|
| graphwavenet_transfer    | physical_plus_shift | group_by_cell | random_forest |        3 |  0.0638064 | 0.00296827  |  0.388761  | 0.043022   |  0.343834  |  0.429584   | 0.0248387   |           0.315606  |
| graphwavenet_transfer    | physical_knowledge  | group_by_cell | random_forest |        3 |  0.0767288 | 0.00172929  |  0.303711  | 0.0275216  |  0.27877   |  0.333237   | 0.0158896   |           0.201897  |
| graphwavenet_transfer    | generic_shift       | group_by_cell | random_forest |        3 |  0.0809162 | 0.000290151 |  0.145071  | 0.0127661  |  0.130589  |  0.154694   | 0.00737052  |           0.0936513 |
| linear_window            | generic_shift       | group_by_cell | random_forest |        3 |  1.13627   | 0.0124779   | -0.0101844 | 0.007301   | -0.0186027 | -0.00558297 | 0.00421523  |           0.0535596 |
| linear_window            | physical_knowledge  | group_by_cell | random_forest |        3 |  1.18227   | 0.0233022   | -0.137057  | 0.0912996  | -0.239564  | -0.0644758  | 0.0527119   |           0.669768  |
| linear_window            | physical_plus_shift | group_by_cell | random_forest |        3 |  1.18211   | 0.0238345   | -0.138558  | 0.0949061  | -0.245523  | -0.064435   | 0.0547941   |           0.696224  |
| patchtst_small           | generic_shift       | group_by_cell | random_forest |        3 |  1.14147   | 0.0133569   | -0.0099634 | 0.00719803 | -0.0182706 | -0.00557644 | 0.00415579  |           0.0528043 |
| patchtst_small           | physical_knowledge  | group_by_cell | random_forest |        3 |  1.187     | 0.0256915   | -0.136801  | 0.103403   | -0.253949  | -0.0582426  | 0.0596996   |           0.758556  |
| patchtst_small           | physical_plus_shift | group_by_cell | random_forest |        3 |  1.1868    | 0.0256759   | -0.137006  | 0.10308    | -0.253758  | -0.0585707  | 0.0595135   |           0.756191  |
| regional_doy_climatology | generic_shift       | group_by_cell | random_forest |        3 |  0.10731   | 0.000166597 |  0.966417  | 0.00138943 |  0.96509   |  0.967862   | 0.000802187 |           0.0101928 |
| regional_doy_climatology | physical_plus_shift | group_by_cell | random_forest |        3 |  0.116483  | 0.00923851  |  0.826721  | 0.058974   |  0.762438  |  0.878324   | 0.0340486   |           0.432629  |
| regional_doy_climatology | physical_knowledge  | group_by_cell | random_forest |        3 |  0.658923  | 0.00724456  |  0.0395058 | 0.0090841  |  0.0317011 |  0.0494774  | 0.00524471  |           0.0666403 |
| spatial_knn_ridge        | physical_plus_shift | group_by_cell | random_forest |        3 |  0.0202313 | 0.000908037 |  0.832029  | 0.0198334  |  0.809839  |  0.84803    | 0.0114508   |           0.145497  |
| spatial_knn_ridge        | generic_shift       | group_by_cell | random_forest |        3 |  0.0291958 | 0.000399976 |  0.655541  | 0.00360058 |  0.653273  |  0.659693   | 0.00207879  |           0.0264136 |
| spatial_knn_ridge        | physical_knowledge  | group_by_cell | random_forest |        3 |  0.0600973 | 0.000516127 |  0.305033  | 0.0114471  |  0.295383  |  0.31768    | 0.00660899  |           0.0839752 |
| stgcn_diffusion          | physical_plus_shift | group_by_cell | random_forest |        3 |  0.0506132 | 0.00489245  |  0.373986  | 0.0740188  |  0.324485  |  0.459077   | 0.0427348   |           0.542997  |
| stgcn_diffusion          | physical_knowledge  | group_by_cell | random_forest |        3 |  0.0668585 | 0.00550001  |  0.239426  | 0.0622027  |  0.195526  |  0.310607   | 0.0359127   |           0.456314  |
| stgcn_diffusion          | generic_shift       | group_by_cell | random_forest |        3 |  0.0669332 | 0.00445234  |  0.0832809 | 0.0369316  |  0.0527925 |  0.124347   | 0.0213224   |           0.270927  |

## Conservative decision counts

| model                    | conservative_decision   |   n_pairs |
|:-------------------------|:------------------------|----------:|
| graphwavenet_transfer    | adapt                   |         7 |
| graphwavenet_transfer    | retrain                 |       103 |
| linear_window            | retrain                 |       110 |
| patchtst_small           | retrain                 |       110 |
| regional_doy_climatology | adapt                   |         2 |
| regional_doy_climatology | deploy                  |        46 |
| regional_doy_climatology | retrain                 |        62 |
| spatial_knn_ridge        | adapt                   |        11 |
| spatial_knn_ridge        | deploy                  |        37 |
| spatial_knn_ridge        | retrain                 |        62 |
| stgcn_diffusion          | adapt                   |         5 |
| stgcn_diffusion          | deploy                  |         1 |
| stgcn_diffusion          | retrain                 |       104 |

## Outputs

- `all_viable_min100_full_pair_summary_all.csv`
- `all_viable_min100_full_pair_uncertainty.csv`
- `all_viable_min100_full_kbs_results_all.csv`
- `all_viable_min100_full_kbs_uncertainty.csv`
- `all_viable_min100_full_transfer_decisions.csv`
