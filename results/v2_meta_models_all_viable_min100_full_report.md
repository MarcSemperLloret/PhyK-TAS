# PhyK-TAS v2 meta-model comparison (all_viable_min100_full)

Feature set: physical_plus_shift. Hierarchical bootstrap over (seed, cell5), N=300. Pooled across seeds ['s1', 's2', 's3'].

## group_by_cell

| forecast_model           |   bayes_ridge |   fusion_mean |   fusion_stack |   hist_gbm |   mixedlm_pool |   random_forest |
|:-------------------------|--------------:|--------------:|---------------:|-----------:|---------------:|----------------:|
| graphwavenet_transfer    |         0.117 |         0.258 |          0.412 |      0.434 |         -1.495 |           0.336 |
| linear_window            |        -0.001 |        -0.004 |         -0     |     -0.016 |         -0.005 |          -0.033 |
| patchtst_small           |        -0.001 |        -0.004 |         -0     |     -0.014 |         -0.006 |          -0.036 |
| regional_doy_climatology |         0.574 |         0.905 |          0.92  |      0.888 |          0.945 |           0.885 |
| spatial_knn_ridge        |         0.166 |         0.746 |          0.847 |      0.844 |          0.542 |           0.823 |
| stgcn_diffusion          |         0.098 |         0.307 |          0.308 |      0.297 |         -0.214 |           0.311 |

## leave_target_region_out

| forecast_model           |   bayes_ridge |   fusion_mean |   fusion_stack |   hist_gbm |   mixedlm_pool |   random_forest |
|:-------------------------|--------------:|--------------:|---------------:|-----------:|---------------:|----------------:|
| graphwavenet_transfer    |         0.054 |         0.157 |          0.129 |      0.198 |         -1.23  |           0.136 |
| linear_window            |        -0     |        -0.004 |         -0     |     -0.02  |         -0.003 |          -0.046 |
| patchtst_small           |        -0     |        -0.005 |          0     |     -0.027 |         -0.003 |          -0.053 |
| regional_doy_climatology |         0.215 |         0.299 |          0.857 |     -0.416 |          0.859 |          -0.695 |
| spatial_knn_ridge        |        -0.258 |        -0.005 |          0.315 |     -0.404 |          0.264 |          -0.969 |
| stgcn_diffusion          |         0.063 |         0.133 |          0.114 |      0.022 |         -0.064 |           0.002 |
