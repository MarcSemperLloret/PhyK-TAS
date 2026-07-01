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
| CNA             | CNA             | stgcn_diffusion |          438 |        14 |    2.07537 |    0.161839  |             0           |               0           |
| CNA             | EAS             | stgcn_diffusion |          110 |        16 |    6.323   |    0.242622  |             0.162638    |               0.0174393   |
| CNA             | EAU             | stgcn_diffusion |          241 |         6 |    2.82082 |    0.211615  |             0.0313562   |               0.00291736  |
| CNA             | ENA             | stgcn_diffusion |          522 |        21 |    3.07816 |    0.253551  |             0.008911    |               0.00289928  |
| CNA             | MED             | stgcn_diffusion |          328 |        19 |    1.7495  |    0.177075  |             0.0368478   |               0.00698505  |
| CNA             | NCA             | stgcn_diffusion |          144 |         7 |    1.02414 |    0.0968599 |            -0.000912786 |               0.0011816   |
| CNA             | NEU             | stgcn_diffusion |         1000 |        28 |    2.32782 |    0.319219  |             0.094202    |               0.0273886   |
| CNA             | NWN             | stgcn_diffusion |          183 |        36 |    2.51936 |    0.252369  |             0.168486    |               0.0325576   |
| CNA             | SAU             | stgcn_diffusion |          351 |        13 |    1.90894 |    0.2239    |             0.0261856   |               0.00525163  |
| CNA             | WCE             | stgcn_diffusion |         1000 |        17 |    2.19801 |    0.302669  |             0.0484946   |               0.0127175   |
| CNA             | WNA             | stgcn_diffusion |          975 |        17 |    2.03507 |    0.235726  |             0.0745154   |               0.0197863   |
| EAS             | CNA             | stgcn_diffusion |          438 |        14 |    2.17245 |    0.180869  |             0.0970808   |               0.0190293   |
| EAS             | EAS             | stgcn_diffusion |          110 |        16 |    6.16037 |    0.225183  |             0           |               0           |
| EAS             | EAU             | stgcn_diffusion |          241 |         6 |    2.80183 |    0.211468  |             0.0123736   |               0.00277035  |
| EAS             | ENA             | stgcn_diffusion |          522 |        21 |    3.19466 |    0.273902  |             0.125408    |               0.0232503   |
| EAS             | MED             | stgcn_diffusion |          328 |        19 |    1.71245 |    0.169487  |            -0.000200735 |              -0.000602896 |
| EAS             | NCA             | stgcn_diffusion |          144 |         7 |    1.02885 |    0.097089  |             0.0037958   |               0.0014107   |
| EAS             | NEU             | stgcn_diffusion |         1000 |        28 |    2.28251 |    0.305182  |             0.048891    |               0.0133518   |
| EAS             | NWN             | stgcn_diffusion |          183 |        36 |    2.48434 |    0.238398  |             0.133461    |               0.0185874   |
| EAS             | SAU             | stgcn_diffusion |          351 |        13 |    1.88554 |    0.219918  |             0.00278296  |               0.00126918  |
| EAS             | WCE             | stgcn_diffusion |         1000 |        17 |    2.16316 |    0.292262  |             0.0136454   |               0.00231088  |
| EAS             | WNA             | stgcn_diffusion |          975 |        17 |    2.00251 |    0.226062  |             0.0419482   |               0.0101215   |
| EAU             | CNA             | stgcn_diffusion |          438 |        14 |    2.15718 |    0.175685  |             0.0818074   |               0.0138456   |
| EAU             | EAS             | stgcn_diffusion |          110 |        16 |    6.16795 |    0.226443  |             0.00758346  |               0.00126038  |
| EAU             | EAU             | stgcn_diffusion |          241 |         6 |    2.78946 |    0.208697  |             0           |               0           |
| EAU             | ENA             | stgcn_diffusion |          522 |        21 |    3.18399 |    0.271613  |             0.114738    |               0.0209615   |
| EAU             | MED             | stgcn_diffusion |          328 |        19 |    1.71011 |    0.168871  |            -0.00253994  |              -0.00121851  |
| EAU             | NCA             | stgcn_diffusion |          144 |         7 |    1.0258  |    0.0960955 |             0.000737328 |               0.000417205 |
| EAU             | NEU             | stgcn_diffusion |         1000 |        28 |    2.26569 |    0.300065  |             0.0320664   |               0.00823437  |
| EAU             | NWN             | stgcn_diffusion |          183 |        36 |    2.47149 |    0.236428  |             0.120616    |               0.0166172   |
| EAU             | SAU             | stgcn_diffusion |          351 |        13 |    1.88309 |    0.218855  |             0.000331567 |               0.000206336 |
| EAU             | WCE             | stgcn_diffusion |         1000 |        17 |    2.1566  |    0.290115  |             0.0070916   |               0.000163443 |
| EAU             | WNA             | stgcn_diffusion |          975 |        17 |    1.995   |    0.224704  |             0.0344451   |               0.00876399  |
| ENA             | CNA             | stgcn_diffusion |          438 |        14 |    2.10257 |    0.164563  |             0.0272019   |               0.00272409  |
| ENA             | EAS             | stgcn_diffusion |          110 |        16 |    6.32664 |    0.245593  |             0.166276    |               0.0204103   |
| ENA             | EAU             | stgcn_diffusion |          241 |         6 |    2.86396 |    0.217223  |             0.074501    |               0.0085259   |
| ENA             | ENA             | stgcn_diffusion |          522 |        21 |    3.06925 |    0.250652  |             0           |               0           |
| ENA             | MED             | stgcn_diffusion |          328 |        19 |    1.7567  |    0.179711  |             0.0440497   |               0.00962153  |
| ENA             | NCA             | stgcn_diffusion |          144 |         7 |    1.03018 |    0.0978335 |             0.00512094  |               0.00215521  |
| ENA             | NEU             | stgcn_diffusion |         1000 |        28 |    2.31307 |    0.322992  |             0.0794498   |               0.0311614   |
| ENA             | NWN             | stgcn_diffusion |          183 |        36 |    2.52035 |    0.250531  |             0.169476    |               0.0307201   |
| ENA             | SAU             | stgcn_diffusion |          351 |        13 |    1.92633 |    0.230787  |             0.0435755   |               0.0121379   |
| ENA             | WCE             | stgcn_diffusion |         1000 |        17 |    2.18944 |    0.307421  |             0.039924    |               0.0174699   |
| ENA             | WNA             | stgcn_diffusion |          975 |        17 |    2.04828 |    0.23581   |             0.0877222   |               0.0198703   |
| MED             | CNA             | stgcn_diffusion |          438 |        14 |    2.18043 |    0.183259  |             0.105063    |               0.02142     |
| MED             | EAS             | stgcn_diffusion |          110 |        16 |    6.16707 |    0.225574  |             0.00670611  |               0.000390946 |
| MED             | EAU             | stgcn_diffusion |          241 |         6 |    2.80081 |    0.213229  |             0.011353    |               0.00453218  |
| MED             | ENA             | stgcn_diffusion |          522 |        21 |    3.20566 |    0.276994  |             0.13641     |               0.026342    |
| MED             | MED             | stgcn_diffusion |          328 |        19 |    1.71265 |    0.17009   |             0           |               0           |
| MED             | NCA             | stgcn_diffusion |          144 |         7 |    1.03149 |    0.0982851 |             0.00643303  |               0.00260682  |
| MED             | NEU             | stgcn_diffusion |         1000 |        28 |    2.25015 |    0.294358  |             0.0165301   |               0.00252769  |
| MED             | NWN             | stgcn_diffusion |          183 |        36 |    2.42321 |    0.224681  |             0.0723369   |               0.00486998  |
| MED             | SAU             | stgcn_diffusion |          351 |        13 |    1.88879 |    0.221841  |             0.00603574  |               0.00319269  |
| MED             | WCE             | stgcn_diffusion |         1000 |        17 |    2.15979 |    0.2894    |             0.0102795   |              -0.000551375 |
| MED             | WNA             | stgcn_diffusion |          975 |        17 |    1.97706 |    0.219168  |             0.016501    |               0.00322765  |
| NCA             | CNA             | stgcn_diffusion |          438 |        14 |    2.15244 |    0.173339  |             0.0770738   |               0.0115      |
| NCA             | EAS             | stgcn_diffusion |          110 |        16 |    6.38821 |    0.229818  |             0.227845    |               0.00463528  |
| NCA             | EAU             | stgcn_diffusion |          241 |         6 |    2.80758 |    0.21055   |             0.0181174   |               0.00185251  |
| NCA             | ENA             | stgcn_diffusion |          522 |        21 |    3.18305 |    0.266978  |             0.113801    |               0.0163263   |
| NCA             | MED             | stgcn_diffusion |          328 |        19 |    1.72093 |    0.170468  |             0.00827427  |               0.000378574 |
| NCA             | NCA             | stgcn_diffusion |          144 |         7 |    1.02506 |    0.0956783 |             0           |               0           |
| NCA             | NEU             | stgcn_diffusion |         1000 |        28 |    2.29754 |    0.306495  |             0.0639179   |               0.0146647   |
| NCA             | NWN             | stgcn_diffusion |          183 |        36 |    2.4934  |    0.245132  |             0.142528    |               0.0253208   |
| NCA             | SAU             | stgcn_diffusion |          351 |        13 |    1.89696 |    0.220693  |             0.0142021   |               0.00204403  |
| NCA             | WCE             | stgcn_diffusion |         1000 |        17 |    2.17524 |    0.292558  |             0.0257268   |               0.00260698  |
| NCA             | WNA             | stgcn_diffusion |          975 |        17 |    2.00243 |    0.228142  |             0.041871    |               0.0122017   |
| NEU             | CNA             | stgcn_diffusion |          438 |        14 |    2.19453 |    0.190001  |             0.119163    |               0.0281614   |
| NEU             | EAS             | stgcn_diffusion |          110 |        16 |    6.16236 |    0.227591  |             0.00199073  |               0.00240838  |
| NEU             | EAU             | stgcn_diffusion |          241 |         6 |    2.81477 |    0.216932  |             0.0253136   |               0.00823477  |
| NEU             | ENA             | stgcn_diffusion |          522 |        21 |    3.21001 |    0.285275  |             0.140752    |               0.0346226   |
| NEU             | MED             | stgcn_diffusion |          328 |        19 |    1.71959 |    0.17278   |             0.00694137  |               0.0026902   |
| NEU             | NCA             | stgcn_diffusion |          144 |         7 |    1.04406 |    0.1008    |             0.0189995   |               0.00512169  |
| NEU             | NEU             | stgcn_diffusion |         1000 |        28 |    2.23362 |    0.291831  |             0           |               0           |
| NEU             | NWN             | stgcn_diffusion |          183 |        36 |    2.44241 |    0.222759  |             0.0915359   |               0.00294828  |
| NEU             | SAU             | stgcn_diffusion |          351 |        13 |    1.89387 |    0.225609  |             0.0111197   |               0.0069607   |
| NEU             | WCE             | stgcn_diffusion |         1000 |        17 |    2.14747 |    0.289928  |            -0.00204417  |              -2.34465e-05 |
| NEU             | WNA             | stgcn_diffusion |          975 |        17 |    1.99662 |    0.218259  |             0.0360618   |               0.00231852  |
| NWN             | CNA             | stgcn_diffusion |          438 |        14 |    2.33264 |    0.197479  |             0.257269    |               0.0356401   |
| NWN             | EAS             | stgcn_diffusion |          110 |        16 |    6.66287 |    0.230102  |             0.502506    |               0.00491983  |
| NWN             | EAU             | stgcn_diffusion |          241 |         6 |    2.95943 |    0.222936  |             0.16997     |               0.0142391   |
| NWN             | ENA             | stgcn_diffusion |          522 |        21 |    3.4219  |    0.286431  |             0.352642    |               0.0357794   |
| NWN             | MED             | stgcn_diffusion |          328 |        19 |    1.8014  |    0.177889  |             0.0887532   |               0.00779911  |
| NWN             | NCA             | stgcn_diffusion |          144 |         7 |    1.0788  |    0.105799  |             0.0537421   |               0.0101212   |
| NWN             | NEU             | stgcn_diffusion |         1000 |        28 |    2.34652 |    0.29264   |             0.112903    |               0.000809065 |
| NWN             | NWN             | stgcn_diffusion |          183 |        36 |    2.35087 |    0.219811  |             0           |               0           |
| NWN             | SAU             | stgcn_diffusion |          351 |        13 |    2.00218 |    0.230903  |             0.119423    |               0.0122546   |
| NWN             | WCE             | stgcn_diffusion |         1000 |        17 |    2.27703 |    0.291668  |             0.127521    |               0.00171633  |
| NWN             | WNA             | stgcn_diffusion |          975 |        17 |    1.99047 |    0.216991  |             0.0299122   |               0.00105098  |
| SAU             | CNA             | stgcn_diffusion |          438 |        14 |    2.16852 |    0.179852  |             0.0931501   |               0.0180121   |
| SAU             | EAS             | stgcn_diffusion |          110 |        16 |    6.19503 |    0.226146  |             0.0346637   |               0.000963055 |
| SAU             | EAU             | stgcn_diffusion |          241 |         6 |    2.81403 |    0.209996  |             0.0245744   |               0.0012987   |
| SAU             | ENA             | stgcn_diffusion |          522 |        21 |    3.18411 |    0.274123  |             0.114853    |               0.0234712   |
| SAU             | MED             | stgcn_diffusion |          328 |        19 |    1.71257 |    0.169023  |            -7.73211e-05 |              -0.00106642  |
| SAU             | NCA             | stgcn_diffusion |          144 |         7 |    1.03081 |    0.0969323 |             0.00574735  |               0.001254    |
| SAU             | NEU             | stgcn_diffusion |         1000 |        28 |    2.27142 |    0.302018  |             0.0377964   |               0.0101878   |
| SAU             | NWN             | stgcn_diffusion |          183 |        36 |    2.49336 |    0.235717  |             0.142481    |               0.0159064   |
| SAU             | SAU             | stgcn_diffusion |          351 |        13 |    1.88275 |    0.218649  |             0           |               0           |
| SAU             | WCE             | stgcn_diffusion |         1000 |        17 |    2.15301 |    0.290639  |             0.00350027  |               0.000687358 |
| SAU             | WNA             | stgcn_diffusion |          975 |        17 |    2.01784 |    0.22506   |             0.0572767   |               0.00912023  |
| WCE             | CNA             | stgcn_diffusion |          438 |        14 |    2.17805 |    0.182182  |             0.102684    |               0.0203426   |
| WCE             | EAS             | stgcn_diffusion |          110 |        16 |    6.1938  |    0.226118  |             0.0334312   |               0.000935682 |
| WCE             | EAU             | stgcn_diffusion |          241 |         6 |    2.8213  |    0.212326  |             0.0318432   |               0.0036288   |
| WCE             | ENA             | stgcn_diffusion |          522 |        21 |    3.18772 |    0.275653  |             0.118467    |               0.025001    |
| WCE             | MED             | stgcn_diffusion |          328 |        19 |    1.71886 |    0.169896  |             0.00621015  |              -0.000194187 |
| WCE             | NCA             | stgcn_diffusion |          144 |         7 |    1.03835 |    0.0975489 |             0.0132954   |               0.00187066  |
| WCE             | NEU             | stgcn_diffusion |         1000 |        28 |    2.26262 |    0.299534  |             0.0290037   |               0.00770356  |
| WCE             | NWN             | stgcn_diffusion |          183 |        36 |    2.49911 |    0.234981  |             0.148232    |               0.0151705   |
| WCE             | SAU             | stgcn_diffusion |          351 |        13 |    1.88792 |    0.22081   |             0.00516622  |               0.00216127  |
| WCE             | WCE             | stgcn_diffusion |         1000 |        17 |    2.14951 |    0.289951  |             0           |               0           |
| WCE             | WNA             | stgcn_diffusion |          975 |        17 |    2.02362 |    0.22323   |             0.0630569   |               0.00728961  |
| WNA             | CNA             | stgcn_diffusion |          438 |        14 |    2.2231  |    0.191162  |             0.147731    |               0.0293225   |
| WNA             | EAS             | stgcn_diffusion |          110 |        16 |    6.18249 |    0.229838  |             0.0221271   |               0.00465543  |
| WNA             | EAU             | stgcn_diffusion |          241 |         6 |    2.8436  |    0.220679  |             0.0541348   |               0.0119815   |
| WNA             | ENA             | stgcn_diffusion |          522 |        21 |    3.27177 |    0.282488  |             0.202517    |               0.0318357   |
| WNA             | MED             | stgcn_diffusion |          328 |        19 |    1.74464 |    0.175933  |             0.0319851   |               0.00584289  |
| WNA             | NCA             | stgcn_diffusion |          144 |         7 |    1.04011 |    0.100993  |             0.0150485   |               0.00531477  |
| WNA             | NEU             | stgcn_diffusion |         1000 |        28 |    2.29046 |    0.29265   |             0.0568386   |               0.000819747 |
| WNA             | NWN             | stgcn_diffusion |          183 |        36 |    2.37131 |    0.219598  |             0.0204321   |              -0.000212893 |
| WNA             | SAU             | stgcn_diffusion |          351 |        13 |    1.94027 |    0.232138  |             0.0575199   |               0.0134893   |
| WNA             | WCE             | stgcn_diffusion |         1000 |        17 |    2.22218 |    0.292884  |             0.0726681   |               0.00293316  |
| WNA             | WNA             | stgcn_diffusion |          975 |        17 |    1.96056 |    0.21594   |             0           |               0           |
