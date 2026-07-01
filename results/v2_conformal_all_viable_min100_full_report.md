# PhyK-TAS v2 conformal decision layer (all_viable_min100_full)

One-sided split-conformal upper bound on degradation; deploy threshold 0.01. 200 random calibration/test splits per model. Empirical coverage should be >= target; the unsafe-deploy rate should sit at or below alpha.

| forecast_model           |   n_pairs |   alpha |   target_coverage |   empirical_coverage |   unsafe_deploy_rate |   mean_deploy_per_split |   mean_tested_per_split |
|:-------------------------|----------:|--------:|------------------:|---------------------:|---------------------:|------------------------:|------------------------:|
| graphwavenet_transfer    |       110 |    0.2  |              0.8  |                0.798 |                0     |                   0.02  |                      55 |
| graphwavenet_transfer    |       110 |    0.1  |              0.9  |                0.908 |                0     |                   0     |                      55 |
| graphwavenet_transfer    |       110 |    0.05 |              0.95 |                0.964 |                0     |                   0     |                      55 |
| linear_window            |       110 |    0.2  |              0.8  |                0.808 |                0.002 |                   0.015 |                      55 |
| linear_window            |       110 |    0.1  |              0.9  |                0.906 |                0     |                   0     |                      55 |
| linear_window            |       110 |    0.05 |              0.95 |                0.958 |                0     |                   0     |                      55 |
| patchtst_small           |       110 |    0.2  |              0.8  |                0.794 |                0.005 |                   0.475 |                      55 |
| patchtst_small           |       110 |    0.1  |              0.9  |                0.908 |                0     |                   0     |                      55 |
| patchtst_small           |       110 |    0.05 |              0.95 |                0.965 |                0     |                   0     |                      55 |
| regional_doy_climatology |       110 |    0.2  |              0.8  |                0.798 |                0.113 |                   9.14  |                      55 |
| regional_doy_climatology |       110 |    0.1  |              0.9  |                0.916 |                0.014 |                   5.775 |                      55 |
| regional_doy_climatology |       110 |    0.05 |              0.95 |                0.967 |                0     |                   2.61  |                      55 |
| spatial_knn_ridge        |       110 |    0.2  |              0.8  |                0.805 |                0     |                   8.17  |                      55 |
| spatial_knn_ridge        |       110 |    0.1  |              0.9  |                0.91  |                0     |                   3.2   |                      55 |
| spatial_knn_ridge        |       110 |    0.05 |              0.95 |                0.964 |                0     |                   0.84  |                      55 |
| stgcn_diffusion          |       110 |    0.2  |              0.8  |                0.8   |                0     |                   0.13  |                      55 |
| stgcn_diffusion          |       110 |    0.1  |              0.9  |                0.908 |                0     |                   0     |                      55 |
| stgcn_diffusion          |       110 |    0.05 |              0.95 |                0.965 |                0     |                   0     |                      55 |
