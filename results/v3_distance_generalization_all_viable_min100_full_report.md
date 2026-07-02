# Cross-regime generalization vs. distance (all_viable_min100_full)

LTRO with HistGBM(physical+shift). Conformal alpha=0.1 (target coverage 0.90), calibrated on other regions.

- **pooled**: Spearman(phys-distance, LTRO MAE) = 0.189 (p=0.220); Spearman(phys-distance, coverage) = -0.248 (p=0.105); mean coverage = 0.858
- **spatial_knn_ridge**: Spearman(phys-distance, LTRO MAE) = 0.385 (p=0.242); Spearman(phys-distance, coverage) = -0.372 (p=0.261); mean coverage = 0.826
- **stgcn_diffusion**: Spearman(phys-distance, LTRO MAE) = 0.188 (p=0.580); Spearman(phys-distance, coverage) = -0.266 (p=0.429); mean coverage = 0.888
- **graphwavenet_transfer**: Spearman(phys-distance, LTRO MAE) = 0.092 (p=0.788); Spearman(phys-distance, coverage) = 0.037 (p=0.915); mean coverage = 0.896
- **regional_doy_climatology**: Spearman(phys-distance, LTRO MAE) = 0.757 (p=0.007); Spearman(phys-distance, coverage) = -0.384 (p=0.243); mean coverage = 0.820

| model                    | held_out_region   |     n |   phys_distance |   geo_distance |   ltro_mae |   ltro_r2 |   ltro_spearman |   conformal_coverage |
|:-------------------------|:------------------|------:|----------------:|---------------:|-----------:|----------:|----------------:|---------------------:|
| spatial_knn_ridge        | CNA               | 13140 |           2.488 |         12.762 |      0.065 |    -0.127 |           0.338 |                0.883 |
| spatial_knn_ridge        | EAS               |  3300 |           6.529 |         64.551 |      0.098 |    -1.582 |           0.207 |                0.988 |
| spatial_knn_ridge        | EAU               |  7230 |           1.883 |         14.533 |      0.066 |    -0.334 |          -0.143 |                0.988 |
| spatial_knn_ridge        | ENA               | 15660 |           2.488 |         16.632 |      0.088 |    -0.769 |           0.315 |                0.991 |
| spatial_knn_ridge        | MED               |  9840 |           1.883 |         10.323 |      0.091 |    -1.11  |          -0.069 |                0.693 |
| spatial_knn_ridge        | NCA               |  4320 |           4.77  |         11.955 |      0.251 |   -11.479 |          -0.571 |                0.108 |
| spatial_knn_ridge        | NEU               | 30000 |           0.845 |          8.37  |      0.074 |    -3.55  |          -0.133 |                1     |
| spatial_knn_ridge        | NWN               |  5490 |           1.087 |         24.773 |      0.128 |    -0.25  |          -0.079 |                0.785 |
| spatial_knn_ridge        | SAU               | 10530 |           2.557 |         14.533 |      0.069 |    -0.58  |          -0.034 |                0.865 |
| spatial_knn_ridge        | WCE               | 30000 |           0.845 |          8.37  |      0.056 |    -1.14  |           0.6   |                1     |
| spatial_knn_ridge        | WNA               | 29250 |           1.087 |         11.955 |      0.074 |    -0.387 |           0.105 |                0.786 |
| stgcn_diffusion          | CNA               | 13140 |           2.488 |         12.762 |      0.118 |    -0.36  |           0.288 |                0.785 |
| stgcn_diffusion          | EAS               |  3300 |           6.529 |         64.551 |      0.181 |    -0.018 |           0.097 |                0.817 |
| stgcn_diffusion          | EAU               |  7230 |           1.883 |         14.533 |      0.052 |    -0.13  |           0.243 |                0.927 |
| stgcn_diffusion          | ENA               | 15660 |           2.488 |         16.632 |      0.159 |    -0.094 |           0.192 |                0.724 |
| stgcn_diffusion          | MED               |  9840 |           1.883 |         10.323 |      0.035 |    -0.195 |           0.034 |                0.965 |
| stgcn_diffusion          | NCA               |  4320 |           4.77  |         11.955 |      0.048 |    -2.411 |           0.058 |                0.944 |
| stgcn_diffusion          | NEU               | 30000 |           0.845 |          8.37  |      0.05  |     0.184 |           0.366 |                0.913 |
| stgcn_diffusion          | NWN               |  5490 |           1.087 |         24.773 |      0.207 |     0.003 |           0.057 |                0.832 |
| stgcn_diffusion          | SAU               | 10530 |           2.557 |         14.533 |      0.041 |    -0.356 |           0.119 |                0.953 |
| stgcn_diffusion          | WCE               | 30000 |           0.845 |          8.37  |      0.038 |    -0.28  |           0.274 |                0.978 |
| stgcn_diffusion          | WNA               | 29250 |           1.087 |         11.955 |      0.059 |     0.169 |           0.225 |                0.932 |
| graphwavenet_transfer    | CNA               | 13140 |           2.488 |         12.762 |      0.154 |     0.116 |           0.382 |                0.56  |
| graphwavenet_transfer    | EAS               |  3300 |           6.529 |         64.551 |      0.11  |    -2.223 |           0.112 |                0.941 |
| graphwavenet_transfer    | EAU               |  7230 |           1.883 |         14.533 |      0.042 |    -0.567 |           0.256 |                0.988 |
| graphwavenet_transfer    | ENA               | 15660 |           2.488 |         16.632 |      0.235 |     0.002 |           0.337 |                0.722 |
| graphwavenet_transfer    | MED               |  9840 |           1.883 |         10.323 |      0.026 |    -0.234 |           0.208 |                0.995 |
| graphwavenet_transfer    | NCA               |  4320 |           4.77  |         11.955 |      0.04  |    -1.339 |           0.199 |                0.997 |
| graphwavenet_transfer    | NEU               | 30000 |           0.845 |          8.37  |      0.042 |     0.207 |           0.619 |                0.958 |
| graphwavenet_transfer    | NWN               |  5490 |           1.087 |         24.773 |      0.139 |     0.114 |           0.301 |                0.838 |
| graphwavenet_transfer    | SAU               | 10530 |           2.557 |         14.533 |      0.028 |    -0.218 |           0.246 |                0.991 |
| graphwavenet_transfer    | WCE               | 30000 |           0.845 |          8.37  |      0.034 |    -0.199 |           0.454 |                0.994 |
| graphwavenet_transfer    | WNA               | 29250 |           1.087 |         11.955 |      0.068 |     0.196 |           0.183 |                0.878 |
| regional_doy_climatology | CNA               | 13140 |           2.488 |         12.762 |      0.774 |    -1.373 |          -0.418 |                0.854 |
| regional_doy_climatology | EAS               |  3300 |           6.529 |         64.551 |      4.614 |   -68.407 |          -0.17  |                1     |
| regional_doy_climatology | EAU               |  7230 |           1.883 |         14.533 |      0.894 |    -1.081 |          -0.824 |                0.9   |
| regional_doy_climatology | ENA               | 15660 |           2.488 |         16.632 |      1.276 |    -2.424 |          -0.487 |                0.9   |
| regional_doy_climatology | MED               |  9840 |           1.883 |         10.323 |      0.975 |    -1.182 |          -0.71  |                0.673 |
| regional_doy_climatology | NCA               |  4320 |           4.77  |         11.955 |      2.108 |    -6.04  |          -0.839 |                0.101 |
| regional_doy_climatology | NEU               | 30000 |           0.845 |          8.37  |      0.303 |     0.822 |          -0.186 |                1     |
| regional_doy_climatology | NWN               |  5490 |           1.087 |         24.773 |      0.955 |    -1.455 |          -0.59  |                0.9   |
| regional_doy_climatology | SAU               | 10530 |           2.557 |         14.533 |      0.592 |     0.448 |          -0.022 |                0.753 |
| regional_doy_climatology | WCE               | 30000 |           0.845 |          8.37  |      0.284 |     0.866 |           0.216 |                0.999 |
| regional_doy_climatology | WNA               | 29250 |           1.087 |         11.955 |      0.395 |     0.738 |           0.243 |                0.94  |
