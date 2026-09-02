# PhyK-TAS negative-control permutation (all_viable_min100_full)

Group-by-cell random forest, 5 permutations of the physical block, pooled over seeds. Positive loss = permutation destroys signal.

| model                    |   r2_phys |   r2_phys_perm |   phys_signal_loss |   r2_shift |   r2_comb |   combined_gain |   combined_gain_perm |   gain_loss |
|:-------------------------|----------:|---------------:|-------------------:|-----------:|----------:|----------------:|---------------------:|------------:|
| spatial_knn_ridge        |     0.3   |         -0.057 |              0.357 |      0.655 |     0.823 |           0.168 |               -0.013 |       0.181 |
| stgcn_diffusion          |     0.215 |         -0.048 |              0.263 |      0.034 |     0.311 |           0.277 |               -0.032 |       0.31  |
| graphwavenet_transfer    |     0.249 |         -0.054 |              0.303 |      0.158 |     0.336 |           0.178 |               -0.029 |       0.207 |
| regional_doy_climatology |     0.077 |         -0.051 |              0.128 |      0.965 |     0.885 |          -0.081 |               -0.001 |      -0.08  |
