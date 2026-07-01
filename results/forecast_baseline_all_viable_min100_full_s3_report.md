# Baseline forecasting experiment

Dataset:

- `forecast_dataset_large_all_viable_min100_full_s3.npz`;
- test period 2020-2025.

Models:

- `regional_doy_climatology`: source-region daily climatology learned on 2005-2012 and transferred to each target region;
- `station_persistence`: previous observed day at the same station, reported as a non-transfer meteorological baseline.

## Regional climatology pair summary

| source_region   | target_region   | model                    |   n_stations |   n_cells |   mae_mean |   brier_mean |   mae_out_minus_in_mean |   brier_out_minus_in_mean |
|:----------------|:----------------|:-------------------------|-------------:|----------:|-----------:|-------------:|------------------------:|--------------------------:|
| CNA             | CNA             | regional_doy_climatology |          438 |        14 |    3.49519 |     0.719544 |              0          |                0          |
| CNA             | EAS             | regional_doy_climatology |          110 |        16 |    7.051   |     0.626171 |             -1.81385    |                0.035252   |
| CNA             | EAU             | regional_doy_climatology |          241 |         6 |    4.08816 |     0.704585 |             -0.110242   |                0.0396785  |
| CNA             | ENA             | regional_doy_climatology |          522 |        21 |    4.14971 |     0.654317 |             -0.557076   |               -0.0698913  |
| CNA             | MED             | regional_doy_climatology |          328 |        19 |    3.15061 |     0.734532 |              0.344803   |                0.102945   |
| CNA             | NCA             | regional_doy_climatology |          144 |         7 |    2.75023 |     0.780482 |              0.893314   |                0.301809   |
| CNA             | NEU             | regional_doy_climatology |         1000 |        29 |    3.06321 |     0.627662 |              0.0159305  |               -0.0216993  |
| CNA             | NWN             | regional_doy_climatology |          183 |        36 |    3.54392 |     0.659596 |             -0.19641    |               -0.0656336  |
| CNA             | SAU             | regional_doy_climatology |          351 |        13 |    3.00673 |     0.678999 |              0.2294     |                0.0297962  |
| CNA             | WCE             | regional_doy_climatology |         1000 |        15 |    3.00157 |     0.634849 |             -0.0330287  |               -0.0209031  |
| CNA             | WNA             | regional_doy_climatology |          975 |        17 |    3.26712 |     0.69128  |              0.1392     |                0.0795171  |
| EAS             | CNA             | regional_doy_climatology |          438 |        14 |    6.50642 |     0.695442 |              3.01123    |               -0.0241016  |
| EAS             | EAS             | regional_doy_climatology |          110 |        16 |    8.86486 |     0.590919 |              0          |                0          |
| EAS             | EAU             | regional_doy_climatology |          241 |         6 |    7.32019 |     0.692859 |              3.12179    |                0.0279525  |
| EAS             | ENA             | regional_doy_climatology |          522 |        21 |    6.89441 |     0.642956 |              2.18763    |               -0.0812528  |
| EAS             | MED             | regional_doy_climatology |          328 |        19 |    6.58247 |     0.722718 |              3.77667    |                0.0911308  |
| EAS             | NCA             | regional_doy_climatology |          144 |         7 |    6.15121 |     0.752277 |              4.29429    |                0.273603   |
| EAS             | NEU             | regional_doy_climatology |         1000 |        29 |    6.05835 |     0.614914 |              3.01106    |               -0.0344478  |
| EAS             | NWN             | regional_doy_climatology |          183 |        36 |    6.55582 |     0.640414 |              2.81549    |               -0.0848161  |
| EAS             | SAU             | regional_doy_climatology |          351 |        13 |    6.05651 |     0.646349 |              3.27918    |               -0.00285443 |
| EAS             | WCE             | regional_doy_climatology |         1000 |        15 |    5.97185 |     0.623181 |              2.93724    |               -0.0325713  |
| EAS             | WNA             | regional_doy_climatology |          975 |        17 |    6.61807 |     0.683491 |              3.49015    |                0.0717281  |
| EAU             | CNA             | regional_doy_climatology |          438 |        14 |    3.77801 |     0.703005 |              0.282819   |               -0.0165387  |
| EAU             | EAS             | regional_doy_climatology |          110 |        16 |    7.53113 |     0.67661  |             -1.33372    |                0.0856906  |
| EAU             | EAU             | regional_doy_climatology |          241 |         6 |    4.1984  |     0.664906 |              0          |                0          |
| EAU             | ENA             | regional_doy_climatology |          522 |        21 |    4.35502 |     0.638499 |             -0.351761   |               -0.0857097  |
| EAU             | MED             | regional_doy_climatology |          328 |        19 |    3.27382 |     0.678137 |              0.468011   |                0.0465503  |
| EAU             | NCA             | regional_doy_climatology |          144 |         7 |    2.98502 |     0.744061 |              1.1281     |                0.265388   |
| EAU             | NEU             | regional_doy_climatology |         1000 |        29 |    3.2177  |     0.595765 |              0.170417   |               -0.0535966  |
| EAU             | NWN             | regional_doy_climatology |          183 |        36 |    3.75465 |     0.641234 |              0.01432    |               -0.0839953  |
| EAU             | SAU             | regional_doy_climatology |          351 |        13 |    3.30943 |     0.674493 |              0.532103   |                0.0252904  |
| EAU             | WCE             | regional_doy_climatology |         1000 |        15 |    3.18608 |     0.611595 |              0.151477   |               -0.0441569  |
| EAU             | WNA             | regional_doy_climatology |          975 |        17 |    3.28806 |     0.628201 |              0.160134   |                0.0164374  |
| ENA             | CNA             | regional_doy_climatology |          438 |        14 |    4.22986 |     0.816781 |              0.734675   |                0.0972376  |
| ENA             | EAS             | regional_doy_climatology |          110 |        16 |    7.69208 |     0.722788 |             -1.17278    |                0.131869   |
| ENA             | EAU             | regional_doy_climatology |          241 |         6 |    4.68285 |     0.770662 |              0.48445    |                0.105755   |
| ENA             | ENA             | regional_doy_climatology |          522 |        21 |    4.70679 |     0.724208 |              0          |                0          |
| ENA             | MED             | regional_doy_climatology |          328 |        19 |    3.84056 |     0.817314 |              1.03475    |                0.185728   |
| ENA             | NCA             | regional_doy_climatology |          144 |         7 |    3.56958 |     0.893239 |              1.71267    |                0.414565   |
| ENA             | NEU             | regional_doy_climatology |         1000 |        29 |    3.55766 |     0.662041 |              0.510382   |                0.0126788  |
| ENA             | NWN             | regional_doy_climatology |          183 |        36 |    4.11817 |     0.72092  |              0.377848   |               -0.00431002 |
| ENA             | SAU             | regional_doy_climatology |          351 |        13 |    3.66583 |     0.761603 |              0.888504   |                0.1124     |
| ENA             | WCE             | regional_doy_climatology |         1000 |        15 |    3.53222 |     0.687836 |              0.497613   |                0.0320843  |
| ENA             | WNA             | regional_doy_climatology |          975 |        17 |    3.82408 |     0.742494 |              0.696154   |                0.130731   |
| MED             | CNA             | regional_doy_climatology |          438 |        14 |    3.35909 |     0.68787  |             -0.136096   |               -0.0316731  |
| MED             | EAS             | regional_doy_climatology |          110 |        16 |    7.20818 |     0.6902   |             -1.65667    |                0.0992807  |
| MED             | EAU             | regional_doy_climatology |          241 |         6 |    3.80353 |     0.629389 |             -0.394873   |               -0.0355172  |
| MED             | ENA             | regional_doy_climatology |          522 |        21 |    4.02263 |     0.63437  |             -0.684155   |               -0.0898385  |
| MED             | MED             | regional_doy_climatology |          328 |        19 |    2.80581 |     0.631587 |              0          |                0          |
| MED             | NCA             | regional_doy_climatology |          144 |         7 |    2.50117 |     0.730183 |              0.644253   |                0.251509   |
| MED             | NEU             | regional_doy_climatology |         1000 |        29 |    2.84969 |     0.586864 |             -0.197593   |               -0.0624977  |
| MED             | NWN             | regional_doy_climatology |          183 |        36 |    3.36387 |     0.627526 |             -0.376459   |               -0.0977032  |
| MED             | SAU             | regional_doy_climatology |          351 |        13 |    2.91974 |     0.683377 |              0.142412   |                0.0341744  |
| MED             | WCE             | regional_doy_climatology |         1000 |        15 |    2.81934 |     0.602191 |             -0.215257   |               -0.0535612  |
| MED             | WNA             | regional_doy_climatology |          975 |        17 |    2.91549 |     0.582854 |             -0.212434   |               -0.0289088  |
| NCA             | CNA             | regional_doy_climatology |          438 |        14 |    2.81791 |     0.495244 |             -0.677282   |               -0.224299   |
| NCA             | EAS             | regional_doy_climatology |          110 |        16 |    6.65054 |     0.462896 |             -2.21432    |               -0.128023   |
| NCA             | EAU             | regional_doy_climatology |          241 |         6 |    3.41825 |     0.506921 |             -0.780145   |               -0.157986   |
| NCA             | ENA             | regional_doy_climatology |          522 |        21 |    3.62374 |     0.494718 |             -1.08305    |               -0.22949    |
| NCA             | MED             | regional_doy_climatology |          328 |        19 |    2.43119 |     0.523838 |             -0.374613   |               -0.107749   |
| NCA             | NCA             | regional_doy_climatology |          144 |         7 |    1.85692 |     0.478674 |              0          |                0          |
| NCA             | NEU             | regional_doy_climatology |         1000 |        29 |    2.55936 |     0.4818   |             -0.487923   |               -0.167562   |
| NCA             | NWN             | regional_doy_climatology |          183 |        36 |    2.98938 |     0.483935 |             -0.750943   |               -0.241295   |
| NCA             | SAU             | regional_doy_climatology |          351 |        13 |    2.41443 |     0.486517 |             -0.362901   |               -0.162686   |
| NCA             | WCE             | regional_doy_climatology |         1000 |        15 |    2.4773  |     0.487616 |             -0.557299   |               -0.168136   |
| NCA             | WNA             | regional_doy_climatology |          975 |        17 |    2.6607  |     0.527086 |             -0.467222   |               -0.0846774  |
| NEU             | CNA             | regional_doy_climatology |          438 |        14 |    3.64741 |     0.807581 |              0.152222   |                0.0880374  |
| NEU             | EAS             | regional_doy_climatology |          110 |        16 |    7.23914 |     0.714544 |             -1.62572    |                0.123625   |
| NEU             | EAU             | regional_doy_climatology |          241 |         6 |    4.14328 |     0.75979  |             -0.0551189  |                0.0948839  |
| NEU             | ENA             | regional_doy_climatology |          522 |        21 |    4.23621 |     0.718668 |             -0.470576   |               -0.00554006 |
| NEU             | MED             | regional_doy_climatology |          328 |        19 |    3.23227 |     0.808851 |              0.426468   |                0.177265   |
| NEU             | NCA             | regional_doy_climatology |          144 |         7 |    2.85314 |     0.877779 |              0.996224   |                0.399106   |
| NEU             | NEU             | regional_doy_climatology |         1000 |        29 |    3.04728 |     0.649362 |              0          |                0          |
| NEU             | NWN             | regional_doy_climatology |          183 |        36 |    3.57211 |     0.70934  |             -0.168215   |               -0.0158893  |
| NEU             | SAU             | regional_doy_climatology |          351 |        13 |    3.09121 |     0.75099  |              0.313877   |                0.101787   |
| NEU             | WCE             | regional_doy_climatology |         1000 |        15 |    3.03804 |     0.678378 |              0.00343982 |                0.0226262  |
| NEU             | WNA             | regional_doy_climatology |          975 |        17 |    3.31129 |     0.734978 |              0.183366   |                0.123215   |
| NWN             | CNA             | regional_doy_climatology |          438 |        14 |    3.86986 |     0.823085 |              0.374672   |                0.103541   |
| NWN             | EAS             | regional_doy_climatology |          110 |        16 |    7.41907 |     0.728712 |             -1.44579    |                0.137793   |
| NWN             | EAU             | regional_doy_climatology |          241 |         6 |    4.30863 |     0.776445 |              0.11023    |                0.111539   |
| NWN             | ENA             | regional_doy_climatology |          522 |        21 |    4.41392 |     0.730457 |             -0.292863   |                0.00624852 |
| NWN             | MED             | regional_doy_climatology |          328 |        19 |    3.41038 |     0.821682 |              0.604575   |                0.190096   |
| NWN             | NCA             | regional_doy_climatology |          144 |         7 |    3.09972 |     0.899926 |              1.2428     |                0.421253   |
| NWN             | NEU             | regional_doy_climatology |         1000 |        29 |    3.19046 |     0.664237 |              0.143177   |                0.0148752  |
| NWN             | NWN             | regional_doy_climatology |          183 |        36 |    3.74033 |     0.72523  |              0          |                0          |
| NWN             | SAU             | regional_doy_climatology |          351 |        13 |    3.29013 |     0.767077 |              0.512798   |                0.117874   |
| NWN             | WCE             | regional_doy_climatology |         1000 |        15 |    3.18973 |     0.688427 |              0.155125   |                0.0326746  |
| NWN             | WNA             | regional_doy_climatology |          975 |        17 |    3.44803 |     0.745215 |              0.320105   |                0.133451   |
| SAU             | CNA             | regional_doy_climatology |          438 |        14 |    3.26783 |     0.700613 |             -0.227357   |               -0.0189303  |
| SAU             | EAS             | regional_doy_climatology |          110 |        16 |    6.93752 |     0.612551 |             -1.92734    |                0.0216321  |
| SAU             | EAU             | regional_doy_climatology |          241 |         6 |    3.8371  |     0.691127 |             -0.3613     |                0.0262202  |
| SAU             | ENA             | regional_doy_climatology |          522 |        21 |    3.95573 |     0.647875 |             -0.75106    |               -0.0763338  |
| SAU             | MED             | regional_doy_climatology |          328 |        19 |    2.8843  |     0.716628 |              0.0784903  |                0.0850408  |
| SAU             | NCA             | regional_doy_climatology |          144 |         7 |    2.43959 |     0.757645 |              0.582668   |                0.278972   |
| SAU             | NEU             | regional_doy_climatology |         1000 |        29 |    2.85953 |     0.611352 |             -0.187757   |               -0.0380095  |
| SAU             | NWN             | regional_doy_climatology |          183 |        36 |    3.32206 |     0.638284 |             -0.418267   |               -0.0869455  |
| SAU             | SAU             | regional_doy_climatology |          351 |        13 |    2.77733 |     0.649203 |              0          |                0          |
| SAU             | WCE             | regional_doy_climatology |         1000 |        15 |    2.80228 |     0.623499 |             -0.232321   |               -0.0322534  |
| SAU             | WNA             | regional_doy_climatology |          975 |        17 |    3.03619 |     0.678235 |             -0.091733   |                0.0664721  |
| WCE             | CNA             | regional_doy_climatology |          438 |        14 |    3.59079 |     0.7632   |              0.0955983  |                0.0436563  |
| WCE             | EAS             | regional_doy_climatology |          110 |        16 |    7.18244 |     0.680412 |             -1.68242    |                0.0894925  |
| WCE             | EAU             | regional_doy_climatology |          241 |         6 |    4.11107 |     0.728381 |             -0.0873269  |                0.0634751  |
| WCE             | ENA             | regional_doy_climatology |          522 |        21 |    4.20052 |     0.683952 |             -0.50627    |               -0.0402565  |
| WCE             | MED             | regional_doy_climatology |          328 |        19 |    3.21336 |     0.767688 |              0.407556   |                0.136101   |
| WCE             | NCA             | regional_doy_climatology |          144 |         7 |    2.81177 |     0.826235 |              0.954854   |                0.347562   |
| WCE             | NEU             | regional_doy_climatology |         1000 |        29 |    3.07476 |     0.637004 |              0.0274755  |               -0.0123574  |
| WCE             | NWN             | regional_doy_climatology |          183 |        36 |    3.58302 |     0.685129 |             -0.157306   |               -0.0401011  |
| WCE             | SAU             | regional_doy_climatology |          351 |        13 |    3.06984 |     0.714049 |              0.292509   |                0.064846   |
| WCE             | WCE             | regional_doy_climatology |         1000 |        15 |    3.0346  |     0.655752 |              0          |                0          |
| WCE             | WNA             | regional_doy_climatology |          975 |        17 |    3.31202 |     0.705335 |              0.184091   |                0.0935721  |
| WNA             | CNA             | regional_doy_climatology |          438 |        14 |    3.65173 |     0.708279 |              0.156543   |               -0.0112645  |
| WNA             | EAS             | regional_doy_climatology |          110 |        16 |    7.48927 |     0.699627 |             -1.37559    |                0.108708   |
| WNA             | EAU             | regional_doy_climatology |          241 |         6 |    4.02786 |     0.655937 |             -0.170542   |               -0.00896949 |
| WNA             | ENA             | regional_doy_climatology |          522 |        21 |    4.2445  |     0.653222 |             -0.462289   |               -0.0709866  |
| WNA             | MED             | regional_doy_climatology |          328 |        19 |    3.12306 |     0.671619 |              0.31725    |                0.040032   |
| WNA             | NCA             | regional_doy_climatology |          144 |         7 |    2.86538 |     0.764725 |              1.00846    |                0.286051   |
| WNA             | NEU             | regional_doy_climatology |         1000 |        29 |    3.08048 |     0.597913 |              0.033198   |               -0.0514492  |
| WNA             | NWN             | regional_doy_climatology |          183 |        36 |    3.64202 |     0.652177 |             -0.0983048  |               -0.073053   |
| WNA             | SAU             | regional_doy_climatology |          351 |        13 |    3.20977 |     0.698999 |              0.432435   |                0.049796   |
| WNA             | WCE             | regional_doy_climatology |         1000 |        15 |    3.06825 |     0.6158   |              0.0336438  |               -0.0399519  |
| WNA             | WNA             | regional_doy_climatology |          975 |        17 |    3.12792 |     0.611763 |              0          |                0          |

## Station persistence summary

| target_region   | model               |   n_stations |   n_cells |   mae_mean |   brier_mean |
|:----------------|:--------------------|-------------:|----------:|-----------:|-------------:|
| CNA             | station_persistence |          438 |        14 |    3.4813  |     0.231502 |
| EAS             | station_persistence |          110 |        16 |    8.38245 |     0.239891 |
| EAU             | station_persistence |          241 |         6 |    4.0092  |     0.241208 |
| ENA             | station_persistence |          522 |        21 |    4.99402 |     0.326025 |
| MED             | station_persistence |          328 |        19 |    2.46845 |     0.194539 |
| NCA             | station_persistence |          144 |         7 |    1.6008  |     0.127613 |
| NEU             | station_persistence |         1000 |        29 |    2.94369 |     0.306355 |
| NWN             | station_persistence |          183 |        36 |    3.11986 |     0.254985 |
| SAU             | station_persistence |          351 |        13 |    2.72817 |     0.255502 |
| WCE             | station_persistence |         1000 |        15 |    2.89794 |     0.305967 |
| WNA             | station_persistence |          975 |        17 |    2.64721 |     0.246933 |
