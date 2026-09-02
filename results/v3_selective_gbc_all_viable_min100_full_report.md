# Within-library selective deployment (all_viable_min100_full)

Group-by-cell, deploy threshold 0.01, 200 split-conformal repetitions. Max safe deployments at a capped unsafe-deploy rate.

## Mean safe deployments/split at unsafe-rate <= 0.05
|                          |   global |   conflict |   n_safe(of 55/split) |
|:-------------------------|---------:|-----------:|----------------------:|
| spatial_knn_ridge        |     23.4 |       23.7 |                  24   |
| regional_doy_climatology |     19.9 |       20.1 |                  24.5 |
| stgcn_diffusion          |      6.2 |        5.8 |                  11.5 |
| graphwavenet_transfer    |      5.3 |        5.4 |                  10   |

## Mean safe deployments/split at unsafe-rate <= 0.1
|                          |   global |   conflict |   n_safe(of 55/split) |
|:-------------------------|---------:|-----------:|----------------------:|
| spatial_knn_ridge        |     23.4 |       23.7 |                  24   |
| regional_doy_climatology |     19.9 |       20.1 |                  24.5 |
| stgcn_diffusion          |      6.2 |        5.8 |                  11.5 |
| graphwavenet_transfer    |      5.3 |        5.7 |                  10   |
