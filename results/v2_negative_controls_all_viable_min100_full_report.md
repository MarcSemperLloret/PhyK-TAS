# PhyK-TAS v2 negative controls (all_viable_min100_full)

Random-forest degradation inferrer. Physical descriptors are permuted as a block across rows for 5 repeats, preserving their joint distribution while breaking physical alignment with each transfer row. Rows are aggregated to source-target-cell-seed units; RF trees=120.

| cv_kind       | forecast_model        | feature_set         | control           |   r2_mean |    r2_sd |   mae_mean |
|:--------------|:----------------------|:--------------------|:------------------|----------:|---------:|-----------:|
| group_by_cell | graphwavenet_transfer | physical            | observed          |    0.0517 | nan      |     0.0583 |
| group_by_cell | graphwavenet_transfer | physical            | permuted_physical |   -0.0515 |   0.0107 |     0.0772 |
| group_by_cell | graphwavenet_transfer | physical_plus_shift | observed          |    0.1365 | nan      |     0.0518 |
| group_by_cell | graphwavenet_transfer | physical_plus_shift | permuted_physical |    0.0973 |   0.005  |     0.0635 |
| group_by_cell | graphwavenet_transfer | shift               | observed          |    0.1202 | nan      |     0.0627 |
| group_by_cell | spatial_knn_ridge     | physical            | observed          |    0.0878 | nan      |     0.066  |
| group_by_cell | spatial_knn_ridge     | physical            | permuted_physical |   -0.0572 |   0.0061 |     0.0735 |
| group_by_cell | spatial_knn_ridge     | physical_plus_shift | observed          |    0.5256 | nan      |     0.0334 |
| group_by_cell | spatial_knn_ridge     | physical_plus_shift | permuted_physical |    0.6416 |   0.0037 |     0.031  |
| group_by_cell | spatial_knn_ridge     | shift               | observed          |    0.656  | nan      |     0.0301 |
| group_by_cell | stgcn_diffusion       | physical            | observed          |    0.061  | nan      |     0.0794 |
| group_by_cell | stgcn_diffusion       | physical            | permuted_physical |   -0.0431 |   0.0023 |     0.0967 |
| group_by_cell | stgcn_diffusion       | physical_plus_shift | observed          |    0.2979 | nan      |     0.0643 |
| group_by_cell | stgcn_diffusion       | physical_plus_shift | permuted_physical |    0.1467 |   0.0209 |     0.0807 |
| group_by_cell | stgcn_diffusion       | shift               | observed          |    0.1825 | nan      |     0.0793 |
