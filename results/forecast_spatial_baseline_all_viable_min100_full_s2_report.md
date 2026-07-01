# Spatial baseline forecasting experiment

Dataset: `forecast_dataset_large_all_viable_min100_full_s2.npz`.

Model:

- `spatial_knn_ridge`: ridge regression trained on source-region stations;
- features: own previous-day log precipitation, local kNN previous-day mean, local kNN wet fraction;
- kNN graph: 5 nearest stations within each target/source AR6 region.

Interpretation:

- this is a lightweight spatial model, not a full ST-GNN;
- it tests whether a transferable local spatial-lag rule adds value before training Graph WaveNet or AGCRN.

## Pair summary

| source_region   | target_region   | model             |   n_stations |   n_cells |   mae_mean |   brier_mean |   mae_out_minus_in_mean |   brier_out_minus_in_mean |
|:----------------|:----------------|:------------------|-------------:|----------:|-----------:|-------------:|------------------------:|--------------------------:|
| CNA             | CNA             | spatial_knn_ridge |          438 |        14 |    2.35993 |     0.202591 |             0           |               0           |
| CNA             | EAS             | spatial_knn_ridge |          110 |        16 |    6.23103 |     0.237972 |            -0.0264059   |              -0.00804076  |
| CNA             | EAU             | spatial_knn_ridge |          241 |         6 |    2.98103 |     0.229746 |            -0.0114375   |              -0.00250263  |
| CNA             | ENA             | spatial_knn_ridge |          522 |        21 |    3.31907 |     0.295923 |            -0.0812374   |              -0.0145256   |
| CNA             | MED             | spatial_knn_ridge |          328 |        19 |    1.89643 |     0.187058 |             0.0224523   |               0.000377442 |
| CNA             | NCA             | spatial_knn_ridge |          144 |         7 |    1.26216 |     0.111315 |             0.121021    |               0.00139012  |
| CNA             | NEU             | spatial_knn_ridge |         1000 |        28 |    2.31385 |     0.298397 |            -0.0538156   |              -0.00510675  |
| CNA             | NWN             | spatial_knn_ridge |          183 |        36 |    2.59225 |     0.242452 |             0.0749518   |              -0.00292386  |
| CNA             | SAU             | spatial_knn_ridge |          351 |        13 |    2.0157  |     0.238427 |            -0.018018    |               0.000398096 |
| CNA             | WCE             | spatial_knn_ridge |         1000 |        17 |    2.21176 |     0.297474 |            -0.069079    |              -0.00706954  |
| CNA             | WNA             | spatial_knn_ridge |          975 |        17 |    2.18035 |     0.227427 |             0.0285721   |              -0.00393979  |
| EAS             | CNA             | spatial_knn_ridge |          438 |        14 |    2.51555 |     0.229948 |             0.155612    |               0.0273565   |
| EAS             | EAS             | spatial_knn_ridge |          110 |        16 |    6.25743 |     0.246012 |             0           |               0           |
| EAS             | EAU             | spatial_knn_ridge |          241 |         6 |    3.08389 |     0.244946 |             0.0914245   |               0.0126977   |
| EAS             | ENA             | spatial_knn_ridge |          522 |        21 |    3.47351 |     0.32358  |             0.0731986   |               0.0131318   |
| EAS             | MED             | spatial_knn_ridge |          328 |        19 |    2.00464 |     0.199266 |             0.130653    |               0.0125854   |
| EAS             | NCA             | spatial_knn_ridge |          144 |         7 |    1.39155 |     0.127273 |             0.250413    |               0.0173475   |
| EAS             | NEU             | spatial_knn_ridge |         1000 |        28 |    2.36938 |     0.305539 |             0.00172038  |               0.00203566  |
| EAS             | NWN             | spatial_knn_ridge |          183 |        36 |    2.60455 |     0.254045 |             0.087255    |               0.00866916  |
| EAS             | SAU             | spatial_knn_ridge |          351 |        13 |    2.1282  |     0.256573 |             0.0944786   |               0.0185445   |
| EAS             | WCE             | spatial_knn_ridge |         1000 |        17 |    2.29769 |     0.308521 |             0.016851    |               0.00397756  |
| EAS             | WNA             | spatial_knn_ridge |          975 |        17 |    2.23318 |     0.236794 |             0.0814023   |               0.00542665  |
| EAU             | CNA             | spatial_knn_ridge |          438 |        14 |    2.39156 |     0.211227 |             0.0316273   |               0.00863574  |
| EAU             | EAS             | spatial_knn_ridge |          110 |        16 |    6.21437 |     0.235356 |            -0.0430591   |              -0.0106565   |
| EAU             | EAU             | spatial_knn_ridge |          241 |         6 |    2.99247 |     0.232249 |             0           |               0           |
| EAU             | ENA             | spatial_knn_ridge |          522 |        21 |    3.35331 |     0.304667 |            -0.0470013   |              -0.00578109  |
| EAU             | MED             | spatial_knn_ridge |          328 |        19 |    1.90757 |     0.186751 |             0.0335856   |               7.07563e-05 |
| EAU             | NCA             | spatial_knn_ridge |          144 |         7 |    1.28033 |     0.114007 |             0.139191    |               0.00408181  |
| EAU             | NEU             | spatial_knn_ridge |         1000 |        28 |    2.31486 |     0.297808 |            -0.0527993   |              -0.00569588  |
| EAU             | NWN             | spatial_knn_ridge |          183 |        36 |    2.57062 |     0.235951 |             0.053322    |              -0.00942433  |
| EAU             | SAU             | spatial_knn_ridge |          351 |        13 |    2.03045 |     0.24048  |            -0.00326644  |               0.002451    |
| EAU             | WCE             | spatial_knn_ridge |         1000 |        17 |    2.22145 |     0.29836  |            -0.0593896   |              -0.00618369  |
| EAU             | WNA             | spatial_knn_ridge |          975 |        17 |    2.17628 |     0.225087 |             0.0245109   |              -0.00627952  |
| ENA             | CNA             | spatial_knn_ridge |          438 |        14 |    2.4818  |     0.216856 |             0.121862    |               0.014265    |
| ENA             | EAS             | spatial_knn_ridge |          110 |        16 |    6.33243 |     0.246766 |             0.0749949   |               0.000753715 |
| ENA             | EAU             | spatial_knn_ridge |          241 |         6 |    3.09042 |     0.240855 |             0.0979579   |               0.00860595  |
| ENA             | ENA             | spatial_knn_ridge |          522 |        21 |    3.40031 |     0.310448 |             0           |               0           |
| ENA             | MED             | spatial_knn_ridge |          328 |        19 |    2.02209 |     0.199126 |             0.148109    |               0.0124452   |
| ENA             | NCA             | spatial_knn_ridge |          144 |         7 |    1.42189 |     0.122142 |             0.280754    |               0.0122168   |
| ENA             | NEU             | spatial_knn_ridge |         1000 |        28 |    2.37485 |     0.305478 |             0.00719172  |               0.00197454  |
| ENA             | NWN             | spatial_knn_ridge |          183 |        36 |    2.68341 |     0.25925  |             0.166111    |               0.013874    |
| ENA             | SAU             | spatial_knn_ridge |          351 |        13 |    2.11851 |     0.252874 |             0.0847909   |               0.0148451   |
| ENA             | WCE             | spatial_knn_ridge |         1000 |        17 |    2.28252 |     0.307291 |             0.00167854  |               0.00274736  |
| ENA             | WNA             | spatial_knn_ridge |          975 |        17 |    2.28786 |     0.237014 |             0.136088    |               0.00564677  |
| MED             | CNA             | spatial_knn_ridge |          438 |        14 |    2.36728 |     0.214365 |             0.00734615  |               0.0117738   |
| MED             | EAS             | spatial_knn_ridge |          110 |        16 |    6.19146 |     0.233606 |            -0.0659763   |              -0.0124063   |
| MED             | EAU             | spatial_knn_ridge |          241 |         6 |    2.96613 |     0.232169 |            -0.0263383   |              -8.0162e-05  |
| MED             | ENA             | spatial_knn_ridge |          522 |        21 |    3.34227 |     0.307501 |            -0.0580428   |              -0.00294768  |
| MED             | MED             | spatial_knn_ridge |          328 |        19 |    1.87398 |     0.18668  |             0           |               0           |
| MED             | NCA             | spatial_knn_ridge |          144 |         7 |    1.23885 |     0.114731 |             0.0977084   |               0.00480525  |
| MED             | NEU             | spatial_knn_ridge |         1000 |        28 |    2.30099 |     0.298417 |            -0.0666679   |              -0.00508683  |
| MED             | NWN             | spatial_knn_ridge |          183 |        36 |    2.54231 |     0.234628 |             0.0250106   |              -0.0107478   |
| MED             | SAU             | spatial_knn_ridge |          351 |        13 |    2.0075  |     0.241788 |            -0.0262191   |               0.00375892  |
| MED             | WCE             | spatial_knn_ridge |         1000 |        17 |    2.20718 |     0.299221 |            -0.0736574   |              -0.00532272  |
| MED             | WNA             | spatial_knn_ridge |          975 |        17 |    2.14808 |     0.225532 |            -0.00369516  |              -0.00583454  |
| NCA             | CNA             | spatial_knn_ridge |          438 |        14 |    2.28889 |     0.204899 |            -0.0710437   |               0.00230777  |
| NCA             | EAS             | spatial_knn_ridge |          110 |        16 |    6.13608 |     0.233898 |            -0.121348    |              -0.0121145   |
| NCA             | EAU             | spatial_knn_ridge |          241 |         6 |    2.90434 |     0.228684 |            -0.0881247   |              -0.00356494  |
| NCA             | ENA             | spatial_knn_ridge |          522 |        21 |    3.28945 |     0.29744  |            -0.110859    |              -0.0130085   |
| NCA             | MED             | spatial_knn_ridge |          328 |        19 |    1.8068  |     0.184245 |            -0.0671861   |              -0.0024352   |
| NCA             | NCA             | spatial_knn_ridge |          144 |         7 |    1.14114 |     0.109925 |             0           |               0           |
| NCA             | NEU             | spatial_knn_ridge |         1000 |        28 |    2.27189 |     0.297059 |            -0.0957735   |              -0.00644431  |
| NCA             | NWN             | spatial_knn_ridge |          183 |        36 |    2.50278 |     0.234922 |            -0.0145203   |              -0.010454    |
| NCA             | SAU             | spatial_knn_ridge |          351 |        13 |    1.95387 |     0.237141 |            -0.0798482   |              -0.000887594 |
| NCA             | WCE             | spatial_knn_ridge |         1000 |        17 |    2.17274 |     0.29656  |            -0.108099    |              -0.00798319  |
| NCA             | WNA             | spatial_knn_ridge |          975 |        17 |    2.08557 |     0.223852 |            -0.0662014   |              -0.00751491  |
| NEU             | CNA             | spatial_knn_ridge |          438 |        14 |    2.50284 |     0.224965 |             0.142908    |               0.022374    |
| NEU             | EAS             | spatial_knn_ridge |          110 |        16 |    6.29115 |     0.242649 |             0.0337204   |              -0.00336305  |
| NEU             | EAU             | spatial_knn_ridge |          241 |         6 |    3.08687 |     0.241601 |             0.0944043   |               0.00935228  |
| NEU             | ENA             | spatial_knn_ridge |          522 |        21 |    3.43219 |     0.318532 |             0.0318836   |               0.00808336  |
| NEU             | MED             | spatial_knn_ridge |          328 |        19 |    2.01574 |     0.19617  |             0.141756    |               0.00948957  |
| NEU             | NCA             | spatial_knn_ridge |          144 |         7 |    1.41881 |     0.123367 |             0.277674    |               0.0134414   |
| NEU             | NEU             | spatial_knn_ridge |         1000 |        28 |    2.36766 |     0.303503 |             0           |               0           |
| NEU             | NWN             | spatial_knn_ridge |          183 |        36 |    2.64286 |     0.249009 |             0.125567    |               0.00363337  |
| NEU             | SAU             | spatial_knn_ridge |          351 |        13 |    2.12013 |     0.252444 |             0.0864087   |               0.0144149   |
| NEU             | WCE             | spatial_knn_ridge |         1000 |        17 |    2.28376 |     0.306022 |             0.00291457  |               0.0014788   |
| NEU             | WNA             | spatial_knn_ridge |          975 |        17 |    2.2645  |     0.233864 |             0.112729    |               0.00249701  |
| NWN             | CNA             | spatial_knn_ridge |          438 |        14 |    2.48266 |     0.224621 |             0.122723    |               0.0220302   |
| NWN             | EAS             | spatial_knn_ridge |          110 |        16 |    6.24495 |     0.240654 |            -0.0124781   |              -0.00535878  |
| NWN             | EAU             | spatial_knn_ridge |          241 |         6 |    3.04754 |     0.239994 |             0.0550738   |               0.00774491  |
| NWN             | ENA             | spatial_knn_ridge |          522 |        21 |    3.50356 |     0.318339 |             0.103255    |               0.00789057  |
| NWN             | MED             | spatial_knn_ridge |          328 |        19 |    1.93909 |     0.193593 |             0.0651085   |               0.00691232  |
| NWN             | NCA             | spatial_knn_ridge |          144 |         7 |    1.28413 |     0.12332  |             0.142989    |               0.0133947   |
| NWN             | NEU             | spatial_knn_ridge |         1000 |        28 |    2.35821 |     0.301136 |            -0.00945605  |              -0.0023675   |
| NWN             | NWN             | spatial_knn_ridge |          183 |        36 |    2.5173  |     0.245376 |             0           |               0           |
| NWN             | SAU             | spatial_knn_ridge |          351 |        13 |    2.09987 |     0.249126 |             0.0661495   |               0.0110977   |
| NWN             | WCE             | spatial_knn_ridge |         1000 |        17 |    2.29061 |     0.302995 |             0.00976943  |              -0.00154893  |
| NWN             | WNA             | spatial_knn_ridge |          975 |        17 |    2.15269 |     0.232984 |             0.00091299  |               0.00161699  |
| SAU             | CNA             | spatial_knn_ridge |          438 |        14 |    2.3964  |     0.210366 |             0.0364618   |               0.00777499  |
| SAU             | EAS             | spatial_knn_ridge |          110 |        16 |    6.23471 |     0.232957 |            -0.0227193   |              -0.0130557   |
| SAU             | EAU             | spatial_knn_ridge |          241 |         6 |    2.99974 |     0.229824 |             0.00727607  |              -0.00242489  |
| SAU             | ENA             | spatial_knn_ridge |          522 |        21 |    3.34941 |     0.303713 |            -0.0508981   |              -0.00673559  |
| SAU             | MED             | spatial_knn_ridge |          328 |        19 |    1.91544 |     0.184552 |             0.0414576   |              -0.00212831  |
| SAU             | NCA             | spatial_knn_ridge |          144 |         7 |    1.29575 |     0.112876 |             0.154607    |               0.00295065  |
| SAU             | NEU             | spatial_knn_ridge |         1000 |        28 |    2.32113 |     0.296838 |            -0.0465372   |              -0.00666581  |
| SAU             | NWN             | spatial_knn_ridge |          183 |        36 |    2.58449 |     0.23255  |             0.0671925   |              -0.0128259   |
| SAU             | SAU             | spatial_knn_ridge |          351 |        13 |    2.03372 |     0.238029 |             0           |               0           |
| SAU             | WCE             | spatial_knn_ridge |         1000 |        17 |    2.22297 |     0.296822 |            -0.0578752   |              -0.0077221   |
| SAU             | WNA             | spatial_knn_ridge |          975 |        17 |    2.19255 |     0.223831 |             0.040781    |              -0.00753606  |
| WCE             | CNA             | spatial_knn_ridge |          438 |        14 |    2.49752 |     0.222744 |             0.137589    |               0.0201528   |
| WCE             | EAS             | spatial_knn_ridge |          110 |        16 |    6.31195 |     0.239501 |             0.0545189   |              -0.00651133  |
| WCE             | EAU             | spatial_knn_ridge |          241 |         6 |    3.08848 |     0.239577 |             0.096013    |               0.00732842  |
| WCE             | ENA             | spatial_knn_ridge |          522 |        21 |    3.41887 |     0.316063 |             0.0185602   |               0.00561442  |
| WCE             | MED             | spatial_knn_ridge |          328 |        19 |    2.01745 |     0.193526 |             0.143465    |               0.00684545  |
| WCE             | NCA             | spatial_knn_ridge |          144 |         7 |    1.42521 |     0.121054 |             0.284064    |               0.0111286   |
| WCE             | NEU             | spatial_knn_ridge |         1000 |        28 |    2.37048 |     0.302363 |             0.00281446  |              -0.00114065  |
| WCE             | NWN             | spatial_knn_ridge |          183 |        36 |    2.65632 |     0.245032 |             0.139024    |              -0.000343515 |
| WCE             | SAU             | spatial_knn_ridge |          351 |        13 |    2.11779 |     0.250323 |             0.0840714   |               0.0122944   |
| WCE             | WCE             | spatial_knn_ridge |         1000 |        17 |    2.28084 |     0.304544 |             0           |               0           |
| WCE             | WNA             | spatial_knn_ridge |          975 |        17 |    2.27707 |     0.232411 |             0.125291    |               0.00104407  |
| WNA             | CNA             | spatial_knn_ridge |          438 |        14 |    2.40235 |     0.221321 |             0.0424178   |               0.0187296   |
| WNA             | EAS             | spatial_knn_ridge |          110 |        16 |    6.18829 |     0.239841 |            -0.0691434   |              -0.00617164  |
| WNA             | EAU             | spatial_knn_ridge |          241 |         6 |    2.99276 |     0.239417 |             0.000291038 |               0.00716823  |
| WNA             | ENA             | spatial_knn_ridge |          522 |        21 |    3.38994 |     0.31425  |            -0.0103637   |               0.00380158  |
| WNA             | MED             | spatial_knn_ridge |          328 |        19 |    1.9003  |     0.19388  |             0.0263207   |               0.00719922  |
| WNA             | NCA             | spatial_knn_ridge |          144 |         7 |    1.25484 |     0.120198 |             0.113696    |               0.0102725   |
| WNA             | NEU             | spatial_knn_ridge |         1000 |        28 |    2.32161 |     0.303008 |            -0.0460559   |              -0.00049541  |
| WNA             | NWN             | spatial_knn_ridge |          183 |        36 |    2.54222 |     0.246383 |             0.0249222   |               0.0010077   |
| WNA             | SAU             | spatial_knn_ridge |          351 |        13 |    2.04503 |     0.250753 |             0.0113058   |               0.0127246   |
| WNA             | WCE             | spatial_knn_ridge |         1000 |        17 |    2.24303 |     0.305124 |            -0.0378083   |               0.000580711 |
| WNA             | WNA             | spatial_knn_ridge |          975 |        17 |    2.15177 |     0.231367 |             0           |               0           |
