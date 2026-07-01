# Pilot light power analysis

This pilot uses post-dedup operational stations sampled from the preregistration candidate design.

Sample: up to 300 stations per region.

Model:

- daily region-level climatology trained on 2005-2012;
- evaluated on 2020-2025;
- degradation per station is mean out-region climatology MAE minus in-region climatology MAE.

This is not the final model comparison. It estimates variance of degradation for power planning.

## Degradation summary

| ar6_region   |   n_station |   n_cell5 |   mean_deg |    sd_deg |   median_ratio |
|:-------------|------------:|----------:|-----------:|----------:|---------------:|
| MED          |         300 |        17 |  0.239514  | 0.0509019 |       1.07625  |
| NEU          |         300 |        23 | -0.0781766 | 0.0326439 |       0.971809 |
| WCE          |         300 |        12 |  0.0284319 | 0.0451514 |       1.00944  |

## Power bounds

| ar6_region   |   n_station |   n_cell5 |   sd_degradation |   min_detectable_r2_station_iid |   min_detectable_r2_cell_effective |
|:-------------|------------:|----------:|-----------------:|--------------------------------:|-----------------------------------:|
| MED          |         300 |        17 |        0.0509019 |                       0.0259338 |                           0.374687 |
| NEU          |         300 |        23 |        0.0326439 |                       0.0259338 |                           0.291415 |
| WCE          |         300 |        12 |        0.0451514 |                       0.0259338 |                           0.491684 |

## Interpretation

- The station-level sample supports detecting small associations if stations were independent.
- The cell-level bound remains conservative and shows MED is the limiting region.
- The preregistered analysis must therefore use hierarchical/bootstrap uncertainty and avoid claiming IID station-level power.
