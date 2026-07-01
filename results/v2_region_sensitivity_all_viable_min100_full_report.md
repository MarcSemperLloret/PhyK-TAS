# PhyK-TAS v2 regional-set sensitivity (all_viable_min100_full)

Primary group-by-cell random-forest feature comparison recomputed on region subsets. The stricter subsets remove the 80% coverage regions and then require at least 300 stations.

| region_set       |   n_regions | forecast_model           |   n_rows |   n_pairs |   r2_physical |   r2_shift |   r2_physical_plus_shift |   delta_combined_minus_shift |
|:-----------------|------------:|:-------------------------|---------:|----------:|--------------:|-----------:|-------------------------:|-----------------------------:|
| all_11           |          11 | graphwavenet_transfer    |   158760 |       110 |        0.3034 |     0.1453 |                   0.3881 |                       0.2428 |
| all_11           |          11 | linear_window            |   158760 |       110 |       -0.138  |    -0.0102 |                  -0.1395 |                      -0.1292 |
| all_11           |          11 | patchtst_small           |   158760 |       110 |       -0.1378 |    -0.01   |                  -0.138  |                      -0.128  |
| all_11           |          11 | regional_doy_climatology |   158760 |       110 |        0.0395 |     0.9664 |                   0.8268 |                      -0.1396 |
| all_11           |          11 | spatial_knn_ridge        |   158760 |       110 |        0.3052 |     0.6555 |                   0.832  |                       0.1765 |
| all_11           |          11 | stgcn_diffusion          |   158760 |       110 |        0.2341 |     0.0803 |                   0.3676 |                       0.2873 |
| coverage95_only  |           8 | graphwavenet_transfer    |   101955 |        56 |        0.3054 |     0.1541 |                   0.3966 |                       0.2425 |
| coverage95_only  |           8 | linear_window            |   101955 |        56 |       -0.0626 |    -0.003  |                  -0.0616 |                      -0.0585 |
| coverage95_only  |           8 | patchtst_small           |   101955 |        56 |       -0.0625 |    -0.0031 |                  -0.062  |                      -0.0589 |
| coverage95_only  |           8 | regional_doy_climatology |   101955 |        56 |       -0.3512 |     0.9247 |                   0.9496 |                       0.0249 |
| coverage95_only  |           8 | spatial_knn_ridge        |   101955 |        56 |        0.3287 |     0.7625 |                   0.8686 |                       0.1061 |
| coverage95_only  |           8 | stgcn_diffusion          |   101955 |        56 |        0.2105 |     0.0976 |                   0.3573 |                       0.2597 |
| coverage95_ge300 |           7 | graphwavenet_transfer    |    83052 |        42 |        0.2995 |     0.1534 |                   0.4092 |                       0.2558 |
| coverage95_ge300 |           7 | linear_window            |    83052 |        42 |       -0.0657 |    -0.0015 |                  -0.0643 |                      -0.0627 |
| coverage95_ge300 |           7 | patchtst_small           |    83052 |        42 |       -0.0652 |    -0.0016 |                  -0.0645 |                      -0.0629 |
| coverage95_ge300 |           7 | regional_doy_climatology |    83052 |        42 |       -0.2785 |     0.9233 |                   0.9526 |                       0.0293 |
| coverage95_ge300 |           7 | spatial_knn_ridge        |    83052 |        42 |        0.3371 |     0.7578 |                   0.8778 |                       0.12   |
| coverage95_ge300 |           7 | stgcn_diffusion          |    83052 |        42 |        0.2191 |     0.0954 |                   0.3785 |                       0.283  |
