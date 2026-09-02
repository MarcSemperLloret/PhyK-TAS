# Operational policy comparison with the agreement source (all_viable_min100_full)

Same protocol as v3_operational_policy_comparison (300 splits, deploy <= 0.010, adapt <= 0.025), on the agreement-run out-of-fold predictions so all six policies share identical targets. Shown for alpha=0.10.

| forecast_model           | policy                                      |   point_r2 |   empirical_coverage |   mean_bound_width |   deploy_rate |   unsafe_deploy_rate |   mean_cost |
|:-------------------------|:--------------------------------------------|-----------:|---------------------:|-------------------:|--------------:|---------------------:|------------:|
| graphwavenet_transfer    | concat_global                               |     0.8406 |               0.9133 |             0.0412 |        0      |               0      |      0.6569 |
| graphwavenet_transfer    | fixed_source_fusion_global                  |     0.893  |               0.9099 |             0.0341 |        0      |               0      |      0.67   |
| graphwavenet_transfer    | reliability_fusion_global                   |     0.8795 |               0.9096 |             0.0358 |        0      |               0      |      0.6522 |
| graphwavenet_transfer    | reliability_fusion_conflict_stratified      |     0.8795 |               0.9389 |             0.0292 |        0      |               0      |      0.591  |
| graphwavenet_transfer    | three_source_excl_local_global              |     0.6578 |               0.9102 |             0.0455 |        0      |               0      |      0.6693 |
| graphwavenet_transfer    | three_source_excl_local_conflict_stratified |     0.6578 |               0.9324 |             0.0293 |        0.0092 |               0.0082 |      0.4926 |
| linear_window            | concat_global                               |    -2.1141 |               0.9114 |             0.0164 |        0.003  |               0      |      0.7856 |
| linear_window            | fixed_source_fusion_global                  |     0.2175 |               0.9145 |             0.0271 |        0      |               0      |      1.1437 |
| linear_window            | reliability_fusion_global                   |     0.217  |               0.9112 |             0.0243 |        0      |               0      |      1.1213 |
| linear_window            | reliability_fusion_conflict_stratified      |     0.217  |               0.942  |             0.028  |        0.009  |               0      |      0.7068 |
| linear_window            | three_source_excl_local_global              |     0.01   |               0.9116 |             0.0175 |        0.0009 |               0      |      0.7969 |
| linear_window            | three_source_excl_local_conflict_stratified |     0.01   |               0.9403 |             0.0184 |        0.0891 |               0      |      0.4382 |
| patchtst_small           | concat_global                               |     0.8395 |               0.9108 |             0.0173 |        0.0001 |               0      |      0.8592 |
| patchtst_small           | fixed_source_fusion_global                  |     0.7771 |               0.912  |             0.0349 |        0      |               0      |      1.1741 |
| patchtst_small           | reliability_fusion_global                   |     0.7606 |               0.9123 |             0.0363 |        0      |               0      |      1.1647 |
| patchtst_small           | reliability_fusion_conflict_stratified      |     0.7606 |               0.9373 |             0.0339 |        0.007  |               0      |      0.7408 |
| patchtst_small           | three_source_excl_local_global              |     0.8247 |               0.9102 |             0.0125 |        0.0021 |               0      |      0.6555 |
| patchtst_small           | three_source_excl_local_conflict_stratified |     0.8247 |               0.9351 |             0.0117 |        0.1196 |               0      |      0.3901 |
| regional_doy_climatology | concat_global                               |     0.701  |               0.911  |             0.0473 |        0.3535 |               0      |      0.2858 |
| regional_doy_climatology | fixed_source_fusion_global                  |     0.8291 |               0.9129 |             0.9404 |        0.1016 |               0      |      1.0501 |
| regional_doy_climatology | reliability_fusion_global                   |     0.9793 |               0.9141 |             0.3588 |        0.2459 |               0      |      0.6337 |
| regional_doy_climatology | reliability_fusion_conflict_stratified      |     0.9793 |               0.9322 |             0.2127 |        0.3399 |               0      |      0.3353 |
| regional_doy_climatology | three_source_excl_local_global              |     0.9914 |               0.9192 |             0.2058 |        0.3279 |               0      |      0.3628 |
| regional_doy_climatology | three_source_excl_local_conflict_stratified |     0.9914 |               0.9307 |             0.1889 |        0.341  |               0      |      0.3208 |
| spatial_knn_ridge        | concat_global                               |     0.9693 |               0.9189 |             0.0232 |        0.3112 |               0.0535 |      0.5333 |
| spatial_knn_ridge        | fixed_source_fusion_global                  |     0.8539 |               0.9101 |             0.0502 |        0.0971 |               0      |      0.9123 |
| spatial_knn_ridge        | reliability_fusion_global                   |     0.9318 |               0.9147 |             0.0354 |        0.2432 |               0      |      0.5654 |
| spatial_knn_ridge        | reliability_fusion_conflict_stratified      |     0.9318 |               0.9342 |             0.0346 |        0.221  |               0.0004 |      0.5359 |
| spatial_knn_ridge        | three_source_excl_local_global              |     0.9377 |               0.9079 |             0.0193 |        0.2695 |               0      |      0.407  |
| spatial_knn_ridge        | three_source_excl_local_conflict_stratified |     0.9377 |               0.9388 |             0.0207 |        0.2884 |               0.0046 |      0.3949 |
| stgcn_diffusion          | concat_global                               |     0.6478 |               0.9107 |             0.0321 |        0      |               0      |      0.7745 |
| stgcn_diffusion          | fixed_source_fusion_global                  |     0.6663 |               0.9086 |             0.0348 |        0      |               0      |      0.7792 |
| stgcn_diffusion          | reliability_fusion_global                   |     0.6557 |               0.9122 |             0.038  |        0      |               0      |      0.7758 |
| stgcn_diffusion          | reliability_fusion_conflict_stratified      |     0.6557 |               0.9375 |             0.0729 |        0.0001 |               0      |      0.7268 |
| stgcn_diffusion          | three_source_excl_local_global              |     0.6469 |               0.9059 |             0.0288 |        0      |               0      |      0.7616 |
| stgcn_diffusion          | three_source_excl_local_conflict_stratified |     0.6469 |               0.9384 |             0.0284 |        0.0048 |               0      |      0.505  |
