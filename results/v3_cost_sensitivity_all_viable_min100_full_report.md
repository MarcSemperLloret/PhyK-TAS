# Cost-matrix sensitivity of the policy ranking (all_viable_min100_full)

alpha=0.10, 300 splits, deploy <= 0.010, adapt <= 0.025. All matrices share identical splits and decisions.

| forecast_model           | policy                                      |   C1_baseline |   C2_safety |   C3_throughput |
|:-------------------------|:--------------------------------------------|--------------:|------------:|----------------:|
| graphwavenet_transfer    | concat_global                               |         0.668 |       0.668 |           1.337 |
| graphwavenet_transfer    | reliability_fusion_conflict_stratified      |         0.588 |       0.588 |           1.175 |
| graphwavenet_transfer    | three_source_excl_local_conflict_stratified |         0.476 |       0.477 |           0.95  |
| linear_window            | concat_global                               |         0.805 |       0.805 |           1.61  |
| linear_window            | reliability_fusion_conflict_stratified      |         0.693 |       0.693 |           1.37  |
| linear_window            | three_source_excl_local_conflict_stratified |         0.428 |       0.428 |           0.846 |
| patchtst_small           | concat_global                               |         0.864 |       0.864 |           1.728 |
| patchtst_small           | reliability_fusion_conflict_stratified      |         0.731 |       0.731 |           1.399 |
| patchtst_small           | three_source_excl_local_conflict_stratified |         0.395 |       0.395 |           0.785 |
| regional_doy_climatology | concat_global                               |         0.295 |       0.295 |           0.591 |
| regional_doy_climatology | reliability_fusion_conflict_stratified      |         0.347 |       0.347 |           0.694 |
| regional_doy_climatology | three_source_excl_local_conflict_stratified |         0.342 |       0.342 |           0.685 |
| spatial_knn_ridge        | concat_global                               |         0.536 |       0.714 |           0.893 |
| spatial_knn_ridge        | reliability_fusion_conflict_stratified      |         0.541 |       0.541 |           1.03  |
| spatial_knn_ridge        | three_source_excl_local_conflict_stratified |         0.404 |       0.421 |           0.745 |
| stgcn_diffusion          | concat_global                               |         0.777 |       0.777 |           1.555 |
| stgcn_diffusion          | reliability_fusion_conflict_stratified      |         0.716 |       0.716 |           1.432 |
| stgcn_diffusion          | three_source_excl_local_conflict_stratified |         0.496 |       0.496 |           0.992 |

## Winner per model per matrix

- C1_baseline: three-source+conflict cheapest for 5 of 6 families (exceptions: regional_doy_climatology)
- C2_safety: three-source+conflict cheapest for 5 of 6 families (exceptions: regional_doy_climatology)
- C3_throughput: three-source+conflict cheapest for 5 of 6 families (exceptions: regional_doy_climatology)
