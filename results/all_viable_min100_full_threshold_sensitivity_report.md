# Decision threshold sensitivity report

Experiment prefix: `all_viable_min100_full`.

Decisions use conservative risk score: mean degradation + 95% half-width across seeds.

Threshold profiles:

- strict: deploy <= 0.005, adapt <= 0.020;
- main: deploy <= 0.010, adapt <= 0.025;
- lenient: deploy <= 0.015, adapt <= 0.030.

## Decision counts

| threshold_profile   | model                    |   adapt |   deploy |   retrain |
|:--------------------|:-------------------------|--------:|---------:|----------:|
| lenient             | graphwavenet_transfer    |       4 |        4 |       102 |
| lenient             | linear_window            |       0 |        0 |       110 |
| lenient             | patchtst_small           |       0 |        0 |       110 |
| lenient             | regional_doy_climatology |       1 |       47 |        62 |
| lenient             | spatial_knn_ridge        |       9 |       40 |        61 |
| lenient             | stgcn_diffusion          |       9 |        2 |        99 |
| main                | graphwavenet_transfer    |       7 |        0 |       103 |
| main                | linear_window            |       0 |        0 |       110 |
| main                | patchtst_small           |       0 |        0 |       110 |
| main                | regional_doy_climatology |       2 |       46 |        62 |
| main                | spatial_knn_ridge        |      11 |       37 |        62 |
| main                | stgcn_diffusion          |       5 |        1 |       104 |
| strict              | graphwavenet_transfer    |       5 |        0 |       105 |
| strict              | linear_window            |       0 |        0 |       110 |
| strict              | patchtst_small           |       0 |        0 |       110 |
| strict              | regional_doy_climatology |       3 |       45 |        62 |
| strict              | spatial_knn_ridge        |      13 |       32 |        65 |
| strict              | stgcn_diffusion          |       5 |        0 |       105 |

Figure:

- `figures/fig_all_viable_threshold_sensitivity.png`
