# Spatial baseline forecasting experiment

Dataset: `forecast_dataset_large_all_viable_min100_full_s1.npz`.

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
| CNA             | CNA             | spatial_knn_ridge |          438 |        14 |    2.35517 |     0.202462 |             0           |               0           |
| CNA             | EAS             | spatial_knn_ridge |          110 |        16 |    6.23092 |     0.237736 |            -0.0230846   |              -0.00808933  |
| CNA             | EAU             | spatial_knn_ridge |          241 |         6 |    2.97739 |     0.229663 |            -0.0129018   |              -0.00169274  |
| CNA             | ENA             | spatial_knn_ridge |          522 |        21 |    3.31536 |     0.295743 |            -0.0858925   |              -0.0147558   |
| CNA             | MED             | spatial_knn_ridge |          328 |        19 |    1.89166 |     0.186859 |             0.0194666   |               4.08838e-06 |
| CNA             | NCA             | spatial_knn_ridge |          144 |         7 |    1.25647 |     0.110905 |             0.114013    |               0.00105571  |
| CNA             | NEU             | spatial_knn_ridge |         1000 |        28 |    2.327   |     0.298462 |            -0.0585105   |              -0.00553634  |
| CNA             | NWN             | spatial_knn_ridge |          183 |        36 |    2.58982 |     0.241864 |             0.0731321   |              -0.0037554   |
| CNA             | SAU             | spatial_knn_ridge |          351 |        13 |    2.01224 |     0.238562 |            -0.0169311   |               0.00102617  |
| CNA             | WCE             | spatial_knn_ridge |         1000 |        14 |    2.19414 |     0.296328 |            -0.0742674   |              -0.0066443   |
| CNA             | WNA             | spatial_knn_ridge |          975 |        17 |    2.17786 |     0.226837 |             0.0265251   |              -0.00444179  |
| EAS             | CNA             | spatial_knn_ridge |          438 |        14 |    2.50863 |     0.229262 |             0.153456    |               0.0268009   |
| EAS             | EAS             | spatial_knn_ridge |          110 |        16 |    6.25401 |     0.245825 |             0           |               0           |
| EAS             | EAU             | spatial_knn_ridge |          241 |         6 |    3.07926 |     0.244696 |             0.0889704   |               0.0133403   |
| EAS             | ENA             | spatial_knn_ridge |          522 |        21 |    3.46815 |     0.322994 |             0.0668968   |               0.0124948   |
| EAS             | MED             | spatial_knn_ridge |          328 |        19 |    1.99959 |     0.19929  |             0.127402    |               0.0124349   |
| EAS             | NCA             | spatial_knn_ridge |          144 |         7 |    1.38401 |     0.126923 |             0.241549    |               0.0170739   |
| EAS             | NEU             | spatial_knn_ridge |         1000 |        28 |    2.38097 |     0.305602 |            -0.00453622  |               0.0016036   |
| EAS             | NWN             | spatial_knn_ridge |          183 |        36 |    2.60212 |     0.253798 |             0.0854261   |               0.00817835  |
| EAS             | SAU             | spatial_knn_ridge |          351 |        13 |    2.12415 |     0.256088 |             0.0949758   |               0.0185516   |
| EAS             | WCE             | spatial_knn_ridge |         1000 |        14 |    2.28113 |     0.307415 |             0.0127199   |               0.00444233  |
| EAS             | WNA             | spatial_knn_ridge |          975 |        17 |    2.22897 |     0.236693 |             0.0776326   |               0.00541442  |
| EAU             | CNA             | spatial_knn_ridge |          438 |        14 |    2.38911 |     0.210127 |             0.0339345   |               0.00766591  |
| EAU             | EAS             | spatial_knn_ridge |          110 |        16 |    6.2123  |     0.234873 |            -0.0417018   |              -0.0109519   |
| EAU             | EAU             | spatial_knn_ridge |          241 |         6 |    2.99029 |     0.231356 |             0           |               0           |
| EAU             | ENA             | spatial_knn_ridge |          522 |        21 |    3.35111 |     0.303556 |            -0.0501413   |              -0.00694307  |
| EAU             | MED             | spatial_knn_ridge |          328 |        19 |    1.90555 |     0.186112 |             0.0333557   |              -0.000743349 |
| EAU             | NCA             | spatial_knn_ridge |          144 |         7 |    1.27808 |     0.113485 |             0.135618    |               0.00363661  |
| EAU             | NEU             | spatial_knn_ridge |         1000 |        28 |    2.32808 |     0.297384 |            -0.0574279   |              -0.00661463  |
| EAU             | NWN             | spatial_knn_ridge |          183 |        36 |    2.56937 |     0.235131 |             0.052676    |              -0.0104883   |
| EAU             | SAU             | spatial_knn_ridge |          351 |        13 |    2.02806 |     0.239076 |            -0.00111817  |               0.00153958  |
| EAU             | WCE             | spatial_knn_ridge |         1000 |        14 |    2.20489 |     0.296464 |            -0.0635234   |              -0.0065083   |
| EAU             | WNA             | spatial_knn_ridge |          975 |        17 |    2.17454 |     0.224539 |             0.0232115   |              -0.00673922  |
| ENA             | CNA             | spatial_knn_ridge |          438 |        14 |    2.48403 |     0.216968 |             0.128853    |               0.0145065   |
| ENA             | EAS             | spatial_knn_ridge |          110 |        16 |    6.33607 |     0.246607 |             0.0820629   |               0.000781873 |
| ENA             | EAU             | spatial_knn_ridge |          241 |         6 |    3.09259 |     0.240653 |             0.102302    |               0.00929656  |
| ENA             | ENA             | spatial_knn_ridge |          522 |        21 |    3.40125 |     0.310499 |             0           |               0           |
| ENA             | MED             | spatial_knn_ridge |          328 |        19 |    2.02438 |     0.198891 |             0.152189    |               0.012036    |
| ENA             | NCA             | spatial_knn_ridge |          144 |         7 |    1.42542 |     0.12194  |             0.282963    |               0.0120913   |
| ENA             | NEU             | spatial_knn_ridge |         1000 |        28 |    2.39187 |     0.305521 |             0.00635707  |               0.00152263  |
| ENA             | NWN             | spatial_knn_ridge |          183 |        36 |    2.68531 |     0.258799 |             0.168616    |               0.0131796   |
| ENA             | SAU             | spatial_knn_ridge |          351 |        13 |    2.12033 |     0.25297  |             0.091151    |               0.0154335   |
| ENA             | WCE             | spatial_knn_ridge |         1000 |        14 |    2.26901 |     0.30592  |             0.000601824 |               0.00294714  |
| ENA             | WNA             | spatial_knn_ridge |          975 |        17 |    2.29074 |     0.236566 |             0.139409    |               0.0052875   |
| MED             | CNA             | spatial_knn_ridge |          438 |        14 |    2.36407 |     0.21426  |             0.00889744  |               0.0117989   |
| MED             | EAS             | spatial_knn_ridge |          110 |        16 |    6.1929  |     0.233763 |            -0.0611087   |              -0.0120623   |
| MED             | EAU             | spatial_knn_ridge |          241 |         6 |    2.96467 |     0.232248 |            -0.0256161   |               0.000892385 |
| MED             | ENA             | spatial_knn_ridge |          522 |        21 |    3.33913 |     0.307376 |            -0.0621207   |              -0.00312297  |
| MED             | MED             | spatial_knn_ridge |          328 |        19 |    1.87219 |     0.186855 |             0           |               0           |
| MED             | NCA             | spatial_knn_ridge |          144 |         7 |    1.23618 |     0.114556 |             0.0937247   |               0.00470673  |
| MED             | NEU             | spatial_knn_ridge |         1000 |        28 |    2.31499 |     0.298909 |            -0.0705233   |              -0.00508931  |
| MED             | NWN             | spatial_knn_ridge |          183 |        36 |    2.54319 |     0.234645 |             0.0264992   |              -0.0109751   |
| MED             | SAU             | spatial_knn_ridge |          351 |        13 |    2.00618 |     0.242274 |            -0.0229971   |               0.00473819  |
| MED             | WCE             | spatial_knn_ridge |         1000 |        14 |    2.19189 |     0.298572 |            -0.0765248   |              -0.0044005   |
| MED             | WNA             | spatial_knn_ridge |          975 |        17 |    2.14779 |     0.225619 |            -0.00354329  |              -0.00565923  |
| NCA             | CNA             | spatial_knn_ridge |          438 |        14 |    2.29041 |     0.204862 |            -0.0647687   |               0.00240018  |
| NCA             | EAS             | spatial_knn_ridge |          110 |        16 |    6.13562 |     0.233611 |            -0.11839     |              -0.0122147   |
| NCA             | EAU             | spatial_knn_ridge |          241 |         6 |    2.90491 |     0.228537 |            -0.0853752   |              -0.00281884  |
| NCA             | ENA             | spatial_knn_ridge |          522 |        21 |    3.29086 |     0.297421 |            -0.110387    |              -0.0130779   |
| NCA             | MED             | spatial_knn_ridge |          328 |        19 |    1.80749 |     0.183986 |            -0.0647036   |              -0.0028695   |
| NCA             | NCA             | spatial_knn_ridge |          144 |         7 |    1.14246 |     0.109849 |             0           |               0           |
| NCA             | NEU             | spatial_knn_ridge |         1000 |        28 |    2.28582 |     0.297076 |            -0.0996923   |              -0.00692304  |
| NCA             | NWN             | spatial_knn_ridge |          183 |        36 |    2.50206 |     0.234611 |            -0.0146303   |              -0.0110086   |
| NCA             | SAU             | spatial_knn_ridge |          351 |        13 |    1.95431 |     0.236609 |            -0.0748668   |              -0.000927547 |
| NCA             | WCE             | spatial_knn_ridge |         1000 |        14 |    2.15765 |     0.295281 |            -0.110766    |              -0.00769207  |
| NCA             | WNA             | spatial_knn_ridge |          975 |        17 |    2.08569 |     0.223673 |            -0.0656461   |              -0.0076054   |
| NEU             | CNA             | spatial_knn_ridge |          438 |        14 |    2.5125  |     0.226195 |             0.15733     |               0.0237338   |
| NEU             | EAS             | spatial_knn_ridge |          110 |        16 |    6.29142 |     0.243484 |             0.0374135   |              -0.00234149  |
| NEU             | EAU             | spatial_knn_ridge |          241 |         6 |    3.09293 |     0.242303 |             0.102643    |               0.0109472   |
| NEU             | ENA             | spatial_knn_ridge |          522 |        21 |    3.44166 |     0.320009 |             0.0404054   |               0.00950983  |
| NEU             | MED             | spatial_knn_ridge |          328 |        19 |    2.02254 |     0.196794 |             0.150348    |               0.00993827  |
| NEU             | NCA             | spatial_knn_ridge |          144 |         7 |    1.4271  |     0.124535 |             0.284644    |               0.0146864   |
| NEU             | NEU             | spatial_knn_ridge |         1000 |        28 |    2.38551 |     0.303999 |             0           |               0           |
| NEU             | NWN             | spatial_knn_ridge |          183 |        36 |    2.64363 |     0.249739 |             0.126943    |               0.00411928  |
| NEU             | SAU             | spatial_knn_ridge |          351 |        13 |    2.12655 |     0.253144 |             0.0973727   |               0.0156074   |
| NEU             | WCE             | spatial_knn_ridge |         1000 |        14 |    2.27439 |     0.305367 |             0.00597945  |               0.00239384  |
| NEU             | WNA             | spatial_knn_ridge |          975 |        17 |    2.2673  |     0.234404 |             0.115966    |               0.00312576  |
| NWN             | CNA             | spatial_knn_ridge |          438 |        14 |    2.48513 |     0.224844 |             0.129955    |               0.0223828   |
| NWN             | EAS             | spatial_knn_ridge |          110 |        16 |    6.24775 |     0.240771 |            -0.00625909  |              -0.00505414  |
| NWN             | EAU             | spatial_knn_ridge |          241 |         6 |    3.04948 |     0.240056 |             0.0591864   |               0.0087004   |
| NWN             | ENA             | spatial_knn_ridge |          522 |        21 |    3.50763 |     0.318561 |             0.10638     |               0.00806225  |
| NWN             | MED             | spatial_knn_ridge |          328 |        19 |    1.94002 |     0.193718 |             0.067828    |               0.00686297  |
| NWN             | NCA             | spatial_knn_ridge |          144 |         7 |    1.28435 |     0.123402 |             0.141888    |               0.0135528   |
| NWN             | NEU             | spatial_knn_ridge |         1000 |        28 |    2.37234 |     0.301406 |            -0.0131737   |              -0.0025927   |
| NWN             | NWN             | spatial_knn_ridge |          183 |        36 |    2.51669 |     0.24562  |             0           |               0           |
| NWN             | SAU             | spatial_knn_ridge |          351 |        13 |    2.10183 |     0.249303 |             0.072654    |               0.0117664   |
| NWN             | WCE             | spatial_knn_ridge |         1000 |        14 |    2.27843 |     0.302152 |             0.0100192   |              -0.000820797 |
| NWN             | WNA             | spatial_knn_ridge |          975 |        17 |    2.15285 |     0.233105 |             0.00151608  |               0.001827    |
| SAU             | CNA             | spatial_knn_ridge |          438 |        14 |    2.39014 |     0.209626 |             0.0349628   |               0.00716425  |
| SAU             | EAS             | spatial_knn_ridge |          110 |        16 |    6.23301 |     0.232346 |            -0.020991    |              -0.0134795   |
| SAU             | EAU             | spatial_knn_ridge |          241 |         6 |    2.99514 |     0.229272 |             0.00484886  |              -0.00208387  |
| SAU             | ENA             | spatial_knn_ridge |          522 |        21 |    3.34436 |     0.302996 |            -0.056889    |              -0.00750275  |
| SAU             | MED             | spatial_knn_ridge |          328 |        19 |    1.90996 |     0.18399  |             0.0377736   |              -0.00286519  |
| SAU             | NCA             | spatial_knn_ridge |          144 |         7 |    1.28884 |     0.112378 |             0.146386    |               0.00252932  |
| SAU             | NEU             | spatial_knn_ridge |         1000 |        28 |    2.33352 |     0.296892 |            -0.0519868   |              -0.00710629  |
| SAU             | NWN             | spatial_knn_ridge |          183 |        36 |    2.58217 |     0.231861 |             0.0654791   |              -0.0137591   |
| SAU             | SAU             | spatial_knn_ridge |          351 |        13 |    2.02918 |     0.237536 |             0           |               0           |
| SAU             | WCE             | spatial_knn_ridge |         1000 |        14 |    2.20528 |     0.295606 |            -0.063131    |              -0.0073672   |
| SAU             | WNA             | spatial_knn_ridge |          975 |        17 |    2.18919 |     0.223501 |             0.0378609   |              -0.00777742  |
| WCE             | CNA             | spatial_knn_ridge |          438 |        14 |    2.49988 |     0.221405 |             0.144707    |               0.0189433   |
| WCE             | EAS             | spatial_knn_ridge |          110 |        16 |    6.31349 |     0.240035 |             0.0594805   |              -0.00579058  |
| WCE             | EAU             | spatial_knn_ridge |          241 |         6 |    3.09153 |     0.238993 |             0.101245    |               0.00763678  |
| WCE             | ENA             | spatial_knn_ridge |          522 |        21 |    3.4194  |     0.314786 |             0.0181536   |               0.00428686  |
| WCE             | MED             | spatial_knn_ridge |          328 |        19 |    2.02221 |     0.193522 |             0.150022    |               0.00666627  |
| WCE             | NCA             | spatial_knn_ridge |          144 |         7 |    1.43058 |     0.120647 |             0.288121    |               0.0107985   |
| WCE             | NEU             | spatial_knn_ridge |         1000 |        28 |    2.38739 |     0.302133 |             0.00187613  |              -0.00186563  |
| WCE             | NWN             | spatial_knn_ridge |          183 |        36 |    2.66061 |     0.245118 |             0.143919    |              -0.000501457 |
| WCE             | SAU             | spatial_knn_ridge |          351 |        13 |    2.1204  |     0.249424 |             0.0912289   |               0.0118876   |
| WCE             | WCE             | spatial_knn_ridge |         1000 |        14 |    2.26841 |     0.302973 |             0           |               0           |
| WCE             | WNA             | spatial_knn_ridge |          975 |        17 |    2.28042 |     0.230696 |             0.129082    |              -0.000582417 |
| WNA             | CNA             | spatial_knn_ridge |          438 |        14 |    2.40705 |     0.22141  |             0.0518766   |               0.0189484   |
| WNA             | EAS             | spatial_knn_ridge |          110 |        16 |    6.18737 |     0.240095 |            -0.0666356   |              -0.00573039  |
| WNA             | EAU             | spatial_knn_ridge |          241 |         6 |    2.9954  |     0.239381 |             0.00511311  |               0.00802466  |
| WNA             | ENA             | spatial_knn_ridge |          522 |        21 |    3.39604 |     0.314497 |            -0.00521323  |               0.00399813  |
| WNA             | MED             | spatial_knn_ridge |          328 |        19 |    1.90285 |     0.19385  |             0.0306563   |               0.00699418  |
| WNA             | NCA             | spatial_knn_ridge |          144 |         7 |    1.2572  |     0.120332 |             0.114741    |               0.0104827   |
| WNA             | NEU             | spatial_knn_ridge |         1000 |        28 |    2.33668 |     0.302887 |            -0.0488243   |              -0.00111132  |
| WNA             | NWN             | spatial_knn_ridge |          183 |        36 |    2.54035 |     0.246184 |             0.0236599   |               0.000564148 |
| WNA             | SAU             | spatial_knn_ridge |          351 |        13 |    2.04787 |     0.250496 |             0.0186988   |               0.0129598   |
| WNA             | WCE             | spatial_knn_ridge |         1000 |        14 |    2.23066 |     0.303941 |            -0.0377551   |               0.000967741 |
| WNA             | WNA             | spatial_knn_ridge |          975 |        17 |    2.15133 |     0.231278 |             0           |               0           |
