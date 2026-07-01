# KBS comparison on forecasting models

Target:

- `mae_out_minus_in` from forecast station-metric files.
- Only out-of-region rows.

Forecast models:

- `linear_window`
- `patchtst_small`
- `regional_doy_climatology`
- `spatial_knn_ridge`
- `stgcn_diffusion`
- `graphwavenet_transfer`

Feature sets:

- physical knowledge;
- generic shift;
- physical plus shift.

## Forecast degradation summary

| model                    | source_region   | target_region   |    n |   mean_degradation |
|:-------------------------|:----------------|:----------------|-----:|-------------------:|
| graphwavenet_transfer    | CNA             | EAS             |  110 |        0.142258    |
| graphwavenet_transfer    | CNA             | EAU             |  241 |        0.0221183   |
| graphwavenet_transfer    | CNA             | ENA             |  522 |        0.0249174   |
| graphwavenet_transfer    | CNA             | MED             |  328 |        0.0293285   |
| graphwavenet_transfer    | CNA             | NCA             |  144 |       -0.00407786  |
| graphwavenet_transfer    | CNA             | NEU             | 1000 |        0.0903934   |
| graphwavenet_transfer    | CNA             | NWN             |  183 |        0.194374    |
| graphwavenet_transfer    | CNA             | SAU             |  351 |        0.025747    |
| graphwavenet_transfer    | CNA             | WCE             | 1000 |        0.0485638   |
| graphwavenet_transfer    | CNA             | WNA             |  975 |        0.0805062   |
| graphwavenet_transfer    | EAS             | CNA             |  438 |        0.218494    |
| graphwavenet_transfer    | EAS             | EAU             |  241 |        0.0198955   |
| graphwavenet_transfer    | EAS             | ENA             |  522 |        0.295062    |
| graphwavenet_transfer    | EAS             | MED             |  328 |        0.00415841  |
| graphwavenet_transfer    | EAS             | NCA             |  144 |        0.0204307   |
| graphwavenet_transfer    | EAS             | NEU             | 1000 |        0.0419349   |
| graphwavenet_transfer    | EAS             | NWN             |  183 |        0.11925     |
| graphwavenet_transfer    | EAS             | SAU             |  351 |        0.0100316   |
| graphwavenet_transfer    | EAS             | WCE             | 1000 |        0.026549    |
| graphwavenet_transfer    | EAS             | WNA             |  975 |        0.0473754   |
| graphwavenet_transfer    | EAU             | CNA             |  438 |        0.179879    |
| graphwavenet_transfer    | EAU             | EAS             |  110 |        0.0181392   |
| graphwavenet_transfer    | EAU             | ENA             |  522 |        0.256429    |
| graphwavenet_transfer    | EAU             | MED             |  328 |        0.000191321 |
| graphwavenet_transfer    | EAU             | NCA             |  144 |        0.0114519   |
| graphwavenet_transfer    | EAU             | NEU             | 1000 |        0.0314521   |
| graphwavenet_transfer    | EAU             | NWN             |  183 |        0.169414    |
| graphwavenet_transfer    | EAU             | SAU             |  351 |       -0.000607337 |
| graphwavenet_transfer    | EAU             | WCE             | 1000 |        0.00713133  |
| graphwavenet_transfer    | EAU             | WNA             |  975 |        0.0657372   |
| graphwavenet_transfer    | ENA             | CNA             |  438 |        0.0155742   |
| graphwavenet_transfer    | ENA             | EAS             |  110 |        0.186355    |
| graphwavenet_transfer    | ENA             | EAU             |  241 |        0.0480359   |
| graphwavenet_transfer    | ENA             | MED             |  328 |        0.0484023   |
| graphwavenet_transfer    | ENA             | NCA             |  144 |        0.00976632  |
| graphwavenet_transfer    | ENA             | NEU             | 1000 |        0.107393    |
| graphwavenet_transfer    | ENA             | NWN             |  183 |        0.15924     |
| graphwavenet_transfer    | ENA             | SAU             |  351 |        0.042441    |
| graphwavenet_transfer    | ENA             | WCE             | 1000 |        0.0663757   |
| graphwavenet_transfer    | ENA             | WNA             |  975 |        0.0867844   |
| graphwavenet_transfer    | MED             | CNA             |  438 |        0.205147    |
| graphwavenet_transfer    | MED             | EAS             |  110 |        0.00102069  |
| graphwavenet_transfer    | MED             | EAU             |  241 |        0.0131358   |
| graphwavenet_transfer    | MED             | ENA             |  522 |        0.276723    |
| graphwavenet_transfer    | MED             | NCA             |  144 |        0.0144921   |
| graphwavenet_transfer    | MED             | NEU             | 1000 |        0.0133277   |
| graphwavenet_transfer    | MED             | NWN             |  183 |        0.115413    |
| graphwavenet_transfer    | MED             | SAU             |  351 |        0.00138747  |
| graphwavenet_transfer    | MED             | WCE             | 1000 |        0.00633882  |
| graphwavenet_transfer    | MED             | WNA             |  975 |        0.0381267   |
| graphwavenet_transfer    | NCA             | CNA             |  438 |        0.13176     |
| graphwavenet_transfer    | NCA             | EAS             |  110 |        0.110882    |
| graphwavenet_transfer    | NCA             | EAU             |  241 |        0.0278719   |
| graphwavenet_transfer    | NCA             | ENA             |  522 |        0.152569    |
| graphwavenet_transfer    | NCA             | MED             |  328 |        0.028154    |
| graphwavenet_transfer    | NCA             | NEU             | 1000 |        0.114621    |
| graphwavenet_transfer    | NCA             | NWN             |  183 |        0.127529    |
| graphwavenet_transfer    | NCA             | SAU             |  351 |        0.0390366   |
| graphwavenet_transfer    | NCA             | WCE             | 1000 |        0.0864203   |
| graphwavenet_transfer    | NCA             | WNA             |  975 |        0.0626399   |
| graphwavenet_transfer    | NEU             | CNA             |  438 |        0.218438    |
| graphwavenet_transfer    | NEU             | EAS             |  110 |        0.0439322   |
| graphwavenet_transfer    | NEU             | EAU             |  241 |        0.0293135   |
| graphwavenet_transfer    | NEU             | ENA             |  522 |        0.280926    |
| graphwavenet_transfer    | NEU             | MED             |  328 |        0.00757952  |
| graphwavenet_transfer    | NEU             | NCA             |  144 |        0.0290484   |
| graphwavenet_transfer    | NEU             | NWN             |  183 |        0.134216    |
| graphwavenet_transfer    | NEU             | SAU             |  351 |        0.0131449   |
| graphwavenet_transfer    | NEU             | WCE             | 1000 |       -0.00326382  |
| graphwavenet_transfer    | NEU             | WNA             |  975 |        0.062998    |
| graphwavenet_transfer    | NWN             | CNA             |  438 |        0.239194    |
| graphwavenet_transfer    | NWN             | EAS             |  110 |        0.0864821   |
| graphwavenet_transfer    | NWN             | EAU             |  241 |        0.0689385   |
| graphwavenet_transfer    | NWN             | ENA             |  522 |        0.275216    |
| graphwavenet_transfer    | NWN             | MED             |  328 |        0.0293063   |
| graphwavenet_transfer    | NWN             | NCA             |  144 |        0.0271865   |
| graphwavenet_transfer    | NWN             | NEU             | 1000 |        0.0335267   |
| graphwavenet_transfer    | NWN             | SAU             |  351 |        0.0387904   |
| graphwavenet_transfer    | NWN             | WCE             | 1000 |        0.0418292   |
| graphwavenet_transfer    | NWN             | WNA             |  975 |        0.00944037  |
| graphwavenet_transfer    | SAU             | CNA             |  438 |        0.193222    |
| graphwavenet_transfer    | SAU             | EAS             |  110 |        0.0631007   |
| graphwavenet_transfer    | SAU             | EAU             |  241 |        0.0214509   |
| graphwavenet_transfer    | SAU             | ENA             |  522 |        0.258446    |
| graphwavenet_transfer    | SAU             | MED             |  328 |        0.000435791 |
| graphwavenet_transfer    | SAU             | NCA             |  144 |        0.0171844   |
| graphwavenet_transfer    | SAU             | NEU             | 1000 |        0.0241744   |
| graphwavenet_transfer    | SAU             | NWN             |  183 |        0.171135    |
| graphwavenet_transfer    | SAU             | WCE             | 1000 |        0.00392768  |
| graphwavenet_transfer    | SAU             | WNA             |  975 |        0.0765832   |
| graphwavenet_transfer    | WCE             | CNA             |  438 |        0.196138    |
| graphwavenet_transfer    | WCE             | EAS             |  110 |        0.0910634   |
| graphwavenet_transfer    | WCE             | EAU             |  241 |        0.0308289   |
| graphwavenet_transfer    | WCE             | ENA             |  522 |        0.256554    |
| graphwavenet_transfer    | WCE             | MED             |  328 |        0.00477658  |
| graphwavenet_transfer    | WCE             | NCA             |  144 |        0.0179316   |
| graphwavenet_transfer    | WCE             | NEU             | 1000 |        0.0329577   |
| graphwavenet_transfer    | WCE             | NWN             |  183 |        0.204792    |
| graphwavenet_transfer    | WCE             | SAU             |  351 |        0.00623398  |
| graphwavenet_transfer    | WCE             | WNA             |  975 |        0.0910263   |
| graphwavenet_transfer    | WNA             | CNA             |  438 |        0.20624     |
| graphwavenet_transfer    | WNA             | EAS             |  110 |        0.0571863   |
| graphwavenet_transfer    | WNA             | EAU             |  241 |        0.0570885   |
| graphwavenet_transfer    | WNA             | ENA             |  522 |        0.253315    |
| graphwavenet_transfer    | WNA             | MED             |  328 |        0.0328896   |
| graphwavenet_transfer    | WNA             | NCA             |  144 |        0.0112409   |
| graphwavenet_transfer    | WNA             | NEU             | 1000 |        0.0447598   |
| graphwavenet_transfer    | WNA             | NWN             |  183 |        0.0283388   |
| graphwavenet_transfer    | WNA             | SAU             |  351 |        0.0574794   |
| graphwavenet_transfer    | WNA             | WCE             | 1000 |        0.0573357   |
| linear_window            | CNA             | EAS             |  110 |        0.0552522   |
| linear_window            | CNA             | EAU             |  241 |       -0.0202326   |
| linear_window            | CNA             | ENA             |  522 |        0.028349    |
| linear_window            | CNA             | MED             |  328 |        0.032695    |
| linear_window            | CNA             | NCA             |  144 |        0.0318041   |
| linear_window            | CNA             | NEU             | 1000 |        0.156531    |
| linear_window            | CNA             | NWN             |  183 |        0.227118    |
| linear_window            | CNA             | SAU             |  351 |        0.0403544   |
| linear_window            | CNA             | WCE             | 1000 |        0.0389814   |
| linear_window            | CNA             | WNA             |  975 |       -0.0036185   |
| linear_window            | EAS             | CNA             |  438 |       -0.00722104  |
| linear_window            | EAS             | EAU             |  241 |       -0.0400065   |
| linear_window            | EAS             | ENA             |  522 |        0.00648771  |
| linear_window            | EAS             | MED             |  328 |       -0.028652    |
| linear_window            | EAS             | NCA             |  144 |        0.112793    |
| linear_window            | EAS             | NEU             | 1000 |       -0.00511037  |
| linear_window            | EAS             | NWN             |  183 |        0.0565183   |
| linear_window            | EAS             | SAU             |  351 |        0.0226588   |
| linear_window            | EAS             | WCE             | 1000 |       -0.0467047   |
| linear_window            | EAS             | WNA             |  975 |       -0.0451073   |
| linear_window            | EAU             | CNA             |  438 |        0.0707901   |
| linear_window            | EAU             | EAS             |  110 |        0.923175    |
| linear_window            | EAU             | ENA             |  522 |        0.00489099  |
| linear_window            | EAU             | MED             |  328 |       -0.0448011   |
| linear_window            | EAU             | NCA             |  144 |       -0.119823    |
| linear_window            | EAU             | NEU             | 1000 |        0.033847    |
| linear_window            | EAU             | NWN             |  183 |       -0.0182825   |
| linear_window            | EAU             | SAU             |  351 |       -0.061656    |
| linear_window            | EAU             | WCE             | 1000 |       -0.0262783   |
| linear_window            | EAU             | WNA             |  975 |       -0.00950709  |
| linear_window            | ENA             | CNA             |  438 |        0.0285817   |
| linear_window            | ENA             | EAS             |  110 |        0.863701    |
| linear_window            | ENA             | EAU             |  241 |        0.145315    |
| linear_window            | ENA             | MED             |  328 |       -0.081326    |
| linear_window            | ENA             | NCA             |  144 |        0.0973897   |
| linear_window            | ENA             | NEU             | 1000 |        0.181534    |
| linear_window            | ENA             | NWN             |  183 |       -0.0183888   |
| linear_window            | ENA             | SAU             |  351 |       -0.102531    |
| linear_window            | ENA             | WCE             | 1000 |        0.0648546   |
| linear_window            | ENA             | WNA             |  975 |        0.0343064   |
| linear_window            | MED             | CNA             |  438 |        0.0562341   |
| linear_window            | MED             | EAS             |  110 |       -0.15887     |
| linear_window            | MED             | EAU             |  241 |        0.0706904   |
| linear_window            | MED             | ENA             |  522 |        0.189831    |
| linear_window            | MED             | NCA             |  144 |        0.0856379   |
| linear_window            | MED             | NEU             | 1000 |        0.0420339   |
| linear_window            | MED             | NWN             |  183 |        0.194625    |
| linear_window            | MED             | SAU             |  351 |        0.0199018   |
| linear_window            | MED             | WCE             | 1000 |       -0.0049048   |
| linear_window            | MED             | WNA             |  975 |       -0.0153177   |
| linear_window            | NCA             | CNA             |  438 |        0.0167756   |
| linear_window            | NCA             | EAS             |  110 |        0.271995    |
| linear_window            | NCA             | EAU             |  241 |        0.223304    |
| linear_window            | NCA             | ENA             |  522 |       -0.0891508   |
| linear_window            | NCA             | MED             |  328 |        0.00561025  |
| linear_window            | NCA             | NEU             | 1000 |        0.133663    |
| linear_window            | NCA             | NWN             |  183 |        0.0740501   |
| linear_window            | NCA             | SAU             |  351 |        0.0321608   |
| linear_window            | NCA             | WCE             | 1000 |        0.0276928   |
| linear_window            | NCA             | WNA             |  975 |        0.0661905   |
| linear_window            | NEU             | CNA             |  438 |        0.228024    |
| linear_window            | NEU             | EAS             |  110 |       -0.106022    |
| linear_window            | NEU             | EAU             |  241 |        0.146027    |
| linear_window            | NEU             | ENA             |  522 |        0.215178    |
| linear_window            | NEU             | MED             |  328 |        0.123284    |
| linear_window            | NEU             | NCA             |  144 |       -0.0209121   |
| linear_window            | NEU             | NWN             |  183 |        0.186451    |
| linear_window            | NEU             | SAU             |  351 |       -0.0296396   |
| linear_window            | NEU             | WCE             | 1000 |       -0.0434141   |
| linear_window            | NEU             | WNA             |  975 |       -0.00252825  |
| linear_window            | NWN             | CNA             |  438 |       -0.021696    |
| linear_window            | NWN             | EAS             |  110 |       -0.357554    |
| linear_window            | NWN             | EAU             |  241 |        0.241143    |
| linear_window            | NWN             | ENA             |  522 |        0.0941199   |
| linear_window            | NWN             | MED             |  328 |        0.0332746   |
| linear_window            | NWN             | NCA             |  144 |        0.245216    |
| linear_window            | NWN             | NEU             | 1000 |       -0.0236351   |
| linear_window            | NWN             | SAU             |  351 |       -0.0584058   |
| linear_window            | NWN             | WCE             | 1000 |       -0.039742    |
| linear_window            | NWN             | WNA             |  975 |       -0.0151931   |
| linear_window            | SAU             | CNA             |  438 |        0.0240785   |
| linear_window            | SAU             | EAS             |  110 |        0.510847    |
| linear_window            | SAU             | EAU             |  241 |       -0.0936402   |
| linear_window            | SAU             | ENA             |  522 |       -0.146201    |
| linear_window            | SAU             | MED             |  328 |       -0.00635861  |
| linear_window            | SAU             | NCA             |  144 |        0.00254824  |
| linear_window            | SAU             | NEU             | 1000 |        0.00274084  |
| linear_window            | SAU             | NWN             |  183 |        0.0346611   |
| linear_window            | SAU             | WCE             | 1000 |       -0.0217534   |
| linear_window            | SAU             | WNA             |  975 |       -0.0649128   |
| linear_window            | WCE             | CNA             |  438 |       -0.040973    |
| linear_window            | WCE             | EAS             |  110 |        0.202016    |
| linear_window            | WCE             | EAU             |  241 |       -0.0318412   |
| linear_window            | WCE             | ENA             |  522 |        0.176286    |
| linear_window            | WCE             | MED             |  328 |        0.0177301   |
| linear_window            | WCE             | NCA             |  144 |        0.0884957   |
| linear_window            | WCE             | NEU             | 1000 |        0.0155407   |
| linear_window            | WCE             | NWN             |  183 |        0.0921524   |
| linear_window            | WCE             | SAU             |  351 |        0.0457703   |
| linear_window            | WCE             | WNA             |  975 |        0.00173191  |
| linear_window            | WNA             | CNA             |  438 |        0.066096    |
| linear_window            | WNA             | EAS             |  110 |        0.199399    |
| linear_window            | WNA             | EAU             |  241 |       -0.00261074  |
| linear_window            | WNA             | ENA             |  522 |        0.128678    |
| linear_window            | WNA             | MED             |  328 |       -0.0379123   |
| linear_window            | WNA             | NCA             |  144 |        0.115351    |
| linear_window            | WNA             | NEU             | 1000 |        0.0216883   |
| linear_window            | WNA             | NWN             |  183 |       -0.00496343  |
| linear_window            | WNA             | SAU             |  351 |       -0.0311053   |
| linear_window            | WNA             | WCE             | 1000 |       -0.0125597   |
| patchtst_small           | CNA             | EAS             |  110 |        0.00910222  |
| patchtst_small           | CNA             | EAU             |  241 |       -0.0316596   |
| patchtst_small           | CNA             | ENA             |  522 |        0.0285675   |
| patchtst_small           | CNA             | MED             |  328 |        0.031321    |
| patchtst_small           | CNA             | NCA             |  144 |        0.0271614   |
| patchtst_small           | CNA             | NEU             | 1000 |        0.154917    |
| patchtst_small           | CNA             | NWN             |  183 |        0.220962    |
| patchtst_small           | CNA             | SAU             |  351 |        0.0348365   |
| patchtst_small           | CNA             | WCE             | 1000 |        0.0367377   |
| patchtst_small           | CNA             | WNA             |  975 |       -0.00550209  |
| patchtst_small           | EAS             | CNA             |  438 |       -0.0192438   |
| patchtst_small           | EAS             | EAU             |  241 |       -0.0552165   |
| patchtst_small           | EAS             | ENA             |  522 |       -0.00509817  |
| patchtst_small           | EAS             | MED             |  328 |       -0.0307653   |
| patchtst_small           | EAS             | NCA             |  144 |        0.106816    |
| patchtst_small           | EAS             | NEU             | 1000 |        0.0177557   |
| patchtst_small           | EAS             | NWN             |  183 |        0.045325    |
| patchtst_small           | EAS             | SAU             |  351 |        0.0162392   |
| patchtst_small           | EAS             | WCE             | 1000 |       -0.0404568   |
| patchtst_small           | EAS             | WNA             |  975 |       -0.0389863   |
| patchtst_small           | EAU             | CNA             |  438 |        0.0707153   |
| patchtst_small           | EAU             | EAS             |  110 |        0.951386    |
| patchtst_small           | EAU             | ENA             |  522 |       -0.00207701  |
| patchtst_small           | EAU             | MED             |  328 |       -0.0418543   |
| patchtst_small           | EAU             | NCA             |  144 |       -0.12198     |
| patchtst_small           | EAU             | NEU             | 1000 |        0.0361728   |
| patchtst_small           | EAU             | NWN             |  183 |        0.0124895   |
| patchtst_small           | EAU             | SAU             |  351 |       -0.0597305   |
| patchtst_small           | EAU             | WCE             | 1000 |       -0.0303336   |
| patchtst_small           | EAU             | WNA             |  975 |        0.00769285  |
| patchtst_small           | ENA             | CNA             |  438 |        0.0301446   |
| patchtst_small           | ENA             | EAS             |  110 |        0.832226    |
| patchtst_small           | ENA             | EAU             |  241 |        0.138167    |
| patchtst_small           | ENA             | MED             |  328 |       -0.0795727   |
| patchtst_small           | ENA             | NCA             |  144 |        0.0974937   |
| patchtst_small           | ENA             | NEU             | 1000 |        0.185776    |
| patchtst_small           | ENA             | NWN             |  183 |       -0.0168508   |
| patchtst_small           | ENA             | SAU             |  351 |       -0.103858    |
| patchtst_small           | ENA             | WCE             | 1000 |        0.0661925   |
| patchtst_small           | ENA             | WNA             |  975 |        0.0368038   |
| patchtst_small           | MED             | CNA             |  438 |        0.05276     |
| patchtst_small           | MED             | EAS             |  110 |       -0.173012    |
| patchtst_small           | MED             | EAU             |  241 |        0.0659616   |
| patchtst_small           | MED             | ENA             |  522 |        0.184407    |
| patchtst_small           | MED             | NCA             |  144 |        0.0805898   |
| patchtst_small           | MED             | NEU             | 1000 |        0.0534823   |
| patchtst_small           | MED             | NWN             |  183 |        0.213098    |
| patchtst_small           | MED             | SAU             |  351 |        0.0155151   |
| patchtst_small           | MED             | WCE             | 1000 |       -0.00151563  |
| patchtst_small           | MED             | WNA             |  975 |       -0.0101706   |
| patchtst_small           | NCA             | CNA             |  438 |        0.0206824   |
| patchtst_small           | NCA             | EAS             |  110 |        0.229649    |
| patchtst_small           | NCA             | EAU             |  241 |        0.215078    |
| patchtst_small           | NCA             | ENA             |  522 |       -0.0869123   |
| patchtst_small           | NCA             | MED             |  328 |        0.00671823  |
| patchtst_small           | NCA             | NEU             | 1000 |        0.129693    |
| patchtst_small           | NCA             | NWN             |  183 |        0.0695009   |
| patchtst_small           | NCA             | SAU             |  351 |        0.0282335   |
| patchtst_small           | NCA             | WCE             | 1000 |        0.0238016   |
| patchtst_small           | NCA             | WNA             |  975 |        0.0673639   |
| patchtst_small           | NEU             | CNA             |  438 |        0.2315      |
| patchtst_small           | NEU             | EAS             |  110 |       -0.148122    |
| patchtst_small           | NEU             | EAU             |  241 |        0.142292    |
| patchtst_small           | NEU             | ENA             |  522 |        0.206597    |
| patchtst_small           | NEU             | MED             |  328 |        0.131282    |
| patchtst_small           | NEU             | NCA             |  144 |       -0.0107603   |
| patchtst_small           | NEU             | NWN             |  183 |        0.19125     |
| patchtst_small           | NEU             | SAU             |  351 |       -0.0270475   |
| patchtst_small           | NEU             | WCE             | 1000 |       -0.0416204   |
| patchtst_small           | NEU             | WNA             |  975 |        0.0073067   |
| patchtst_small           | NWN             | CNA             |  438 |       -0.0232285   |
| patchtst_small           | NWN             | EAS             |  110 |       -0.501913    |
| patchtst_small           | NWN             | EAU             |  241 |        0.234001    |
| patchtst_small           | NWN             | ENA             |  522 |        0.0810687   |
| patchtst_small           | NWN             | MED             |  328 |        0.0405539   |
| patchtst_small           | NWN             | NCA             |  144 |        0.259294    |
| patchtst_small           | NWN             | NEU             | 1000 |       -0.0187979   |
| patchtst_small           | NWN             | SAU             |  351 |       -0.0555547   |
| patchtst_small           | NWN             | WCE             | 1000 |       -0.038327    |
| patchtst_small           | NWN             | WNA             |  975 |       -0.00613836  |
| patchtst_small           | SAU             | CNA             |  438 |        0.0178518   |
| patchtst_small           | SAU             | EAS             |  110 |        0.523435    |
| patchtst_small           | SAU             | EAU             |  241 |       -0.0888087   |
| patchtst_small           | SAU             | ENA             |  522 |       -0.164152    |
| patchtst_small           | SAU             | MED             |  328 |       -0.00452143  |
| patchtst_small           | SAU             | NCA             |  144 |       -0.00126507  |
| patchtst_small           | SAU             | NEU             | 1000 |        0.018534    |
| patchtst_small           | SAU             | NWN             |  183 |        0.131786    |
| patchtst_small           | SAU             | WCE             | 1000 |       -0.0195409   |
| patchtst_small           | SAU             | WNA             |  975 |       -0.0385261   |
| patchtst_small           | WCE             | CNA             |  438 |       -0.0516707   |
| patchtst_small           | WCE             | EAS             |  110 |        0.179753    |
| patchtst_small           | WCE             | EAU             |  241 |       -0.0396426   |
| patchtst_small           | WCE             | ENA             |  522 |        0.165734    |
| patchtst_small           | WCE             | MED             |  328 |        0.0156369   |
| patchtst_small           | WCE             | NCA             |  144 |        0.0817687   |
| patchtst_small           | WCE             | NEU             | 1000 |        0.0135891   |
| patchtst_small           | WCE             | NWN             |  183 |        0.0995619   |
| patchtst_small           | WCE             | SAU             |  351 |        0.042716    |
| patchtst_small           | WCE             | WNA             |  975 |        0.00495354  |
| patchtst_small           | WNA             | CNA             |  438 |        0.0612383   |
| patchtst_small           | WNA             | EAS             |  110 |        0.0578466   |
| patchtst_small           | WNA             | EAU             |  241 |       -0.00593658  |
| patchtst_small           | WNA             | ENA             |  522 |        0.124442    |
| patchtst_small           | WNA             | MED             |  328 |       -0.033596    |
| patchtst_small           | WNA             | NCA             |  144 |        0.112826    |
| patchtst_small           | WNA             | NEU             | 1000 |        0.0375572   |
| patchtst_small           | WNA             | NWN             |  183 |        0.00113611  |
| patchtst_small           | WNA             | SAU             |  351 |       -0.0339143   |
| patchtst_small           | WNA             | WCE             | 1000 |       -0.00286369  |
| regional_doy_climatology | CNA             | EAS             |  110 |       -1.81385     |
| regional_doy_climatology | CNA             | EAU             |  241 |       -0.110242    |
| regional_doy_climatology | CNA             | ENA             |  522 |       -0.557076    |
| regional_doy_climatology | CNA             | MED             |  328 |        0.344803    |
| regional_doy_climatology | CNA             | NCA             |  144 |        0.893314    |
| regional_doy_climatology | CNA             | NEU             | 1000 |       -0.00572199  |
| regional_doy_climatology | CNA             | NWN             |  183 |       -0.19641     |
| regional_doy_climatology | CNA             | SAU             |  351 |        0.2294      |
| regional_doy_climatology | CNA             | WCE             | 1000 |       -0.049288    |
| regional_doy_climatology | CNA             | WNA             |  975 |        0.1392      |
| regional_doy_climatology | EAS             | CNA             |  438 |        3.01123     |
| regional_doy_climatology | EAS             | EAU             |  241 |        3.12179     |
| regional_doy_climatology | EAS             | ENA             |  522 |        2.18762     |
| regional_doy_climatology | EAS             | MED             |  328 |        3.77667     |
| regional_doy_climatology | EAS             | NCA             |  144 |        4.29429     |
| regional_doy_climatology | EAS             | NEU             | 1000 |        2.98338     |
| regional_doy_climatology | EAS             | NWN             |  183 |        2.81549     |
| regional_doy_climatology | EAS             | SAU             |  351 |        3.27918     |
| regional_doy_climatology | EAS             | WCE             | 1000 |        2.91102     |
| regional_doy_climatology | EAS             | WNA             |  975 |        3.49015     |
| regional_doy_climatology | EAU             | CNA             |  438 |        0.282819    |
| regional_doy_climatology | EAU             | EAS             |  110 |       -1.33372     |
| regional_doy_climatology | EAU             | ENA             |  522 |       -0.351761    |
| regional_doy_climatology | EAU             | MED             |  328 |        0.468011    |
| regional_doy_climatology | EAU             | NCA             |  144 |        1.1281      |
| regional_doy_climatology | EAU             | NEU             | 1000 |        0.14188     |
| regional_doy_climatology | EAU             | NWN             |  183 |        0.01432     |
| regional_doy_climatology | EAU             | SAU             |  351 |        0.532103    |
| regional_doy_climatology | EAU             | WCE             | 1000 |        0.134601    |
| regional_doy_climatology | EAU             | WNA             |  975 |        0.160134    |
| regional_doy_climatology | ENA             | CNA             |  438 |        0.734675    |
| regional_doy_climatology | ENA             | EAS             |  110 |       -1.17278     |
| regional_doy_climatology | ENA             | EAU             |  241 |        0.48445     |
| regional_doy_climatology | ENA             | MED             |  328 |        1.03475     |
| regional_doy_climatology | ENA             | NCA             |  144 |        1.71267     |
| regional_doy_climatology | ENA             | NEU             | 1000 |        0.482088    |
| regional_doy_climatology | ENA             | NWN             |  183 |        0.377848    |
| regional_doy_climatology | ENA             | SAU             |  351 |        0.888504    |
| regional_doy_climatology | ENA             | WCE             | 1000 |        0.48011     |
| regional_doy_climatology | ENA             | WNA             |  975 |        0.696154    |
| regional_doy_climatology | MED             | CNA             |  438 |       -0.136096    |
| regional_doy_climatology | MED             | EAS             |  110 |       -1.65667     |
| regional_doy_climatology | MED             | EAU             |  241 |       -0.394873    |
| regional_doy_climatology | MED             | ENA             |  522 |       -0.684155    |
| regional_doy_climatology | MED             | NCA             |  144 |        0.644253    |
| regional_doy_climatology | MED             | NEU             | 1000 |       -0.222737    |
| regional_doy_climatology | MED             | NWN             |  183 |       -0.376459    |
| regional_doy_climatology | MED             | SAU             |  351 |        0.142412    |
| regional_doy_climatology | MED             | WCE             | 1000 |       -0.230736    |
| regional_doy_climatology | MED             | WNA             |  975 |       -0.212434    |
| regional_doy_climatology | NCA             | CNA             |  438 |       -0.677282    |
| regional_doy_climatology | NCA             | EAS             |  110 |       -2.21432     |
| regional_doy_climatology | NCA             | EAU             |  241 |       -0.780145    |
| regional_doy_climatology | NCA             | ENA             |  522 |       -1.08305     |
| regional_doy_climatology | NCA             | MED             |  328 |       -0.374613    |
| regional_doy_climatology | NCA             | NEU             | 1000 |       -0.506486    |
| regional_doy_climatology | NCA             | NWN             |  183 |       -0.750943    |
| regional_doy_climatology | NCA             | SAU             |  351 |       -0.362901    |
| regional_doy_climatology | NCA             | WCE             | 1000 |       -0.571246    |
| regional_doy_climatology | NCA             | WNA             |  975 |       -0.467222    |
| regional_doy_climatology | NEU             | CNA             |  438 |        0.189134    |
| regional_doy_climatology | NEU             | EAS             |  110 |       -1.59376     |
| regional_doy_climatology | NEU             | EAU             |  241 |       -0.0239802   |
| regional_doy_climatology | NEU             | ENA             |  522 |       -0.441286    |
| regional_doy_climatology | NEU             | MED             |  328 |        0.460559    |
| regional_doy_climatology | NEU             | NCA             |  144 |        1.03828     |
| regional_doy_climatology | NEU             | NWN             |  183 |       -0.139243    |
| regional_doy_climatology | NEU             | SAU             |  351 |        0.348044    |
| regional_doy_climatology | NEU             | WCE             | 1000 |        0.0154295   |
| regional_doy_climatology | NEU             | WNA             |  975 |        0.211143    |
| regional_doy_climatology | NWN             | CNA             |  438 |        0.374672    |
| regional_doy_climatology | NWN             | EAS             |  110 |       -1.44579     |
| regional_doy_climatology | NWN             | EAU             |  241 |        0.11023     |
| regional_doy_climatology | NWN             | ENA             |  522 |       -0.292863    |
| regional_doy_climatology | NWN             | MED             |  328 |        0.604575    |
| regional_doy_climatology | NWN             | NCA             |  144 |        1.2428      |
| regional_doy_climatology | NWN             | NEU             | 1000 |        0.116583    |
| regional_doy_climatology | NWN             | SAU             |  351 |        0.512798    |
| regional_doy_climatology | NWN             | WCE             | 1000 |        0.138272    |
| regional_doy_climatology | NWN             | WNA             |  975 |        0.320105    |
| regional_doy_climatology | SAU             | CNA             |  438 |       -0.227357    |
| regional_doy_climatology | SAU             | EAS             |  110 |       -1.92734     |
| regional_doy_climatology | SAU             | EAU             |  241 |       -0.3613      |
| regional_doy_climatology | SAU             | ENA             |  522 |       -0.75106     |
| regional_doy_climatology | SAU             | MED             |  328 |        0.0784903   |
| regional_doy_climatology | SAU             | NCA             |  144 |        0.582668    |
| regional_doy_climatology | SAU             | NEU             | 1000 |       -0.209395    |
| regional_doy_climatology | SAU             | NWN             |  183 |       -0.418267    |
| regional_doy_climatology | SAU             | WCE             | 1000 |       -0.247514    |
| regional_doy_climatology | SAU             | WNA             |  975 |       -0.091733    |
| regional_doy_climatology | WCE             | CNA             |  438 |        0.118748    |
| regional_doy_climatology | WCE             | EAS             |  110 |       -1.66502     |
| regional_doy_climatology | WCE             | EAU             |  241 |       -0.0673023   |
| regional_doy_climatology | WCE             | ENA             |  522 |       -0.489036    |
| regional_doy_climatology | WCE             | MED             |  328 |        0.430702    |
| regional_doy_climatology | WCE             | NCA             |  144 |        0.982865    |
| regional_doy_climatology | WCE             | NEU             | 1000 |        0.019234    |
| regional_doy_climatology | WCE             | NWN             |  183 |       -0.139548    |
| regional_doy_climatology | WCE             | SAU             |  351 |        0.313502    |
| regional_doy_climatology | WCE             | WNA             |  975 |        0.203982    |
| regional_doy_climatology | WNA             | CNA             |  438 |        0.156543    |
| regional_doy_climatology | WNA             | EAS             |  110 |       -1.37559     |
| regional_doy_climatology | WNA             | EAU             |  241 |       -0.170542    |
| regional_doy_climatology | WNA             | ENA             |  522 |       -0.462289    |
| regional_doy_climatology | WNA             | MED             |  328 |        0.31725     |
| regional_doy_climatology | WNA             | NCA             |  144 |        1.00846     |
| regional_doy_climatology | WNA             | NEU             | 1000 |        0.00513235  |
| regional_doy_climatology | WNA             | NWN             |  183 |       -0.0983048   |
| regional_doy_climatology | WNA             | SAU             |  351 |        0.432435    |
| regional_doy_climatology | WNA             | WCE             | 1000 |        0.0173442   |
| spatial_knn_ridge        | CNA             | EAS             |  110 |       -0.0264059   |
| spatial_knn_ridge        | CNA             | EAU             |  241 |       -0.0114375   |
| spatial_knn_ridge        | CNA             | ENA             |  522 |       -0.0812374   |
| spatial_knn_ridge        | CNA             | MED             |  328 |        0.0224523   |
| spatial_knn_ridge        | CNA             | NCA             |  144 |        0.121021    |
| spatial_knn_ridge        | CNA             | NEU             | 1000 |       -0.0538156   |
| spatial_knn_ridge        | CNA             | NWN             |  183 |        0.0749518   |
| spatial_knn_ridge        | CNA             | SAU             |  351 |       -0.018018    |
| spatial_knn_ridge        | CNA             | WCE             | 1000 |       -0.069079    |
| spatial_knn_ridge        | CNA             | WNA             |  975 |        0.0285721   |
| spatial_knn_ridge        | EAS             | CNA             |  438 |        0.155612    |
| spatial_knn_ridge        | EAS             | EAU             |  241 |        0.0914245   |
| spatial_knn_ridge        | EAS             | ENA             |  522 |        0.0731986   |
| spatial_knn_ridge        | EAS             | MED             |  328 |        0.130653    |
| spatial_knn_ridge        | EAS             | NCA             |  144 |        0.250413    |
| spatial_knn_ridge        | EAS             | NEU             | 1000 |        0.00172038  |
| spatial_knn_ridge        | EAS             | NWN             |  183 |        0.087255    |
| spatial_knn_ridge        | EAS             | SAU             |  351 |        0.0944786   |
| spatial_knn_ridge        | EAS             | WCE             | 1000 |        0.016851    |
| spatial_knn_ridge        | EAS             | WNA             |  975 |        0.0814023   |
| spatial_knn_ridge        | EAU             | CNA             |  438 |        0.0316273   |
| spatial_knn_ridge        | EAU             | EAS             |  110 |       -0.0430591   |
| spatial_knn_ridge        | EAU             | ENA             |  522 |       -0.0470013   |
| spatial_knn_ridge        | EAU             | MED             |  328 |        0.0335856   |
| spatial_knn_ridge        | EAU             | NCA             |  144 |        0.139191    |
| spatial_knn_ridge        | EAU             | NEU             | 1000 |       -0.0527993   |
| spatial_knn_ridge        | EAU             | NWN             |  183 |        0.053322    |
| spatial_knn_ridge        | EAU             | SAU             |  351 |       -0.00326644  |
| spatial_knn_ridge        | EAU             | WCE             | 1000 |       -0.0593896   |
| spatial_knn_ridge        | EAU             | WNA             |  975 |        0.0245109   |
| spatial_knn_ridge        | ENA             | CNA             |  438 |        0.121862    |
| spatial_knn_ridge        | ENA             | EAS             |  110 |        0.0749949   |
| spatial_knn_ridge        | ENA             | EAU             |  241 |        0.0979579   |
| spatial_knn_ridge        | ENA             | MED             |  328 |        0.148109    |
| spatial_knn_ridge        | ENA             | NCA             |  144 |        0.280754    |
| spatial_knn_ridge        | ENA             | NEU             | 1000 |        0.00719172  |
| spatial_knn_ridge        | ENA             | NWN             |  183 |        0.166111    |
| spatial_knn_ridge        | ENA             | SAU             |  351 |        0.0847909   |
| spatial_knn_ridge        | ENA             | WCE             | 1000 |        0.00167854  |
| spatial_knn_ridge        | ENA             | WNA             |  975 |        0.136088    |
| spatial_knn_ridge        | MED             | CNA             |  438 |        0.00734615  |
| spatial_knn_ridge        | MED             | EAS             |  110 |       -0.0659763   |
| spatial_knn_ridge        | MED             | EAU             |  241 |       -0.0263383   |
| spatial_knn_ridge        | MED             | ENA             |  522 |       -0.0580428   |
| spatial_knn_ridge        | MED             | NCA             |  144 |        0.0977084   |
| spatial_knn_ridge        | MED             | NEU             | 1000 |       -0.0666679   |
| spatial_knn_ridge        | MED             | NWN             |  183 |        0.0250106   |
| spatial_knn_ridge        | MED             | SAU             |  351 |       -0.0262191   |
| spatial_knn_ridge        | MED             | WCE             | 1000 |       -0.0736574   |
| spatial_knn_ridge        | MED             | WNA             |  975 |       -0.00369516  |
| spatial_knn_ridge        | NCA             | CNA             |  438 |       -0.0710437   |
| spatial_knn_ridge        | NCA             | EAS             |  110 |       -0.121348    |
| spatial_knn_ridge        | NCA             | EAU             |  241 |       -0.0881247   |
| spatial_knn_ridge        | NCA             | ENA             |  522 |       -0.110859    |
| spatial_knn_ridge        | NCA             | MED             |  328 |       -0.0671861   |
| spatial_knn_ridge        | NCA             | NEU             | 1000 |       -0.0957735   |
| spatial_knn_ridge        | NCA             | NWN             |  183 |       -0.0145203   |
| spatial_knn_ridge        | NCA             | SAU             |  351 |       -0.0798482   |
| spatial_knn_ridge        | NCA             | WCE             | 1000 |       -0.108099    |
| spatial_knn_ridge        | NCA             | WNA             |  975 |       -0.0662014   |
| spatial_knn_ridge        | NEU             | CNA             |  438 |        0.142908    |
| spatial_knn_ridge        | NEU             | EAS             |  110 |        0.0337204   |
| spatial_knn_ridge        | NEU             | EAU             |  241 |        0.0944043   |
| spatial_knn_ridge        | NEU             | ENA             |  522 |        0.0318836   |
| spatial_knn_ridge        | NEU             | MED             |  328 |        0.141756    |
| spatial_knn_ridge        | NEU             | NCA             |  144 |        0.277674    |
| spatial_knn_ridge        | NEU             | NWN             |  183 |        0.125567    |
| spatial_knn_ridge        | NEU             | SAU             |  351 |        0.0864087   |
| spatial_knn_ridge        | NEU             | WCE             | 1000 |        0.00291457  |
| spatial_knn_ridge        | NEU             | WNA             |  975 |        0.112729    |
| spatial_knn_ridge        | NWN             | CNA             |  438 |        0.122723    |
| spatial_knn_ridge        | NWN             | EAS             |  110 |       -0.0124781   |
| spatial_knn_ridge        | NWN             | EAU             |  241 |        0.0550738   |
| spatial_knn_ridge        | NWN             | ENA             |  522 |        0.103255    |
| spatial_knn_ridge        | NWN             | MED             |  328 |        0.0651085   |
| spatial_knn_ridge        | NWN             | NCA             |  144 |        0.142989    |
| spatial_knn_ridge        | NWN             | NEU             | 1000 |       -0.00945605  |
| spatial_knn_ridge        | NWN             | SAU             |  351 |        0.0661495   |
| spatial_knn_ridge        | NWN             | WCE             | 1000 |        0.00976943  |
| spatial_knn_ridge        | NWN             | WNA             |  975 |        0.00091299  |
| spatial_knn_ridge        | SAU             | CNA             |  438 |        0.0364618   |
| spatial_knn_ridge        | SAU             | EAS             |  110 |       -0.0227193   |
| spatial_knn_ridge        | SAU             | EAU             |  241 |        0.00727607  |
| spatial_knn_ridge        | SAU             | ENA             |  522 |       -0.0508981   |
| spatial_knn_ridge        | SAU             | MED             |  328 |        0.0414576   |
| spatial_knn_ridge        | SAU             | NCA             |  144 |        0.154607    |
| spatial_knn_ridge        | SAU             | NEU             | 1000 |       -0.0465372   |
| spatial_knn_ridge        | SAU             | NWN             |  183 |        0.0671925   |
| spatial_knn_ridge        | SAU             | WCE             | 1000 |       -0.0578752   |
| spatial_knn_ridge        | SAU             | WNA             |  975 |        0.040781    |
| spatial_knn_ridge        | WCE             | CNA             |  438 |        0.137589    |
| spatial_knn_ridge        | WCE             | EAS             |  110 |        0.0545189   |
| spatial_knn_ridge        | WCE             | EAU             |  241 |        0.096013    |
| spatial_knn_ridge        | WCE             | ENA             |  522 |        0.0185602   |
| spatial_knn_ridge        | WCE             | MED             |  328 |        0.143465    |
| spatial_knn_ridge        | WCE             | NCA             |  144 |        0.284064    |
| spatial_knn_ridge        | WCE             | NEU             | 1000 |        0.00281446  |
| spatial_knn_ridge        | WCE             | NWN             |  183 |        0.139024    |
| spatial_knn_ridge        | WCE             | SAU             |  351 |        0.0840714   |
| spatial_knn_ridge        | WCE             | WNA             |  975 |        0.125291    |
| spatial_knn_ridge        | WNA             | CNA             |  438 |        0.0424178   |
| spatial_knn_ridge        | WNA             | EAS             |  110 |       -0.0691434   |
| spatial_knn_ridge        | WNA             | EAU             |  241 |        0.000291038 |
| spatial_knn_ridge        | WNA             | ENA             |  522 |       -0.0103637   |
| spatial_knn_ridge        | WNA             | MED             |  328 |        0.0263207   |
| spatial_knn_ridge        | WNA             | NCA             |  144 |        0.113696    |
| spatial_knn_ridge        | WNA             | NEU             | 1000 |       -0.0460559   |
| spatial_knn_ridge        | WNA             | NWN             |  183 |        0.0249222   |
| spatial_knn_ridge        | WNA             | SAU             |  351 |        0.0113058   |
| spatial_knn_ridge        | WNA             | WCE             | 1000 |       -0.0378083   |
| stgcn_diffusion          | CNA             | EAS             |  110 |        0.162638    |
| stgcn_diffusion          | CNA             | EAU             |  241 |        0.0313562   |
| stgcn_diffusion          | CNA             | ENA             |  522 |        0.008911    |
| stgcn_diffusion          | CNA             | MED             |  328 |        0.0368478   |
| stgcn_diffusion          | CNA             | NCA             |  144 |       -0.000912786 |
| stgcn_diffusion          | CNA             | NEU             | 1000 |        0.094202    |
| stgcn_diffusion          | CNA             | NWN             |  183 |        0.168486    |
| stgcn_diffusion          | CNA             | SAU             |  351 |        0.0261856   |
| stgcn_diffusion          | CNA             | WCE             | 1000 |        0.0484946   |
| stgcn_diffusion          | CNA             | WNA             |  975 |        0.0745154   |
| stgcn_diffusion          | EAS             | CNA             |  438 |        0.0970808   |
| stgcn_diffusion          | EAS             | EAU             |  241 |        0.0123736   |
| stgcn_diffusion          | EAS             | ENA             |  522 |        0.125408    |
| stgcn_diffusion          | EAS             | MED             |  328 |       -0.000200735 |
| stgcn_diffusion          | EAS             | NCA             |  144 |        0.0037958   |
| stgcn_diffusion          | EAS             | NEU             | 1000 |        0.048891    |
| stgcn_diffusion          | EAS             | NWN             |  183 |        0.133461    |
| stgcn_diffusion          | EAS             | SAU             |  351 |        0.00278296  |
| stgcn_diffusion          | EAS             | WCE             | 1000 |        0.0136454   |
| stgcn_diffusion          | EAS             | WNA             |  975 |        0.0419482   |
| stgcn_diffusion          | EAU             | CNA             |  438 |        0.0818074   |
| stgcn_diffusion          | EAU             | EAS             |  110 |        0.00758346  |
| stgcn_diffusion          | EAU             | ENA             |  522 |        0.114738    |
| stgcn_diffusion          | EAU             | MED             |  328 |       -0.00253994  |
| stgcn_diffusion          | EAU             | NCA             |  144 |        0.000737328 |
| stgcn_diffusion          | EAU             | NEU             | 1000 |        0.0320664   |
| stgcn_diffusion          | EAU             | NWN             |  183 |        0.120616    |
| stgcn_diffusion          | EAU             | SAU             |  351 |        0.000331567 |
| stgcn_diffusion          | EAU             | WCE             | 1000 |        0.0070916   |
| stgcn_diffusion          | EAU             | WNA             |  975 |        0.0344451   |
| stgcn_diffusion          | ENA             | CNA             |  438 |        0.0272019   |
| stgcn_diffusion          | ENA             | EAS             |  110 |        0.166276    |
| stgcn_diffusion          | ENA             | EAU             |  241 |        0.074501    |
| stgcn_diffusion          | ENA             | MED             |  328 |        0.0440497   |
| stgcn_diffusion          | ENA             | NCA             |  144 |        0.00512094  |
| stgcn_diffusion          | ENA             | NEU             | 1000 |        0.0794498   |
| stgcn_diffusion          | ENA             | NWN             |  183 |        0.169476    |
| stgcn_diffusion          | ENA             | SAU             |  351 |        0.0435755   |
| stgcn_diffusion          | ENA             | WCE             | 1000 |        0.039924    |
| stgcn_diffusion          | ENA             | WNA             |  975 |        0.0877222   |
| stgcn_diffusion          | MED             | CNA             |  438 |        0.105063    |
| stgcn_diffusion          | MED             | EAS             |  110 |        0.00670611  |
| stgcn_diffusion          | MED             | EAU             |  241 |        0.011353    |
| stgcn_diffusion          | MED             | ENA             |  522 |        0.13641     |
| stgcn_diffusion          | MED             | NCA             |  144 |        0.00643303  |
| stgcn_diffusion          | MED             | NEU             | 1000 |        0.0165301   |
| stgcn_diffusion          | MED             | NWN             |  183 |        0.0723369   |
| stgcn_diffusion          | MED             | SAU             |  351 |        0.00603574  |
| stgcn_diffusion          | MED             | WCE             | 1000 |        0.0102795   |
| stgcn_diffusion          | MED             | WNA             |  975 |        0.016501    |
| stgcn_diffusion          | NCA             | CNA             |  438 |        0.0770738   |
| stgcn_diffusion          | NCA             | EAS             |  110 |        0.227845    |
| stgcn_diffusion          | NCA             | EAU             |  241 |        0.0181174   |
| stgcn_diffusion          | NCA             | ENA             |  522 |        0.113801    |
| stgcn_diffusion          | NCA             | MED             |  328 |        0.00827427  |
| stgcn_diffusion          | NCA             | NEU             | 1000 |        0.0639179   |
| stgcn_diffusion          | NCA             | NWN             |  183 |        0.142528    |
| stgcn_diffusion          | NCA             | SAU             |  351 |        0.0142021   |
| stgcn_diffusion          | NCA             | WCE             | 1000 |        0.0257268   |
| stgcn_diffusion          | NCA             | WNA             |  975 |        0.041871    |
| stgcn_diffusion          | NEU             | CNA             |  438 |        0.119163    |
| stgcn_diffusion          | NEU             | EAS             |  110 |        0.00199073  |
| stgcn_diffusion          | NEU             | EAU             |  241 |        0.0253136   |
| stgcn_diffusion          | NEU             | ENA             |  522 |        0.140752    |
| stgcn_diffusion          | NEU             | MED             |  328 |        0.00694137  |
| stgcn_diffusion          | NEU             | NCA             |  144 |        0.0189995   |
| stgcn_diffusion          | NEU             | NWN             |  183 |        0.0915359   |
| stgcn_diffusion          | NEU             | SAU             |  351 |        0.0111197   |
| stgcn_diffusion          | NEU             | WCE             | 1000 |       -0.00204417  |
| stgcn_diffusion          | NEU             | WNA             |  975 |        0.0360618   |
| stgcn_diffusion          | NWN             | CNA             |  438 |        0.257269    |
| stgcn_diffusion          | NWN             | EAS             |  110 |        0.502506    |
| stgcn_diffusion          | NWN             | EAU             |  241 |        0.16997     |
| stgcn_diffusion          | NWN             | ENA             |  522 |        0.352642    |
| stgcn_diffusion          | NWN             | MED             |  328 |        0.0887532   |
| stgcn_diffusion          | NWN             | NCA             |  144 |        0.0537421   |
| stgcn_diffusion          | NWN             | NEU             | 1000 |        0.112903    |
| stgcn_diffusion          | NWN             | SAU             |  351 |        0.119423    |
| stgcn_diffusion          | NWN             | WCE             | 1000 |        0.127521    |
| stgcn_diffusion          | NWN             | WNA             |  975 |        0.0299122   |
| stgcn_diffusion          | SAU             | CNA             |  438 |        0.0931501   |
| stgcn_diffusion          | SAU             | EAS             |  110 |        0.0346637   |
| stgcn_diffusion          | SAU             | EAU             |  241 |        0.0245744   |
| stgcn_diffusion          | SAU             | ENA             |  522 |        0.114853    |
| stgcn_diffusion          | SAU             | MED             |  328 |       -7.73211e-05 |
| stgcn_diffusion          | SAU             | NCA             |  144 |        0.00574735  |
| stgcn_diffusion          | SAU             | NEU             | 1000 |        0.0377964   |
| stgcn_diffusion          | SAU             | NWN             |  183 |        0.142481    |
| stgcn_diffusion          | SAU             | WCE             | 1000 |        0.00350027  |
| stgcn_diffusion          | SAU             | WNA             |  975 |        0.0572767   |
| stgcn_diffusion          | WCE             | CNA             |  438 |        0.102684    |
| stgcn_diffusion          | WCE             | EAS             |  110 |        0.0334312   |
| stgcn_diffusion          | WCE             | EAU             |  241 |        0.0318432   |
| stgcn_diffusion          | WCE             | ENA             |  522 |        0.118467    |
| stgcn_diffusion          | WCE             | MED             |  328 |        0.00621015  |
| stgcn_diffusion          | WCE             | NCA             |  144 |        0.0132954   |
| stgcn_diffusion          | WCE             | NEU             | 1000 |        0.0290037   |
| stgcn_diffusion          | WCE             | NWN             |  183 |        0.148232    |
| stgcn_diffusion          | WCE             | SAU             |  351 |        0.00516622  |
| stgcn_diffusion          | WCE             | WNA             |  975 |        0.0630569   |
| stgcn_diffusion          | WNA             | CNA             |  438 |        0.147731    |
| stgcn_diffusion          | WNA             | EAS             |  110 |        0.0221271   |
| stgcn_diffusion          | WNA             | EAU             |  241 |        0.0541348   |
| stgcn_diffusion          | WNA             | ENA             |  522 |        0.202517    |
| stgcn_diffusion          | WNA             | MED             |  328 |        0.0319851   |
| stgcn_diffusion          | WNA             | NCA             |  144 |        0.0150485   |
| stgcn_diffusion          | WNA             | NEU             | 1000 |        0.0568386   |
| stgcn_diffusion          | WNA             | NWN             |  183 |        0.0204321   |
| stgcn_diffusion          | WNA             | SAU             |  351 |        0.0575199   |
| stgcn_diffusion          | WNA             | WCE             | 1000 |        0.0726681   |

## KBS predictive comparison

| forecast_model           | feature_set         | cv_kind                 | estimator     |     n |   n_features |       mae |           r2 |
|:-------------------------|:--------------------|:------------------------|:--------------|------:|-------------:|----------:|-------------:|
| graphwavenet_transfer    | physical_knowledge  | leave_target_region_out | ridge         | 52920 |           12 | 0.0951737 |  0.0607598   |
| graphwavenet_transfer    | physical_knowledge  | leave_target_region_out | random_forest | 52920 |           12 | 0.0923984 | -0.0153102   |
| graphwavenet_transfer    | generic_shift       | leave_target_region_out | ridge         | 52920 |           11 | 0.106937  | -0.113655    |
| graphwavenet_transfer    | generic_shift       | leave_target_region_out | random_forest | 52920 |           11 | 0.0947782 | -0.054102    |
| graphwavenet_transfer    | physical_plus_shift | leave_target_region_out | ridge         | 52920 |           23 | 0.097576  |  0.0372659   |
| graphwavenet_transfer    | physical_plus_shift | leave_target_region_out | random_forest | 52920 |           23 | 0.09138   | -0.0528425   |
| graphwavenet_transfer    | physical_knowledge  | group_by_cell           | ridge         | 52920 |           12 | 0.0941606 |  0.121004    |
| graphwavenet_transfer    | physical_knowledge  | group_by_cell           | random_forest | 52920 |           12 | 0.0787036 |  0.27877     |
| graphwavenet_transfer    | generic_shift       | group_by_cell           | ridge         | 52920 |           11 | 0.0937563 |  0.00361922  |
| graphwavenet_transfer    | generic_shift       | group_by_cell           | random_forest | 52920 |           11 | 0.0811231 |  0.149931    |
| graphwavenet_transfer    | physical_plus_shift | group_by_cell           | ridge         | 52920 |           23 | 0.0935739 |  0.127265    |
| graphwavenet_transfer    | physical_plus_shift | group_by_cell           | random_forest | 52920 |           23 | 0.0672166 |  0.343834    |
| linear_window            | physical_knowledge  | leave_target_region_out | ridge         | 52920 |           12 | 1.12139   | -0.00103315  |
| linear_window            | physical_knowledge  | leave_target_region_out | random_forest | 52920 |           12 | 1.14918   | -0.0507081   |
| linear_window            | generic_shift       | leave_target_region_out | ridge         | 52920 |           11 | 1.12039   | -0.000655486 |
| linear_window            | generic_shift       | leave_target_region_out | random_forest | 52920 |           11 | 1.12501   | -0.00535273  |
| linear_window            | physical_plus_shift | leave_target_region_out | ridge         | 52920 |           23 | 1.12132   | -0.000827247 |
| linear_window            | physical_plus_shift | leave_target_region_out | random_forest | 52920 |           23 | 1.14712   | -0.045704    |
| linear_window            | physical_knowledge  | group_by_cell           | ridge         | 52920 |           12 | 1.12248   | -0.00210424  |
| linear_window            | physical_knowledge  | group_by_cell           | random_forest | 52920 |           12 | 1.15729   | -0.0644758   |
| linear_window            | generic_shift       | group_by_cell           | ridge         | 52920 |           11 | 1.12013   | -0.000426942 |
| linear_window            | generic_shift       | group_by_cell           | random_forest | 52920 |           11 | 1.12285   | -0.00558297  |
| linear_window            | physical_plus_shift | group_by_cell           | ridge         | 52920 |           23 | 1.12241   | -0.00195412  |
| linear_window            | physical_plus_shift | group_by_cell           | random_forest | 52920 |           23 | 1.15676   | -0.064435    |
| patchtst_small           | physical_knowledge  | leave_target_region_out | ridge         | 52920 |           12 | 1.12599   | -0.00125741  |
| patchtst_small           | physical_knowledge  | leave_target_region_out | random_forest | 52920 |           12 | 1.15308   | -0.048869    |
| patchtst_small           | generic_shift       | leave_target_region_out | ridge         | 52920 |           11 | 1.12466   | -0.000525051 |
| patchtst_small           | generic_shift       | leave_target_region_out | random_forest | 52920 |           11 | 1.12955   | -0.00546855  |
| patchtst_small           | physical_plus_shift | leave_target_region_out | ridge         | 52920 |           23 | 1.12595   | -0.00108952  |
| patchtst_small           | physical_plus_shift | leave_target_region_out | random_forest | 52920 |           23 | 1.15136   | -0.0445663   |
| patchtst_small           | physical_knowledge  | group_by_cell           | ridge         | 52920 |           12 | 1.12727   | -0.00244696  |
| patchtst_small           | physical_knowledge  | group_by_cell           | random_forest | 52920 |           12 | 1.15956   | -0.0582426   |
| patchtst_small           | generic_shift       | group_by_cell           | ridge         | 52920 |           11 | 1.12451   | -0.000407228 |
| patchtst_small           | generic_shift       | group_by_cell           | random_forest | 52920 |           11 | 1.12739   | -0.00557644  |
| patchtst_small           | physical_plus_shift | group_by_cell           | ridge         | 52920 |           23 | 1.12716   | -0.00222827  |
| patchtst_small           | physical_plus_shift | group_by_cell           | random_forest | 52920 |           23 | 1.15924   | -0.0585707   |
| regional_doy_climatology | physical_knowledge  | leave_target_region_out | ridge         | 52920 |           12 | 0.706046  | -0.0366288   |
| regional_doy_climatology | physical_knowledge  | leave_target_region_out | random_forest | 52920 |           12 | 0.721957  | -0.0587501   |
| regional_doy_climatology | generic_shift       | leave_target_region_out | ridge         | 52920 |           11 | 0.632956  |  0.0545713   |
| regional_doy_climatology | generic_shift       | leave_target_region_out | random_forest | 52920 |           11 | 0.799163  | -0.484345    |
| regional_doy_climatology | physical_plus_shift | leave_target_region_out | ridge         | 52920 |           23 | 0.548684  |  0.212441    |
| regional_doy_climatology | physical_plus_shift | leave_target_region_out | random_forest | 52920 |           23 | 0.692472  | -0.328571    |
| regional_doy_climatology | physical_knowledge  | group_by_cell           | ridge         | 52920 |           12 | 0.658968  |  0.0425894   |
| regional_doy_climatology | physical_knowledge  | group_by_cell           | random_forest | 52920 |           12 | 0.656097  |  0.0373389   |
| regional_doy_climatology | generic_shift       | group_by_cell           | ridge         | 52920 |           11 | 0.455771  |  0.391125    |
| regional_doy_climatology | generic_shift       | group_by_cell           | random_forest | 52920 |           11 | 0.107198  |  0.966298    |
| regional_doy_climatology | physical_plus_shift | group_by_cell           | ridge         | 52920 |           23 | 0.396776  |  0.581675    |
| regional_doy_climatology | physical_plus_shift | group_by_cell           | random_forest | 52920 |           23 | 0.114305  |  0.8394      |
| spatial_knn_ridge        | physical_knowledge  | leave_target_region_out | ridge         | 52920 |           12 | 0.0702495 | -0.139605    |
| spatial_knn_ridge        | physical_knowledge  | leave_target_region_out | random_forest | 52920 |           12 | 0.0688486 | -0.041979    |
| spatial_knn_ridge        | generic_shift       | leave_target_region_out | ridge         | 52920 |           11 | 0.071595  | -0.161622    |
| spatial_knn_ridge        | generic_shift       | leave_target_region_out | random_forest | 52920 |           11 | 0.0932158 | -0.945189    |
| spatial_knn_ridge        | physical_plus_shift | leave_target_region_out | ridge         | 52920 |           23 | 0.0697196 | -0.250538    |
| spatial_knn_ridge        | physical_plus_shift | leave_target_region_out | random_forest | 52920 |           23 | 0.0869895 | -0.808704    |
| spatial_knn_ridge        | physical_knowledge  | group_by_cell           | ridge         | 52920 |           12 | 0.065037  |  0.0447078   |
| spatial_knn_ridge        | physical_knowledge  | group_by_cell           | random_forest | 52920 |           12 | 0.0595914 |  0.302035    |
| spatial_knn_ridge        | generic_shift       | group_by_cell           | ridge         | 52920 |           11 | 0.056547  |  0.203958    |
| spatial_knn_ridge        | generic_shift       | group_by_cell           | random_forest | 52920 |           11 | 0.0288126 |  0.659693    |
| spatial_knn_ridge        | physical_plus_shift | group_by_cell           | ridge         | 52920 |           23 | 0.0544617 |  0.184526    |
| spatial_knn_ridge        | physical_plus_shift | group_by_cell           | random_forest | 52920 |           23 | 0.0193666 |  0.84803     |
| stgcn_diffusion          | physical_knowledge  | leave_target_region_out | ridge         | 52920 |           12 | 0.0770582 |  0.0570458   |
| stgcn_diffusion          | physical_knowledge  | leave_target_region_out | random_forest | 52920 |           12 | 0.0731374 |  0.0730328   |
| stgcn_diffusion          | generic_shift       | leave_target_region_out | ridge         | 52920 |           11 | 0.0860512 | -0.0829554   |
| stgcn_diffusion          | generic_shift       | leave_target_region_out | random_forest | 52920 |           11 | 0.078461  | -0.014878    |
| stgcn_diffusion          | physical_plus_shift | leave_target_region_out | ridge         | 52920 |           23 | 0.0791725 |  0.0432729   |
| stgcn_diffusion          | physical_plus_shift | leave_target_region_out | random_forest | 52920 |           23 | 0.0786469 | -0.137175    |
| stgcn_diffusion          | physical_knowledge  | group_by_cell           | ridge         | 52920 |           12 | 0.07635   |  0.104774    |
| stgcn_diffusion          | physical_knowledge  | group_by_cell           | random_forest | 52920 |           12 | 0.066262  |  0.310607    |
| stgcn_diffusion          | generic_shift       | group_by_cell           | ridge         | 52920 |           11 | 0.0785176 |  0.00208447  |
| stgcn_diffusion          | generic_shift       | group_by_cell           | random_forest | 52920 |           11 | 0.065061  |  0.124347    |
| stgcn_diffusion          | physical_plus_shift | group_by_cell           | ridge         | 52920 |           23 | 0.0754878 |  0.125083    |
| stgcn_diffusion          | physical_plus_shift | group_by_cell           | random_forest | 52920 |           23 | 0.0495835 |  0.459077    |
