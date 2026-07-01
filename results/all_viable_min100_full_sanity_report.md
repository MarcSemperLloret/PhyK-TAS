# All-viable final sanity report

Scope:

- Region set: `all_viable_min100`.
- Experiment prefix: `all_viable_min100_full`.
- Runs: 3 seeds, up to 1000 stations per viable AR6 region.
- Out-of-region pairs per model: 110.

## Region audit

| ar6_region   |   coverage_threshold |   n_stations_threshold_file |   n_cell5_threshold_file |   n_stations |   n_cell5 |   lat_mean |   lon_mean | top_sources                                                                     |
|:-------------|---------------------:|----------------------------:|-------------------------:|-------------:|----------:|-----------:|-----------:|:--------------------------------------------------------------------------------|
| WCE          |                   95 |                        4493 |                       20 |         4493 |        20 |    50.0514 |   11.1362  | eur_ecad_01:3011, deu_dwd_cdc_01:1145, che_meteoswiss_01:333, global_ghcnd_01:4 |
| NEU          |                   95 |                        2355 |                       33 |         2355 |        33 |    58.3595 |   12.1683  | eur_ecad_01:2235, deu_dwd_cdc_01:115, global_ghcnd_01:5                         |
| WNA          |                   95 |                         975 |                       17 |          975 |        17 |    42.1009 | -113.851   | global_ghcnd_01:957, can_eccc_climate_stations_01:17, usa_nerrs_totprcp_01:1    |
| ENA          |                   95 |                         522 |                       21 |          522 |        21 |    38.9896 |  -80.5533  | global_ghcnd_01:479, can_eccc_climate_stations_01:36, usa_nerrs_totprcp_01:7    |
| CNA          |                   95 |                         438 |                       14 |          438 |        14 |    38.5615 |  -97.1799  | global_ghcnd_01:432, can_eccc_climate_stations_01:6                             |
| SAU          |                   95 |                         351 |                       13 |          351 |        13 |   -36.5433 |  137.494   | global_ghcnd_01:351                                                             |
| MED          |                   95 |                         328 |                       19 |          328 |        19 |    40.1191 |    8.27413 | eur_ecad_01:223, esp_aemet_daily_hist_01:101, global_ghcnd_01:4                 |
| EAU          |                   95 |                         241 |                        6 |          241 |         6 |   -30.5702 |  150.744   | global_ghcnd_01:241                                                             |
| NWN          |                   80 |                         183 |                       36 |          183 |        36 |    58.2417 | -132.56    | global_ghcnd_01:107, can_eccc_climate_stations_01:76                            |
| NCA          |                   80 |                         144 |                        7 |          144 |         7 |    31.7436 | -108.06    | global_ghcnd_01:143, usa_nerrs_totprcp_01:1                                     |
| EAS          |                   80 |                         110 |                       16 |          110 |        16 |    24.9998 |  117.893   | hkg_geo_raingauge_01:83, global_ghcnd_01:27                                     |

## Regional physical descriptor snapshot

| ar6_region   |   wet_day_fraction_gt1mm_mean |   wet_day_mean_intensity_mean |   dry_spell_p95_days_median |   wet_day_p99_median |   top3_month_precip_fraction_mean |
|:-------------|------------------------------:|------------------------------:|----------------------------:|---------------------:|----------------------------------:|
| CNA          |                      0.176994 |                      11.7046  |                      21     |               62.785 |                          0.411484 |
| EAS          |                      0.261965 |                      22.3213  |                      20.875 |              161.827 |                          0.544501 |
| EAU          |                      0.206281 |                      11.2412  |                      20.1   |               60.778 |                          0.407055 |
| ENA          |                      0.263687 |                      11.868   |                      13     |               63.553 |                          0.333226 |
| MED          |                      0.186145 |                       9.53591 |                      28     |               50.424 |                          0.420385 |
| NCA          |                      0.102872 |                      10.4915  |                      50     |               50.712 |                          0.561246 |
| NEU          |                      0.342105 |                       6.44887 |                      13     |               29.036 |                          0.363377 |
| NWN          |                      0.27859  |                       7.2607  |                      19     |               30.6   |                          0.460801 |
| SAU          |                      0.225114 |                       7.57774 |                      18     |               41.392 |                          0.364629 |
| WCE          |                      0.323754 |                       6.72346 |                      13     |               31.039 |                          0.362656 |
| WNA          |                      0.27319  |                       7.96122 |                      16     |               34.404 |                          0.429574 |

## Best feature set by model

| forecast_model           | feature_set         |   mae_mean |    r2_mean |      r2_sd |     r2_min |      r2_max |
|:-------------------------|:--------------------|-----------:|-----------:|-----------:|-----------:|------------:|
| graphwavenet_transfer    | physical_plus_shift |  0.0638064 |  0.388761  | 0.043022   |  0.343834  |  0.429584   |
| linear_window            | generic_shift       |  1.13627   | -0.0101844 | 0.007301   | -0.0186027 | -0.00558297 |
| patchtst_small           | generic_shift       |  1.14147   | -0.0099634 | 0.00719803 | -0.0182706 | -0.00557644 |
| regional_doy_climatology | generic_shift       |  0.10731   |  0.966417  | 0.00138943 |  0.96509   |  0.967862   |
| spatial_knn_ridge        | physical_plus_shift |  0.0202313 |  0.832029  | 0.0198334  |  0.809839  |  0.84803    |
| stgcn_diffusion          | physical_plus_shift |  0.0506132 |  0.373986  | 0.0740188  |  0.324485  |  0.459077   |

## Source accuracy versus transfer degradation

| model                    |   n_pairs |   pearson_source_mae_vs_degradation |   spearman_source_mae_vs_degradation |   pearson_source_mae_vs_abs_degradation |   mean_source_in_region_mae |   mean_degradation |   max_degradation |
|:-------------------------|----------:|------------------------------------:|-------------------------------------:|----------------------------------------:|----------------------------:|-------------------:|------------------:|
| graphwavenet_transfer    |       330 |                           0.0254606 |                            0.0339718 |                               0.0216007 |                     2.45733 |          0.0772772 |          0.332576 |
| linear_window            |       330 |                          -0.0532256 |                           -0.0729247 |                              -0.0456743 |                     2.51912 |          0.0402494 |          0.923175 |
| patchtst_small           |       330 |                          -0.0597402 |                           -0.0753868 |                              -0.0571318 |                     2.52419 |          0.0386768 |          0.951386 |
| regional_doy_climatology |       330 |                           0.839057  |                            0.644369  |                               0.769991  |                     3.79471 |          0.221828  |          4.29429  |
| spatial_knn_ridge        |       330 |                           0.392549  |                            0.498179  |                               0.160234  |                     2.6673  |          0.0374391 |          0.288121 |
| stgcn_diffusion          |       330 |                          -0.0657763 |                            0.0493459 |                              -0.073314  |                     2.4919  |          0.0694925 |          0.963289 |

Interpretation: source-region accuracy is at best an incomplete proxy for transfer risk. The sign and magnitude of the correlation vary by model, so deployment assessment needs source-target descriptors rather than source validation alone.

## Conservative decision counts

| model                    | conservative_decision   |   n_pairs |
|:-------------------------|:------------------------|----------:|
| graphwavenet_transfer    | adapt                   |         7 |
| graphwavenet_transfer    | retrain                 |       103 |
| linear_window            | retrain                 |       110 |
| patchtst_small           | retrain                 |       110 |
| regional_doy_climatology | adapt                   |         2 |
| regional_doy_climatology | deploy                  |        46 |
| regional_doy_climatology | retrain                 |        62 |
| spatial_knn_ridge        | adapt                   |        11 |
| spatial_knn_ridge        | deploy                  |        37 |
| spatial_knn_ridge        | retrain                 |        62 |
| stgcn_diffusion          | adapt                   |         5 |
| stgcn_diffusion          | deploy                  |         1 |
| stgcn_diffusion          | retrain                 |       104 |

## Generated artifacts

- `all_viable_min100_full_region_audit.csv`
- `all_viable_min100_full_model_feature_summary.csv`
- `all_viable_min100_full_source_accuracy_vs_transfer.csv`
- `all_viable_min100_full_source_accuracy_vs_transfer_summary.csv`
- `figures/fig_all_viable_region_map.png`
- `figures/fig_all_viable_kbs_r2_by_model.png`
- `figures/fig_all_viable_decision_counts.png`
- `figures/fig_all_viable_source_accuracy_vs_transfer.png`
- `figures/fig_all_viable_degradation_heatmap_spatial_knn_ridge.png`
- `figures/fig_all_viable_degradation_heatmap_stgcn_diffusion.png`
- `figures/fig_all_viable_degradation_heatmap_graphwavenet_transfer.png`
