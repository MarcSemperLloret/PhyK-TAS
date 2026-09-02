# Ternary reliability/conflict fusion (all_viable_min100_full)

Same conformal decision protocol as v3_operational_agreement (300 splits, deploy <= 0.010, adapt <= 0.025). Shown for alpha=0.10.

## Policy comparison

| forecast_model           | policy                            |   point_r2 |   empirical_coverage |   mean_bound_width |   deploy_rate |   unsafe_deploy_rate |   mean_cost |
|:-------------------------|:----------------------------------|-----------:|---------------------:|-------------------:|--------------:|---------------------:|------------:|
| graphwavenet_transfer    | reliability_fusion_2src_conflict2 |     0.8795 |               0.9357 |             0.0291 |        0      |               0      |      0.5876 |
| graphwavenet_transfer    | three_source_concat_conflict2     |     0.6578 |               0.9284 |             0.0291 |        0.0083 |               0      |      0.4955 |
| graphwavenet_transfer    | reliability_fusion_3src_global    |     0.6499 |               0.9112 |             0.055  |        0      |               0      |      0.6522 |
| graphwavenet_transfer    | reliability_fusion_3src_conflict3 |     0.6499 |               0.9342 |             0.0343 |        0.0004 |               0      |      0.5539 |
| graphwavenet_transfer    | three_source_concat_conflict3     |     0.6578 |               0.9354 |             0.0307 |        0.0265 |               0      |      0.3709 |
| linear_window            | reliability_fusion_2src_conflict2 |     0.217  |               0.9416 |             0.0282 |        0.0071 |               0      |      0.7011 |
| linear_window            | three_source_concat_conflict2     |     0.01   |               0.9359 |             0.0178 |        0.093  |               0      |      0.4338 |
| linear_window            | reliability_fusion_3src_global    |     0.55   |               0.9141 |             0.0236 |        0      |               0      |      1.1322 |
| linear_window            | reliability_fusion_3src_conflict3 |     0.55   |               0.9389 |             0.0242 |        0.0579 |               0      |      0.6025 |
| linear_window            | three_source_concat_conflict3     |     0.01   |               0.9329 |             0.0184 |        0.1339 |               0.0019 |      0.3772 |
| patchtst_small           | reliability_fusion_2src_conflict2 |     0.7606 |               0.9335 |             0.0337 |        0.0099 |               0      |      0.7341 |
| patchtst_small           | three_source_concat_conflict2     |     0.8247 |               0.9416 |             0.0119 |        0.1148 |               0      |      0.3987 |
| patchtst_small           | reliability_fusion_3src_global    |     0.8429 |               0.9122 |             0.0302 |        0      |               0      |      1.1835 |
| patchtst_small           | reliability_fusion_3src_conflict3 |     0.8429 |               0.9326 |             0.0268 |        0.0334 |               0.0022 |      0.6268 |
| patchtst_small           | three_source_concat_conflict3     |     0.8247 |               0.9332 |             0.0124 |        0.1201 |               0      |      0.4115 |
| regional_doy_climatology | reliability_fusion_2src_conflict2 |     0.9793 |               0.9278 |             0.2136 |        0.3388 |               0      |      0.3398 |
| regional_doy_climatology | three_source_concat_conflict2     |     0.9914 |               0.9307 |             0.1867 |        0.3396 |               0      |      0.319  |
| regional_doy_climatology | reliability_fusion_3src_global    |     0.9799 |               0.9095 |             0.3124 |        0.2551 |               0      |      0.5971 |
| regional_doy_climatology | reliability_fusion_3src_conflict3 |     0.9799 |               0.9362 |             0.2794 |        0.2558 |               0      |      0.5873 |
| regional_doy_climatology | three_source_concat_conflict3     |     0.9914 |               0.9344 |             0.1977 |        0.3287 |               0      |      0.3259 |
| spatial_knn_ridge        | reliability_fusion_2src_conflict2 |     0.9318 |               0.9426 |             0.035  |        0.2157 |               0      |      0.5416 |
| spatial_knn_ridge        | three_source_concat_conflict2     |     0.9377 |               0.9309 |             0.0201 |        0.2931 |               0.0057 |      0.3935 |
| spatial_knn_ridge        | reliability_fusion_3src_global    |     0.925  |               0.9149 |             0.0352 |        0.2291 |               0      |      0.5779 |
| spatial_knn_ridge        | reliability_fusion_3src_conflict3 |     0.925  |               0.9372 |             0.0355 |        0.2151 |               0      |      0.4921 |
| spatial_knn_ridge        | three_source_concat_conflict3     |     0.9377 |               0.9422 |             0.0193 |        0.3096 |               0.0165 |      0.3741 |
| stgcn_diffusion          | reliability_fusion_2src_conflict2 |     0.6557 |               0.9314 |             0.0711 |        0      |               0      |      0.7319 |
| stgcn_diffusion          | three_source_concat_conflict2     |     0.6469 |               0.9342 |             0.0279 |        0.0058 |               0      |      0.5116 |
| stgcn_diffusion          | reliability_fusion_3src_global    |     0.6841 |               0.9122 |             0.0416 |        0      |               0      |      0.7768 |
| stgcn_diffusion          | reliability_fusion_3src_conflict3 |     0.6841 |               0.9347 |             0.0399 |        0.0036 |               0      |      0.5118 |
| stgcn_diffusion          | three_source_concat_conflict3     |     0.6469 |               0.9388 |             0.0286 |        0.0128 |               0      |      0.4272 |

## Mean three-source reliability weights (leave-one-region-out)

| forecast_model           |   mean_w_phys |   mean_w_shift |   mean_w_agree |
|:-------------------------|--------------:|---------------:|---------------:|
| graphwavenet_transfer    |         0.302 |          0.262 |          0.436 |
| linear_window            |         0.267 |          0.327 |          0.406 |
| patchtst_small           |         0.319 |          0.283 |          0.398 |
| regional_doy_climatology |         0.02  |          0.545 |          0.435 |
| spatial_knn_ridge        |         0.21  |          0.43  |          0.36  |
| stgcn_diffusion          |         0.336 |          0.275 |          0.389 |

## Ternary conflict as an uncertainty proxy (3-source reliability fusion)

| forecast_model           |   pearson_r_conflict3_abs_err |   pearson_p |   abs_err_low |   abs_err_mid |   abs_err_high |
|:-------------------------|------------------------------:|------------:|--------------:|--------------:|---------------:|
| graphwavenet_transfer    |                        0.6731 |           0 |        0.0133 |        0.0215 |         0.0623 |
| linear_window            |                        0.8816 |           0 |        0.005  |        0.0094 |         0.0388 |
| patchtst_small           |                        0.7528 |           0 |        0.0066 |        0.0121 |         0.0246 |
| regional_doy_climatology |                        0.446  |           0 |        0.0216 |        0.06   |         0.1838 |
| spatial_knn_ridge        |                        0.7162 |           0 |        0.0091 |        0.0146 |         0.0303 |
| stgcn_diffusion          |                        0.4837 |           0 |        0.011  |        0.0152 |         0.0569 |
