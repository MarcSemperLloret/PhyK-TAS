# PhyK-TAS v2 cost-sensitive decision evaluation (all_viable_min100_full)

Cost matrix: unsafe deploy to an adapt case = 5; unsafe deploy to a retrain case = 10; unnecessary retrain of a deploy case = 3; adapt instead of deploy = 1; retrain instead of adapt = 1; adapt instead of retrain = 4. These costs are illustrative and test decision asymmetry.

## observed_expected_decision

| forecast_model           | observed_reference         | policy                |   mean_cost |   unsafe_deploy_rate |   unnecessary_retrain_rate |   deploy_rate |   adapt_rate |   retrain_rate |   n_pairs |
|:-------------------------|:---------------------------|:----------------------|------------:|---------------------:|---------------------------:|--------------:|-------------:|---------------:|----------:|
| graphwavenet_transfer    | observed_expected_decision | phyk_tas_expected     |      0.3818 |               0      |                     0.0545 |        0.0182 |       0.1455 |         0.8364 |       110 |
| graphwavenet_transfer    | observed_expected_decision | predicted_mean        |      0.3818 |               0      |                     0.0545 |        0.0182 |       0.1455 |         0.8364 |       110 |
| graphwavenet_transfer    | observed_expected_decision | phyk_tas_conservative |      0.5273 |               0      |                     0.1    |        0      |       0.0818 |         0.9182 |       110 |
| linear_window            | observed_expected_decision | phyk_tas_conservative |      1.0455 |               0      |                     0.3182 |        0.0273 |       0      |         0.9727 |       110 |
| linear_window            | observed_expected_decision | phyk_tas_expected     |      1.0545 |               0.1    |                     0      |        0.4182 |       0.1182 |         0.4636 |       110 |
| linear_window            | observed_expected_decision | predicted_mean        |      1.0545 |               0.1    |                     0      |        0.4182 |       0.1182 |         0.4636 |       110 |
| patchtst_small           | observed_expected_decision | phyk_tas_conservative |      1.0273 |               0      |                     0.3    |        0.0182 |       0.0091 |         0.9727 |       110 |
| patchtst_small           | observed_expected_decision | phyk_tas_expected     |      1.0364 |               0.1091 |                     0      |        0.4182 |       0.0909 |         0.4909 |       110 |
| patchtst_small           | observed_expected_decision | predicted_mean        |      1.0364 |               0.1091 |                     0      |        0.4182 |       0.0909 |         0.4909 |       110 |
| regional_doy_climatology | observed_expected_decision | phyk_tas_expected     |      0.0455 |               0.0091 |                     0      |        0.4545 |       0.0273 |         0.5182 |       110 |
| regional_doy_climatology | observed_expected_decision | predicted_mean        |      0.0455 |               0.0091 |                     0      |        0.4545 |       0.0273 |         0.5182 |       110 |
| regional_doy_climatology | observed_expected_decision | phyk_tas_conservative |      0.0545 |               0      |                     0.0091 |        0.4364 |       0.0091 |         0.5545 |       110 |
| spatial_knn_ridge        | observed_expected_decision | phyk_tas_expected     |      0.2727 |               0.0091 |                     0      |        0.4182 |       0.1091 |         0.4727 |       110 |
| spatial_knn_ridge        | observed_expected_decision | predicted_mean        |      0.2727 |               0.0091 |                     0      |        0.4182 |       0.1091 |         0.4727 |       110 |
| spatial_knn_ridge        | observed_expected_decision | phyk_tas_conservative |      0.3    |               0      |                     0.0545 |        0.3364 |       0.1    |         0.5636 |       110 |
| stgcn_diffusion          | observed_expected_decision | phyk_tas_expected     |      0.3455 |               0      |                     0.0455 |        0.0273 |       0.2182 |         0.7545 |       110 |
| stgcn_diffusion          | observed_expected_decision | predicted_mean        |      0.3455 |               0      |                     0.0455 |        0.0273 |       0.2182 |         0.7545 |       110 |
| stgcn_diffusion          | observed_expected_decision | phyk_tas_conservative |      0.5455 |               0      |                     0.1    |        0.0182 |       0.0909 |         0.8909 |       110 |

## observed_conservative_decision

| forecast_model           | observed_reference             | policy                |   mean_cost |   unsafe_deploy_rate |   unnecessary_retrain_rate |   deploy_rate |   adapt_rate |   retrain_rate |   n_pairs |
|:-------------------------|:-------------------------------|:----------------------|------------:|---------------------:|---------------------------:|--------------:|-------------:|---------------:|----------:|
| graphwavenet_transfer    | observed_conservative_decision | always_retrain        |      0.0636 |               0      |                     0      |        0      |       0      |         1      |       110 |
| graphwavenet_transfer    | observed_conservative_decision | phyk_tas_conservative |      0.1182 |               0      |                     0      |        0      |       0.0818 |         0.9182 |       110 |
| graphwavenet_transfer    | observed_conservative_decision | phyk_tas_expected     |      0.5    |               0.0182 |                     0      |        0.0182 |       0.1455 |         0.8364 |       110 |
| linear_window            | observed_conservative_decision | always_retrain        |      0      |               0      |                     0      |        0      |       0      |         1      |       110 |
| linear_window            | observed_conservative_decision | phyk_tas_conservative |      0.2727 |               0.0273 |                     0      |        0.0273 |       0      |         0.9727 |       110 |
| linear_window            | observed_conservative_decision | shift_rank            |      3.3818 |               0.2364 |                     0      |        0.2364 |       0.2545 |         0.5091 |       110 |
| patchtst_small           | observed_conservative_decision | always_retrain        |      0      |               0      |                     0      |        0      |       0      |         1      |       110 |
| patchtst_small           | observed_conservative_decision | phyk_tas_conservative |      0.2182 |               0.0182 |                     0      |        0.0182 |       0.0091 |         0.9727 |       110 |
| patchtst_small           | observed_conservative_decision | shift_rank            |      3.3818 |               0.2364 |                     0      |        0.2364 |       0.2545 |         0.5091 |       110 |
| regional_doy_climatology | observed_conservative_decision | phyk_tas_conservative |      0.1364 |               0.0182 |                     0      |        0.4364 |       0.0091 |         0.5545 |       110 |
| regional_doy_climatology | observed_conservative_decision | phyk_tas_expected     |      0.3818 |               0.0364 |                     0      |        0.4545 |       0.0273 |         0.5182 |       110 |
| regional_doy_climatology | observed_conservative_decision | predicted_mean        |      0.3818 |               0.0364 |                     0      |        0.4545 |       0.0273 |         0.5182 |       110 |
| spatial_knn_ridge        | observed_conservative_decision | phyk_tas_conservative |      0.5818 |               0.0455 |                     0.0364 |        0.3364 |       0.1    |         0.5636 |       110 |
| spatial_knn_ridge        | observed_conservative_decision | phyk_tas_expected     |      0.8455 |               0.0909 |                     0      |        0.4182 |       0.1091 |         0.4727 |       110 |
| spatial_knn_ridge        | observed_conservative_decision | predicted_mean        |      0.8455 |               0.0909 |                     0      |        0.4182 |       0.1091 |         0.4727 |       110 |
| stgcn_diffusion          | observed_conservative_decision | always_retrain        |      0.0727 |               0      |                     0.0091 |        0      |       0      |         1      |       110 |
| stgcn_diffusion          | observed_conservative_decision | phyk_tas_conservative |      0.3545 |               0.0091 |                     0      |        0.0182 |       0.0909 |         0.8909 |       110 |
| stgcn_diffusion          | observed_conservative_decision | phyk_tas_expected     |      0.8636 |               0.0182 |                     0      |        0.0273 |       0.2182 |         0.7545 |       110 |
