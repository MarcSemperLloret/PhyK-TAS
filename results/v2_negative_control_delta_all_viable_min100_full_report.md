# PhyK-TAS v2 negative-control delta (all_viable_min100_full)

This table interprets the physical-descriptor permutation control as a gain over the shift-only baseline. A positive `delta_gain_lost_under_permutation` means the aligned physical descriptors add signal beyond shift diagnostics that is reduced by permutation.

| cv_kind       | forecast_model        |   r2_shift_observed |   r2_physical_observed |   r2_physical_permuted_mean |   physical_signal_loss |   delta_combined_minus_shift_observed |   delta_combined_minus_shift_permuted_mean |   delta_gain_lost_under_permutation |   n_permutations |
|:--------------|:----------------------|--------------------:|-----------------------:|----------------------------:|-----------------------:|--------------------------------------:|-------------------------------------------:|------------------------------------:|-----------------:|
| group_by_cell | graphwavenet_transfer |              0.1202 |                 0.0517 |                     -0.0515 |                 0.1032 |                                0.0163 |                                    -0.023  |                              0.0393 |                5 |
| group_by_cell | spatial_knn_ridge     |              0.656  |                 0.0878 |                     -0.0572 |                 0.145  |                               -0.1304 |                                    -0.0144 |                             -0.116  |                5 |
| group_by_cell | stgcn_diffusion       |              0.1825 |                 0.061  |                     -0.0431 |                 0.1041 |                                0.1154 |                                    -0.0358 |                              0.1512 |                5 |
