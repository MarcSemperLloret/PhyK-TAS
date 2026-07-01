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
| CNA             | CNA             | graphwavenet_transfer |          438 |        14 |    1.97953 |    0.149319  |              0          |               0           |
| CNA             | EAS             | graphwavenet_transfer |          110 |        16 |    6.23956 |    0.238834  |              0.0397943  |               0.0139257   |
| CNA             | EAU             | graphwavenet_transfer |          241 |         6 |    2.81626 |    0.209307  |              0.0198429  |               0.000605244 |
| CNA             | ENA             | graphwavenet_transfer |          522 |        21 |    2.9592  |    0.236853  |              0.0407596  |               0.00524148  |
| CNA             | MED             | graphwavenet_transfer |          328 |        19 |    1.75391 |    0.173879  |              0.0455082  |               0.00455445  |
| CNA             | NCA             | graphwavenet_transfer |          144 |         7 |    1.00986 |    0.094073  |             -0.00852295 |               0.000117149 |
| CNA             | NEU             | graphwavenet_transfer |         1000 |        29 |    2.32001 |    0.310249  |              0.142859   |               0.0194789   |
| CNA             | NWN             | graphwavenet_transfer |          183 |        36 |    2.48483 |    0.248345  |              0.186263   |               0.0359388   |
| CNA             | SAU             | graphwavenet_transfer |          351 |        13 |    1.91464 |    0.22196   |              0.0401159  |               0.00522269  |
| CNA             | WCE             | graphwavenet_transfer |         1000 |        15 |    2.20299 |    0.298841  |              0.0961149  |               0.00991884  |
| CNA             | WNA             | graphwavenet_transfer |          975 |        17 |    2.01057 |    0.232406  |              0.0806262  |               0.0217913   |
| EAS             | CNA             | graphwavenet_transfer |          438 |        14 |    2.19947 |    0.185064  |              0.219938   |               0.0357451   |
| EAS             | EAS             | graphwavenet_transfer |          110 |        16 |    6.19977 |    0.224908  |              0          |               0           |
| EAS             | EAU             | graphwavenet_transfer |          241 |         6 |    2.8131  |    0.211034  |              0.0166839  |               0.0023326   |
| EAS             | ENA             | graphwavenet_transfer |          522 |        21 |    3.24522 |    0.280064  |              0.326777   |               0.0484524   |
| EAS             | MED             | graphwavenet_transfer |          328 |        19 |    1.72141 |    0.170539  |              0.0130051  |               0.00121512  |
| EAS             | NCA             | graphwavenet_transfer |          144 |         7 |    1.03362 |    0.0986344 |              0.0152324  |               0.00467853  |
| EAS             | NEU             | graphwavenet_transfer |         1000 |        29 |    2.26225 |    0.297537  |              0.0850952  |               0.00676682  |
| EAS             | NWN             | graphwavenet_transfer |          183 |        36 |    2.38989 |    0.222015  |              0.0913231  |               0.00960855  |
| EAS             | SAU             | graphwavenet_transfer |          351 |        13 |    1.90295 |    0.219644  |              0.0284262  |               0.00290697  |
| EAS             | WCE             | graphwavenet_transfer |         1000 |        15 |    2.1739  |    0.290509  |              0.0670217  |               0.00158692  |
| EAS             | WNA             | graphwavenet_transfer |          975 |        17 |    1.97545 |    0.220317  |              0.0455081  |               0.00970303  |
| EAU             | CNA             | graphwavenet_transfer |          438 |        14 |    2.16135 |    0.176995  |              0.181817   |               0.0276767   |
| EAU             | EAS             | graphwavenet_transfer |          110 |        16 |    6.14407 |    0.228877  |             -0.0557014  |               0.00396879  |
| EAU             | EAU             | graphwavenet_transfer |          241 |         6 |    2.79641 |    0.208702  |              0          |               0           |
| EAU             | ENA             | graphwavenet_transfer |          522 |        21 |    3.18813 |    0.271643  |              0.269683   |               0.0400313   |
| EAU             | MED             | graphwavenet_transfer |          328 |        19 |    1.71015 |    0.168807  |              0.00174697 |              -0.000517619 |
| EAU             | NCA             | graphwavenet_transfer |          144 |         7 |    1.02654 |    0.0968149 |              0.00815359 |               0.00285911  |
| EAU             | NEU             | graphwavenet_transfer |         1000 |        29 |    2.21282 |    0.29824   |              0.0356654  |               0.00746946  |
| EAU             | NWN             | graphwavenet_transfer |          183 |        36 |    2.46051 |    0.230818  |              0.161944   |               0.0184118   |
| EAU             | SAU             | graphwavenet_transfer |          351 |        13 |    1.87742 |    0.216985  |              0.0028965  |               0.000247619 |
| EAU             | WCE             | graphwavenet_transfer |         1000 |        15 |    2.12384 |    0.291581  |              0.0169608  |               0.00265895  |
| EAU             | WNA             | graphwavenet_transfer |          975 |        17 |    1.99806 |    0.224433  |              0.0681149  |               0.0138188   |
| ENA             | CNA             | graphwavenet_transfer |          438 |        14 |    1.99971 |    0.150629  |              0.0201778  |               0.00130995  |
| ENA             | EAS             | graphwavenet_transfer |          110 |        16 |    6.32429 |    0.270604  |              0.124526   |               0.0456956   |
| ENA             | EAU             | graphwavenet_transfer |          241 |         6 |    2.83946 |    0.218569  |              0.0430458  |               0.00986748  |
| ENA             | ENA             | graphwavenet_transfer |          522 |        21 |    2.91844 |    0.231611  |              0          |               0           |
| ENA             | MED             | graphwavenet_transfer |          328 |        19 |    1.73562 |    0.176004  |              0.027212   |               0.00667979  |
| ENA             | NCA             | graphwavenet_transfer |          144 |         7 |    1.00332 |    0.0928133 |             -0.0150645  |              -0.00114254  |
| ENA             | NEU             | graphwavenet_transfer |         1000 |        29 |    2.27983 |    0.328259  |              0.102678   |               0.0374886   |
| ENA             | NWN             | graphwavenet_transfer |          183 |        36 |    2.46447 |    0.244445  |              0.165908   |               0.0320389   |
| ENA             | SAU             | graphwavenet_transfer |          351 |        13 |    1.91034 |    0.229094  |              0.0358212  |               0.0123563   |
| ENA             | WCE             | graphwavenet_transfer |         1000 |        15 |    2.16421 |    0.309256  |              0.0573301  |               0.0203337   |
| ENA             | WNA             | graphwavenet_transfer |          975 |        17 |    2.01519 |    0.236769  |              0.0852494  |               0.0261545   |
| MED             | CNA             | graphwavenet_transfer |          438 |        14 |    2.17127 |    0.182242  |              0.191746   |               0.0329231   |
| MED             | EAS             | graphwavenet_transfer |          110 |        16 |    6.14406 |    0.224859  |             -0.0557108  |              -4.86605e-05 |
| MED             | EAU             | graphwavenet_transfer |          241 |         6 |    2.80284 |    0.210621  |              0.00643003 |               0.0019187   |
| MED             | ENA             | graphwavenet_transfer |          522 |        21 |    3.18794 |    0.274661  |              0.2695     |               0.0430497   |
| MED             | MED             | graphwavenet_transfer |          328 |        19 |    1.70841 |    0.169324  |              0          |               0           |
| MED             | NCA             | graphwavenet_transfer |          144 |         7 |    1.02648 |    0.0967294 |              0.00809136 |               0.00277358  |
| MED             | NEU             | graphwavenet_transfer |         1000 |        29 |    2.19685 |    0.294607  |              0.0197008  |               0.00383737  |
| MED             | NWN             | graphwavenet_transfer |          183 |        36 |    2.43174 |    0.222549  |              0.13318    |               0.0101424   |
| MED             | SAU             | graphwavenet_transfer |          351 |        13 |    1.87635 |    0.2185    |              0.00183255 |               0.00176276  |
| MED             | WCE             | graphwavenet_transfer |         1000 |        15 |    2.11431 |    0.289185  |              0.00742988 |               0.000262177 |
| MED             | WNA             | graphwavenet_transfer |          975 |        17 |    1.98066 |    0.218444  |              0.050719   |               0.00783018  |
| NCA             | CNA             | graphwavenet_transfer |          438 |        14 |    2.13969 |    0.169649  |              0.16016    |               0.0203304   |
| NCA             | EAS             | graphwavenet_transfer |          110 |        16 |    6.20742 |    0.229482  |              0.00765274 |               0.00457415  |
| NCA             | EAU             | graphwavenet_transfer |          241 |         6 |    2.81375 |    0.210294  |              0.0173341  |               0.00159187  |
| NCA             | ENA             | graphwavenet_transfer |          522 |        21 |    3.14776 |    0.257623  |              0.229319   |               0.0260115   |
| NCA             | MED             | graphwavenet_transfer |          328 |        19 |    1.73791 |    0.170654  |              0.0295017  |               0.00132981  |
| NCA             | NCA             | graphwavenet_transfer |          144 |         7 |    1.01838 |    0.0939558 |              0          |               0           |
| NCA             | NEU             | graphwavenet_transfer |         1000 |        29 |    2.33286 |    0.29852   |              0.15571    |               0.00774952  |
| NCA             | NWN             | graphwavenet_transfer |          183 |        36 |    2.40394 |    0.225302  |              0.105381   |               0.0128959   |
| NCA             | SAU             | graphwavenet_transfer |          351 |        13 |    1.91781 |    0.218462  |              0.0432887  |               0.00172457  |
| NCA             | WCE             | graphwavenet_transfer |         1000 |        15 |    2.23376 |    0.292196  |              0.126879   |               0.00327315  |
| NCA             | WNA             | graphwavenet_transfer |          975 |        17 |    1.97739 |    0.219072  |              0.0474487  |               0.00845809  |
| NEU             | CNA             | graphwavenet_transfer |          438 |        14 |    2.1942  |    0.189889  |              0.214673   |               0.0405699   |
| NEU             | EAS             | graphwavenet_transfer |          110 |        16 |    6.16186 |    0.227423  |             -0.0379037  |               0.00251526  |
| NEU             | EAU             | graphwavenet_transfer |          241 |         6 |    2.81642 |    0.215816  |              0.0200018  |               0.00711461  |
| NEU             | ENA             | graphwavenet_transfer |          522 |        21 |    3.20846 |    0.284658  |              0.290019   |               0.0530463   |
| NEU             | MED             | graphwavenet_transfer |          328 |        19 |    1.71511 |    0.171222  |              0.00670451 |               0.00189804  |
| NEU             | NCA             | graphwavenet_transfer |          144 |         7 |    1.04018 |    0.100202  |              0.0217942  |               0.00624657  |
| NEU             | NEU             | graphwavenet_transfer |         1000 |        29 |    2.17715 |    0.29077   |              0          |               0           |
| NEU             | NWN             | graphwavenet_transfer |          183 |        36 |    2.40405 |    0.217348  |              0.105485   |               0.00494151  |
| NEU             | SAU             | graphwavenet_transfer |          351 |        13 |    1.88614 |    0.221106  |              0.0116197  |               0.00436894  |
| NEU             | WCE             | graphwavenet_transfer |         1000 |        15 |    2.10902 |    0.289633  |              0.0021399  |               0.000710496 |
| NEU             | WNA             | graphwavenet_transfer |          975 |        17 |    1.97992 |    0.215175  |              0.0499777  |               0.00456129  |
| NWN             | CNA             | graphwavenet_transfer |          438 |        14 |    2.18587 |    0.178848  |              0.20634    |               0.0295297   |
| NWN             | EAS             | graphwavenet_transfer |          110 |        16 |    6.2169  |    0.228891  |              0.0171311  |               0.00398307  |
| NWN             | EAU             | graphwavenet_transfer |          241 |         6 |    2.84776 |    0.215684  |              0.051343   |               0.00698256  |
| NWN             | ENA             | graphwavenet_transfer |          522 |        21 |    3.17018 |    0.262685  |              0.251737   |               0.0310733   |
| NWN             | MED             | graphwavenet_transfer |          328 |        19 |    1.73254 |    0.17203   |              0.0241308  |               0.00270563  |
| NWN             | NCA             | graphwavenet_transfer |          144 |         7 |    1.03272 |    0.0976369 |              0.0143333  |               0.00368106  |
| NWN             | NEU             | graphwavenet_transfer |         1000 |        29 |    2.21121 |    0.294605  |              0.0340536  |               0.0038348   |
| NWN             | NWN             | graphwavenet_transfer |          183 |        36 |    2.29856 |    0.212407  |              0          |               0           |
| NWN             | SAU             | graphwavenet_transfer |          351 |        13 |    1.90795 |    0.220786  |              0.033427   |               0.00404892  |
| NWN             | WCE             | graphwavenet_transfer |         1000 |        15 |    2.14883 |    0.293279  |              0.0419493  |               0.00435636  |
| NWN             | WNA             | graphwavenet_transfer |          975 |        17 |    1.94099 |    0.214724  |              0.0110489  |               0.00410959  |
| SAU             | CNA             | graphwavenet_transfer |          438 |        14 |    2.16585 |    0.179299  |              0.186324   |               0.0299805   |
| SAU             | EAS             | graphwavenet_transfer |          110 |        16 |    6.18877 |    0.225394  |             -0.0109953  |               0.000486175 |
| SAU             | EAU             | graphwavenet_transfer |          241 |         6 |    2.81068 |    0.209122  |              0.0142699  |               0.00041996  |
| SAU             | ENA             | graphwavenet_transfer |          522 |        21 |    3.18002 |    0.272526  |              0.261576   |               0.0409149   |
| SAU             | MED             | graphwavenet_transfer |          328 |        19 |    1.71116 |    0.169086  |              0.00275275 |              -0.000238156 |
| SAU             | NCA             | graphwavenet_transfer |          144 |         7 |    1.02816 |    0.096525  |              0.00977454 |               0.00256912  |
| SAU             | NEU             | graphwavenet_transfer |         1000 |        29 |    2.20112 |    0.296447  |              0.0239637  |               0.00567677  |
| SAU             | NWN             | graphwavenet_transfer |          183 |        36 |    2.45349 |    0.224754  |              0.154931   |               0.0123476   |
| SAU             | SAU             | graphwavenet_transfer |          351 |        13 |    1.87452 |    0.216737  |              0          |               0           |
| SAU             | WCE             | graphwavenet_transfer |         1000 |        15 |    2.11367 |    0.29056   |              0.00678794 |               0.00163767  |
| SAU             | WNA             | graphwavenet_transfer |          975 |        17 |    2.00247 |    0.221412  |              0.0725307  |               0.0107982   |
| WCE             | CNA             | graphwavenet_transfer |          438 |        14 |    2.17982 |    0.185517  |              0.200292   |               0.0361984   |
| WCE             | EAS             | graphwavenet_transfer |          110 |        16 |    6.19143 |    0.227539  |             -0.00833573 |               0.00263047  |
| WCE             | EAU             | graphwavenet_transfer |          241 |         6 |    2.81667 |    0.212656  |              0.0202545  |               0.00395388  |
| WCE             | ENA             | graphwavenet_transfer |          522 |        21 |    3.19314 |    0.279929  |              0.274701   |               0.0483171   |
| WCE             | MED             | graphwavenet_transfer |          328 |        19 |    1.7133  |    0.170071  |              0.00489173 |               0.000746712 |
| WCE             | NCA             | graphwavenet_transfer |          144 |         7 |    1.03353 |    0.0985317 |              0.0151444  |               0.00457585  |
| WCE             | NEU             | graphwavenet_transfer |         1000 |        29 |    2.1921  |    0.292358  |              0.0149425  |               0.00158811  |
| WCE             | NWN             | graphwavenet_transfer |          183 |        36 |    2.46558 |    0.22468   |              0.167015   |               0.0122731   |
| WCE             | SAU             | graphwavenet_transfer |          351 |        13 |    1.88413 |    0.221307  |              0.00961141 |               0.00456937  |
| WCE             | WCE             | graphwavenet_transfer |         1000 |        15 |    2.10688 |    0.288922  |              0          |               0           |
| WCE             | WNA             | graphwavenet_transfer |          975 |        17 |    2.00565 |    0.21872   |              0.0757122  |               0.00810572  |
| WNA             | CNA             | graphwavenet_transfer |          438 |        14 |    2.16567 |    0.176181  |              0.186141   |               0.0268626   |
| WNA             | EAS             | graphwavenet_transfer |          110 |        16 |    6.15005 |    0.227688  |             -0.049721   |               0.00278032  |
| WNA             | EAU             | graphwavenet_transfer |          241 |         6 |    2.81329 |    0.213208  |              0.0168777  |               0.00450594  |
| WNA             | ENA             | graphwavenet_transfer |          522 |        21 |    3.17224 |    0.265158  |              0.2538     |               0.0335461   |
| WNA             | MED             | graphwavenet_transfer |          328 |        19 |    1.72196 |    0.171033  |              0.0135518  |               0.00170884  |
| WNA             | NCA             | graphwavenet_transfer |          144 |         7 |    1.0222  |    0.0955215 |              0.00381255 |               0.00156562  |
| WNA             | NEU             | graphwavenet_transfer |         1000 |        29 |    2.20888 |    0.292035  |              0.031727   |               0.00126536  |
| WNA             | NWN             | graphwavenet_transfer |          183 |        36 |    2.33601 |    0.214978  |              0.0374461  |               0.00257168  |
| WNA             | SAU             | graphwavenet_transfer |          351 |        13 |    1.90376 |    0.224642  |              0.0292385  |               0.00790425  |
| WNA             | WCE             | graphwavenet_transfer |         1000 |        15 |    2.14811 |    0.29226   |              0.0412262  |               0.00333781  |
| WNA             | WNA             | graphwavenet_transfer |          975 |        17 |    1.92994 |    0.210614  |              0          |               0           |
