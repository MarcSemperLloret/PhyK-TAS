# ST-GNN forecasting experiment

Model:

- `stgcn_diffusion`: temporal convolution plus two fixed-graph diffusion layers;
- graph: symmetric kNN adjacency within each AR6 region;
- no node-specific embeddings, so weights can transfer across regions with different station identities.

Training:

- source region only;
- train 2005-2012;
- validation 2013-2015;
- test 2020-2025 on each target-region graph.

## Pair summary

| source_region   | target_region   | model           |   n_stations |   n_cells |   mae_mean |   brier_mean |   mae_out_minus_in_mean |   brier_out_minus_in_mean |
|:----------------|:----------------|:----------------|-------------:|----------:|-----------:|-------------:|------------------------:|--------------------------:|
| CNA             | CNA             | stgcn_diffusion |          438 |        14 |    2.08599 |    0.163595  |             0           |               0           |
| CNA             | EAS             | stgcn_diffusion |          110 |        16 |    6.65203 |    0.243614  |             0.462583    |               0.018536    |
| CNA             | EAU             | stgcn_diffusion |          241 |         6 |    2.83356 |    0.212694  |             0.0420106   |               0.00388911  |
| CNA             | ENA             | stgcn_diffusion |          522 |        21 |    3.07623 |    0.254005  |             0.00676768  |               0.00345952  |
| CNA             | MED             | stgcn_diffusion |          328 |        19 |    1.76214 |    0.177548  |             0.0512264   |               0.00869021  |
| CNA             | NCA             | stgcn_diffusion |          144 |         7 |    1.02942 |    0.096705  |             0.000394123 |               0.00087089  |
| CNA             | NEU             | stgcn_diffusion |         1000 |        29 |    2.28205 |    0.319069  |             0.0976968   |               0.0269174   |
| CNA             | NWN             | stgcn_diffusion |          183 |        36 |    2.53713 |    0.255281  |             0.192823    |               0.036911    |
| CNA             | SAU             | stgcn_diffusion |          351 |        13 |    1.91707 |    0.225305  |             0.0334789   |               0.00650363  |
| CNA             | WCE             | stgcn_diffusion |         1000 |        15 |    2.16555 |    0.302975  |             0.055822    |               0.0142848   |
| CNA             | WNA             | stgcn_diffusion |          975 |        17 |    2.04579 |    0.236493  |             0.0771824   |               0.0205074   |
| EAS             | CNA             | stgcn_diffusion |          438 |        14 |    2.2017  |    0.188192  |             0.115717    |               0.0245966   |
| EAS             | EAS             | stgcn_diffusion |          110 |        16 |    6.18945 |    0.225078  |             0           |               0           |
| EAS             | EAU             | stgcn_diffusion |          241 |         6 |    2.81413 |    0.214231  |             0.022582    |               0.00542609  |
| EAS             | ENA             | stgcn_diffusion |          522 |        21 |    3.23425 |    0.281285  |             0.164783    |               0.0307393   |
| EAS             | MED             | stgcn_diffusion |          328 |        19 |    1.72069 |    0.171195  |             0.00976964  |               0.00233804  |
| EAS             | NCA             | stgcn_diffusion |          144 |         7 |    1.0361  |    0.0996316 |             0.0070772   |               0.00379746  |
| EAS             | NEU             | stgcn_diffusion |         1000 |        29 |    2.22073 |    0.296712  |             0.0363686   |               0.00456085  |
| EAS             | NWN             | stgcn_diffusion |          183 |        36 |    2.43689 |    0.226477  |             0.0925756   |               0.00810755  |
| EAS             | SAU             | stgcn_diffusion |          351 |        13 |    1.89775 |    0.222591  |             0.0141649   |               0.00378981  |
| EAS             | WCE             | stgcn_diffusion |         1000 |        15 |    2.13201 |    0.289083  |             0.0222797   |               0.000392898 |
| EAS             | WNA             | stgcn_diffusion |          975 |        17 |    1.98162 |    0.220336  |             0.0130184   |               0.00434988  |
| EAU             | CNA             | stgcn_diffusion |          438 |        14 |    2.15659 |    0.175759  |             0.0706018   |               0.0121637   |
| EAU             | EAS             | stgcn_diffusion |          110 |        16 |    6.14935 |    0.226509  |            -0.040093    |               0.0014309   |
| EAU             | EAU             | stgcn_diffusion |          241 |         6 |    2.79155 |    0.208805  |             0           |               0           |
| EAU             | ENA             | stgcn_diffusion |          522 |        21 |    3.18291 |    0.271981  |             0.113443    |               0.0214353   |
| EAU             | MED             | stgcn_diffusion |          328 |        19 |    1.70998 |    0.169052  |            -0.000935402 |               0.000195002 |
| EAU             | NCA             | stgcn_diffusion |          144 |         7 |    1.02582 |    0.0961032 |            -0.00319893  |               0.000269044 |
| EAU             | NEU             | stgcn_diffusion |         1000 |        29 |    2.20996 |    0.298486  |             0.0255992   |               0.00633522  |
| EAU             | NWN             | stgcn_diffusion |          183 |        36 |    2.4754  |    0.236749  |             0.131093    |               0.0183793   |
| EAU             | SAU             | stgcn_diffusion |          351 |        13 |    1.88245 |    0.218892  |            -0.00113951  |               9.05837e-05 |
| EAU             | WCE             | stgcn_diffusion |         1000 |        15 |    2.11714 |    0.289499  |             0.00741113  |               0.000809284 |
| EAU             | WNA             | stgcn_diffusion |          975 |        17 |    1.99616 |    0.224595  |             0.0275557   |               0.00860933  |
| ENA             | CNA             | stgcn_diffusion |          438 |        14 |    2.10013 |    0.164344  |             0.0141476   |               0.000748328 |
| ENA             | EAS             | stgcn_diffusion |          110 |        16 |    6.32948 |    0.252457  |             0.140031    |               0.0273792   |
| ENA             | EAU             | stgcn_diffusion |          241 |         6 |    2.85577 |    0.218693  |             0.0642156   |               0.00988846  |
| ENA             | ENA             | stgcn_diffusion |          522 |        21 |    3.06946 |    0.250546  |             0           |               0           |
| ENA             | MED             | stgcn_diffusion |          328 |        19 |    1.7487  |    0.178811  |             0.037787    |               0.00995363  |
| ENA             | NCA             | stgcn_diffusion |          144 |         7 |    1.02423 |    0.0964881 |            -0.00479566  |               0.000653985 |
| ENA             | NEU             | stgcn_diffusion |         1000 |        29 |    2.26933 |    0.325574  |             0.0849753   |               0.0334229   |
| ENA             | NWN             | stgcn_diffusion |          183 |        36 |    2.52659 |    0.255919  |             0.18228     |               0.0375491   |
| ENA             | SAU             | stgcn_diffusion |          351 |        13 |    1.9209  |    0.231413  |             0.0373088   |               0.0126118   |
| ENA             | WCE             | stgcn_diffusion |         1000 |        15 |    2.15464 |    0.308532  |             0.0449104   |               0.0198424   |
| ENA             | WNA             | stgcn_diffusion |          975 |        17 |    2.04615 |    0.239841  |             0.0775446   |               0.0238546   |
| MED             | CNA             | stgcn_diffusion |          438 |        14 |    2.16243 |    0.178039  |             0.0764399   |               0.0144441   |
| MED             | EAS             | stgcn_diffusion |          110 |        16 |    6.16734 |    0.22664   |            -0.0221103   |               0.00156206  |
| MED             | EAU             | stgcn_diffusion |          241 |         6 |    2.80612 |    0.210008  |             0.0145717   |               0.00120286  |
| MED             | ENA             | stgcn_diffusion |          522 |        21 |    3.17886 |    0.272821  |             0.109392    |               0.022275    |
| MED             | MED             | stgcn_diffusion |          328 |        19 |    1.71092 |    0.168857  |             0           |               0           |
| MED             | NCA             | stgcn_diffusion |          144 |         7 |    1.02821 |    0.0966146 |            -0.000816828 |               0.000780498 |
| MED             | NEU             | stgcn_diffusion |         1000 |        29 |    2.21436 |    0.300031  |             0.0299982   |               0.00788017  |
| MED             | NWN             | stgcn_diffusion |          183 |        36 |    2.48433 |    0.23532   |             0.140016    |               0.0169499   |
| MED             | SAU             | stgcn_diffusion |          351 |        13 |    1.88336 |    0.219118  |            -0.000225739 |               0.000316832 |
| MED             | WCE             | stgcn_diffusion |         1000 |        15 |    2.1152  |    0.289876  |             0.00547013  |               0.00118577  |
| MED             | WNA             | stgcn_diffusion |          975 |        17 |    2.00847 |    0.224261  |             0.039866    |               0.0082753   |
| NCA             | CNA             | stgcn_diffusion |          438 |        14 |    2.16898 |    0.175018  |             0.0829892   |               0.0114226   |
| NCA             | EAS             | stgcn_diffusion |          110 |        16 |    7.15274 |    0.227721  |             0.963289    |               0.00264293  |
| NCA             | EAU             | stgcn_diffusion |          241 |         6 |    2.88859 |    0.210403  |             0.09704     |               0.00159845  |
| NCA             | ENA             | stgcn_diffusion |          522 |        21 |    3.21261 |    0.269095  |             0.143146    |               0.018549    |
| NCA             | MED             | stgcn_diffusion |          328 |        19 |    1.7443  |    0.170054  |             0.0333838   |               0.00119671  |
| NCA             | NCA             | stgcn_diffusion |          144 |         7 |    1.02902 |    0.0958341 |             0           |               0           |
| NCA             | NEU             | stgcn_diffusion |         1000 |        29 |    2.30022 |    0.300763  |             0.115862    |               0.00861213  |
| NCA             | NWN             | stgcn_diffusion |          183 |        36 |    2.45178 |    0.237328  |             0.107471    |               0.0189579   |
| NCA             | SAU             | stgcn_diffusion |          351 |        13 |    1.91926 |    0.219908  |             0.0356766   |               0.00110625  |
| NCA             | WCE             | stgcn_diffusion |         1000 |        15 |    2.1979  |    0.289928  |             0.0881691   |               0.00123758  |
| NCA             | WNA             | stgcn_diffusion |          975 |        17 |    2.01119 |    0.224267  |             0.0425863   |               0.0082814   |
| NEU             | CNA             | stgcn_diffusion |          438 |        14 |    2.21271 |    0.195083  |             0.12672     |               0.0314877   |
| NEU             | EAS             | stgcn_diffusion |          110 |        16 |    6.22428 |    0.229448  |             0.034836    |               0.00437003  |
| NEU             | EAU             | stgcn_diffusion |          241 |         6 |    2.82697 |    0.220927  |             0.0354144   |               0.0121226   |
| NEU             | ENA             | stgcn_diffusion |          522 |        21 |    3.23956 |    0.292267  |             0.1701      |               0.0417217   |
| NEU             | MED             | stgcn_diffusion |          328 |        19 |    1.7273  |    0.175446  |             0.0163786   |               0.00658894  |
| NEU             | NCA             | stgcn_diffusion |          144 |         7 |    1.04944 |    0.103354  |             0.0204183   |               0.00752014  |
| NEU             | NEU             | stgcn_diffusion |         1000 |        29 |    2.18436 |    0.292151  |             0           |               0           |
| NEU             | NWN             | stgcn_diffusion |          183 |        36 |    2.41185 |    0.223337  |             0.0675415   |               0.00496725  |
| NEU             | SAU             | stgcn_diffusion |          351 |        13 |    1.90851 |    0.229921  |             0.02492     |               0.011119    |
| NEU             | WCE             | stgcn_diffusion |         1000 |        15 |    2.12423 |    0.291716  |             0.0144978   |               0.00302609  |
| NEU             | WNA             | stgcn_diffusion |          975 |        17 |    1.98798 |    0.218892  |             0.019376    |               0.0029064   |
| NWN             | CNA             | stgcn_diffusion |          438 |        14 |    2.29476 |    0.194566  |             0.208774    |               0.0309703   |
| NWN             | EAS             | stgcn_diffusion |          110 |        16 |    6.42283 |    0.228778  |             0.23338     |               0.00370024  |
| NWN             | EAU             | stgcn_diffusion |          241 |         6 |    2.91902 |    0.221223  |             0.127465    |               0.0124185   |
| NWN             | ENA             | stgcn_diffusion |          522 |        21 |    3.3622  |    0.283341  |             0.292736    |               0.0327948   |
| NWN             | MED             | stgcn_diffusion |          328 |        19 |    1.7818  |    0.176213  |             0.0708784   |               0.00735545  |
| NWN             | NCA             | stgcn_diffusion |          144 |         7 |    1.06412 |    0.103569  |             0.0351002   |               0.00773472  |
| NWN             | NEU             | stgcn_diffusion |         1000 |        29 |    2.27616 |    0.292447  |             0.0917986   |               0.00029556  |
| NWN             | NWN             | stgcn_diffusion |          183 |        36 |    2.34431 |    0.21837   |             0           |               0           |
| NWN             | SAU             | stgcn_diffusion |          351 |        13 |    1.98023 |    0.228945  |             0.0966396   |               0.0101434   |
| NWN             | WCE             | stgcn_diffusion |         1000 |        15 |    2.21859 |    0.290465  |             0.10886     |               0.00177512  |
| NWN             | WNA             | stgcn_diffusion |          975 |        17 |    1.97505 |    0.216131  |             0.00644281  |               0.000145413 |
| SAU             | CNA             | stgcn_diffusion |          438 |        14 |    2.17016 |    0.180938  |             0.0841744   |               0.0173429   |
| SAU             | EAS             | stgcn_diffusion |          110 |        16 |    6.17987 |    0.226631  |            -0.00957535  |               0.0015526   |
| SAU             | EAU             | stgcn_diffusion |          241 |         6 |    2.81097 |    0.21048   |             0.0194197   |               0.00167522  |
| SAU             | ENA             | stgcn_diffusion |          522 |        21 |    3.18502 |    0.274103  |             0.115559    |               0.0235569   |
| SAU             | MED             | stgcn_diffusion |          328 |        19 |    1.71193 |    0.168816  |             0.00100872  |              -4.166e-05   |
| SAU             | NCA             | stgcn_diffusion |          144 |         7 |    1.03113 |    0.0973777 |             0.00210587  |               0.00154356  |
| SAU             | NEU             | stgcn_diffusion |         1000 |        29 |    2.22322 |    0.304211  |             0.0388605   |               0.0120601   |
| SAU             | NWN             | stgcn_diffusion |          183 |        36 |    2.4894  |    0.236323  |             0.14509     |               0.0179527   |
| SAU             | SAU             | stgcn_diffusion |          351 |        13 |    1.88359 |    0.218802  |             0           |               0           |
| SAU             | WCE             | stgcn_diffusion |         1000 |        15 |    2.11915 |    0.292565  |             0.009421    |               0.00387472  |
| SAU             | WNA             | stgcn_diffusion |          975 |        17 |    2.01626 |    0.226527  |             0.0476542   |               0.0105407   |
| WCE             | CNA             | stgcn_diffusion |          438 |        14 |    2.17695 |    0.18269   |             0.0909643   |               0.0190943   |
| WCE             | EAS             | stgcn_diffusion |          110 |        16 |    6.20092 |    0.227303  |             0.0114694   |               0.00222552  |
| WCE             | EAU             | stgcn_diffusion |          241 |         6 |    2.82156 |    0.212728  |             0.0300073   |               0.00392306  |
| WCE             | ENA             | stgcn_diffusion |          522 |        21 |    3.18854 |    0.277044  |             0.119081    |               0.0264986   |
| WCE             | MED             | stgcn_diffusion |          328 |        19 |    1.71711 |    0.169997  |             0.00618766  |               0.00113935  |
| WCE             | NCA             | stgcn_diffusion |          144 |         7 |    1.03603 |    0.0977837 |             0.00701208  |               0.00194957  |
| WCE             | NEU             | stgcn_diffusion |         1000 |        29 |    2.20331 |    0.295001  |             0.0189553   |               0.00284928  |
| WCE             | NWN             | stgcn_diffusion |          183 |        36 |    2.49405 |    0.231828  |             0.149736    |               0.0134578   |
| WCE             | SAU             | stgcn_diffusion |          351 |        13 |    1.88754 |    0.221479  |             0.00395744  |               0.00267702  |
| WCE             | WCE             | stgcn_diffusion |         1000 |        15 |    2.10973 |    0.28869   |             0           |               0           |
| WCE             | WNA             | stgcn_diffusion |          975 |        17 |    2.01973 |    0.221705  |             0.051127    |               0.00571941  |
| WNA             | CNA             | stgcn_diffusion |          438 |        14 |    2.18762 |    0.186529  |             0.101634    |               0.0229334   |
| WNA             | EAS             | stgcn_diffusion |          110 |        16 |    6.14476 |    0.229947  |            -0.0446865   |               0.00486936  |
| WNA             | EAU             | stgcn_diffusion |          241 |         6 |    2.81651 |    0.21789   |             0.0249542   |               0.00908498  |
| WNA             | ENA             | stgcn_diffusion |          522 |        21 |    3.21518 |    0.278203  |             0.145713    |               0.0276573   |
| WNA             | MED             | stgcn_diffusion |          328 |        19 |    1.7214  |    0.174314  |             0.0104775   |               0.00545646  |
| WNA             | NCA             | stgcn_diffusion |          144 |         7 |    1.03121 |    0.0992744 |             0.00218511  |               0.00344031  |
| WNA             | NEU             | stgcn_diffusion |         1000 |        29 |    2.2026  |    0.292764  |             0.0182392   |               0.000612602 |
| WNA             | NWN             | stgcn_diffusion |          183 |        36 |    2.41363 |    0.221435  |             0.0693217   |               0.00306525  |
| WNA             | SAU             | stgcn_diffusion |          351 |        13 |    1.90204 |    0.229596  |             0.0184558   |               0.0107946   |
| WNA             | WCE             | stgcn_diffusion |         1000 |        15 |    2.13185 |    0.291774  |             0.0221213   |               0.00308355  |
| WNA             | WNA             | stgcn_diffusion |          975 |        17 |    1.96861 |    0.215986  |             0           |               0           |
