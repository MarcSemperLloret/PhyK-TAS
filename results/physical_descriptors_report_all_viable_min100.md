# Physical descriptors report

Operational design:

- Assignment file: `dedup_assignments_core_2005_all_sources.csv`.
- Region thresholds: WCE:95, NEU:95, WNA:95, ENA:95, CNA:95, SAU:95, MED:95, EAU:95, NWN:80, NCA:80, EAS:80.
- Training period for descriptor calculation: 2005-2012.

Outputs:

- `physical_descriptors_station.csv`
- `physical_descriptors_cell5.csv`
- `physical_descriptors_region.csv`

## Regional descriptor summary

| ar6_region   |   n_stations |   wet_day_fraction |   wet_intensity |   dry_spell_p95 |   wet_p99 |   top3_fraction |
|:-------------|-------------:|-------------------:|----------------:|----------------:|----------:|----------------:|
| CNA          |          438 |           0.176994 |        11.7046  |          21     |    62.785 |        0.411484 |
| EAS          |          110 |           0.261965 |        22.3213  |          20.875 |   161.827 |        0.544501 |
| EAU          |          241 |           0.206281 |        11.2412  |          20.1   |    60.778 |        0.407055 |
| ENA          |          522 |           0.263687 |        11.868   |          13     |    63.553 |        0.333226 |
| MED          |          328 |           0.186145 |         9.53591 |          28     |    50.424 |        0.420385 |
| NCA          |          144 |           0.102872 |        10.4915  |          50     |    50.712 |        0.561246 |
| NEU          |         2355 |           0.342105 |         6.44887 |          13     |    29.036 |        0.363377 |
| NWN          |          183 |           0.27859  |         7.2607  |          19     |    30.6   |        0.460801 |
| SAU          |          351 |           0.225114 |         7.57774 |          18     |    41.392 |        0.364629 |
| WCE          |         4493 |           0.323754 |         6.72346 |          13     |    31.039 |        0.362656 |
| WNA          |          975 |           0.27319  |         7.96122 |          16     |    34.404 |        0.429574 |
