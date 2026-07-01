# Baseline forecasting experiment

Dataset:

- `forecast_dataset_large_all_viable_min100_full_s1.npz`;
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
| CNA             | NEU             | regional_doy_climatology |         1000 |        28 |    3.13375 |     0.627491 |             -0.0148559  |               -0.0189368  |
| CNA             | NWN             | regional_doy_climatology |          183 |        36 |    3.54392 |     0.659596 |             -0.19641    |               -0.0656336  |
| CNA             | SAU             | regional_doy_climatology |          351 |        13 |    3.00673 |     0.678999 |              0.2294     |                0.0297962  |
| CNA             | WCE             | regional_doy_climatology |         1000 |        14 |    3.02442 |     0.634846 |             -0.0424347  |               -0.0217253  |
| CNA             | WNA             | regional_doy_climatology |          975 |        17 |    3.26712 |     0.69128  |              0.1392     |                0.0795171  |
| EAS             | CNA             | regional_doy_climatology |          438 |        14 |    6.50642 |     0.695442 |              3.01123    |               -0.0241016  |
| EAS             | EAS             | regional_doy_climatology |          110 |        16 |    8.86486 |     0.590919 |              0          |                0          |
| EAS             | EAU             | regional_doy_climatology |          241 |         6 |    7.32019 |     0.692859 |              3.12179    |                0.0279525  |
| EAS             | ENA             | regional_doy_climatology |          522 |        21 |    6.89441 |     0.642956 |              2.18762    |               -0.0812528  |
| EAS             | MED             | regional_doy_climatology |          328 |        19 |    6.58247 |     0.722718 |              3.77667    |                0.0911308  |
| EAS             | NCA             | regional_doy_climatology |          144 |         7 |    6.15121 |     0.752277 |              4.29429    |                0.273603   |
| EAS             | NEU             | regional_doy_climatology |         1000 |        28 |    6.12304 |     0.615112 |              2.97444    |               -0.0313154  |
| EAS             | NWN             | regional_doy_climatology |          183 |        36 |    6.55582 |     0.640414 |              2.81549    |               -0.0848161  |
| EAS             | SAU             | regional_doy_climatology |          351 |        13 |    6.05651 |     0.646349 |              3.27918    |               -0.00285443 |
| EAS             | WCE             | regional_doy_climatology |         1000 |        14 |    5.97821 |     0.622579 |              2.91135    |               -0.0339919  |
| EAS             | WNA             | regional_doy_climatology |          975 |        17 |    6.61807 |     0.683491 |              3.49015    |                0.0717281  |
| EAU             | CNA             | regional_doy_climatology |          438 |        14 |    3.77801 |     0.703005 |              0.282819   |               -0.0165387  |
| EAU             | EAS             | regional_doy_climatology |          110 |        16 |    7.53113 |     0.67661  |             -1.33372    |                0.0856906  |
| EAU             | EAU             | regional_doy_climatology |          241 |         6 |    4.1984  |     0.664906 |              0          |                0          |
| EAU             | ENA             | regional_doy_climatology |          522 |        21 |    4.35502 |     0.638499 |             -0.351761   |               -0.0857097  |
| EAU             | MED             | regional_doy_climatology |          328 |        19 |    3.27382 |     0.678137 |              0.468011   |                0.0465503  |
| EAU             | NCA             | regional_doy_climatology |          144 |         7 |    2.98502 |     0.744061 |              1.1281     |                0.265388   |
| EAU             | NEU             | regional_doy_climatology |         1000 |        28 |    3.28093 |     0.594553 |              0.13233    |               -0.0518745  |
| EAU             | NWN             | regional_doy_climatology |          183 |        36 |    3.75465 |     0.641234 |              0.01432    |               -0.0839953  |
| EAU             | SAU             | regional_doy_climatology |          351 |        13 |    3.30943 |     0.674493 |              0.532103   |                0.0252904  |
| EAU             | WCE             | regional_doy_climatology |         1000 |        14 |    3.21142 |     0.612324 |              0.144564   |               -0.044247   |
| EAU             | WNA             | regional_doy_climatology |          975 |        17 |    3.28806 |     0.628201 |              0.160134   |                0.0164374  |
| ENA             | CNA             | regional_doy_climatology |          438 |        14 |    4.22986 |     0.816781 |              0.734675   |                0.0972376  |
| ENA             | EAS             | regional_doy_climatology |          110 |        16 |    7.69208 |     0.722788 |             -1.17278    |                0.131869   |
| ENA             | EAU             | regional_doy_climatology |          241 |         6 |    4.68285 |     0.770662 |              0.48445    |                0.105755   |
| ENA             | ENA             | regional_doy_climatology |          522 |        21 |    4.70679 |     0.724208 |              0          |                0          |
| ENA             | MED             | regional_doy_climatology |          328 |        19 |    3.84056 |     0.817314 |              1.03475    |                0.185728   |
| ENA             | NCA             | regional_doy_climatology |          144 |         7 |    3.56958 |     0.893239 |              1.71267    |                0.414565   |
| ENA             | NEU             | regional_doy_climatology |         1000 |        28 |    3.62333 |     0.661291 |              0.474722   |                0.0148634  |
| ENA             | NWN             | regional_doy_climatology |          183 |        36 |    4.11817 |     0.72092  |              0.377848   |               -0.00431002 |
| ENA             | SAU             | regional_doy_climatology |          351 |        13 |    3.66583 |     0.761603 |              0.888504   |                0.1124     |
| ENA             | WCE             | regional_doy_climatology |         1000 |        14 |    3.5559  |     0.688333 |              0.489044   |                0.0317615  |
| ENA             | WNA             | regional_doy_climatology |          975 |        17 |    3.82408 |     0.742494 |              0.696154   |                0.130731   |
| MED             | CNA             | regional_doy_climatology |          438 |        14 |    3.35909 |     0.68787  |             -0.136096   |               -0.0316731  |
| MED             | EAS             | regional_doy_climatology |          110 |        16 |    7.20818 |     0.6902   |             -1.65667    |                0.0992807  |
| MED             | EAU             | regional_doy_climatology |          241 |         6 |    3.80353 |     0.629389 |             -0.394873   |               -0.0355172  |
| MED             | ENA             | regional_doy_climatology |          522 |        21 |    4.02263 |     0.63437  |             -0.684155   |               -0.0898385  |
| MED             | MED             | regional_doy_climatology |          328 |        19 |    2.80581 |     0.631587 |              0          |                0          |
| MED             | NCA             | regional_doy_climatology |          144 |         7 |    2.50117 |     0.730183 |              0.644253   |                0.251509   |
| MED             | NEU             | regional_doy_climatology |         1000 |        28 |    2.91637 |     0.585764 |             -0.232233   |               -0.0606639  |
| MED             | NWN             | regional_doy_climatology |          183 |        36 |    3.36387 |     0.627526 |             -0.376459   |               -0.0977032  |
| MED             | SAU             | regional_doy_climatology |          351 |        13 |    2.91974 |     0.683377 |              0.142412   |                0.0341744  |
| MED             | WCE             | regional_doy_climatology |         1000 |        14 |    2.84643 |     0.603133 |             -0.220427   |               -0.0534387  |
| MED             | WNA             | regional_doy_climatology |          975 |        17 |    2.91549 |     0.582854 |             -0.212434   |               -0.0289088  |
| NCA             | CNA             | regional_doy_climatology |          438 |        14 |    2.81791 |     0.495244 |             -0.677282   |               -0.224299   |
| NCA             | EAS             | regional_doy_climatology |          110 |        16 |    6.65054 |     0.462896 |             -2.21432    |               -0.128023   |
| NCA             | EAU             | regional_doy_climatology |          241 |         6 |    3.41825 |     0.506921 |             -0.780145   |               -0.157986   |
| NCA             | ENA             | regional_doy_climatology |          522 |        21 |    3.62374 |     0.494718 |             -1.08305    |               -0.22949    |
| NCA             | MED             | regional_doy_climatology |          328 |        19 |    2.43119 |     0.523838 |             -0.374613   |               -0.107749   |
| NCA             | NCA             | regional_doy_climatology |          144 |         7 |    1.85692 |     0.478674 |              0          |                0          |
| NCA             | NEU             | regional_doy_climatology |         1000 |        28 |    2.62936 |     0.481545 |             -0.519248   |               -0.164882   |
| NCA             | NWN             | regional_doy_climatology |          183 |        36 |    2.98938 |     0.483935 |             -0.750943   |               -0.241295   |
| NCA             | SAU             | regional_doy_climatology |          351 |        13 |    2.41443 |     0.486517 |             -0.362901   |               -0.162686   |
| NCA             | WCE             | regional_doy_climatology |         1000 |        14 |    2.50176 |     0.48775  |             -0.565099   |               -0.168821   |
| NCA             | WNA             | regional_doy_climatology |          975 |        17 |    2.6607  |     0.527086 |             -0.467222   |               -0.0846774  |
| NEU             | CNA             | regional_doy_climatology |          438 |        14 |    3.70005 |     0.807227 |              0.204856   |                0.087683   |
| NEU             | EAS             | regional_doy_climatology |          110 |        16 |    7.28498 |     0.714939 |             -1.57988    |                0.12402    |
| NEU             | EAU             | regional_doy_climatology |          241 |         6 |    4.18663 |     0.757074 |             -0.0117633  |                0.092168   |
| NEU             | ENA             | regional_doy_climatology |          522 |        21 |    4.27723 |     0.717473 |             -0.429559   |               -0.00673506 |
| NEU             | MED             | regional_doy_climatology |          328 |        19 |    3.28027 |     0.807094 |              0.474462   |                0.175508   |
| NEU             | NCA             | regional_doy_climatology |          144 |         7 |    2.91131 |     0.874496 |              1.05439    |                0.395822   |
| NEU             | NEU             | regional_doy_climatology |         1000 |        28 |    3.1486  |     0.646428 |              0          |                0          |
| NEU             | NWN             | regional_doy_climatology |          183 |        36 |    3.61249 |     0.707997 |             -0.127834   |               -0.0172329  |
| NEU             | SAU             | regional_doy_climatology |          351 |        13 |    3.13932 |     0.750286 |              0.36199    |                0.101083   |
| NEU             | WCE             | regional_doy_climatology |         1000 |        14 |    3.10215 |     0.678376 |              0.0352905  |                0.0218043  |
| NEU             | WNA             | regional_doy_climatology |          975 |        17 |    3.34979 |     0.732108 |              0.221867   |                0.120345   |
| NWN             | CNA             | regional_doy_climatology |          438 |        14 |    3.86986 |     0.823085 |              0.374672   |                0.103541   |
| NWN             | EAS             | regional_doy_climatology |          110 |        16 |    7.41907 |     0.728712 |             -1.44579    |                0.137793   |
| NWN             | EAU             | regional_doy_climatology |          241 |         6 |    4.30863 |     0.776445 |              0.11023    |                0.111539   |
| NWN             | ENA             | regional_doy_climatology |          522 |        21 |    4.41392 |     0.730457 |             -0.292863   |                0.00624852 |
| NWN             | MED             | regional_doy_climatology |          328 |        19 |    3.41038 |     0.821682 |              0.604575   |                0.190096   |
| NWN             | NCA             | regional_doy_climatology |          144 |         7 |    3.09972 |     0.899926 |              1.2428     |                0.421253   |
| NWN             | NEU             | regional_doy_climatology |         1000 |        28 |    3.25698 |     0.663431 |              0.108381   |                0.0170034  |
| NWN             | NWN             | regional_doy_climatology |          183 |        36 |    3.74033 |     0.72523  |              0          |                0          |
| NWN             | SAU             | regional_doy_climatology |          351 |        13 |    3.29013 |     0.767077 |              0.512798   |                0.117874   |
| NWN             | WCE             | regional_doy_climatology |         1000 |        14 |    3.21496 |     0.688995 |              0.148107   |                0.0324234  |
| NWN             | WNA             | regional_doy_climatology |          975 |        17 |    3.44803 |     0.745215 |              0.320105   |                0.133451   |
| SAU             | CNA             | regional_doy_climatology |          438 |        14 |    3.26783 |     0.700613 |             -0.227357   |               -0.0189303  |
| SAU             | EAS             | regional_doy_climatology |          110 |        16 |    6.93752 |     0.612551 |             -1.92734    |                0.0216321  |
| SAU             | EAU             | regional_doy_climatology |          241 |         6 |    3.8371  |     0.691127 |             -0.3613     |                0.0262202  |
| SAU             | ENA             | regional_doy_climatology |          522 |        21 |    3.95573 |     0.647875 |             -0.75106    |               -0.0763338  |
| SAU             | MED             | regional_doy_climatology |          328 |        19 |    2.8843  |     0.716628 |              0.0784903  |                0.0850408  |
| SAU             | NCA             | regional_doy_climatology |          144 |         7 |    2.43959 |     0.757645 |              0.582668   |                0.278972   |
| SAU             | NEU             | regional_doy_climatology |         1000 |        28 |    2.92896 |     0.611447 |             -0.219642   |               -0.0349809  |
| SAU             | NWN             | regional_doy_climatology |          183 |        36 |    3.32206 |     0.638284 |             -0.418267   |               -0.0869455  |
| SAU             | SAU             | regional_doy_climatology |          351 |        13 |    2.77733 |     0.649203 |              0          |                0          |
| SAU             | WCE             | regional_doy_climatology |         1000 |        14 |    2.8268  |     0.623481 |             -0.240053   |               -0.0330906  |
| SAU             | WNA             | regional_doy_climatology |          975 |        17 |    3.03619 |     0.678235 |             -0.091733   |                0.0664721  |
| WCE             | CNA             | regional_doy_climatology |          438 |        14 |    3.60011 |     0.764504 |              0.104918   |                0.0449604  |
| WCE             | EAS             | regional_doy_climatology |          110 |        16 |    7.18634 |     0.679532 |             -1.67852    |                0.0886134  |
| WCE             | EAU             | regional_doy_climatology |          241 |         6 |    4.12135 |     0.73064  |             -0.0770476  |                0.0657339  |
| WCE             | ENA             | regional_doy_climatology |          522 |        21 |    4.20765 |     0.684982 |             -0.499136   |               -0.0392265  |
| WCE             | MED             | regional_doy_climatology |          328 |        19 |    3.22509 |     0.770141 |              0.419286   |                0.138554   |
| WCE             | NCA             | regional_doy_climatology |          144 |         7 |    2.82349 |     0.828096 |              0.966576   |                0.349423   |
| WCE             | NEU             | regional_doy_climatology |         1000 |        28 |    3.15095 |     0.636584 |              0.00234779 |               -0.00984409 |
| WCE             | NWN             | regional_doy_climatology |          183 |        36 |    3.59116 |     0.686762 |             -0.149167   |               -0.0384673  |
| WCE             | SAU             | regional_doy_climatology |          351 |        13 |    3.07825 |     0.71552  |              0.30092    |                0.0663169  |
| WCE             | WCE             | regional_doy_climatology |         1000 |        14 |    3.06686 |     0.656571 |              0          |                0          |
| WCE             | WNA             | regional_doy_climatology |          975 |        17 |    3.32383 |     0.707116 |              0.195905   |                0.0953532  |
| WNA             | CNA             | regional_doy_climatology |          438 |        14 |    3.65173 |     0.708279 |              0.156543   |               -0.0112645  |
| WNA             | EAS             | regional_doy_climatology |          110 |        16 |    7.48927 |     0.699627 |             -1.37559    |                0.108708   |
| WNA             | EAU             | regional_doy_climatology |          241 |         6 |    4.02786 |     0.655937 |             -0.170542   |               -0.00896949 |
| WNA             | ENA             | regional_doy_climatology |          522 |        21 |    4.2445  |     0.653222 |             -0.462289   |               -0.0709866  |
| WNA             | MED             | regional_doy_climatology |          328 |        19 |    3.12306 |     0.671619 |              0.31725    |                0.040032   |
| WNA             | NCA             | regional_doy_climatology |          144 |         7 |    2.86538 |     0.764725 |              1.00846    |                0.286051   |
| WNA             | NEU             | regional_doy_climatology |         1000 |        28 |    3.14393 |     0.596777 |             -0.00467519 |               -0.0496503  |
| WNA             | NWN             | regional_doy_climatology |          183 |        36 |    3.64202 |     0.652177 |             -0.0983048  |               -0.073053   |
| WNA             | SAU             | regional_doy_climatology |          351 |        13 |    3.20977 |     0.698999 |              0.432435   |                0.049796   |
| WNA             | WCE             | regional_doy_climatology |         1000 |        14 |    3.09558 |     0.61678  |              0.0287172  |               -0.0397915  |
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
| NEU             | station_persistence |         1000 |        28 |    3.01822 |     0.306192 |
| NWN             | station_persistence |          183 |        36 |    3.11986 |     0.254985 |
| SAU             | station_persistence |          351 |        13 |    2.72817 |     0.255502 |
| WCE             | station_persistence |         1000 |        14 |    2.93422 |     0.305836 |
| WNA             | station_persistence |          975 |        17 |    2.64721 |     0.246933 |
