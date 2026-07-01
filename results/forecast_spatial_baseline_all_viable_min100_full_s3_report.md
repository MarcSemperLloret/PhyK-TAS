# Spatial baseline forecasting experiment

Dataset: `forecast_dataset_large_all_viable_min100_full_s3.npz`.

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
| CNA             | CNA             | spatial_knn_ridge |          438 |        14 |    2.35432 |     0.201743 |             0           |               0           |
| CNA             | EAS             | spatial_knn_ridge |          110 |        16 |    6.22662 |     0.2369   |            -0.0308225   |              -0.00912794  |
| CNA             | EAU             | spatial_knn_ridge |          241 |         6 |    2.97546 |     0.228817 |            -0.0153574   |              -0.00311019  |
| CNA             | ENA             | spatial_knn_ridge |          522 |        21 |    3.31499 |     0.295064 |            -0.0832291   |              -0.0150655   |
| CNA             | MED             | spatial_knn_ridge |          328 |        19 |    1.8899  |     0.185848 |             0.0186985   |              -0.00041637  |
| CNA             | NCA             | spatial_knn_ridge |          144 |         7 |    1.25492 |     0.110322 |             0.111891    |              -0.000187296 |
| CNA             | NEU             | spatial_knn_ridge |         1000 |        29 |    2.25769 |     0.297768 |            -0.0595742   |              -0.00589111  |
| CNA             | NWN             | spatial_knn_ridge |          183 |        36 |    2.58684 |     0.240661 |             0.0710216   |              -0.00424239  |
| CNA             | SAU             | spatial_knn_ridge |          351 |        13 |    2.01035 |     0.237153 |            -0.0256182   |              -0.000805212 |
| CNA             | WCE             | spatial_knn_ridge |         1000 |        15 |    2.17037 |     0.296329 |            -0.0723241   |              -0.00699546  |
| CNA             | WNA             | spatial_knn_ridge |          975 |        17 |    2.17546 |     0.226403 |             0.0242992   |              -0.00494467  |
| EAS             | CNA             | spatial_knn_ridge |          438 |        14 |    2.5142  |     0.229663 |             0.159883    |               0.0279205   |
| EAS             | EAS             | spatial_knn_ridge |          110 |        16 |    6.25744 |     0.246028 |             0           |               0           |
| EAS             | EAU             | spatial_knn_ridge |          241 |         6 |    3.08334 |     0.244889 |             0.0925222   |               0.0129621   |
| EAS             | ENA             | spatial_knn_ridge |          522 |        21 |    3.47177 |     0.323369 |             0.0735518   |               0.0132392   |
| EAS             | MED             | spatial_knn_ridge |          328 |        19 |    2.00434 |     0.19939  |             0.133141    |               0.0131257   |
| EAS             | NCA             | spatial_knn_ridge |          144 |         7 |    1.39107 |     0.12721  |             0.248041    |               0.0167006   |
| EAS             | NEU             | spatial_knn_ridge |         1000 |        29 |    2.31844 |     0.305923 |             0.00117507  |               0.00226419  |
| EAS             | NWN             | spatial_knn_ridge |          183 |        36 |    2.60507 |     0.253874 |             0.0892572   |               0.00897002  |
| EAS             | SAU             | spatial_knn_ridge |          351 |        13 |    2.12755 |     0.256347 |             0.0915802   |               0.0183888   |
| EAS             | WCE             | spatial_knn_ridge |         1000 |        15 |    2.25959 |     0.30791  |             0.0169036   |               0.00458508  |
| EAS             | WNA             | spatial_knn_ridge |          975 |        17 |    2.2331  |     0.236305 |             0.0819363   |               0.00495732  |
| EAU             | CNA             | spatial_knn_ridge |          438 |        14 |    2.39132 |     0.211451 |             0.0370055   |               0.00970871  |
| EAU             | EAS             | spatial_knn_ridge |          110 |        16 |    6.21121 |     0.235    |            -0.0462349   |              -0.0110278   |
| EAU             | EAU             | spatial_knn_ridge |          241 |         6 |    2.99082 |     0.231927 |             0           |               0           |
| EAU             | ENA             | spatial_knn_ridge |          522 |        21 |    3.35422 |     0.30501  |            -0.0440047   |              -0.00511928  |
| EAU             | MED             | spatial_knn_ridge |          328 |        19 |    1.90549 |     0.186443 |             0.0342938   |               0.000178167 |
| EAU             | NCA             | spatial_knn_ridge |          144 |         7 |    1.27818 |     0.11412  |             0.135144    |               0.00361089  |
| EAU             | NEU             | spatial_knn_ridge |         1000 |        29 |    2.26133 |     0.297831 |            -0.0559434   |              -0.00582802  |
| EAU             | NWN             | spatial_knn_ridge |          183 |        36 |    2.56708 |     0.235246 |             0.051268    |              -0.00965823  |
| EAU             | SAU             | spatial_knn_ridge |          351 |        13 |    2.02905 |     0.240034 |            -0.00691449  |               0.0020756   |
| EAU             | WCE             | spatial_knn_ridge |         1000 |        15 |    2.18282 |     0.297516 |            -0.0598681   |              -0.00580832  |
| EAU             | WNA             | spatial_knn_ridge |          975 |        17 |    2.17368 |     0.224863 |             0.0225176   |              -0.00648446  |
| ENA             | CNA             | spatial_knn_ridge |          438 |        14 |    2.47979 |     0.216628 |             0.125472    |               0.0148853   |
| ENA             | EAS             | spatial_knn_ridge |          110 |        16 |    6.33461 |     0.24639  |             0.0771634   |               0.000361917 |
| ENA             | EAU             | spatial_knn_ridge |          241 |         6 |    3.08932 |     0.240488 |             0.0985069   |               0.00856066  |
| ENA             | ENA             | spatial_knn_ridge |          522 |        21 |    3.39822 |     0.31013  |             0           |               0           |
| ENA             | MED             | spatial_knn_ridge |          328 |        19 |    2.02036 |     0.198694 |             0.149163    |               0.0124292   |
| ENA             | NCA             | spatial_knn_ridge |          144 |         7 |    1.42017 |     0.121679 |             0.277142    |               0.0111696   |
| ENA             | NEU             | spatial_knn_ridge |         1000 |        29 |    2.32133 |     0.30582  |             0.00405796  |               0.00216078  |
| ENA             | NWN             | spatial_knn_ridge |          183 |        36 |    2.68321 |     0.258631 |             0.167395    |               0.0137273   |
| ENA             | SAU             | spatial_knn_ridge |          351 |        13 |    2.11727 |     0.252922 |             0.0812992   |               0.0149638   |
| ENA             | WCE             | spatial_knn_ridge |         1000 |        15 |    2.24375 |     0.306457 |             0.0010633   |               0.00313208  |
| ENA             | WNA             | spatial_knn_ridge |          975 |        17 |    2.28799 |     0.236492 |             0.13683     |               0.00514479  |
| MED             | CNA             | spatial_knn_ridge |          438 |        14 |    2.36446 |     0.213612 |             0.010144    |               0.0118695   |
| MED             | EAS             | spatial_knn_ridge |          110 |        16 |    6.18797 |     0.233449 |            -0.0694716   |              -0.0125788   |
| MED             | EAU             | spatial_knn_ridge |          241 |         6 |    2.9634  |     0.231681 |            -0.0274185   |              -0.000246282 |
| MED             | ENA             | spatial_knn_ridge |          522 |        21 |    3.34045 |     0.306972 |            -0.0577706   |              -0.0031577   |
| MED             | MED             | spatial_knn_ridge |          328 |        19 |    1.8712  |     0.186265 |             0           |               0           |
| MED             | NCA             | spatial_knn_ridge |          144 |         7 |    1.23523 |     0.114367 |             0.0921963   |               0.00385754  |
| MED             | NEU             | spatial_knn_ridge |         1000 |        29 |    2.247   |     0.298561 |            -0.0702692   |              -0.00509788  |
| MED             | NWN             | spatial_knn_ridge |          183 |        36 |    2.53985 |     0.234089 |             0.0240324   |              -0.0108147   |
| MED             | SAU             | spatial_knn_ridge |          351 |        13 |    2.00492 |     0.241013 |            -0.0310493   |               0.00305408  |
| MED             | WCE             | spatial_knn_ridge |         1000 |        15 |    2.16765 |     0.298216 |            -0.0750362   |              -0.0051088   |
| MED             | WNA             | spatial_knn_ridge |          975 |        17 |    2.14513 |     0.22526  |            -0.00603726  |              -0.00608764  |
| NCA             | CNA             | spatial_knn_ridge |          438 |        14 |    2.28982 |     0.205929 |            -0.0644941   |               0.00418621  |
| NCA             | EAS             | spatial_knn_ridge |          110 |        16 |    6.14077 |     0.23427  |            -0.116677    |              -0.0117578   |
| NCA             | EAU             | spatial_knn_ridge |          241 |         6 |    2.90634 |     0.229667 |            -0.0844815   |              -0.00225999  |
| NCA             | ENA             | spatial_knn_ridge |          522 |        21 |    3.28942 |     0.298454 |            -0.108798    |              -0.0116754   |
| NCA             | MED             | spatial_knn_ridge |          328 |        19 |    1.8084  |     0.185065 |            -0.062803    |              -0.00119953  |
| NCA             | NCA             | spatial_knn_ridge |          144 |         7 |    1.14303 |     0.110509 |             0           |               0           |
| NCA             | NEU             | spatial_knn_ridge |         1000 |        29 |    2.22067 |     0.297997 |            -0.0965983   |              -0.00566148  |
| NCA             | NWN             | spatial_knn_ridge |          183 |        36 |    2.50578 |     0.235642 |            -0.0100375   |              -0.00926168  |
| NCA             | SAU             | spatial_knn_ridge |          351 |        13 |    1.95597 |     0.238873 |            -0.0799955   |               0.000914705 |
| NCA             | WCE             | spatial_knn_ridge |         1000 |        15 |    2.13688 |     0.297231 |            -0.105814    |              -0.00609339  |
| NCA             | WNA             | spatial_knn_ridge |          975 |        17 |    2.08863 |     0.224402 |            -0.0625346   |              -0.00694554  |
| NEU             | CNA             | spatial_knn_ridge |          438 |        14 |    2.50647 |     0.225222 |             0.152157    |               0.0234798   |
| NEU             | EAS             | spatial_knn_ridge |          110 |        16 |    6.29546 |     0.241803 |             0.0380146   |              -0.00422543  |
| NEU             | EAU             | spatial_knn_ridge |          241 |         6 |    3.08978 |     0.241391 |             0.0989604   |               0.0094634   |
| NEU             | ENA             | spatial_knn_ridge |          522 |        21 |    3.43358 |     0.318771 |             0.0353562   |               0.00864129  |
| NEU             | MED             | spatial_knn_ridge |          328 |        19 |    2.01899 |     0.195618 |             0.147788    |               0.00935301  |
| NEU             | NCA             | spatial_knn_ridge |          144 |         7 |    1.42453 |     0.123345 |             0.281501    |               0.0128356   |
| NEU             | NEU             | spatial_knn_ridge |         1000 |        29 |    2.31727 |     0.303659 |             0           |               0           |
| NEU             | NWN             | spatial_knn_ridge |          183 |        36 |    2.64573 |     0.248082 |             0.129911    |               0.00317815  |
| NEU             | SAU             | spatial_knn_ridge |          351 |        13 |    2.12208 |     0.252175 |             0.086112    |               0.0142161   |
| NEU             | WCE             | spatial_knn_ridge |         1000 |        15 |    2.24697 |     0.305137 |             0.00428032  |               0.00181216  |
| NEU             | WNA             | spatial_knn_ridge |          975 |        17 |    2.26862 |     0.233655 |             0.117459    |               0.00230786  |
| NWN             | CNA             | spatial_knn_ridge |          438 |        14 |    2.48174 |     0.224305 |             0.127425    |               0.0225619   |
| NWN             | EAS             | spatial_knn_ridge |          110 |        16 |    6.24608 |     0.240573 |            -0.0113627   |              -0.00545557  |
| NWN             | EAU             | spatial_knn_ridge |          241 |         6 |    3.04654 |     0.239733 |             0.0557248   |               0.00780585  |
| NWN             | ENA             | spatial_knn_ridge |          522 |        21 |    3.50316 |     0.318137 |             0.104939    |               0.00800757  |
| NWN             | MED             | spatial_knn_ridge |          328 |        19 |    1.9377  |     0.193281 |             0.0664983   |               0.00701609  |
| NWN             | NCA             | spatial_knn_ridge |          144 |         7 |    1.28259 |     0.12312  |             0.13956     |               0.0126108   |
| NWN             | NEU             | spatial_knn_ridge |         1000 |        29 |    2.30763 |     0.301209 |            -0.00963851  |              -0.00244946  |
| NWN             | NWN             | spatial_knn_ridge |          183 |        36 |    2.51582 |     0.244904 |             0           |               0           |
| NWN             | SAU             | spatial_knn_ridge |          351 |        13 |    2.09849 |     0.248667 |             0.0625234   |               0.0107083   |
| NWN             | WCE             | spatial_knn_ridge |         1000 |        15 |    2.25133 |     0.302125 |             0.00863781  |              -0.00119982  |
| NWN             | WNA             | spatial_knn_ridge |          975 |        17 |    2.15126 |     0.232766 |             9.26597e-05 |               0.00141836  |
| SAU             | CNA             | spatial_knn_ridge |          438 |        14 |    2.39891 |     0.210444 |             0.0445978   |               0.00870137  |
| SAU             | EAS             | spatial_knn_ridge |          110 |        16 |    6.23959 |     0.232719 |            -0.0178513   |              -0.0133094   |
| SAU             | EAU             | spatial_knn_ridge |          241 |         6 |    3.00263 |     0.22968  |             0.0118147   |              -0.00224722  |
| SAU             | ENA             | spatial_knn_ridge |          522 |        21 |    3.35015 |     0.30381  |            -0.048074    |              -0.00631981  |
| SAU             | MED             | spatial_knn_ridge |          328 |        19 |    1.91862 |     0.184374 |             0.0474222   |              -0.00189063  |
| SAU             | NCA             | spatial_knn_ridge |          144 |         7 |    1.30034 |     0.11289  |             0.157304    |               0.00238106  |
| SAU             | NEU             | spatial_knn_ridge |         1000 |        29 |    2.26991 |     0.297054 |            -0.0473617   |              -0.00660525  |
| SAU             | NWN             | spatial_knn_ridge |          183 |        36 |    2.58815 |     0.232383 |             0.0723296   |              -0.0125204   |
| SAU             | SAU             | spatial_knn_ridge |          351 |        13 |    2.03597 |     0.237959 |             0           |               0           |
| SAU             | WCE             | spatial_knn_ridge |         1000 |        15 |    2.18666 |     0.296168 |            -0.0560263   |              -0.00715651  |
| SAU             | WNA             | spatial_knn_ridge |          975 |        17 |    2.19666 |     0.223722 |             0.0454984   |              -0.00762568  |
| WCE             | CNA             | spatial_knn_ridge |          438 |        14 |    2.49728 |     0.222218 |             0.142961    |               0.0204753   |
| WCE             | EAS             | spatial_knn_ridge |          110 |        16 |    6.31485 |     0.238689 |             0.0574015   |              -0.00733905  |
| WCE             | EAU             | spatial_knn_ridge |          241 |         6 |    3.08894 |     0.239045 |             0.0981229   |               0.00711736  |
| WCE             | ENA             | spatial_knn_ridge |          522 |        21 |    3.41738 |     0.315457 |             0.0191542   |               0.00532753  |
| WCE             | MED             | spatial_knn_ridge |          328 |        19 |    2.018   |     0.19274  |             0.146798    |               0.00647512  |
| WCE             | NCA             | spatial_knn_ridge |          144 |         7 |    1.42671 |     0.120599 |             0.28368     |               0.0100895   |
| WCE             | NEU             | spatial_knn_ridge |         1000 |        29 |    2.31831 |     0.302369 |             0.00103814  |              -0.00129007  |
| WCE             | NWN             | spatial_knn_ridge |          183 |        36 |    2.65812 |     0.244016 |             0.142302    |              -0.000887735 |
| WCE             | SAU             | spatial_knn_ridge |          351 |        13 |    2.11753 |     0.249556 |             0.0815646   |               0.0115973   |
| WCE             | WCE             | spatial_knn_ridge |         1000 |        15 |    2.24269 |     0.303325 |             0           |               0           |
| WCE             | WNA             | spatial_knn_ridge |          975 |        17 |    2.27908 |     0.231776 |             0.127919    |               0.000428564 |
| WNA             | CNA             | spatial_knn_ridge |          438 |        14 |    2.40566 |     0.221362 |             0.0513398   |               0.0196197   |
| WNA             | EAS             | spatial_knn_ridge |          110 |        16 |    6.18732 |     0.240124 |            -0.0701285   |              -0.00590454  |
| WNA             | EAU             | spatial_knn_ridge |          241 |         6 |    2.99469 |     0.239394 |             0.00387494  |               0.0074667   |
| WNA             | ENA             | spatial_knn_ridge |          522 |        21 |    3.39459 |     0.314334 |            -0.00363032  |               0.00420444  |
| WNA             | MED             | spatial_knn_ridge |          328 |        19 |    1.90214 |     0.193828 |             0.0309419   |               0.00756296  |
| WNA             | NCA             | spatial_knn_ridge |          144 |         7 |    1.25614 |     0.120335 |             0.113109    |               0.00982617  |
| WNA             | NEU             | spatial_knn_ridge |         1000 |        29 |    2.27182 |     0.303351 |            -0.0454443   |              -0.00030752  |
| WNA             | NWN             | spatial_knn_ridge |          183 |        36 |    2.54073 |     0.246455 |             0.0249193   |               0.00155169  |
| WNA             | SAU             | spatial_knn_ridge |          351 |        13 |    2.04729 |     0.250626 |             0.0113225   |               0.0126669   |
| WNA             | WCE             | spatial_knn_ridge |         1000 |        15 |    2.20746 |     0.304428 |            -0.0352271   |               0.00110323  |
| WNA             | WNA             | spatial_knn_ridge |          975 |        17 |    2.15116 |     0.231347 |             0           |               0           |
