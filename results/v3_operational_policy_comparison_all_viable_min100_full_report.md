# Operational policy comparison (all_viable_min100_full)

Repeated split-conformal evaluation, 300 splits, deploy <= 0.010, adapt <= 0.025. Main table shown for alpha=0.10; the CSV contains all alphas.

| forecast_model           | policy                                 |   point_r2 |   empirical_coverage |   mean_bound_width |   deploy_rate |   unsafe_deploy_rate |   mean_cost |
|:-------------------------|:---------------------------------------|-----------:|---------------------:|-------------------:|--------------:|---------------------:|------------:|
| graphwavenet_transfer    | reliability_fusion_conflict_stratified |     0.7555 |               0.9299 |             0.0302 |        0      |               0      |      0.6347 |
| graphwavenet_transfer    | reliability_fusion_global              |     0.7555 |               0.913  |             0.0384 |        0      |               0      |      0.6816 |
| graphwavenet_transfer    | concat_global                          |     0.489  |               0.9137 |             0.0505 |        0      |               0      |      0.687  |
| graphwavenet_transfer    | fixed_source_fusion_global             |     0.8003 |               0.9076 |             0.0349 |        0      |               0      |      0.6986 |
| linear_window            | reliability_fusion_conflict_stratified |    -0.9672 |               0.929  |             0.1886 |        0.0244 |               0.2889 |      1.0919 |
| linear_window            | fixed_source_fusion_global             |    -0.9864 |               0.9161 |             0.1402 |        0.0707 |               0.4333 |      1.342  |
| linear_window            | reliability_fusion_global              |    -0.9672 |               0.9087 |             0.1347 |        0.0695 |               0.4534 |      1.3562 |
| linear_window            | concat_global                          |    -2.1805 |               0.9101 |             0.1956 |        0.0802 |               0.607  |      1.5113 |
| patchtst_small           | reliability_fusion_conflict_stratified |    -1.5669 |               0.9242 |             0.23   |        0.0204 |               0.3591 |      1.1048 |
| patchtst_small           | fixed_source_fusion_global             |    -1.6191 |               0.9109 |             0.1711 |        0.0752 |               0.4941 |      1.3993 |
| patchtst_small           | reliability_fusion_global              |    -1.5669 |               0.9119 |             0.1674 |        0.0758 |               0.5054 |      1.4127 |
| patchtst_small           | concat_global                          |    -4.0386 |               0.9128 |             0.2846 |        0.0819 |               0.6155 |      1.5057 |
| regional_doy_climatology | reliability_fusion_conflict_stratified |     0.9849 |               0.9258 |             0.1744 |        0.3484 |               0      |      0.3074 |
| regional_doy_climatology | concat_global                          |     0.5584 |               0.9059 |             0.12   |        0.2753 |               0      |      0.5056 |
| regional_doy_climatology | reliability_fusion_global              |     0.9849 |               0.9123 |             0.3148 |        0.2751 |               0      |      0.5419 |
| regional_doy_climatology | fixed_source_fusion_global             |     0.8044 |               0.9035 |             0.8446 |        0.071  |               0      |      1.1467 |
| spatial_knn_ridge        | concat_global                          |     0.962  |               0.9136 |             0.0259 |        0.2538 |               0      |      0.4665 |
| spatial_knn_ridge        | reliability_fusion_conflict_stratified |     0.9312 |               0.9235 |             0.0319 |        0.2418 |               0.0026 |      0.4748 |
| spatial_knn_ridge        | reliability_fusion_global              |     0.9312 |               0.9101 |             0.0346 |        0.2302 |               0      |      0.572  |
| spatial_knn_ridge        | fixed_source_fusion_global             |     0.8486 |               0.9108 |             0.0481 |        0.0978 |               0      |      0.9327 |
| stgcn_diffusion          | reliability_fusion_conflict_stratified |     0.6938 |               0.9253 |             0.0669 |        0      |               0      |      0.6745 |
| stgcn_diffusion          | reliability_fusion_global              |     0.6938 |               0.9093 |             0.0344 |        0      |               0      |      0.7699 |
| stgcn_diffusion          | concat_global                          |     0.647  |               0.904  |             0.0349 |        0      |               0      |      0.7707 |
| stgcn_diffusion          | fixed_source_fusion_global             |     0.7156 |               0.9125 |             0.0331 |        0      |               0      |      0.7853 |
