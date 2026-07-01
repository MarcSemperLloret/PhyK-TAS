# Decision threshold sensitivity report

Decisions use conservative risk score: mean degradation + 95% half-width across seeds.

Threshold profiles:

- strict: deploy <= 0.005, adapt <= 0.020;
- main: deploy <= 0.010, adapt <= 0.025;
- lenient: deploy <= 0.015, adapt <= 0.030.

## Decision counts

| threshold_profile   | model                 |   adapt |   deploy |   retrain |
|:--------------------|:----------------------|--------:|---------:|----------:|
| lenient             | graphwavenet_transfer |       2 |        3 |         1 |
| lenient             | stgcn_diffusion       |       3 |        3 |         0 |
| main                | graphwavenet_transfer |       3 |        1 |         2 |
| main                | stgcn_diffusion       |       2 |        3 |         1 |
| strict              | graphwavenet_transfer |       2 |        1 |         3 |
| strict              | stgcn_diffusion       |       3 |        1 |         2 |

Figure:

- `figures/fig_decision_threshold_sensitivity.png`
