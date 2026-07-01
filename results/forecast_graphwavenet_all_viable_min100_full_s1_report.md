# Transferable Graph WaveNet experiment

Model:

- `graphwavenet_transfer`: Graph WaveNet-style dilated gated temporal convolutions plus graph diffusion;
- fixed source/target kNN supports, forward and backward random-walk matrices;
- no node-specific embeddings, so the model is transferable across station sets.

Training:

- source region only;
- train 2005-2012;
- validation 2013-2015;
- test 2020-2025 on each target-region graph.

## Pair summary

| source_region   | target_region   | model                 |   n_stations |   n_cells |   mae_mean |   brier_mean |   mae_out_minus_in_mean |   brier_out_minus_in_mean |
|:----------------|:----------------|:----------------------|-------------:|----------:|-----------:|-------------:|------------------------:|--------------------------:|
| CNA             | CNA             | graphwavenet_transfer |          438 |        14 |    1.97864 |    0.148102  |              0          |               0           |
| CNA             | EAS             | graphwavenet_transfer |          110 |        16 |    6.32651 |    0.261334  |              0.182715   |               0.0357893   |
| CNA             | EAU             | graphwavenet_transfer |          241 |         6 |    2.8244  |    0.213693  |              0.0356106  |               0.00605918  |
| CNA             | ENA             | graphwavenet_transfer |          522 |        21 |    2.96345 |    0.235708  |              0.0343848  |               0.00441682  |
| CNA             | MED             | graphwavenet_transfer |          328 |        19 |    1.75177 |    0.177797  |              0.0442502  |               0.00863019  |
| CNA             | NCA             | graphwavenet_transfer |          144 |         7 |    1.0144  |    0.0952449 |             -0.00810638 |               0.00053802  |
| CNA             | NEU             | graphwavenet_transfer |         1000 |        28 |    2.36589 |    0.325895  |              0.12823    |               0.0343939   |
| CNA             | NWN             | graphwavenet_transfer |          183 |        36 |    2.49533 |    0.248553  |              0.193982   |               0.0357134   |
| CNA             | SAU             | graphwavenet_transfer |          351 |        13 |    1.91594 |    0.227621  |              0.0419677  |               0.0117338   |
| CNA             | WCE             | graphwavenet_transfer |         1000 |        14 |    2.20324 |    0.307537  |              0.0693719  |               0.0189003   |
| CNA             | WNA             | graphwavenet_transfer |          975 |        17 |    2.03017 |    0.237662  |              0.0977959  |               0.0259156   |
| EAS             | CNA             | graphwavenet_transfer |          438 |        14 |    2.21894 |    0.191743  |              0.240295   |               0.0436402   |
| EAS             | EAS             | graphwavenet_transfer |          110 |        16 |    6.1438  |    0.225545  |              0          |               0           |
| EAS             | EAU             | graphwavenet_transfer |          241 |         6 |    2.82636 |    0.215073  |              0.0375726  |               0.00743855  |
| EAS             | ENA             | graphwavenet_transfer |          522 |        21 |    3.26164 |    0.285156  |              0.332576   |               0.0538654   |
| EAS             | MED             | graphwavenet_transfer |          328 |        19 |    1.72573 |    0.172152  |              0.0182156  |               0.0029854   |
| EAS             | NCA             | graphwavenet_transfer |          144 |         7 |    1.03827 |    0.100921  |              0.0157567  |               0.00621389  |
| EAS             | NEU             | graphwavenet_transfer |         1000 |        28 |    2.29481 |    0.293757  |              0.057158   |               0.00225571  |
| EAS             | NWN             | graphwavenet_transfer |          183 |        36 |    2.39474 |    0.222713  |              0.093396   |               0.00987318  |
| EAS             | SAU             | graphwavenet_transfer |          351 |        13 |    1.91027 |    0.222501  |              0.0362998  |               0.00661436  |
| EAS             | WCE             | graphwavenet_transfer |         1000 |        14 |    2.18303 |    0.288646  |              0.049164   |               9.23582e-06 |
| EAS             | WNA             | graphwavenet_transfer |          975 |        17 |    1.96988 |    0.218997  |              0.0375073  |               0.00725048  |
| EAU             | CNA             | graphwavenet_transfer |          438 |        14 |    2.15846 |    0.175228  |              0.179814   |               0.0271251   |
| EAU             | EAS             | graphwavenet_transfer |          110 |        16 |    6.15309 |    0.232446  |              0.00929778 |               0.00690076  |
| EAU             | EAU             | graphwavenet_transfer |          241 |         6 |    2.78879 |    0.207634  |              0          |               0           |
| EAU             | ENA             | graphwavenet_transfer |          522 |        21 |    3.18815 |    0.269432  |              0.25909    |               0.0381414   |
| EAU             | MED             | graphwavenet_transfer |          328 |        19 |    1.71299 |    0.169389  |              0.00547806 |               0.000222547 |
| EAU             | NCA             | graphwavenet_transfer |          144 |         7 |    1.02675 |    0.0964465 |              0.00424555 |               0.00173959  |
| EAU             | NEU             | graphwavenet_transfer |         1000 |        28 |    2.28484 |    0.302065  |              0.0471858  |               0.010564    |
| EAU             | NWN             | graphwavenet_transfer |          183 |        36 |    2.44593 |    0.23099   |              0.14458    |               0.0181509   |
| EAU             | SAU             | graphwavenet_transfer |          351 |        13 |    1.88601 |    0.218406  |              0.0120396  |               0.00251951  |
| EAU             | WCE             | graphwavenet_transfer |         1000 |        14 |    2.15952 |    0.294418  |              0.0256511  |               0.00578166  |
| EAU             | WNA             | graphwavenet_transfer |          975 |        17 |    1.99526 |    0.226491  |              0.0628867  |               0.0147451   |
| ENA             | CNA             | graphwavenet_transfer |          438 |        14 |    2.01013 |    0.151372  |              0.031487   |               0.00326992  |
| ENA             | EAS             | graphwavenet_transfer |          110 |        16 |    6.31456 |    0.267642  |              0.170764   |               0.0420974   |
| ENA             | EAU             | graphwavenet_transfer |          241 |         6 |    2.83947 |    0.218853  |              0.0506817  |               0.0112193   |
| ENA             | ENA             | graphwavenet_transfer |          522 |        21 |    2.92906 |    0.231291  |              0          |               0           |
| ENA             | MED             | graphwavenet_transfer |          328 |        19 |    1.73701 |    0.176442  |              0.0294941  |               0.0072753   |
| ENA             | NCA             | graphwavenet_transfer |          144 |         7 |    1.00864 |    0.0940167 |             -0.0138642  |              -0.000690244 |
| ENA             | NEU             | graphwavenet_transfer |         1000 |        28 |    2.34251 |    0.328559  |              0.104855   |               0.0370577   |
| ENA             | NWN             | graphwavenet_transfer |          183 |        36 |    2.46246 |    0.241138  |              0.161109   |               0.0282986   |
| ENA             | SAU             | graphwavenet_transfer |          351 |        13 |    1.91092 |    0.229481  |              0.0369432  |               0.0135942   |
| ENA             | WCE             | graphwavenet_transfer |         1000 |        14 |    2.18184 |    0.308512  |              0.047975   |               0.0198753   |
| ENA             | WNA             | graphwavenet_transfer |          975 |        17 |    2.01695 |    0.235157  |              0.0845786  |               0.0234104   |
| MED             | CNA             | graphwavenet_transfer |          438 |        14 |    2.17061 |    0.181114  |              0.191971   |               0.0330114   |
| MED             | EAS             | graphwavenet_transfer |          110 |        16 |    6.13209 |    0.224108  |             -0.0117052  |              -0.00143738  |
| MED             | EAU             | graphwavenet_transfer |          241 |         6 |    2.7986  |    0.209192  |              0.00981107 |               0.00155782  |
| MED             | ENA             | graphwavenet_transfer |          522 |        21 |    3.19251 |    0.2745    |              0.263446   |               0.0432088   |
| MED             | MED             | graphwavenet_transfer |          328 |        19 |    1.70752 |    0.169166  |              0          |               0           |
| MED             | NCA             | graphwavenet_transfer |          144 |         7 |    1.02542 |    0.0965206 |              0.00290734 |               0.00181374  |
| MED             | NEU             | graphwavenet_transfer |         1000 |        28 |    2.25796 |    0.293862  |              0.0203032  |               0.00236078  |
| MED             | NWN             | graphwavenet_transfer |          183 |        36 |    2.42046 |    0.221958  |              0.119107   |               0.00911819  |
| MED             | SAU             | graphwavenet_transfer |          351 |        13 |    1.87763 |    0.21829   |              0.00365345 |               0.00240317  |
| MED             | WCE             | graphwavenet_transfer |         1000 |        14 |    2.13909 |    0.288314  |              0.00522743 |              -0.00032197  |
| MED             | WNA             | graphwavenet_transfer |          975 |        17 |    1.97373 |    0.218008  |              0.0413586  |               0.0062614   |
| NCA             | CNA             | graphwavenet_transfer |          438 |        14 |    2.14586 |    0.171472  |              0.167215   |               0.0233697   |
| NCA             | EAS             | graphwavenet_transfer |          110 |        16 |    6.17046 |    0.230741  |              0.026667   |               0.00519597  |
| NCA             | EAU             | graphwavenet_transfer |          241 |         6 |    2.81161 |    0.210888  |              0.0228164  |               0.00325429  |
| NCA             | ENA             | graphwavenet_transfer |          522 |        21 |    3.15925 |    0.261341  |              0.230191   |               0.0300501   |
| NCA             | MED             | graphwavenet_transfer |          328 |        19 |    1.72843 |    0.17086   |              0.0209162  |               0.00169387  |
| NCA             | NCA             | graphwavenet_transfer |          144 |         7 |    1.02251 |    0.0947069 |              0          |               0           |
| NCA             | NEU             | graphwavenet_transfer |         1000 |        28 |    2.33323 |    0.298483  |              0.0955726  |               0.00698208  |
| NCA             | NWN             | graphwavenet_transfer |          183 |        36 |    2.43956 |    0.231222  |              0.13821    |               0.0183829   |
| NCA             | SAU             | graphwavenet_transfer |          351 |        13 |    1.9033  |    0.219285  |              0.0293224  |               0.00339781  |
| NCA             | WCE             | graphwavenet_transfer |         1000 |        14 |    2.21143 |    0.29071   |              0.0775611  |               0.00207402  |
| NCA             | WNA             | graphwavenet_transfer |          975 |        17 |    1.98511 |    0.221696  |              0.0527343  |               0.00994959  |
| NEU             | CNA             | graphwavenet_transfer |          438 |        14 |    2.20544 |    0.19497   |              0.226793   |               0.0468676   |
| NEU             | EAS             | graphwavenet_transfer |          110 |        16 |    6.16228 |    0.229188  |              0.0184829  |               0.0036434   |
| NEU             | EAU             | graphwavenet_transfer |          241 |         6 |    2.81979 |    0.219775  |              0.031006   |               0.0121408   |
| NEU             | ENA             | graphwavenet_transfer |          522 |        21 |    3.2209  |    0.290182  |              0.291839   |               0.0588906   |
| NEU             | MED             | graphwavenet_transfer |          328 |        19 |    1.72102 |    0.174668  |              0.0135084  |               0.00550196  |
| NEU             | NCA             | graphwavenet_transfer |          144 |         7 |    1.04549 |    0.102347  |              0.022976   |               0.00764009  |
| NEU             | NEU             | graphwavenet_transfer |         1000 |        28 |    2.23766 |    0.291501  |              0          |               0           |
| NEU             | NWN             | graphwavenet_transfer |          183 |        36 |    2.38781 |    0.218189  |              0.0864619  |               0.0053492   |
| NEU             | SAU             | graphwavenet_transfer |          351 |        13 |    1.89375 |    0.227136  |              0.0197794  |               0.0112494   |
| NEU             | WCE             | graphwavenet_transfer |         1000 |        14 |    2.13787 |    0.289926  |              0.00400415 |               0.00128948  |
| NEU             | WNA             | graphwavenet_transfer |          975 |        17 |    1.97301 |    0.215386  |              0.0406339  |               0.00363959  |
| NWN             | CNA             | graphwavenet_transfer |          438 |        14 |    2.20239 |    0.181774  |              0.223749   |               0.0336717   |
| NWN             | EAS             | graphwavenet_transfer |          110 |        16 |    6.24771 |    0.230008  |              0.103918   |               0.00446348  |
| NWN             | EAU             | graphwavenet_transfer |          241 |         6 |    2.88059 |    0.218719  |              0.0918019  |               0.0110847   |
| NWN             | ENA             | graphwavenet_transfer |          522 |        21 |    3.19871 |    0.268041  |              0.269653   |               0.0367504   |
| NWN             | MED             | graphwavenet_transfer |          328 |        19 |    1.75434 |    0.174391  |              0.046827   |               0.00522514  |
| NWN             | NCA             | graphwavenet_transfer |          144 |         7 |    1.0403  |    0.099319  |              0.01779    |               0.00461213  |
| NWN             | NEU             | graphwavenet_transfer |         1000 |        28 |    2.30982 |    0.295091  |              0.0721681  |               0.00359006  |
| NWN             | NWN             | graphwavenet_transfer |          183 |        36 |    2.30135 |    0.21284   |              0          |               0           |
| NWN             | SAU             | graphwavenet_transfer |          351 |        13 |    1.93291 |    0.22298   |              0.0589402  |               0.0070931   |
| NWN             | WCE             | graphwavenet_transfer |         1000 |        14 |    2.21352 |    0.293501  |              0.079655   |               0.00486433  |
| NWN             | WNA             | graphwavenet_transfer |          975 |        17 |    1.95302 |    0.214893  |              0.0206435  |               0.00314681  |
| SAU             | CNA             | graphwavenet_transfer |          438 |        14 |    2.16342 |    0.178104  |              0.184773   |               0.0300015   |
| SAU             | EAS             | graphwavenet_transfer |          110 |        16 |    6.18309 |    0.226374  |              0.039295   |               0.000829235 |
| SAU             | EAU             | graphwavenet_transfer |          241 |         6 |    2.80607 |    0.207748  |              0.0172851  |               0.000113743 |
| SAU             | ENA             | graphwavenet_transfer |          522 |        21 |    3.17804 |    0.271023  |              0.24898    |               0.0397324   |
| SAU             | MED             | graphwavenet_transfer |          328 |        19 |    1.71108 |    0.168724  |              0.00356421 |              -0.000442086 |
| SAU             | NCA             | graphwavenet_transfer |          144 |         7 |    1.02904 |    0.0968541 |              0.00653412 |               0.0021472   |
| SAU             | NEU             | graphwavenet_transfer |         1000 |        28 |    2.26359 |    0.295717  |              0.0259353  |               0.00421582  |
| SAU             | NWN             | graphwavenet_transfer |          183 |        36 |    2.44227 |    0.224133  |              0.140918   |               0.0112934   |
| SAU             | SAU             | graphwavenet_transfer |          351 |        13 |    1.87397 |    0.215887  |              0          |               0           |
| SAU             | WCE             | graphwavenet_transfer |         1000 |        14 |    2.13902 |    0.290067  |              0.00515521 |               0.00143069  |
| SAU             | WNA             | graphwavenet_transfer |          975 |        17 |    1.9988  |    0.221691  |              0.0664277  |               0.00994469  |
| WCE             | CNA             | graphwavenet_transfer |          438 |        14 |    2.17412 |    0.181157  |              0.195472   |               0.033055    |
| WCE             | EAS             | graphwavenet_transfer |          110 |        16 |    6.22185 |    0.229074  |              0.0780553  |               0.00352909  |
| WCE             | EAU             | graphwavenet_transfer |          241 |         6 |    2.82296 |    0.210868  |              0.0341714  |               0.0032334   |
| WCE             | ENA             | graphwavenet_transfer |          522 |        21 |    3.18386 |    0.275063  |              0.254799   |               0.043772    |
| WCE             | MED             | graphwavenet_transfer |          328 |        19 |    1.71639 |    0.169209  |              0.00887338 |               4.28885e-05 |
| WCE             | NCA             | graphwavenet_transfer |          144 |         7 |    1.03386 |    0.0973951 |              0.0113537  |               0.00268822  |
| WCE             | NEU             | graphwavenet_transfer |         1000 |        28 |    2.27378 |    0.297271  |              0.0361191  |               0.00576977  |
| WCE             | NWN             | graphwavenet_transfer |          183 |        36 |    2.49746 |    0.234147  |              0.196107   |               0.0213074   |
| WCE             | SAU             | graphwavenet_transfer |          351 |        13 |    1.88775 |    0.219458  |              0.0137812  |               0.00357157  |
| WCE             | WCE             | graphwavenet_transfer |         1000 |        14 |    2.13387 |    0.288636  |              0          |               0           |
| WCE             | WNA             | graphwavenet_transfer |          975 |        17 |    2.02504 |    0.223968  |              0.09266    |               0.0122216   |
| WNA             | CNA             | graphwavenet_transfer |          438 |        14 |    2.18654 |    0.182967  |              0.2079     |               0.0348645   |
| WNA             | EAS             | graphwavenet_transfer |          110 |        16 |    6.15508 |    0.231611  |              0.0112808  |               0.00606653  |
| WNA             | EAU             | graphwavenet_transfer |          241 |         6 |    2.84215 |    0.220895  |              0.0533649  |               0.0132611   |
| WNA             | ENA             | graphwavenet_transfer |          522 |        21 |    3.19107 |    0.270441  |              0.262011   |               0.0391498   |
| WNA             | MED             | graphwavenet_transfer |          328 |        19 |    1.73762 |    0.176863  |              0.0300997  |               0.00769641  |
| WNA             | NCA             | graphwavenet_transfer |          144 |         7 |    1.02677 |    0.0979649 |              0.00425855 |               0.00325795  |
| WNA             | NEU             | graphwavenet_transfer |         1000 |        28 |    2.264   |    0.292338  |              0.0263486  |               0.000836917 |
| WNA             | NWN             | graphwavenet_transfer |          183 |        36 |    2.33811 |    0.217384  |              0.0367617  |               0.00454483  |
| WNA             | SAU             | graphwavenet_transfer |          351 |        13 |    1.92401 |    0.231746  |              0.0500367  |               0.0158589   |
| WNA             | WCE             | graphwavenet_transfer |         1000 |        14 |    2.16872 |    0.292459  |              0.0348581  |               0.00382267  |
| WNA             | WNA             | graphwavenet_transfer |          975 |        17 |    1.93238 |    0.211746  |              0          |               0           |
