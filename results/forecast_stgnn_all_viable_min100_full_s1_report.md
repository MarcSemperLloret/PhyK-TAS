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
| CNA             | CNA             | stgcn_diffusion |          438 |        14 |    2.087   |    0.163195  |             0           |               0           |
| CNA             | EAS             | stgcn_diffusion |          110 |        16 |    6.94797 |    0.240682  |             0.745035    |               0.0137992   |
| CNA             | EAU             | stgcn_diffusion |          241 |         6 |    2.92219 |    0.211961  |             0.13085     |               0.00261906  |
| CNA             | ENA             | stgcn_diffusion |          522 |        21 |    3.1279  |    0.255139  |             0.0633677   |               0.00511299  |
| CNA             | MED             | stgcn_diffusion |          328 |        19 |    1.81176 |    0.179874  |             0.10199     |               0.011012    |
| CNA             | NCA             | stgcn_diffusion |          144 |         7 |    1.05125 |    0.0994961 |             0.0250245   |               0.00318648  |
| CNA             | NEU             | stgcn_diffusion |         1000 |        28 |    2.34404 |    0.311382  |             0.0998095   |               0.0191986   |
| CNA             | NWN             | stgcn_diffusion |          183 |        36 |    2.53433 |    0.248202  |             0.184426    |               0.0289377   |
| CNA             | SAU             | stgcn_diffusion |          351 |        13 |    1.95291 |    0.224341  |             0.0710189   |               0.00545841  |
| CNA             | WCE             | stgcn_diffusion |         1000 |        14 |    2.19882 |    0.298622  |             0.0665974   |               0.010531    |
| CNA             | WNA             | stgcn_diffusion |          975 |        17 |    2.08732 |    0.232497  |             0.121122    |               0.0160624   |
| EAS             | CNA             | stgcn_diffusion |          438 |        14 |    2.21069 |    0.189251  |             0.12368     |               0.0260568   |
| EAS             | EAS             | stgcn_diffusion |          110 |        16 |    6.20293 |    0.226883  |             0           |               0           |
| EAS             | EAU             | stgcn_diffusion |          241 |         6 |    2.82025 |    0.214902  |             0.028914    |               0.0055601   |
| EAS             | ENA             | stgcn_diffusion |          522 |        21 |    3.24825 |    0.28186   |             0.183724    |               0.031834    |
| EAS             | MED             | stgcn_diffusion |          328 |        19 |    1.72574 |    0.171462  |             0.0159779   |               0.00260032  |
| EAS             | NCA             | stgcn_diffusion |          144 |         7 |    1.03866 |    0.10039   |             0.0124404   |               0.00408035  |
| EAS             | NEU             | stgcn_diffusion |         1000 |        28 |    2.28649 |    0.295061  |             0.0422626   |               0.00287844  |
| EAS             | NWN             | stgcn_diffusion |          183 |        36 |    2.42    |    0.224891  |             0.0701027   |               0.00562635  |
| EAS             | SAU             | stgcn_diffusion |          351 |        13 |    1.90555 |    0.222948  |             0.0236555   |               0.00406529  |
| EAS             | WCE             | stgcn_diffusion |         1000 |        14 |    2.16751 |    0.288768  |             0.0352904   |               0.000676862 |
| EAS             | WNA             | stgcn_diffusion |          975 |        17 |    1.97618 |    0.219563  |             0.00998092  |               0.00312823  |
| EAU             | CNA             | stgcn_diffusion |          438 |        14 |    2.15927 |    0.175904  |             0.072267    |               0.0127096   |
| EAU             | EAS             | stgcn_diffusion |          110 |        16 |    6.17011 |    0.22672   |            -0.0328218   |              -0.00016329  |
| EAU             | EAU             | stgcn_diffusion |          241 |         6 |    2.79134 |    0.209342  |             0           |               0           |
| EAU             | ENA             | stgcn_diffusion |          522 |        21 |    3.18698 |    0.271702  |             0.122446    |               0.0216766   |
| EAU             | MED             | stgcn_diffusion |          328 |        19 |    1.71148 |    0.169321  |             0.00171219  |               0.000458926 |
| EAU             | NCA             | stgcn_diffusion |          144 |         7 |    1.02656 |    0.0961022 |             0.000337697 |              -0.000207474 |
| EAU             | NEU             | stgcn_diffusion |         1000 |        28 |    2.27508 |    0.298614  |             0.0308494   |               0.00643079  |
| EAU             | NWN             | stgcn_diffusion |          183 |        36 |    2.46708 |    0.235689  |             0.117173    |               0.0164247   |
| EAU             | SAU             | stgcn_diffusion |          351 |        13 |    1.88437 |    0.219537  |             0.00247433  |               0.000654225 |
| EAU             | WCE             | stgcn_diffusion |         1000 |        14 |    2.14322 |    0.288777  |             0.0109992   |               0.000685842 |
| EAU             | WNA             | stgcn_diffusion |          975 |        17 |    1.99107 |    0.223895  |             0.024865    |               0.00745992  |
| ENA             | CNA             | stgcn_diffusion |          438 |        14 |    2.09786 |    0.164421  |             0.0108596   |               0.00122645  |
| ENA             | EAS             | stgcn_diffusion |          110 |        16 |    6.3574  |    0.242748  |             0.15447     |               0.0158642   |
| ENA             | EAU             | stgcn_diffusion |          241 |         6 |    2.87037 |    0.216765  |             0.0790341   |               0.00742291  |
| ENA             | ENA             | stgcn_diffusion |          522 |        21 |    3.06453 |    0.250026  |             0           |               0           |
| ENA             | MED             | stgcn_diffusion |          328 |        19 |    1.75875 |    0.178772  |             0.0489863   |               0.00990992  |
| ENA             | NCA             | stgcn_diffusion |          144 |         7 |    1.0302  |    0.0976331 |             0.00398034  |               0.00132342  |
| ENA             | NEU             | stgcn_diffusion |         1000 |        28 |    2.32522 |    0.319944  |             0.0809931   |               0.0277613   |
| ENA             | NWN             | stgcn_diffusion |          183 |        36 |    2.5152  |    0.249274  |             0.165298    |               0.0300099   |
| ENA             | SAU             | stgcn_diffusion |          351 |        13 |    1.92571 |    0.229598  |             0.0438189   |               0.0107154   |
| ENA             | WCE             | stgcn_diffusion |         1000 |        14 |    2.17297 |    0.30499   |             0.0407407   |               0.0168985   |
| ENA             | WNA             | stgcn_diffusion |          975 |        17 |    2.04932 |    0.235592  |             0.0831236   |               0.0191573   |
| MED             | CNA             | stgcn_diffusion |          438 |        14 |    2.16447 |    0.178999  |             0.0774605   |               0.0158043   |
| MED             | EAS             | stgcn_diffusion |          110 |        16 |    6.15519 |    0.226352  |            -0.0477401   |              -0.000530899 |
| MED             | EAU             | stgcn_diffusion |          241 |         6 |    2.80177 |    0.210406  |             0.0104373   |               0.00106447  |
| MED             | ENA             | stgcn_diffusion |          522 |        21 |    3.18276 |    0.273236  |             0.118226    |               0.0232104   |
| MED             | MED             | stgcn_diffusion |          328 |        19 |    1.70977 |    0.168862  |             0           |               0           |
| MED             | NCA             | stgcn_diffusion |          144 |         7 |    1.02765 |    0.0968304 |             0.00143091  |               0.000520709 |
| MED             | NEU             | stgcn_diffusion |         1000 |        28 |    2.27552 |    0.298459  |             0.0312951   |               0.00627653  |
| MED             | NWN             | stgcn_diffusion |          183 |        36 |    2.47487 |    0.233768  |             0.12497     |               0.0145035   |
| MED             | SAU             | stgcn_diffusion |          351 |        13 |    1.88202 |    0.219466  |             0.000129453 |               0.000582948 |
| MED             | WCE             | stgcn_diffusion |         1000 |        14 |    2.13694 |    0.288996  |             0.00471607  |               0.000904771 |
| MED             | WNA             | stgcn_diffusion |          975 |        17 |    2.00161 |    0.223442  |             0.035405    |               0.00700679  |
| NCA             | CNA             | stgcn_diffusion |          438 |        14 |    2.15133 |    0.173631  |             0.0643289   |               0.0104362   |
| NCA             | EAS             | stgcn_diffusion |          110 |        16 |    6.19836 |    0.232083  |            -0.00457117  |               0.00519955  |
| NCA             | EAU             | stgcn_diffusion |          241 |         6 |    2.80087 |    0.209332  |             0.00953237  |              -9.80561e-06 |
| NCA             | ENA             | stgcn_diffusion |          522 |        21 |    3.17346 |    0.26743   |             0.108934    |               0.0174045   |
| NCA             | MED             | stgcn_diffusion |          328 |        19 |    1.71533 |    0.170024  |             0.00556233  |               0.00116265  |
| NCA             | NCA             | stgcn_diffusion |          144 |         7 |    1.02622 |    0.0963096 |             0           |               0           |
| NCA             | NEU             | stgcn_diffusion |         1000 |        28 |    2.3063  |    0.308231  |             0.0620738   |               0.016048    |
| NCA             | NWN             | stgcn_diffusion |          183 |        36 |    2.51389 |    0.24898   |             0.163989    |               0.0297159   |
| NCA             | SAU             | stgcn_diffusion |          351 |        13 |    1.89067 |    0.220286  |             0.00877604  |               0.00140311  |
| NCA             | WCE             | stgcn_diffusion |         1000 |        14 |    2.15494 |    0.293865  |             0.0227181   |               0.00577403  |
| NCA             | WNA             | stgcn_diffusion |          975 |        17 |    2.01709 |    0.231974  |             0.0508891   |               0.0155394   |
| NEU             | CNA             | stgcn_diffusion |          438 |        14 |    2.20879 |    0.193742  |             0.121788    |               0.030547    |
| NEU             | EAS             | stgcn_diffusion |          110 |        16 |    6.19345 |    0.228892  |            -0.00948034  |               0.00200823  |
| NEU             | EAU             | stgcn_diffusion |          241 |         6 |    2.82168 |    0.219724  |             0.030341    |               0.0103825   |
| NEU             | ENA             | stgcn_diffusion |          522 |        21 |    3.23102 |    0.290392  |             0.166494    |               0.0403663   |
| NEU             | MED             | stgcn_diffusion |          328 |        19 |    1.7261  |    0.175029  |             0.0163353   |               0.00616727  |
| NEU             | NCA             | stgcn_diffusion |          144 |         7 |    1.0496  |    0.10252   |             0.0233765   |               0.00621019  |
| NEU             | NEU             | stgcn_diffusion |         1000 |        28 |    2.24423 |    0.292183  |             0           |               0           |
| NEU             | NWN             | stgcn_diffusion |          183 |        36 |    2.42602 |    0.223     |             0.0761143   |               0.00373534  |
| NEU             | SAU             | stgcn_diffusion |          351 |        13 |    1.90449 |    0.229483  |             0.0225972   |               0.0106005   |
| NEU             | WCE             | stgcn_diffusion |         1000 |        14 |    2.14203 |    0.291156  |             0.00980363  |               0.00306476  |
| NEU             | WNA             | stgcn_diffusion |          975 |        17 |    1.99202 |    0.218482  |             0.0258153   |               0.00204751  |
| NWN             | CNA             | stgcn_diffusion |          438 |        14 |    2.32529 |    0.1946    |             0.238282    |               0.0314057   |
| NWN             | EAS             | stgcn_diffusion |          110 |        16 |    6.68525 |    0.228692  |             0.482311    |               0.00180876  |
| NWN             | EAU             | stgcn_diffusion |          241 |         6 |    2.96049 |    0.220783  |             0.169155    |               0.0114415   |
| NWN             | ENA             | stgcn_diffusion |          522 |        21 |    3.42143 |    0.282595  |             0.356902    |               0.0325696   |
| NWN             | MED             | stgcn_diffusion |          328 |        19 |    1.80185 |    0.176229  |             0.0920833   |               0.00736728  |
| NWN             | NCA             | stgcn_diffusion |          144 |         7 |    1.07322 |    0.103901  |             0.0470021   |               0.007591    |
| NWN             | NEU             | stgcn_diffusion |         1000 |        28 |    2.37005 |    0.292861  |             0.125826    |               0.000677875 |
| NWN             | NWN             | stgcn_diffusion |          183 |        36 |    2.3499  |    0.219264  |             0           |               0           |
| NWN             | SAU             | stgcn_diffusion |          351 |        13 |    2.01201 |    0.228646  |             0.130118    |               0.00976334  |
| NWN             | WCE             | stgcn_diffusion |         1000 |        14 |    2.27303 |    0.289872  |             0.140803    |               0.00178092  |
| NWN             | WNA             | stgcn_diffusion |          975 |        17 |    1.98579 |    0.216444  |             0.0195863   |               9.43747e-06 |
| SAU             | CNA             | stgcn_diffusion |          438 |        14 |    2.17203 |    0.181566  |             0.085021    |               0.018371    |
| SAU             | EAS             | stgcn_diffusion |          110 |        16 |    6.16313 |    0.225661  |            -0.0398002   |              -0.00122204  |
| SAU             | EAU             | stgcn_diffusion |          241 |         6 |    2.80716 |    0.210887  |             0.0158222   |               0.00154551  |
| SAU             | ENA             | stgcn_diffusion |          522 |        21 |    3.18893 |    0.275482  |             0.124404    |               0.0254562   |
| SAU             | MED             | stgcn_diffusion |          328 |        19 |    1.71071 |    0.168911  |             0.000945651 |               4.953e-05   |
| SAU             | NCA             | stgcn_diffusion |          144 |         7 |    1.03118 |    0.0974233 |             0.00496014  |               0.00111361  |
| SAU             | NEU             | stgcn_diffusion |         1000 |        28 |    2.2783  |    0.299927  |             0.0340681   |               0.00774422  |
| SAU             | NWN             | stgcn_diffusion |          183 |        36 |    2.47996 |    0.233172  |             0.130063    |               0.0139072   |
| SAU             | SAU             | stgcn_diffusion |          351 |        13 |    1.88189 |    0.218883  |             0           |               0           |
| SAU             | WCE             | stgcn_diffusion |         1000 |        14 |    2.1375  |    0.289647  |             0.00527636  |               0.00155587  |
| SAU             | WNA             | stgcn_diffusion |          975 |        17 |    2.0087  |    0.224325  |             0.0424978   |               0.00789007  |
| WCE             | CNA             | stgcn_diffusion |          438 |        14 |    2.18428 |    0.184352  |             0.0972737   |               0.0211579   |
| WCE             | EAS             | stgcn_diffusion |          110 |        16 |    6.19698 |    0.227233  |            -0.0059573   |               0.000349293 |
| WCE             | EAU             | stgcn_diffusion |          241 |         6 |    2.82538 |    0.214346  |             0.0340483   |               0.00500428  |
| WCE             | ENA             | stgcn_diffusion |          522 |        21 |    3.19328 |    0.277784  |             0.128748    |               0.0277584   |
| WCE             | MED             | stgcn_diffusion |          328 |        19 |    1.72231 |    0.170886  |             0.0125491   |               0.00202473  |
| WCE             | NCA             | stgcn_diffusion |          144 |         7 |    1.04323 |    0.0985307 |             0.0170096   |               0.00222108  |
| WCE             | NEU             | stgcn_diffusion |         1000 |        28 |    2.26417 |    0.293761  |             0.0199373   |               0.00157775  |
| WCE             | NWN             | stgcn_diffusion |          183 |        36 |    2.49059 |    0.227768  |             0.140688    |               0.00850398  |
| WCE             | SAU             | stgcn_diffusion |          351 |        13 |    1.89199 |    0.223071  |             0.0100959   |               0.00418839  |
| WCE             | WCE             | stgcn_diffusion |         1000 |        14 |    2.13222 |    0.288091  |             0           |               0           |
| WCE             | WNA             | stgcn_diffusion |          975 |        17 |    2.0208  |    0.219856  |             0.0546018   |               0.00342103  |
| WNA             | CNA             | stgcn_diffusion |          438 |        14 |    2.21454 |    0.193068  |             0.127533    |               0.0298732   |
| WNA             | EAS             | stgcn_diffusion |          110 |        16 |    6.1338  |    0.230534  |            -0.0691345   |               0.00365116  |
| WNA             | EAU             | stgcn_diffusion |          241 |         6 |    2.83583 |    0.220886  |             0.0444993   |               0.0115445   |
| WNA             | ENA             | stgcn_diffusion |          522 |        21 |    3.25345 |    0.283227  |             0.18892     |               0.0332013   |
| WNA             | MED             | stgcn_diffusion |          328 |        19 |    1.73697 |    0.176639  |             0.0272027   |               0.00777764  |
| WNA             | NCA             | stgcn_diffusion |          144 |         7 |    1.03877 |    0.101569  |             0.0125525   |               0.00525981  |
| WNA             | NEU             | stgcn_diffusion |         1000 |        28 |    2.28829 |    0.293033  |             0.0440578   |               0.000850385 |
| WNA             | NWN             | stgcn_diffusion |          183 |        36 |    2.39977 |    0.221332  |             0.0498639   |               0.00206779  |
| WNA             | SAU             | stgcn_diffusion |          351 |        13 |    1.92942 |    0.232046  |             0.0475261   |               0.0131631   |
| WNA             | WCE             | stgcn_diffusion |         1000 |        14 |    2.19068 |    0.292344  |             0.0584507   |               0.00425219  |
| WNA             | WNA             | stgcn_diffusion |          975 |        17 |    1.9662  |    0.216435  |             0           |               0           |
