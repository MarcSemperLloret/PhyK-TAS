# Forecast dataset large report

Large dataset for expensive forecasting experiments.

- Stations per region target: 1000
- Random seed: 20260602
- Date range: 2005-01-01 to 2025-12-31
- Assignment file: `dedup_assignments_core_2005_all_sources.csv`
- Region thresholds: WCE:95, NEU:95, WNA:95, ENA:95, CNA:95, SAU:95, MED:95, EAU:95, NWN:80, NCA:80, EAS:80

## Station summary

| ar6_region   |   n_stations |   n_cells |
|:-------------|-------------:|----------:|
| CNA          |          438 |        14 |
| EAS          |          110 |        16 |
| EAU          |          241 |         6 |
| ENA          |          522 |        21 |
| MED          |          328 |        19 |
| NCA          |          144 |         7 |
| NEU          |         1000 |        28 |
| NWN          |          183 |        36 |
| SAU          |          351 |        13 |
| WCE          |         1000 |        14 |
| WNA          |          975 |        17 |

## Coverage summary

| ar6_region   |     mean |      min |   median |
|:-------------|---------:|---------:|---------:|
| CNA          | 0.992795 | 0.957366 | 0.995763 |
| EAS          | 0.971953 | 0.906519 | 0.979531 |
| EAU          | 0.98918  | 0.968709 | 0.990613 |
| ENA          | 0.992803 | 0.965711 | 0.995697 |
| MED          | 0.994621 | 0.964016 | 0.998044 |
| NCA          | 0.969321 | 0.859192 | 0.976271 |
| NEU          | 0.998013 | 0.973012 | 1        |
| NWN          | 0.966564 | 0.846545 | 0.97575  |
| SAU          | 0.988897 | 0.958279 | 0.990222 |
| WCE          | 0.998586 | 0.978227 | 1        |
| WNA          | 0.996485 | 0.960365 | 0.999218 |

Outputs:

- `forecast_dataset_large_all_viable_min100_full_s1.npz`
- `forecast_dataset_large_all_viable_min100_full_s1_metadata.csv`
