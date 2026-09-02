# Risk-controlled selective deployment (all_viable_min100_full)

LTRO, pair-level, deploy threshold 0.01. At a capped unsafe-deploy rate, how many safe transfers each policy deploys.

## Max safe deployments at unsafe-rate <= 0.05
|                       |   global |   conflict |   distance |   reject |   n_safe |
|:----------------------|---------:|-----------:|-----------:|---------:|---------:|
| spatial_knn_ridge     |        0 |          0 |          0 |        0 |       48 |
| stgcn_diffusion       |        3 |          4 |          3 |        0 |       23 |
| graphwavenet_transfer |        0 |          0 |          0 |        0 |       20 |

## Max safe deployments at unsafe-rate <= 0.1
|                       |   global |   conflict |   distance |   reject |   n_safe |
|:----------------------|---------:|-----------:|-----------:|---------:|---------:|
| spatial_knn_ridge     |        0 |          0 |          0 |        0 |       48 |
| stgcn_diffusion       |        3 |          4 |          3 |        0 |       23 |
| graphwavenet_transfer |        0 |          0 |          0 |        0 |       20 |
