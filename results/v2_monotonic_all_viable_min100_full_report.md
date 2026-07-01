# PhyK-TAS v2 monotonic-constraint comparison (all_viable_min100_full)

Shift features constrained monotone non-decreasing; physical descriptors unconstrained. Bootstrap N=1000.

## group_by_cell

| forecast_model           |   hist_gbm |   hist_gbm_mono |   delta_mono |
|:-------------------------|-----------:|----------------:|-------------:|
| graphwavenet_transfer    |      0.434 |           0.378 |       -0.056 |
| linear_window            |     -0.016 |          -0.023 |       -0.007 |
| patchtst_small           |     -0.014 |          -0.02  |       -0.006 |
| regional_doy_climatology |      0.888 |           0.747 |       -0.141 |
| spatial_knn_ridge        |      0.844 |           0.569 |       -0.275 |
| stgcn_diffusion          |      0.297 |           0.32  |        0.023 |

## leave_target_region_out

| forecast_model           |   hist_gbm |   hist_gbm_mono |   delta_mono |
|:-------------------------|-----------:|----------------:|-------------:|
| graphwavenet_transfer    |      0.198 |           0.152 |       -0.046 |
| linear_window            |     -0.02  |          -0.018 |        0.001 |
| patchtst_small           |     -0.027 |          -0.024 |        0.003 |
| regional_doy_climatology |     -0.416 |           0.124 |        0.54  |
| spatial_knn_ridge        |     -0.404 |          -0.324 |        0.08  |
| stgcn_diffusion          |      0.022 |           0.09  |        0.068 |
