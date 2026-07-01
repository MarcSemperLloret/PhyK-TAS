# PhyK-TAS v2 conformal utility (all_viable_min100_full)

Repeated split-conformal evaluation linking alpha to empirical coverage, unsafe deploys, decision rates, and asymmetric decision cost. Costs are illustrative: deploy-to-adapt=5, deploy-to-retrain=10, adapt-to-deploy=1, adapt-to-retrain=4, retrain-to-deploy=3, retrain-to-adapt=1.

| forecast_model           |   n_pairs |   n_splits |   alpha |   target_coverage |   empirical_coverage |   unsafe_deploy_rate |   deploy_rate |   adapt_rate |   retrain_rate |   mean_cost |
|:-------------------------|----------:|-----------:|--------:|------------------:|---------------------:|---------------------:|--------------:|-------------:|---------------:|------------:|
| graphwavenet_transfer    |       110 |        200 |    0.2  |              0.8  |               0.7981 |               0      |        0.0004 |       0.026  |         0.9736 |      0.6623 |
| graphwavenet_transfer    |       110 |        200 |    0.1  |              0.9  |               0.9078 |               0      |        0      |       0      |         1      |      0.7047 |
| graphwavenet_transfer    |       110 |        200 |    0.05 |              0.95 |               0.9643 |               0      |        0      |       0      |         1      |      0.6866 |
| linear_window            |       110 |        200 |    0.2  |              0.8  |               0.8079 |               0.0025 |        0.0003 |       0.0132 |         0.9865 |      1.1199 |
| linear_window            |       110 |        200 |    0.1  |              0.9  |               0.9062 |               0      |        0      |       0.0002 |         0.9998 |      1.1351 |
| linear_window            |       110 |        200 |    0.05 |              0.95 |               0.958  |               0      |        0      |       0      |         1      |      1.111  |
| patchtst_small           |       110 |        200 |    0.2  |              0.8  |               0.7942 |               0.005  |        0.0086 |       0.0251 |         0.9663 |      1.0876 |
| patchtst_small           |       110 |        200 |    0.1  |              0.9  |               0.9082 |               0      |        0      |       0.0004 |         0.9996 |      1.0876 |
| patchtst_small           |       110 |        200 |    0.05 |              0.95 |               0.9648 |               0      |        0      |       0      |         1      |      1.1005 |
| regional_doy_climatology |       110 |        200 |    0.2  |              0.8  |               0.7984 |               0.1126 |        0.1662 |       0.0065 |         0.8273 |      0.9935 |
| regional_doy_climatology |       110 |        200 |    0.1  |              0.9  |               0.9164 |               0.0136 |        0.105  |       0.009  |         0.886  |      1.0615 |
| regional_doy_climatology |       110 |        200 |    0.05 |              0.95 |               0.9672 |               0      |        0.0475 |       0.0037 |         0.9488 |      1.2235 |
| spatial_knn_ridge        |       110 |        200 |    0.2  |              0.8  |               0.8054 |               0      |        0.1485 |       0.0631 |         0.7884 |      0.8111 |
| spatial_knn_ridge        |       110 |        200 |    0.1  |              0.9  |               0.9104 |               0      |        0.0582 |       0.0519 |         0.8899 |      1.0801 |
| spatial_knn_ridge        |       110 |        200 |    0.05 |              0.95 |               0.9639 |               0      |        0.0153 |       0.0243 |         0.9605 |      1.2685 |
| stgcn_diffusion          |       110 |        200 |    0.2  |              0.8  |               0.8004 |               0      |        0.0024 |       0.0373 |         0.9604 |      0.6983 |
| stgcn_diffusion          |       110 |        200 |    0.1  |              0.9  |               0.9083 |               0      |        0      |       0.0017 |         0.9983 |      0.7875 |
| stgcn_diffusion          |       110 |        200 |    0.05 |              0.95 |               0.9648 |               0      |        0      |       0      |         1      |      0.795  |
