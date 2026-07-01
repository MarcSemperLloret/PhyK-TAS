# Physical group ablation report

Ablation uses large-seed ST-GNN metrics and random-forest KBS predictors.

Feature groups:

- occurrence;
- intensity;
- seasonality;
- intermittency;
- extremes;
- physical_all;
- shift_only;
- physical_plus_shift.

## Group-by-cell results

| forecast_model        | cv_kind       | feature_group       |   n_features |   n_seeds |   mae_mean |     mae_sd |     r2_mean |      r2_sd |     r2_min |     r2_max |
|:----------------------|:--------------|:--------------------|-------------:|----------:|-----------:|-----------:|------------:|-----------:|-----------:|-----------:|
| graphwavenet_transfer | group_by_cell | physical_plus_shift |           23 |         3 |  0.0126041 | 0.00429227 |  0.615455   | 0.0914909  |  0.539729  |  0.717113  |
| graphwavenet_transfer | group_by_cell | physical_all        |           12 |         3 |  0.0158344 | 0.00806855 |  0.510468   | 0.0734185  |  0.431577  |  0.576792  |
| graphwavenet_transfer | group_by_cell | occurrence          |            2 |         3 |  0.0168186 | 0.00812565 |  0.483103   | 0.066518   |  0.425094  |  0.555706  |
| graphwavenet_transfer | group_by_cell | intensity           |            3 |         3 |  0.0168536 | 0.00885327 |  0.439384   | 0.0669871  |  0.373884  |  0.507765  |
| graphwavenet_transfer | group_by_cell | seasonality         |            2 |         3 |  0.0187008 | 0.00886864 |  0.288586   | 0.0713749  |  0.236655  |  0.369975  |
| graphwavenet_transfer | group_by_cell | shift_only          |           11 |         3 |  0.0200164 | 0.00888606 |  0.0282499  | 0.0224022  |  0.0033253 |  0.0467064 |
| graphwavenet_transfer | group_by_cell | extremes            |            3 |         3 |  0.0219622 | 0.0103332  | -0.071255   | 0.0216728  | -0.0953699 | -0.0534039 |
| graphwavenet_transfer | group_by_cell | intermittency       |            2 |         3 |  0.0217016 | 0.0100401  | -0.191009   | 0.0836132  | -0.2475    | -0.0949571 |
| stgcn_diffusion       | group_by_cell | physical_plus_shift |           23 |         3 |  0.0105185 | 0.001053   |  0.658563   | 0.0415641  |  0.618036  |  0.701092  |
| stgcn_diffusion       | group_by_cell | physical_all        |           12 |         3 |  0.0137076 | 0.00198689 |  0.550222   | 0.0443613  |  0.52087   |  0.601254  |
| stgcn_diffusion       | group_by_cell | occurrence          |            2 |         3 |  0.0151864 | 0.00242644 |  0.482716   | 0.0638362  |  0.435438  |  0.555331  |
| stgcn_diffusion       | group_by_cell | intensity           |            3 |         3 |  0.0148833 | 0.00182289 |  0.46597    | 0.0653916  |  0.397319  |  0.527523  |
| stgcn_diffusion       | group_by_cell | seasonality         |            2 |         3 |  0.0170049 | 0.00266626 |  0.228357   | 0.107155   |  0.137539  |  0.346541  |
| stgcn_diffusion       | group_by_cell | shift_only          |           11 |         3 |  0.0182194 | 0.00211379 | -0.00535623 | 0.030753   | -0.0312686 |  0.0286276 |
| stgcn_diffusion       | group_by_cell | extremes            |            3 |         3 |  0.0198763 | 0.00253868 | -0.114635   | 0.00750127 | -0.123246  | -0.109516  |
| stgcn_diffusion       | group_by_cell | intermittency       |            2 |         3 |  0.019022  | 0.00228928 | -0.185799   | 0.117117   | -0.298288  | -0.0645459 |

Figure:

- `figures/fig_physical_group_ablation.png`
