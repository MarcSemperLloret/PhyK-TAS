# Preliminary power analysis

This is a pre-model analytic power check using post-dedup AR6 counts for the core sources and period_start=2005.

It does not replace the later pilot-model power analysis. It estimates the minimum detectable R2 for a single predictor under alpha=0.05 and power=0.8 using two bounds:

- station IID bound: optimistic;
- cell 5 x 5 effective-n bound: conservative for spatial dependence.

| ar6_region   |   coverage_threshold |   n_station |   n_cell5 |   min_detectable_r2_station_iid |   min_detectable_r2_cell_effective |
|:-------------|---------------------:|------------:|----------:|--------------------------------:|-----------------------------------:|
| MED          |                   80 |         913 |        20 |                      0.00867193 |                           0.327856 |
| WCE          |                   80 |        4705 |        21 |                      0.00179916 |                           0.31475  |
| NEU          |                   80 |        2704 |        35 |                      0.00291798 |                           0.201589 |
| MED          |                   95 |         311 |        19 |                      0.0249748  |                           0.342081 |
| WCE          |                   95 |        4100 |        20 |                      0.00195899 |                           0.327856 |
| NEU          |                   95 |        2345 |        33 |                      0.00339748 |                           0.212618 |

## Interpretation

- WCE and NEU have enough stations and cells for inferential analysis.
- MED is viable by station count but remains the limiting region by 5 x 5 cell count.
- The final power analysis must use pilot degradation estimates and hierarchical/bootstrap variance, as specified in the protocol.

## Pilot-model update

A lightweight pilot was run after this analytic pre-check.

Artifacts:

- `pilot_light_stations.csv`
- `pilot_light_degradation.csv`
- `pilot_light_power.md`

Pilot design:

- up to 300 post-dedup operational stations per region;
- region-level daily climatology trained on 2005-2012;
- evaluation on 2020-2025;
- degradation per station = mean out-region climatology MAE minus in-region climatology MAE.

Summary:

| region | n_station | n_cell5 | mean_degradation | sd_degradation | median_ratio |
|---|---:|---:|---:|---:|---:|
| MED | 300 | 17 | 0.239514 | 0.050902 | 1.076247 |
| NEU | 300 | 23 | -0.078177 | 0.032644 | 0.971809 |
| WCE | 300 | 12 | 0.028432 | 0.045151 | 1.009435 |

Interpretation:

- MED shows clear positive degradation under this simple out-region climatology pilot.
- WCE shows weak positive degradation.
- NEU shows negative degradation, meaning the crude out-region climatology can outperform the in-region climatology for some sampled stations under this baseline.
- This confirms the need to treat the pilot as a variance and sanity check, not as final evidence for the main hypothesis.
- The preregistered analysis must retain the planned model comparison and hierarchical uncertainty.
