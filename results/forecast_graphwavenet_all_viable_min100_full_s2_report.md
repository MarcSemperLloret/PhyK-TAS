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
| CNA             | CNA             | graphwavenet_transfer |          438 |        14 |    1.97668 |    0.148294  |             0           |               0           |
| CNA             | EAS             | graphwavenet_transfer |          110 |        16 |    6.26882 |    0.245813  |             0.142258    |               0.0200149   |
| CNA             | EAU             | graphwavenet_transfer |          241 |         6 |    2.81319 |    0.211048  |             0.0221183   |               0.00375719  |
| CNA             | ENA             | graphwavenet_transfer |          522 |        21 |    2.95325 |    0.235397  |             0.0249174   |               0.00390836  |
| CNA             | MED             | graphwavenet_transfer |          328 |        19 |    1.73984 |    0.175285  |             0.0293285   |               0.00543264  |
| CNA             | NCA             | graphwavenet_transfer |          144 |         7 |    1.00972 |    0.0945345 |            -0.00407786  |               0.000742826 |
| CNA             | NEU             | graphwavenet_transfer |         1000 |        28 |    2.32169 |    0.315437  |             0.0903934   |               0.0244411   |
| CNA             | NWN             | graphwavenet_transfer |          183 |        36 |    2.48974 |    0.247882  |             0.194374    |               0.034772    |
| CNA             | SAU             | graphwavenet_transfer |          351 |        13 |    1.90516 |    0.22422   |             0.025747    |               0.00705436  |
| CNA             | WCE             | graphwavenet_transfer |         1000 |        17 |    2.19825 |    0.30164   |             0.0485638   |               0.0112866   |
| CNA             | WNA             | graphwavenet_transfer |          975 |        17 |    2.01204 |    0.23371   |             0.0805062   |               0.0219966   |
| EAS             | CNA             | graphwavenet_transfer |          438 |        14 |    2.19518 |    0.186413  |             0.218494    |               0.038119    |
| EAS             | EAS             | graphwavenet_transfer |          110 |        16 |    6.12657 |    0.225798  |             0           |               0           |
| EAS             | EAU             | graphwavenet_transfer |          241 |         6 |    2.81097 |    0.212201  |             0.0198955   |               0.00491031  |
| EAS             | ENA             | graphwavenet_transfer |          522 |        21 |    3.22339 |    0.27974   |             0.295062    |               0.0482515   |
| EAS             | MED             | graphwavenet_transfer |          328 |        19 |    1.71467 |    0.170214  |             0.00415841  |               0.000360928 |
| EAS             | NCA             | graphwavenet_transfer |          144 |         7 |    1.03423 |    0.0987031 |             0.0204307   |               0.00491139  |
| EAS             | NEU             | graphwavenet_transfer |         1000 |        28 |    2.27324 |    0.296547  |             0.0419349   |               0.00555088  |
| EAS             | NWN             | graphwavenet_transfer |          183 |        36 |    2.41462 |    0.222428  |             0.11925     |               0.00931788  |
| EAS             | SAU             | graphwavenet_transfer |          351 |        13 |    1.88945 |    0.219677  |             0.0100316   |               0.00251143  |
| EAS             | WCE             | graphwavenet_transfer |         1000 |        17 |    2.17623 |    0.289513  |             0.026549    |              -0.000840766 |
| EAS             | WNA             | graphwavenet_transfer |          975 |        17 |    1.97891 |    0.219285  |             0.0473754   |               0.00757086  |
| EAU             | CNA             | graphwavenet_transfer |          438 |        14 |    2.15656 |    0.175167  |             0.179879    |               0.0268732   |
| EAU             | EAS             | graphwavenet_transfer |          110 |        16 |    6.1447  |    0.231392  |             0.0181392   |               0.00559405  |
| EAU             | EAU             | graphwavenet_transfer |          241 |         6 |    2.79107 |    0.207291  |             0           |               0           |
| EAU             | ENA             | graphwavenet_transfer |          522 |        21 |    3.18476 |    0.270384  |             0.256429    |               0.0388951   |
| EAU             | MED             | graphwavenet_transfer |          328 |        19 |    1.7107  |    0.168993  |             0.000191321 |              -0.000859494 |
| EAU             | NCA             | graphwavenet_transfer |          144 |         7 |    1.02525 |    0.0962444 |             0.0114519   |               0.00245274  |
| EAU             | NEU             | graphwavenet_transfer |         1000 |        28 |    2.26275 |    0.299158  |             0.0314521   |               0.00816137  |
| EAU             | NWN             | graphwavenet_transfer |          183 |        36 |    2.46478 |    0.233694  |             0.169414    |               0.0205835   |
| EAU             | SAU             | graphwavenet_transfer |          351 |        13 |    1.87881 |    0.21711   |            -0.000607337 |              -5.56775e-05 |
| EAU             | WCE             | graphwavenet_transfer |         1000 |        17 |    2.15681 |    0.29162   |             0.00713133  |               0.00126625  |
| EAU             | WNA             | graphwavenet_transfer |          975 |        17 |    1.99728 |    0.22426   |             0.0657372   |               0.0125464   |
| ENA             | CNA             | graphwavenet_transfer |          438 |        14 |    1.99226 |    0.151053  |             0.0155742   |               0.00275953  |
| ENA             | EAS             | graphwavenet_transfer |          110 |        16 |    6.31292 |    0.263273  |             0.186355    |               0.0374751   |
| ENA             | EAU             | graphwavenet_transfer |          241 |         6 |    2.83911 |    0.216811  |             0.0480359   |               0.00951997  |
| ENA             | ENA             | graphwavenet_transfer |          522 |        21 |    2.92833 |    0.231489  |             0           |               0           |
| ENA             | MED             | graphwavenet_transfer |          328 |        19 |    1.75891 |    0.177886  |             0.0484023   |               0.00803382  |
| ENA             | NCA             | graphwavenet_transfer |          144 |         7 |    1.02357 |    0.0973899 |             0.00976632  |               0.00359816  |
| ENA             | NEU             | graphwavenet_transfer |         1000 |        28 |    2.33869 |    0.32034   |             0.107393    |               0.0293442   |
| ENA             | NWN             | graphwavenet_transfer |          183 |        36 |    2.45461 |    0.238902  |             0.15924     |               0.0257914   |
| ENA             | SAU             | graphwavenet_transfer |          351 |        13 |    1.92186 |    0.229654  |             0.042441    |               0.0124888   |
| ENA             | WCE             | graphwavenet_transfer |         1000 |        17 |    2.21606 |    0.307425  |             0.0663757   |               0.0170721   |
| ENA             | WNA             | graphwavenet_transfer |          975 |        17 |    2.01832 |    0.2316    |             0.0867844   |               0.0198867   |
| MED             | CNA             | graphwavenet_transfer |          438 |        14 |    2.18183 |    0.184463  |             0.205147    |               0.0361697   |
| MED             | EAS             | graphwavenet_transfer |          110 |        16 |    6.12759 |    0.224568  |             0.00102069  |              -0.00123048  |
| MED             | EAU             | graphwavenet_transfer |          241 |         6 |    2.80421 |    0.211575  |             0.0131358   |               0.00428342  |
| MED             | ENA             | graphwavenet_transfer |          522 |        21 |    3.20506 |    0.277617  |             0.276723    |               0.0461281   |
| MED             | MED             | graphwavenet_transfer |          328 |        19 |    1.71051 |    0.169853  |             0           |               0           |
| MED             | NCA             | graphwavenet_transfer |          144 |         7 |    1.02829 |    0.0975175 |             0.0144921   |               0.00372581  |
| MED             | NEU             | graphwavenet_transfer |         1000 |        28 |    2.24463 |    0.293048  |             0.0133277   |               0.00205167  |
| MED             | NWN             | graphwavenet_transfer |          183 |        36 |    2.41078 |    0.219772  |             0.115413    |               0.00666129  |
| MED             | SAU             | graphwavenet_transfer |          351 |        13 |    1.8808  |    0.219613  |             0.00138747  |               0.00244715  |
| MED             | WCE             | graphwavenet_transfer |         1000 |        17 |    2.15602 |    0.288819  |             0.00633882  |              -0.00153475  |
| MED             | WNA             | graphwavenet_transfer |          975 |        17 |    1.96967 |    0.216686  |             0.0381267   |               0.00497207  |
| NCA             | CNA             | graphwavenet_transfer |          438 |        14 |    2.10844 |    0.165232  |             0.13176     |               0.0169383   |
| NCA             | EAS             | graphwavenet_transfer |          110 |        16 |    6.23745 |    0.238813  |             0.110882    |               0.0130144   |
| NCA             | EAU             | graphwavenet_transfer |          241 |         6 |    2.81894 |    0.211254  |             0.0278719   |               0.00396237  |
| NCA             | ENA             | graphwavenet_transfer |          522 |        21 |    3.0809  |    0.24974   |             0.152569    |               0.0182511   |
| NCA             | MED             | graphwavenet_transfer |          328 |        19 |    1.73866 |    0.172263  |             0.028154    |               0.0024105   |
| NCA             | NCA             | graphwavenet_transfer |          144 |         7 |    1.0138  |    0.0937917 |             0           |               0           |
| NCA             | NEU             | graphwavenet_transfer |         1000 |        28 |    2.34592 |    0.302539  |             0.114621    |               0.0115429   |
| NCA             | NWN             | graphwavenet_transfer |          183 |        36 |    2.42289 |    0.22662   |             0.127529    |               0.0135093   |
| NCA             | SAU             | graphwavenet_transfer |          351 |        13 |    1.91845 |    0.222401  |             0.0390366   |               0.00523579  |
| NCA             | WCE             | graphwavenet_transfer |         1000 |        17 |    2.2361  |    0.297426  |             0.0864203   |               0.00707296  |
| NCA             | WNA             | graphwavenet_transfer |          975 |        17 |    1.99418 |    0.221949  |             0.0626399   |               0.0102354   |
| NEU             | CNA             | graphwavenet_transfer |          438 |        14 |    2.19512 |    0.191545  |             0.218438    |               0.0432509   |
| NEU             | EAS             | graphwavenet_transfer |          110 |        16 |    6.1705  |    0.227955  |             0.0439322   |               0.00215732  |
| NEU             | EAU             | graphwavenet_transfer |          241 |         6 |    2.82039 |    0.217766  |             0.0293135   |               0.0104748   |
| NEU             | ENA             | graphwavenet_transfer |          522 |        21 |    3.20926 |    0.287703  |             0.280926    |               0.0562145   |
| NEU             | MED             | graphwavenet_transfer |          328 |        19 |    1.71809 |    0.173016  |             0.00757952  |               0.00316377  |
| NEU             | NCA             | graphwavenet_transfer |          144 |         7 |    1.04285 |    0.101241  |             0.0290484   |               0.00744943  |
| NEU             | NEU             | graphwavenet_transfer |         1000 |        28 |    2.2313  |    0.290996  |             0           |               0           |
| NEU             | NWN             | graphwavenet_transfer |          183 |        36 |    2.42958 |    0.219586  |             0.134216    |               0.00647539  |
| NEU             | SAU             | graphwavenet_transfer |          351 |        13 |    1.89256 |    0.22502   |             0.0131449   |               0.00785403  |
| NEU             | WCE             | graphwavenet_transfer |         1000 |        17 |    2.14642 |    0.289712  |            -0.00326382  |              -0.000641548 |
| NEU             | WNA             | graphwavenet_transfer |          975 |        17 |    1.99454 |    0.216845  |             0.062998    |               0.00513138  |
| NWN             | CNA             | graphwavenet_transfer |          438 |        14 |    2.21588 |    0.184765  |             0.239194    |               0.0364709   |
| NWN             | EAS             | graphwavenet_transfer |          110 |        16 |    6.21305 |    0.228259  |             0.0864821   |               0.00246039  |
| NWN             | EAU             | graphwavenet_transfer |          241 |         6 |    2.86001 |    0.217044  |             0.0689385   |               0.00975289  |
| NWN             | ENA             | graphwavenet_transfer |          522 |        21 |    3.20355 |    0.269722  |             0.275216    |               0.0382335   |
| NWN             | MED             | graphwavenet_transfer |          328 |        19 |    1.73982 |    0.172934  |             0.0293063   |               0.00308124  |
| NWN             | NCA             | graphwavenet_transfer |          144 |         7 |    1.04099 |    0.100057  |             0.0271865   |               0.00626541  |
| NWN             | NEU             | graphwavenet_transfer |         1000 |        28 |    2.26483 |    0.293678  |             0.0335267   |               0.00268202  |
| NWN             | NWN             | graphwavenet_transfer |          183 |        36 |    2.29537 |    0.21311   |             0           |               0           |
| NWN             | SAU             | graphwavenet_transfer |          351 |        13 |    1.91821 |    0.221273  |             0.0387904   |               0.00410692  |
| NWN             | WCE             | graphwavenet_transfer |         1000 |        17 |    2.19151 |    0.291768  |             0.0418292   |               0.00141499  |
| NWN             | WNA             | graphwavenet_transfer |          975 |        17 |    1.94098 |    0.214056  |             0.00944037  |               0.00234217  |
| SAU             | CNA             | graphwavenet_transfer |          438 |        14 |    2.16991 |    0.180978  |             0.193222    |               0.0326846   |
| SAU             | EAS             | graphwavenet_transfer |          110 |        16 |    6.18967 |    0.225289  |             0.0631007   |              -0.000509312 |
| SAU             | EAU             | graphwavenet_transfer |          241 |         6 |    2.81252 |    0.209952  |             0.0214509   |               0.00266047  |
| SAU             | ENA             | graphwavenet_transfer |          522 |        21 |    3.18678 |    0.275661  |             0.258446    |               0.0441721   |
| SAU             | MED             | graphwavenet_transfer |          328 |        19 |    1.71095 |    0.16868   |             0.000435791 |              -0.00117223  |
| SAU             | NCA             | graphwavenet_transfer |          144 |         7 |    1.03099 |    0.0974284 |             0.0171844   |               0.00363668  |
| SAU             | NEU             | graphwavenet_transfer |         1000 |        28 |    2.25548 |    0.296528  |             0.0241744   |               0.00553134  |
| SAU             | NWN             | graphwavenet_transfer |          183 |        36 |    2.4665  |    0.226371  |             0.171135    |               0.0132611   |
| SAU             | SAU             | graphwavenet_transfer |          351 |        13 |    1.87942 |    0.217166  |             0           |               0           |
| SAU             | WCE             | graphwavenet_transfer |         1000 |        17 |    2.15361 |    0.290753  |             0.00392768  |               0.000400127 |
| SAU             | WNA             | graphwavenet_transfer |          975 |        17 |    2.00812 |    0.222199  |             0.0765832   |               0.0104855   |
| WCE             | CNA             | graphwavenet_transfer |          438 |        14 |    2.17282 |    0.18176   |             0.196138    |               0.0334661   |
| WCE             | EAS             | graphwavenet_transfer |          110 |        16 |    6.21763 |    0.228373  |             0.0910634   |               0.00257447  |
| WCE             | EAU             | graphwavenet_transfer |          241 |         6 |    2.8219  |    0.211382  |             0.0308289   |               0.00409102  |
| WCE             | ENA             | graphwavenet_transfer |          522 |        21 |    3.18489 |    0.275622  |             0.256554    |               0.0441337   |
| WCE             | MED             | graphwavenet_transfer |          328 |        19 |    1.71529 |    0.169494  |             0.00477658  |              -0.000358218 |
| WCE             | NCA             | graphwavenet_transfer |          144 |         7 |    1.03173 |    0.0972035 |             0.0179316   |               0.00341181  |
| WCE             | NEU             | graphwavenet_transfer |         1000 |        28 |    2.26426 |    0.299957  |             0.0329577   |               0.0089609   |
| WCE             | NWN             | graphwavenet_transfer |          183 |        36 |    2.50016 |    0.237278  |             0.204792    |               0.0241679   |
| WCE             | SAU             | graphwavenet_transfer |          351 |        13 |    1.88565 |    0.219757  |             0.00623398  |               0.00259143  |
| WCE             | WCE             | graphwavenet_transfer |         1000 |        17 |    2.14968 |    0.290353  |             0           |               0           |
| WCE             | WNA             | graphwavenet_transfer |          975 |        17 |    2.02256 |    0.224655  |             0.0910263   |               0.012941    |
| WNA             | CNA             | graphwavenet_transfer |          438 |        14 |    2.18292 |    0.18269   |             0.20624     |               0.0343965   |
| WNA             | EAS             | graphwavenet_transfer |          110 |        16 |    6.18375 |    0.230753  |             0.0571863   |               0.00495488  |
| WNA             | EAU             | graphwavenet_transfer |          241 |         6 |    2.84816 |    0.220427  |             0.0570885   |               0.0131359   |
| WNA             | ENA             | graphwavenet_transfer |          522 |        21 |    3.18165 |    0.270968  |             0.253315    |               0.0394792   |
| WNA             | MED             | graphwavenet_transfer |          328 |        19 |    1.7434  |    0.175827  |             0.0328896   |               0.00597475  |
| WNA             | NCA             | graphwavenet_transfer |          144 |         7 |    1.02504 |    0.0975308 |             0.0112409   |               0.00373912  |
| WNA             | NEU             | graphwavenet_transfer |         1000 |        28 |    2.27606 |    0.293591  |             0.0447598   |               0.00259528  |
| WNA             | NWN             | graphwavenet_transfer |          183 |        36 |    2.3237  |    0.216945  |             0.0283388   |               0.00383457  |
| WNA             | SAU             | graphwavenet_transfer |          351 |        13 |    1.9369  |    0.231981  |             0.0574794   |               0.0148149   |
| WNA             | WCE             | graphwavenet_transfer |         1000 |        17 |    2.20702 |    0.294486  |             0.0573357   |               0.00413288  |
| WNA             | WNA             | graphwavenet_transfer |          975 |        17 |    1.93154 |    0.211714  |             0           |               0           |
