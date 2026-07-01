# Large-seed uncertainty report

Seeds:

- `large_s1`: seed 20260524;
- `large_s2`: seed 20260525;
- `large_s3`: seed 20260526.

Scale per run:

- MED: 913 stations;
- WCE: 1000 stations;
- NEU: 1000 stations.

## Degradation uncertainty

| model                 | source_region   | target_region   |   n_seeds |   degradation_mean |   degradation_sd |   degradation_min |   degradation_max |   mae_mean |   brier_mean |   degradation_se |   degradation_ci95_halfwidth |
|:----------------------|:----------------|:----------------|----------:|-------------------:|-----------------:|------------------:|------------------:|-----------:|-------------:|-----------------:|-----------------------------:|
| graphwavenet_transfer | MED             | NEU             |         3 |         0.0167164  |      0.00307475  |       0.0135819   |        0.0197277  |    2.25018 |     0.29611  |      0.00177521  |                  0.0034794   |
| graphwavenet_transfer | MED             | WCE             |         3 |         0.00103611 |      0.00141295  |      -0.000338752 |        0.00248429 |    2.04759 |     0.289614 |      0.000815767 |                  0.0015989   |
| graphwavenet_transfer | NEU             | MED             |         3 |         0.0132737  |      0.010976    |       0.00623078  |        0.0259205  |    2.07325 |     0.189244 |      0.00633699  |                  0.0124205   |
| graphwavenet_transfer | NEU             | WCE             |         3 |         0.00331142 |      0.00888808  |      -0.00207382  |        0.0135702  |    2.04987 |     0.290305 |      0.00513154  |                  0.0100578   |
| graphwavenet_transfer | WCE             | MED             |         3 |         0.00960473 |      0.00080957  |       0.0088151   |        0.0104329  |    2.06959 |     0.186897 |      0.000467405 |                  0.000916114 |
| graphwavenet_transfer | WCE             | NEU             |         3 |         0.0298683  |      0.00659862  |       0.0253058   |        0.0374344  |    2.26333 |     0.294068 |      0.00380971  |                  0.00746704  |
| stgcn_diffusion       | MED             | NEU             |         3 |         0.0239938  |      0.00230038  |       0.0225238   |        0.0266448  |    2.26389 |     0.297742 |      0.00132812  |                  0.00260312  |
| stgcn_diffusion       | MED             | WCE             |         3 |         0.00342997 |      0.000347009 |       0.00314055  |        0.00381466 |    2.04873 |     0.287975 |      0.000200346 |                  0.000392677 |
| stgcn_diffusion       | NEU             | MED             |         3 |         0.0129067  |      0.00363727  |       0.0104951   |        0.0170904  |    2.07699 |     0.1906   |      0.00209998  |                  0.00411596  |
| stgcn_diffusion       | NEU             | WCE             |         3 |         0.00466561 |      0.00218245  |       0.00315708  |        0.00716811 |    2.04997 |     0.289909 |      0.00126004  |                  0.00246967  |
| stgcn_diffusion       | WCE             | MED             |         3 |         0.00641619 |      0.000311808 |       0.00608469  |        0.00670362 |    2.0705  |     0.187907 |      0.000180022 |                  0.000352843 |
| stgcn_diffusion       | WCE             | NEU             |         3 |         0.0177209  |      0.0043303   |       0.0149493   |        0.0227109  |    2.25762 |     0.292968 |      0.0025001   |                  0.0049002   |

## KBS uncertainty, group-by-cell random forest

| forecast_model        | feature_set         | cv_kind       | estimator     |   n_seeds |   mae_mean |     mae_sd |     r2_mean |     r2_sd |     r2_min |    r2_max |     r2_se |   r2_ci95_halfwidth |
|:----------------------|:--------------------|:--------------|:--------------|----------:|-----------:|-----------:|------------:|----------:|-----------:|----------:|----------:|--------------------:|
| graphwavenet_transfer | physical_plus_shift | group_by_cell | random_forest |         3 |  0.0125995 | 0.00429332 |  0.616503   | 0.0907334 |  0.541703  | 0.717435  | 0.052385  |           0.102675  |
| graphwavenet_transfer | physical_knowledge  | group_by_cell | random_forest |         3 |  0.015835  | 0.00806867 |  0.510344   | 0.0737834 |  0.431143  | 0.577135  | 0.0425989 |           0.0834938 |
| graphwavenet_transfer | generic_shift       | group_by_cell | random_forest |         3 |  0.0200164 | 0.00888606 |  0.0282499  | 0.0224022 |  0.0033253 | 0.0467064 | 0.0129339 |           0.0253504 |
| stgcn_diffusion       | physical_plus_shift | group_by_cell | random_forest |         3 |  0.0105191 | 0.00105168 |  0.65827    | 0.0421267 |  0.616846  | 0.701066  | 0.0243219 |           0.0476709 |
| stgcn_diffusion       | physical_knowledge  | group_by_cell | random_forest |         3 |  0.0137071 | 0.00198768 |  0.550399   | 0.0442976 |  0.521474  | 0.601396  | 0.0255752 |           0.0501275 |
| stgcn_diffusion       | generic_shift       | group_by_cell | random_forest |         3 |  0.0182194 | 0.00211379 | -0.00535623 | 0.030753  | -0.0312686 | 0.0286276 | 0.0177553 |           0.0348003 |

## Figures

- `figures/fig_large_degradation_heatmap_graphwavenet.png`
- `figures/fig_large_degradation_heatmap_stgcn.png`
- `figures/fig_large_degradation_uncertainty.png`
- `figures/fig_large_kbs_r2_group_by_cell.png`
