# Conflict-stratified conformal (all_viable_min100_full); target coverage 0.90

| model                    | conflict_tercile   |   coverage_global |   coverage_stratified |   width_global |   width_stratified |
|:-------------------------|:-------------------|------------------:|----------------------:|---------------:|-------------------:|
| spatial_knn_ridge        | low                |             0.919 |                 0.929 |          0.023 |              0.049 |
| spatial_knn_ridge        | mid                |             0.967 |                 0.924 |          0.023 |              0.017 |
| spatial_knn_ridge        | high               |             0.857 |                 0.931 |          0.023 |              0.026 |
| stgcn_diffusion          | low                |             1     |                 0.93  |          0.033 |              0.004 |
| stgcn_diffusion          | mid                |             0.994 |                 0.934 |          0.033 |              0.02  |
| stgcn_diffusion          | high               |             0.743 |                 0.926 |          0.033 |              0.229 |
| graphwavenet_transfer    | low                |             1     |                 0.931 |          0.043 |              0.003 |
| graphwavenet_transfer    | mid                |             0.998 |                 0.92  |          0.043 |              0.023 |
| graphwavenet_transfer    | high               |             0.733 |                 0.924 |          0.043 |              0.061 |
| regional_doy_climatology | low                |             0.926 |                 0.932 |          0.047 |              0.052 |
| regional_doy_climatology | mid                |             0.915 |                 0.92  |          0.047 |              0.097 |
| regional_doy_climatology | high               |             0.89  |                 0.925 |          0.047 |              0.11  |