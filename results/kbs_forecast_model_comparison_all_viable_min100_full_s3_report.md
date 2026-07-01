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
| graphwavenet_transfer    | CNA             | EAS             |  110 |        0.0397943   |
| graphwavenet_transfer    | CNA             | EAU             |  241 |        0.0198429   |
| graphwavenet_transfer    | CNA             | ENA             |  522 |        0.0407596   |
| graphwavenet_transfer    | CNA             | MED             |  328 |        0.0455082   |
| graphwavenet_transfer    | CNA             | NCA             |  144 |       -0.00852295  |
| graphwavenet_transfer    | CNA             | NEU             | 1000 |        0.142859    |
| graphwavenet_transfer    | CNA             | NWN             |  183 |        0.186263    |
| graphwavenet_transfer    | CNA             | SAU             |  351 |        0.0401159   |
| graphwavenet_transfer    | CNA             | WCE             | 1000 |        0.0961149   |
| graphwavenet_transfer    | CNA             | WNA             |  975 |        0.0806262   |
| graphwavenet_transfer    | EAS             | CNA             |  438 |        0.219938    |
| graphwavenet_transfer    | EAS             | EAU             |  241 |        0.0166839   |
| graphwavenet_transfer    | EAS             | ENA             |  522 |        0.326777    |
| graphwavenet_transfer    | EAS             | MED             |  328 |        0.0130051   |
| graphwavenet_transfer    | EAS             | NCA             |  144 |        0.0152324   |
| graphwavenet_transfer    | EAS             | NEU             | 1000 |        0.0850952   |
| graphwavenet_transfer    | EAS             | NWN             |  183 |        0.0913231   |
| graphwavenet_transfer    | EAS             | SAU             |  351 |        0.0284262   |
| graphwavenet_transfer    | EAS             | WCE             | 1000 |        0.0670217   |
| graphwavenet_transfer    | EAS             | WNA             |  975 |        0.0455081   |
| graphwavenet_transfer    | EAU             | CNA             |  438 |        0.181817    |
| graphwavenet_transfer    | EAU             | EAS             |  110 |       -0.0557014   |
| graphwavenet_transfer    | EAU             | ENA             |  522 |        0.269683    |
| graphwavenet_transfer    | EAU             | MED             |  328 |        0.00174697  |
| graphwavenet_transfer    | EAU             | NCA             |  144 |        0.00815359  |
| graphwavenet_transfer    | EAU             | NEU             | 1000 |        0.0356654   |
| graphwavenet_transfer    | EAU             | NWN             |  183 |        0.161944    |
| graphwavenet_transfer    | EAU             | SAU             |  351 |        0.0028965   |
| graphwavenet_transfer    | EAU             | WCE             | 1000 |        0.0169608   |
| graphwavenet_transfer    | EAU             | WNA             |  975 |        0.0681149   |
| graphwavenet_transfer    | ENA             | CNA             |  438 |        0.0201778   |
| graphwavenet_transfer    | ENA             | EAS             |  110 |        0.124526    |
| graphwavenet_transfer    | ENA             | EAU             |  241 |        0.0430458   |
| graphwavenet_transfer    | ENA             | MED             |  328 |        0.027212    |
| graphwavenet_transfer    | ENA             | NCA             |  144 |       -0.0150645   |
| graphwavenet_transfer    | ENA             | NEU             | 1000 |        0.102678    |
| graphwavenet_transfer    | ENA             | NWN             |  183 |        0.165908    |
| graphwavenet_transfer    | ENA             | SAU             |  351 |        0.0358212   |
| graphwavenet_transfer    | ENA             | WCE             | 1000 |        0.0573301   |
| graphwavenet_transfer    | ENA             | WNA             |  975 |        0.0852494   |
| graphwavenet_transfer    | MED             | CNA             |  438 |        0.191746    |
| graphwavenet_transfer    | MED             | EAS             |  110 |       -0.0557108   |
| graphwavenet_transfer    | MED             | EAU             |  241 |        0.00643003  |
| graphwavenet_transfer    | MED             | ENA             |  522 |        0.2695      |
| graphwavenet_transfer    | MED             | NCA             |  144 |        0.00809136  |
| graphwavenet_transfer    | MED             | NEU             | 1000 |        0.0197008   |
| graphwavenet_transfer    | MED             | NWN             |  183 |        0.13318     |
| graphwavenet_transfer    | MED             | SAU             |  351 |        0.00183255  |
| graphwavenet_transfer    | MED             | WCE             | 1000 |        0.00742988  |
| graphwavenet_transfer    | MED             | WNA             |  975 |        0.050719    |
| graphwavenet_transfer    | NCA             | CNA             |  438 |        0.16016     |
| graphwavenet_transfer    | NCA             | EAS             |  110 |        0.00765274  |
| graphwavenet_transfer    | NCA             | EAU             |  241 |        0.0173341   |
| graphwavenet_transfer    | NCA             | ENA             |  522 |        0.229319    |
| graphwavenet_transfer    | NCA             | MED             |  328 |        0.0295017   |
| graphwavenet_transfer    | NCA             | NEU             | 1000 |        0.15571     |
| graphwavenet_transfer    | NCA             | NWN             |  183 |        0.105381    |
| graphwavenet_transfer    | NCA             | SAU             |  351 |        0.0432887   |
| graphwavenet_transfer    | NCA             | WCE             | 1000 |        0.126879    |
| graphwavenet_transfer    | NCA             | WNA             |  975 |        0.0474487   |
| graphwavenet_transfer    | NEU             | CNA             |  438 |        0.214673    |
| graphwavenet_transfer    | NEU             | EAS             |  110 |       -0.0379037   |
| graphwavenet_transfer    | NEU             | EAU             |  241 |        0.0200018   |
| graphwavenet_transfer    | NEU             | ENA             |  522 |        0.290019    |
| graphwavenet_transfer    | NEU             | MED             |  328 |        0.00670451  |
| graphwavenet_transfer    | NEU             | NCA             |  144 |        0.0217942   |
| graphwavenet_transfer    | NEU             | NWN             |  183 |        0.105485    |
| graphwavenet_transfer    | NEU             | SAU             |  351 |        0.0116197   |
| graphwavenet_transfer    | NEU             | WCE             | 1000 |        0.0021399   |
| graphwavenet_transfer    | NEU             | WNA             |  975 |        0.0499777   |
| graphwavenet_transfer    | NWN             | CNA             |  438 |        0.20634     |
| graphwavenet_transfer    | NWN             | EAS             |  110 |        0.0171311   |
| graphwavenet_transfer    | NWN             | EAU             |  241 |        0.051343    |
| graphwavenet_transfer    | NWN             | ENA             |  522 |        0.251737    |
| graphwavenet_transfer    | NWN             | MED             |  328 |        0.0241308   |
| graphwavenet_transfer    | NWN             | NCA             |  144 |        0.0143333   |
| graphwavenet_transfer    | NWN             | NEU             | 1000 |        0.0340536   |
| graphwavenet_transfer    | NWN             | SAU             |  351 |        0.033427    |
| graphwavenet_transfer    | NWN             | WCE             | 1000 |        0.0419493   |
| graphwavenet_transfer    | NWN             | WNA             |  975 |        0.0110489   |
| graphwavenet_transfer    | SAU             | CNA             |  438 |        0.186324    |
| graphwavenet_transfer    | SAU             | EAS             |  110 |       -0.0109953   |
| graphwavenet_transfer    | SAU             | EAU             |  241 |        0.0142699   |
| graphwavenet_transfer    | SAU             | ENA             |  522 |        0.261576    |
| graphwavenet_transfer    | SAU             | MED             |  328 |        0.00275275  |
| graphwavenet_transfer    | SAU             | NCA             |  144 |        0.00977454  |
| graphwavenet_transfer    | SAU             | NEU             | 1000 |        0.0239637   |
| graphwavenet_transfer    | SAU             | NWN             |  183 |        0.154931    |
| graphwavenet_transfer    | SAU             | WCE             | 1000 |        0.00678794  |
| graphwavenet_transfer    | SAU             | WNA             |  975 |        0.0725307   |
| graphwavenet_transfer    | WCE             | CNA             |  438 |        0.200292    |
| graphwavenet_transfer    | WCE             | EAS             |  110 |       -0.00833573  |
| graphwavenet_transfer    | WCE             | EAU             |  241 |        0.0202545   |
| graphwavenet_transfer    | WCE             | ENA             |  522 |        0.274701    |
| graphwavenet_transfer    | WCE             | MED             |  328 |        0.00489173  |
| graphwavenet_transfer    | WCE             | NCA             |  144 |        0.0151444   |
| graphwavenet_transfer    | WCE             | NEU             | 1000 |        0.0149425   |
| graphwavenet_transfer    | WCE             | NWN             |  183 |        0.167015    |
| graphwavenet_transfer    | WCE             | SAU             |  351 |        0.00961141  |
| graphwavenet_transfer    | WCE             | WNA             |  975 |        0.0757122   |
| graphwavenet_transfer    | WNA             | CNA             |  438 |        0.186141    |
| graphwavenet_transfer    | WNA             | EAS             |  110 |       -0.049721    |
| graphwavenet_transfer    | WNA             | EAU             |  241 |        0.0168777   |
| graphwavenet_transfer    | WNA             | ENA             |  522 |        0.2538      |
| graphwavenet_transfer    | WNA             | MED             |  328 |        0.0135518   |
| graphwavenet_transfer    | WNA             | NCA             |  144 |        0.00381255  |
| graphwavenet_transfer    | WNA             | NEU             | 1000 |        0.031727    |
| graphwavenet_transfer    | WNA             | NWN             |  183 |        0.0374461   |
| graphwavenet_transfer    | WNA             | SAU             |  351 |        0.0292385   |
| graphwavenet_transfer    | WNA             | WCE             | 1000 |        0.0412262   |
| linear_window            | CNA             | EAS             |  110 |        0.407234    |
| linear_window            | CNA             | EAU             |  241 |        0.288059    |
| linear_window            | CNA             | ENA             |  522 |       -0.161092    |
| linear_window            | CNA             | MED             |  328 |        0.0679075   |
| linear_window            | CNA             | NCA             |  144 |       -0.0216126   |
| linear_window            | CNA             | NEU             | 1000 |        0.158887    |
| linear_window            | CNA             | NWN             |  183 |        0.121361    |
| linear_window            | CNA             | SAU             |  351 |        0.123356    |
| linear_window            | CNA             | WCE             | 1000 |        0.0798016   |
| linear_window            | CNA             | WNA             |  975 |        0.051981    |
| linear_window            | EAS             | CNA             |  438 |       -0.0404683   |
| linear_window            | EAS             | EAU             |  241 |        0.146611    |
| linear_window            | EAS             | ENA             |  522 |        0.13538     |
| linear_window            | EAS             | MED             |  328 |        0.0229448   |
| linear_window            | EAS             | NCA             |  144 |       -0.113118    |
| linear_window            | EAS             | NEU             | 1000 |        0.0311146   |
| linear_window            | EAS             | NWN             |  183 |       -0.0380137   |
| linear_window            | EAS             | SAU             |  351 |        0.137444    |
| linear_window            | EAS             | WCE             | 1000 |        0.0739367   |
| linear_window            | EAS             | WNA             |  975 |       -0.0917763   |
| linear_window            | EAU             | CNA             |  438 |        0.0422077   |
| linear_window            | EAU             | EAS             |  110 |       -0.474       |
| linear_window            | EAU             | ENA             |  522 |        0.042321    |
| linear_window            | EAU             | MED             |  328 |        0.0935172   |
| linear_window            | EAU             | NCA             |  144 |       -0.0474919   |
| linear_window            | EAU             | NEU             | 1000 |        0.0353015   |
| linear_window            | EAU             | NWN             |  183 |       -0.041326    |
| linear_window            | EAU             | SAU             |  351 |        0.124057    |
| linear_window            | EAU             | WCE             | 1000 |       -0.0251004   |
| linear_window            | EAU             | WNA             |  975 |       -0.0932207   |
| linear_window            | ENA             | CNA             |  438 |       -0.0993518   |
| linear_window            | ENA             | EAS             |  110 |        0.0676641   |
| linear_window            | ENA             | EAU             |  241 |        0.28716     |
| linear_window            | ENA             | MED             |  328 |        0.0588394   |
| linear_window            | ENA             | NCA             |  144 |        0.0650292   |
| linear_window            | ENA             | NEU             | 1000 |        0.086217    |
| linear_window            | ENA             | NWN             |  183 |        0.0960808   |
| linear_window            | ENA             | SAU             |  351 |        0.0748127   |
| linear_window            | ENA             | WCE             | 1000 |        0.0633597   |
| linear_window            | ENA             | WNA             |  975 |        0.0201789   |
| linear_window            | MED             | CNA             |  438 |       -0.0581972   |
| linear_window            | MED             | EAS             |  110 |        0.0733255   |
| linear_window            | MED             | EAU             |  241 |        0.31486     |
| linear_window            | MED             | ENA             |  522 |       -0.109613    |
| linear_window            | MED             | NCA             |  144 |       -0.00768829  |
| linear_window            | MED             | NEU             | 1000 |        0.0341642   |
| linear_window            | MED             | NWN             |  183 |        0.0112939   |
| linear_window            | MED             | SAU             |  351 |        0.189898    |
| linear_window            | MED             | WCE             | 1000 |        0.00516143  |
| linear_window            | MED             | WNA             |  975 |       -0.0632188   |
| linear_window            | NCA             | CNA             |  438 |       -0.0208045   |
| linear_window            | NCA             | EAS             |  110 |       -0.0236456   |
| linear_window            | NCA             | EAU             |  241 |        0.0247157   |
| linear_window            | NCA             | ENA             |  522 |        0.041473    |
| linear_window            | NCA             | MED             |  328 |        0.048889    |
| linear_window            | NCA             | NEU             | 1000 |        0.170625    |
| linear_window            | NCA             | NWN             |  183 |        0.0465337   |
| linear_window            | NCA             | SAU             |  351 |        0.184452    |
| linear_window            | NCA             | WCE             | 1000 |        0.0948102   |
| linear_window            | NCA             | WNA             |  975 |        0.00106775  |
| linear_window            | NEU             | CNA             |  438 |       -0.146293    |
| linear_window            | NEU             | EAS             |  110 |       -0.184167    |
| linear_window            | NEU             | EAU             |  241 |       -0.149426    |
| linear_window            | NEU             | ENA             |  522 |       -0.0383865   |
| linear_window            | NEU             | MED             |  328 |        0.0824427   |
| linear_window            | NEU             | NCA             |  144 |       -0.13374     |
| linear_window            | NEU             | NWN             |  183 |        0.0717876   |
| linear_window            | NEU             | SAU             |  351 |        0.14701     |
| linear_window            | NEU             | WCE             | 1000 |        0.0209506   |
| linear_window            | NEU             | WNA             |  975 |       -0.0973952   |
| linear_window            | NWN             | CNA             |  438 |       -0.0868547   |
| linear_window            | NWN             | EAS             |  110 |        0.193219    |
| linear_window            | NWN             | EAU             |  241 |       -0.0135244   |
| linear_window            | NWN             | ENA             |  522 |        0.0515046   |
| linear_window            | NWN             | MED             |  328 |        0.11853     |
| linear_window            | NWN             | NCA             |  144 |        0.0236641   |
| linear_window            | NWN             | NEU             | 1000 |        0.0507445   |
| linear_window            | NWN             | SAU             |  351 |        0.15761     |
| linear_window            | NWN             | WCE             | 1000 |       -0.00780424  |
| linear_window            | NWN             | WNA             |  975 |       -0.0928353   |
| linear_window            | SAU             | CNA             |  438 |        0.0632368   |
| linear_window            | SAU             | EAS             |  110 |       -0.0771005   |
| linear_window            | SAU             | EAU             |  241 |        0.000296287 |
| linear_window            | SAU             | ENA             |  522 |        0.0365717   |
| linear_window            | SAU             | MED             |  328 |        0.121331    |
| linear_window            | SAU             | NCA             |  144 |       -0.0671469   |
| linear_window            | SAU             | NEU             | 1000 |        0.0189963   |
| linear_window            | SAU             | NWN             |  183 |       -0.0376526   |
| linear_window            | SAU             | WCE             | 1000 |        0.0217946   |
| linear_window            | SAU             | WNA             |  975 |       -0.0851705   |
| linear_window            | WCE             | CNA             |  438 |        0.028413    |
| linear_window            | WCE             | EAS             |  110 |        0.606384    |
| linear_window            | WCE             | EAU             |  241 |        0.176532    |
| linear_window            | WCE             | ENA             |  522 |        0.0873666   |
| linear_window            | WCE             | MED             |  328 |        0.0712431   |
| linear_window            | WCE             | NCA             |  144 |        0.241809    |
| linear_window            | WCE             | NEU             | 1000 |        0.0589459   |
| linear_window            | WCE             | NWN             |  183 |        0.0796877   |
| linear_window            | WCE             | SAU             |  351 |        0.140165    |
| linear_window            | WCE             | WNA             |  975 |       -0.0588912   |
| linear_window            | WNA             | CNA             |  438 |       -0.0350908   |
| linear_window            | WNA             | EAS             |  110 |       -0.0305798   |
| linear_window            | WNA             | EAU             |  241 |        0.110236    |
| linear_window            | WNA             | ENA             |  522 |        0.11584     |
| linear_window            | WNA             | MED             |  328 |       -0.0592421   |
| linear_window            | WNA             | NCA             |  144 |        0.0802227   |
| linear_window            | WNA             | NEU             | 1000 |        0.0339377   |
| linear_window            | WNA             | NWN             |  183 |       -0.00810152  |
| linear_window            | WNA             | SAU             |  351 |        0.136172    |
| linear_window            | WNA             | WCE             | 1000 |       -0.0258596   |
| patchtst_small           | CNA             | EAS             |  110 |        0.40534     |
| patchtst_small           | CNA             | EAU             |  241 |        0.273811    |
| patchtst_small           | CNA             | ENA             |  522 |       -0.155691    |
| patchtst_small           | CNA             | MED             |  328 |        0.0692145   |
| patchtst_small           | CNA             | NCA             |  144 |       -0.0178633   |
| patchtst_small           | CNA             | NEU             | 1000 |        0.151687    |
| patchtst_small           | CNA             | NWN             |  183 |        0.105756    |
| patchtst_small           | CNA             | SAU             |  351 |        0.116311    |
| patchtst_small           | CNA             | WCE             | 1000 |        0.0756867   |
| patchtst_small           | CNA             | WNA             |  975 |        0.053845    |
| patchtst_small           | EAS             | CNA             |  438 |       -0.0411798   |
| patchtst_small           | EAS             | EAU             |  241 |        0.129583    |
| patchtst_small           | EAS             | ENA             |  522 |        0.134025    |
| patchtst_small           | EAS             | MED             |  328 |        0.020169    |
| patchtst_small           | EAS             | NCA             |  144 |       -0.113926    |
| patchtst_small           | EAS             | NEU             | 1000 |        0.044441    |
| patchtst_small           | EAS             | NWN             |  183 |       -0.00585805  |
| patchtst_small           | EAS             | SAU             |  351 |        0.13434     |
| patchtst_small           | EAS             | WCE             | 1000 |        0.0745975   |
| patchtst_small           | EAS             | WNA             |  975 |       -0.0780221   |
| patchtst_small           | EAU             | CNA             |  438 |        0.0317735   |
| patchtst_small           | EAU             | EAS             |  110 |       -0.467345    |
| patchtst_small           | EAU             | ENA             |  522 |        0.0332533   |
| patchtst_small           | EAU             | MED             |  328 |        0.0980153   |
| patchtst_small           | EAU             | NCA             |  144 |       -0.0495635   |
| patchtst_small           | EAU             | NEU             | 1000 |        0.0457634   |
| patchtst_small           | EAU             | NWN             |  183 |       -0.00611737  |
| patchtst_small           | EAU             | SAU             |  351 |        0.121884    |
| patchtst_small           | EAU             | WCE             | 1000 |       -0.0247985   |
| patchtst_small           | EAU             | WNA             |  975 |       -0.0741831   |
| patchtst_small           | ENA             | CNA             |  438 |       -0.1097      |
| patchtst_small           | ENA             | EAS             |  110 |        0.0761841   |
| patchtst_small           | ENA             | EAU             |  241 |        0.272761    |
| patchtst_small           | ENA             | MED             |  328 |        0.0570945   |
| patchtst_small           | ENA             | NCA             |  144 |        0.0582588   |
| patchtst_small           | ENA             | NEU             | 1000 |        0.0932664   |
| patchtst_small           | ENA             | NWN             |  183 |        0.0881522   |
| patchtst_small           | ENA             | SAU             |  351 |        0.069464    |
| patchtst_small           | ENA             | WCE             | 1000 |        0.0681911   |
| patchtst_small           | ENA             | WNA             |  975 |        0.0207908   |
| patchtst_small           | MED             | CNA             |  438 |       -0.0758705   |
| patchtst_small           | MED             | EAS             |  110 |        0.14141     |
| patchtst_small           | MED             | EAU             |  241 |        0.313502    |
| patchtst_small           | MED             | ENA             |  522 |       -0.124115    |
| patchtst_small           | MED             | NCA             |  144 |       -0.016699    |
| patchtst_small           | MED             | NEU             | 1000 |        0.049832    |
| patchtst_small           | MED             | NWN             |  183 |        0.0402975   |
| patchtst_small           | MED             | SAU             |  351 |        0.186898    |
| patchtst_small           | MED             | WCE             | 1000 |        0.00884953  |
| patchtst_small           | MED             | WNA             |  975 |       -0.0435429   |
| patchtst_small           | NCA             | CNA             |  438 |       -0.0246601   |
| patchtst_small           | NCA             | EAS             |  110 |       -0.0214906   |
| patchtst_small           | NCA             | EAU             |  241 |        0.0103332   |
| patchtst_small           | NCA             | ENA             |  522 |        0.0453175   |
| patchtst_small           | NCA             | MED             |  328 |        0.0490686   |
| patchtst_small           | NCA             | NEU             | 1000 |        0.167404    |
| patchtst_small           | NCA             | NWN             |  183 |        0.0348573   |
| patchtst_small           | NCA             | SAU             |  351 |        0.177732    |
| patchtst_small           | NCA             | WCE             | 1000 |        0.0930066   |
| patchtst_small           | NCA             | WNA             |  975 |        0.00225964  |
| patchtst_small           | NEU             | CNA             |  438 |       -0.173022    |
| patchtst_small           | NEU             | EAS             |  110 |       -0.15391     |
| patchtst_small           | NEU             | EAU             |  241 |       -0.167084    |
| patchtst_small           | NEU             | ENA             |  522 |       -0.0605615   |
| patchtst_small           | NEU             | MED             |  328 |        0.0820009   |
| patchtst_small           | NEU             | NCA             |  144 |       -0.145626    |
| patchtst_small           | NEU             | NWN             |  183 |        0.0798358   |
| patchtst_small           | NEU             | SAU             |  351 |        0.142561    |
| patchtst_small           | NEU             | WCE             | 1000 |        0.0219104   |
| patchtst_small           | NEU             | WNA             |  975 |       -0.0907828   |
| patchtst_small           | NWN             | CNA             |  438 |       -0.085641    |
| patchtst_small           | NWN             | EAS             |  110 |        0.0998667   |
| patchtst_small           | NWN             | EAU             |  241 |       -0.00851618  |
| patchtst_small           | NWN             | ENA             |  522 |        0.0616168   |
| patchtst_small           | NWN             | MED             |  328 |        0.12091     |
| patchtst_small           | NWN             | NCA             |  144 |        0.0280333   |
| patchtst_small           | NWN             | NEU             | 1000 |        0.0502363   |
| patchtst_small           | NWN             | SAU             |  351 |        0.157071    |
| patchtst_small           | NWN             | WCE             | 1000 |       -0.00126172  |
| patchtst_small           | NWN             | WNA             |  975 |       -0.0871611   |
| patchtst_small           | SAU             | CNA             |  438 |        0.0633417   |
| patchtst_small           | SAU             | EAS             |  110 |       -0.118334    |
| patchtst_small           | SAU             | EAU             |  241 |       -0.0019323   |
| patchtst_small           | SAU             | ENA             |  522 |        0.0409535   |
| patchtst_small           | SAU             | MED             |  328 |        0.131999    |
| patchtst_small           | SAU             | NCA             |  144 |       -0.0570108   |
| patchtst_small           | SAU             | NEU             | 1000 |        0.0244953   |
| patchtst_small           | SAU             | NWN             |  183 |       -0.0108689   |
| patchtst_small           | SAU             | WCE             | 1000 |        0.0262246   |
| patchtst_small           | SAU             | WNA             |  975 |       -0.0678319   |
| patchtst_small           | WCE             | CNA             |  438 |        0.00406043  |
| patchtst_small           | WCE             | EAS             |  110 |        0.656242    |
| patchtst_small           | WCE             | EAU             |  241 |        0.157989    |
| patchtst_small           | WCE             | ENA             |  522 |        0.0667615   |
| patchtst_small           | WCE             | MED             |  328 |        0.0651984   |
| patchtst_small           | WCE             | NCA             |  144 |        0.227174    |
| patchtst_small           | WCE             | NEU             | 1000 |        0.0599353   |
| patchtst_small           | WCE             | NWN             |  183 |        0.0790679   |
| patchtst_small           | WCE             | SAU             |  351 |        0.129772    |
| patchtst_small           | WCE             | WNA             |  975 |       -0.052732    |
| patchtst_small           | WNA             | CNA             |  438 |       -0.0568851   |
| patchtst_small           | WNA             | EAS             |  110 |       -0.137667    |
| patchtst_small           | WNA             | EAU             |  241 |        0.0919978   |
| patchtst_small           | WNA             | ENA             |  522 |        0.114545    |
| patchtst_small           | WNA             | MED             |  328 |       -0.0657035   |
| patchtst_small           | WNA             | NCA             |  144 |        0.0614887   |
| patchtst_small           | WNA             | NEU             | 1000 |        0.0490038   |
| patchtst_small           | WNA             | NWN             |  183 |       -0.0229657   |
| patchtst_small           | WNA             | SAU             |  351 |        0.123675    |
| patchtst_small           | WNA             | WCE             | 1000 |       -0.015765    |
| regional_doy_climatology | CNA             | EAS             |  110 |       -1.81385     |
| regional_doy_climatology | CNA             | EAU             |  241 |       -0.110242    |
| regional_doy_climatology | CNA             | ENA             |  522 |       -0.557076    |
| regional_doy_climatology | CNA             | MED             |  328 |        0.344803    |
| regional_doy_climatology | CNA             | NCA             |  144 |        0.893314    |
| regional_doy_climatology | CNA             | NEU             | 1000 |        0.0159305   |
| regional_doy_climatology | CNA             | NWN             |  183 |       -0.19641     |
| regional_doy_climatology | CNA             | SAU             |  351 |        0.2294      |
| regional_doy_climatology | CNA             | WCE             | 1000 |       -0.0330287   |
| regional_doy_climatology | CNA             | WNA             |  975 |        0.1392      |
| regional_doy_climatology | EAS             | CNA             |  438 |        3.01123     |
| regional_doy_climatology | EAS             | EAU             |  241 |        3.12179     |
| regional_doy_climatology | EAS             | ENA             |  522 |        2.18763     |
| regional_doy_climatology | EAS             | MED             |  328 |        3.77667     |
| regional_doy_climatology | EAS             | NCA             |  144 |        4.29429     |
| regional_doy_climatology | EAS             | NEU             | 1000 |        3.01106     |
| regional_doy_climatology | EAS             | NWN             |  183 |        2.81549     |
| regional_doy_climatology | EAS             | SAU             |  351 |        3.27918     |
| regional_doy_climatology | EAS             | WCE             | 1000 |        2.93724     |
| regional_doy_climatology | EAS             | WNA             |  975 |        3.49015     |
| regional_doy_climatology | EAU             | CNA             |  438 |        0.282819    |
| regional_doy_climatology | EAU             | EAS             |  110 |       -1.33372     |
| regional_doy_climatology | EAU             | ENA             |  522 |       -0.351761    |
| regional_doy_climatology | EAU             | MED             |  328 |        0.468011    |
| regional_doy_climatology | EAU             | NCA             |  144 |        1.1281      |
| regional_doy_climatology | EAU             | NEU             | 1000 |        0.170417    |
| regional_doy_climatology | EAU             | NWN             |  183 |        0.01432     |
| regional_doy_climatology | EAU             | SAU             |  351 |        0.532103    |
| regional_doy_climatology | EAU             | WCE             | 1000 |        0.151477    |
| regional_doy_climatology | EAU             | WNA             |  975 |        0.160134    |
| regional_doy_climatology | ENA             | CNA             |  438 |        0.734675    |
| regional_doy_climatology | ENA             | EAS             |  110 |       -1.17278     |
| regional_doy_climatology | ENA             | EAU             |  241 |        0.48445     |
| regional_doy_climatology | ENA             | MED             |  328 |        1.03475     |
| regional_doy_climatology | ENA             | NCA             |  144 |        1.71267     |
| regional_doy_climatology | ENA             | NEU             | 1000 |        0.510382    |
| regional_doy_climatology | ENA             | NWN             |  183 |        0.377848    |
| regional_doy_climatology | ENA             | SAU             |  351 |        0.888504    |
| regional_doy_climatology | ENA             | WCE             | 1000 |        0.497613    |
| regional_doy_climatology | ENA             | WNA             |  975 |        0.696154    |
| regional_doy_climatology | MED             | CNA             |  438 |       -0.136096    |
| regional_doy_climatology | MED             | EAS             |  110 |       -1.65667     |
| regional_doy_climatology | MED             | EAU             |  241 |       -0.394873    |
| regional_doy_climatology | MED             | ENA             |  522 |       -0.684155    |
| regional_doy_climatology | MED             | NCA             |  144 |        0.644253    |
| regional_doy_climatology | MED             | NEU             | 1000 |       -0.197593    |
| regional_doy_climatology | MED             | NWN             |  183 |       -0.376459    |
| regional_doy_climatology | MED             | SAU             |  351 |        0.142412    |
| regional_doy_climatology | MED             | WCE             | 1000 |       -0.215257    |
| regional_doy_climatology | MED             | WNA             |  975 |       -0.212434    |
| regional_doy_climatology | NCA             | CNA             |  438 |       -0.677282    |
| regional_doy_climatology | NCA             | EAS             |  110 |       -2.21432     |
| regional_doy_climatology | NCA             | EAU             |  241 |       -0.780145    |
| regional_doy_climatology | NCA             | ENA             |  522 |       -1.08305     |
| regional_doy_climatology | NCA             | MED             |  328 |       -0.374613    |
| regional_doy_climatology | NCA             | NEU             | 1000 |       -0.487923    |
| regional_doy_climatology | NCA             | NWN             |  183 |       -0.750943    |
| regional_doy_climatology | NCA             | SAU             |  351 |       -0.362901    |
| regional_doy_climatology | NCA             | WCE             | 1000 |       -0.557299    |
| regional_doy_climatology | NCA             | WNA             |  975 |       -0.467222    |
| regional_doy_climatology | NEU             | CNA             |  438 |        0.152222    |
| regional_doy_climatology | NEU             | EAS             |  110 |       -1.62572     |
| regional_doy_climatology | NEU             | EAU             |  241 |       -0.0551189   |
| regional_doy_climatology | NEU             | ENA             |  522 |       -0.470576    |
| regional_doy_climatology | NEU             | MED             |  328 |        0.426468    |
| regional_doy_climatology | NEU             | NCA             |  144 |        0.996224    |
| regional_doy_climatology | NEU             | NWN             |  183 |       -0.168215    |
| regional_doy_climatology | NEU             | SAU             |  351 |        0.313877    |
| regional_doy_climatology | NEU             | WCE             | 1000 |        0.00343982  |
| regional_doy_climatology | NEU             | WNA             |  975 |        0.183366    |
| regional_doy_climatology | NWN             | CNA             |  438 |        0.374672    |
| regional_doy_climatology | NWN             | EAS             |  110 |       -1.44579     |
| regional_doy_climatology | NWN             | EAU             |  241 |        0.11023     |
| regional_doy_climatology | NWN             | ENA             |  522 |       -0.292863    |
| regional_doy_climatology | NWN             | MED             |  328 |        0.604575    |
| regional_doy_climatology | NWN             | NCA             |  144 |        1.2428      |
| regional_doy_climatology | NWN             | NEU             | 1000 |        0.143177    |
| regional_doy_climatology | NWN             | SAU             |  351 |        0.512798    |
| regional_doy_climatology | NWN             | WCE             | 1000 |        0.155125    |
| regional_doy_climatology | NWN             | WNA             |  975 |        0.320105    |
| regional_doy_climatology | SAU             | CNA             |  438 |       -0.227357    |
| regional_doy_climatology | SAU             | EAS             |  110 |       -1.92734     |
| regional_doy_climatology | SAU             | EAU             |  241 |       -0.3613      |
| regional_doy_climatology | SAU             | ENA             |  522 |       -0.75106     |
| regional_doy_climatology | SAU             | MED             |  328 |        0.0784903   |
| regional_doy_climatology | SAU             | NCA             |  144 |        0.582668    |
| regional_doy_climatology | SAU             | NEU             | 1000 |       -0.187757    |
| regional_doy_climatology | SAU             | NWN             |  183 |       -0.418267    |
| regional_doy_climatology | SAU             | WCE             | 1000 |       -0.232321    |
| regional_doy_climatology | SAU             | WNA             |  975 |       -0.091733    |
| regional_doy_climatology | WCE             | CNA             |  438 |        0.0955983   |
| regional_doy_climatology | WCE             | EAS             |  110 |       -1.68242     |
| regional_doy_climatology | WCE             | EAU             |  241 |       -0.0873269   |
| regional_doy_climatology | WCE             | ENA             |  522 |       -0.50627     |
| regional_doy_climatology | WCE             | MED             |  328 |        0.407556    |
| regional_doy_climatology | WCE             | NCA             |  144 |        0.954854    |
| regional_doy_climatology | WCE             | NEU             | 1000 |        0.0274755   |
| regional_doy_climatology | WCE             | NWN             |  183 |       -0.157306    |
| regional_doy_climatology | WCE             | SAU             |  351 |        0.292509    |
| regional_doy_climatology | WCE             | WNA             |  975 |        0.184091    |
| regional_doy_climatology | WNA             | CNA             |  438 |        0.156543    |
| regional_doy_climatology | WNA             | EAS             |  110 |       -1.37559     |
| regional_doy_climatology | WNA             | EAU             |  241 |       -0.170542    |
| regional_doy_climatology | WNA             | ENA             |  522 |       -0.462289    |
| regional_doy_climatology | WNA             | MED             |  328 |        0.31725     |
| regional_doy_climatology | WNA             | NCA             |  144 |        1.00846     |
| regional_doy_climatology | WNA             | NEU             | 1000 |        0.033198    |
| regional_doy_climatology | WNA             | NWN             |  183 |       -0.0983048   |
| regional_doy_climatology | WNA             | SAU             |  351 |        0.432435    |
| regional_doy_climatology | WNA             | WCE             | 1000 |        0.0336438   |
| spatial_knn_ridge        | CNA             | EAS             |  110 |       -0.0308225   |
| spatial_knn_ridge        | CNA             | EAU             |  241 |       -0.0153574   |
| spatial_knn_ridge        | CNA             | ENA             |  522 |       -0.0832291   |
| spatial_knn_ridge        | CNA             | MED             |  328 |        0.0186985   |
| spatial_knn_ridge        | CNA             | NCA             |  144 |        0.111891    |
| spatial_knn_ridge        | CNA             | NEU             | 1000 |       -0.0595742   |
| spatial_knn_ridge        | CNA             | NWN             |  183 |        0.0710216   |
| spatial_knn_ridge        | CNA             | SAU             |  351 |       -0.0256182   |
| spatial_knn_ridge        | CNA             | WCE             | 1000 |       -0.0723241   |
| spatial_knn_ridge        | CNA             | WNA             |  975 |        0.0242992   |
| spatial_knn_ridge        | EAS             | CNA             |  438 |        0.159883    |
| spatial_knn_ridge        | EAS             | EAU             |  241 |        0.0925222   |
| spatial_knn_ridge        | EAS             | ENA             |  522 |        0.0735518   |
| spatial_knn_ridge        | EAS             | MED             |  328 |        0.133141    |
| spatial_knn_ridge        | EAS             | NCA             |  144 |        0.248041    |
| spatial_knn_ridge        | EAS             | NEU             | 1000 |        0.00117507  |
| spatial_knn_ridge        | EAS             | NWN             |  183 |        0.0892572   |
| spatial_knn_ridge        | EAS             | SAU             |  351 |        0.0915802   |
| spatial_knn_ridge        | EAS             | WCE             | 1000 |        0.0169036   |
| spatial_knn_ridge        | EAS             | WNA             |  975 |        0.0819363   |
| spatial_knn_ridge        | EAU             | CNA             |  438 |        0.0370055   |
| spatial_knn_ridge        | EAU             | EAS             |  110 |       -0.0462349   |
| spatial_knn_ridge        | EAU             | ENA             |  522 |       -0.0440047   |
| spatial_knn_ridge        | EAU             | MED             |  328 |        0.0342938   |
| spatial_knn_ridge        | EAU             | NCA             |  144 |        0.135144    |
| spatial_knn_ridge        | EAU             | NEU             | 1000 |       -0.0559434   |
| spatial_knn_ridge        | EAU             | NWN             |  183 |        0.051268    |
| spatial_knn_ridge        | EAU             | SAU             |  351 |       -0.00691449  |
| spatial_knn_ridge        | EAU             | WCE             | 1000 |       -0.0598681   |
| spatial_knn_ridge        | EAU             | WNA             |  975 |        0.0225176   |
| spatial_knn_ridge        | ENA             | CNA             |  438 |        0.125472    |
| spatial_knn_ridge        | ENA             | EAS             |  110 |        0.0771634   |
| spatial_knn_ridge        | ENA             | EAU             |  241 |        0.0985069   |
| spatial_knn_ridge        | ENA             | MED             |  328 |        0.149163    |
| spatial_knn_ridge        | ENA             | NCA             |  144 |        0.277142    |
| spatial_knn_ridge        | ENA             | NEU             | 1000 |        0.00405796  |
| spatial_knn_ridge        | ENA             | NWN             |  183 |        0.167395    |
| spatial_knn_ridge        | ENA             | SAU             |  351 |        0.0812992   |
| spatial_knn_ridge        | ENA             | WCE             | 1000 |        0.0010633   |
| spatial_knn_ridge        | ENA             | WNA             |  975 |        0.13683     |
| spatial_knn_ridge        | MED             | CNA             |  438 |        0.010144    |
| spatial_knn_ridge        | MED             | EAS             |  110 |       -0.0694716   |
| spatial_knn_ridge        | MED             | EAU             |  241 |       -0.0274185   |
| spatial_knn_ridge        | MED             | ENA             |  522 |       -0.0577706   |
| spatial_knn_ridge        | MED             | NCA             |  144 |        0.0921963   |
| spatial_knn_ridge        | MED             | NEU             | 1000 |       -0.0702692   |
| spatial_knn_ridge        | MED             | NWN             |  183 |        0.0240324   |
| spatial_knn_ridge        | MED             | SAU             |  351 |       -0.0310493   |
| spatial_knn_ridge        | MED             | WCE             | 1000 |       -0.0750362   |
| spatial_knn_ridge        | MED             | WNA             |  975 |       -0.00603726  |
| spatial_knn_ridge        | NCA             | CNA             |  438 |       -0.0644941   |
| spatial_knn_ridge        | NCA             | EAS             |  110 |       -0.116677    |
| spatial_knn_ridge        | NCA             | EAU             |  241 |       -0.0844815   |
| spatial_knn_ridge        | NCA             | ENA             |  522 |       -0.108798    |
| spatial_knn_ridge        | NCA             | MED             |  328 |       -0.062803    |
| spatial_knn_ridge        | NCA             | NEU             | 1000 |       -0.0965983   |
| spatial_knn_ridge        | NCA             | NWN             |  183 |       -0.0100375   |
| spatial_knn_ridge        | NCA             | SAU             |  351 |       -0.0799955   |
| spatial_knn_ridge        | NCA             | WCE             | 1000 |       -0.105814    |
| spatial_knn_ridge        | NCA             | WNA             |  975 |       -0.0625346   |
| spatial_knn_ridge        | NEU             | CNA             |  438 |        0.152157    |
| spatial_knn_ridge        | NEU             | EAS             |  110 |        0.0380146   |
| spatial_knn_ridge        | NEU             | EAU             |  241 |        0.0989604   |
| spatial_knn_ridge        | NEU             | ENA             |  522 |        0.0353562   |
| spatial_knn_ridge        | NEU             | MED             |  328 |        0.147788    |
| spatial_knn_ridge        | NEU             | NCA             |  144 |        0.281501    |
| spatial_knn_ridge        | NEU             | NWN             |  183 |        0.129911    |
| spatial_knn_ridge        | NEU             | SAU             |  351 |        0.086112    |
| spatial_knn_ridge        | NEU             | WCE             | 1000 |        0.00428032  |
| spatial_knn_ridge        | NEU             | WNA             |  975 |        0.117459    |
| spatial_knn_ridge        | NWN             | CNA             |  438 |        0.127425    |
| spatial_knn_ridge        | NWN             | EAS             |  110 |       -0.0113627   |
| spatial_knn_ridge        | NWN             | EAU             |  241 |        0.0557248   |
| spatial_knn_ridge        | NWN             | ENA             |  522 |        0.104939    |
| spatial_knn_ridge        | NWN             | MED             |  328 |        0.0664983   |
| spatial_knn_ridge        | NWN             | NCA             |  144 |        0.13956     |
| spatial_knn_ridge        | NWN             | NEU             | 1000 |       -0.00963851  |
| spatial_knn_ridge        | NWN             | SAU             |  351 |        0.0625234   |
| spatial_knn_ridge        | NWN             | WCE             | 1000 |        0.00863781  |
| spatial_knn_ridge        | NWN             | WNA             |  975 |        9.26597e-05 |
| spatial_knn_ridge        | SAU             | CNA             |  438 |        0.0445978   |
| spatial_knn_ridge        | SAU             | EAS             |  110 |       -0.0178513   |
| spatial_knn_ridge        | SAU             | EAU             |  241 |        0.0118147   |
| spatial_knn_ridge        | SAU             | ENA             |  522 |       -0.048074    |
| spatial_knn_ridge        | SAU             | MED             |  328 |        0.0474222   |
| spatial_knn_ridge        | SAU             | NCA             |  144 |        0.157304    |
| spatial_knn_ridge        | SAU             | NEU             | 1000 |       -0.0473617   |
| spatial_knn_ridge        | SAU             | NWN             |  183 |        0.0723296   |
| spatial_knn_ridge        | SAU             | WCE             | 1000 |       -0.0560263   |
| spatial_knn_ridge        | SAU             | WNA             |  975 |        0.0454984   |
| spatial_knn_ridge        | WCE             | CNA             |  438 |        0.142961    |
| spatial_knn_ridge        | WCE             | EAS             |  110 |        0.0574015   |
| spatial_knn_ridge        | WCE             | EAU             |  241 |        0.0981229   |
| spatial_knn_ridge        | WCE             | ENA             |  522 |        0.0191542   |
| spatial_knn_ridge        | WCE             | MED             |  328 |        0.146798    |
| spatial_knn_ridge        | WCE             | NCA             |  144 |        0.28368     |
| spatial_knn_ridge        | WCE             | NEU             | 1000 |        0.00103814  |
| spatial_knn_ridge        | WCE             | NWN             |  183 |        0.142302    |
| spatial_knn_ridge        | WCE             | SAU             |  351 |        0.0815646   |
| spatial_knn_ridge        | WCE             | WNA             |  975 |        0.127919    |
| spatial_knn_ridge        | WNA             | CNA             |  438 |        0.0513398   |
| spatial_knn_ridge        | WNA             | EAS             |  110 |       -0.0701285   |
| spatial_knn_ridge        | WNA             | EAU             |  241 |        0.00387494  |
| spatial_knn_ridge        | WNA             | ENA             |  522 |       -0.00363032  |
| spatial_knn_ridge        | WNA             | MED             |  328 |        0.0309419   |
| spatial_knn_ridge        | WNA             | NCA             |  144 |        0.113109    |
| spatial_knn_ridge        | WNA             | NEU             | 1000 |       -0.0454443   |
| spatial_knn_ridge        | WNA             | NWN             |  183 |        0.0249193   |
| spatial_knn_ridge        | WNA             | SAU             |  351 |        0.0113225   |
| spatial_knn_ridge        | WNA             | WCE             | 1000 |       -0.0352271   |
| stgcn_diffusion          | CNA             | EAS             |  110 |        0.462583    |
| stgcn_diffusion          | CNA             | EAU             |  241 |        0.0420106   |
| stgcn_diffusion          | CNA             | ENA             |  522 |        0.00676768  |
| stgcn_diffusion          | CNA             | MED             |  328 |        0.0512264   |
| stgcn_diffusion          | CNA             | NCA             |  144 |        0.000394123 |
| stgcn_diffusion          | CNA             | NEU             | 1000 |        0.0976968   |
| stgcn_diffusion          | CNA             | NWN             |  183 |        0.192823    |
| stgcn_diffusion          | CNA             | SAU             |  351 |        0.0334789   |
| stgcn_diffusion          | CNA             | WCE             | 1000 |        0.055822    |
| stgcn_diffusion          | CNA             | WNA             |  975 |        0.0771824   |
| stgcn_diffusion          | EAS             | CNA             |  438 |        0.115717    |
| stgcn_diffusion          | EAS             | EAU             |  241 |        0.022582    |
| stgcn_diffusion          | EAS             | ENA             |  522 |        0.164783    |
| stgcn_diffusion          | EAS             | MED             |  328 |        0.00976964  |
| stgcn_diffusion          | EAS             | NCA             |  144 |        0.0070772   |
| stgcn_diffusion          | EAS             | NEU             | 1000 |        0.0363686   |
| stgcn_diffusion          | EAS             | NWN             |  183 |        0.0925756   |
| stgcn_diffusion          | EAS             | SAU             |  351 |        0.0141649   |
| stgcn_diffusion          | EAS             | WCE             | 1000 |        0.0222797   |
| stgcn_diffusion          | EAS             | WNA             |  975 |        0.0130184   |
| stgcn_diffusion          | EAU             | CNA             |  438 |        0.0706018   |
| stgcn_diffusion          | EAU             | EAS             |  110 |       -0.040093    |
| stgcn_diffusion          | EAU             | ENA             |  522 |        0.113443    |
| stgcn_diffusion          | EAU             | MED             |  328 |       -0.000935402 |
| stgcn_diffusion          | EAU             | NCA             |  144 |       -0.00319893  |
| stgcn_diffusion          | EAU             | NEU             | 1000 |        0.0255992   |
| stgcn_diffusion          | EAU             | NWN             |  183 |        0.131093    |
| stgcn_diffusion          | EAU             | SAU             |  351 |       -0.00113951  |
| stgcn_diffusion          | EAU             | WCE             | 1000 |        0.00741113  |
| stgcn_diffusion          | EAU             | WNA             |  975 |        0.0275557   |
| stgcn_diffusion          | ENA             | CNA             |  438 |        0.0141476   |
| stgcn_diffusion          | ENA             | EAS             |  110 |        0.140031    |
| stgcn_diffusion          | ENA             | EAU             |  241 |        0.0642156   |
| stgcn_diffusion          | ENA             | MED             |  328 |        0.037787    |
| stgcn_diffusion          | ENA             | NCA             |  144 |       -0.00479566  |
| stgcn_diffusion          | ENA             | NEU             | 1000 |        0.0849753   |
| stgcn_diffusion          | ENA             | NWN             |  183 |        0.18228     |
| stgcn_diffusion          | ENA             | SAU             |  351 |        0.0373088   |
| stgcn_diffusion          | ENA             | WCE             | 1000 |        0.0449104   |
| stgcn_diffusion          | ENA             | WNA             |  975 |        0.0775446   |
| stgcn_diffusion          | MED             | CNA             |  438 |        0.0764399   |
| stgcn_diffusion          | MED             | EAS             |  110 |       -0.0221103   |
| stgcn_diffusion          | MED             | EAU             |  241 |        0.0145717   |
| stgcn_diffusion          | MED             | ENA             |  522 |        0.109392    |
| stgcn_diffusion          | MED             | NCA             |  144 |       -0.000816828 |
| stgcn_diffusion          | MED             | NEU             | 1000 |        0.0299982   |
| stgcn_diffusion          | MED             | NWN             |  183 |        0.140016    |
| stgcn_diffusion          | MED             | SAU             |  351 |       -0.000225739 |
| stgcn_diffusion          | MED             | WCE             | 1000 |        0.00547013  |
| stgcn_diffusion          | MED             | WNA             |  975 |        0.039866    |
| stgcn_diffusion          | NCA             | CNA             |  438 |        0.0829892   |
| stgcn_diffusion          | NCA             | EAS             |  110 |        0.963289    |
| stgcn_diffusion          | NCA             | EAU             |  241 |        0.09704     |
| stgcn_diffusion          | NCA             | ENA             |  522 |        0.143146    |
| stgcn_diffusion          | NCA             | MED             |  328 |        0.0333838   |
| stgcn_diffusion          | NCA             | NEU             | 1000 |        0.115862    |
| stgcn_diffusion          | NCA             | NWN             |  183 |        0.107471    |
| stgcn_diffusion          | NCA             | SAU             |  351 |        0.0356766   |
| stgcn_diffusion          | NCA             | WCE             | 1000 |        0.0881691   |
| stgcn_diffusion          | NCA             | WNA             |  975 |        0.0425863   |
| stgcn_diffusion          | NEU             | CNA             |  438 |        0.12672     |
| stgcn_diffusion          | NEU             | EAS             |  110 |        0.034836    |
| stgcn_diffusion          | NEU             | EAU             |  241 |        0.0354144   |
| stgcn_diffusion          | NEU             | ENA             |  522 |        0.1701      |
| stgcn_diffusion          | NEU             | MED             |  328 |        0.0163786   |
| stgcn_diffusion          | NEU             | NCA             |  144 |        0.0204183   |
| stgcn_diffusion          | NEU             | NWN             |  183 |        0.0675415   |
| stgcn_diffusion          | NEU             | SAU             |  351 |        0.02492     |
| stgcn_diffusion          | NEU             | WCE             | 1000 |        0.0144978   |
| stgcn_diffusion          | NEU             | WNA             |  975 |        0.019376    |
| stgcn_diffusion          | NWN             | CNA             |  438 |        0.208774    |
| stgcn_diffusion          | NWN             | EAS             |  110 |        0.23338     |
| stgcn_diffusion          | NWN             | EAU             |  241 |        0.127465    |
| stgcn_diffusion          | NWN             | ENA             |  522 |        0.292736    |
| stgcn_diffusion          | NWN             | MED             |  328 |        0.0708784   |
| stgcn_diffusion          | NWN             | NCA             |  144 |        0.0351002   |
| stgcn_diffusion          | NWN             | NEU             | 1000 |        0.0917986   |
| stgcn_diffusion          | NWN             | SAU             |  351 |        0.0966396   |
| stgcn_diffusion          | NWN             | WCE             | 1000 |        0.10886     |
| stgcn_diffusion          | NWN             | WNA             |  975 |        0.00644281  |
| stgcn_diffusion          | SAU             | CNA             |  438 |        0.0841744   |
| stgcn_diffusion          | SAU             | EAS             |  110 |       -0.00957535  |
| stgcn_diffusion          | SAU             | EAU             |  241 |        0.0194197   |
| stgcn_diffusion          | SAU             | ENA             |  522 |        0.115559    |
| stgcn_diffusion          | SAU             | MED             |  328 |        0.00100872  |
| stgcn_diffusion          | SAU             | NCA             |  144 |        0.00210587  |
| stgcn_diffusion          | SAU             | NEU             | 1000 |        0.0388605   |
| stgcn_diffusion          | SAU             | NWN             |  183 |        0.14509     |
| stgcn_diffusion          | SAU             | WCE             | 1000 |        0.009421    |
| stgcn_diffusion          | SAU             | WNA             |  975 |        0.0476542   |
| stgcn_diffusion          | WCE             | CNA             |  438 |        0.0909643   |
| stgcn_diffusion          | WCE             | EAS             |  110 |        0.0114694   |
| stgcn_diffusion          | WCE             | EAU             |  241 |        0.0300073   |
| stgcn_diffusion          | WCE             | ENA             |  522 |        0.119081    |
| stgcn_diffusion          | WCE             | MED             |  328 |        0.00618766  |
| stgcn_diffusion          | WCE             | NCA             |  144 |        0.00701208  |
| stgcn_diffusion          | WCE             | NEU             | 1000 |        0.0189553   |
| stgcn_diffusion          | WCE             | NWN             |  183 |        0.149736    |
| stgcn_diffusion          | WCE             | SAU             |  351 |        0.00395744  |
| stgcn_diffusion          | WCE             | WNA             |  975 |        0.051127    |
| stgcn_diffusion          | WNA             | CNA             |  438 |        0.101634    |
| stgcn_diffusion          | WNA             | EAS             |  110 |       -0.0446865   |
| stgcn_diffusion          | WNA             | EAU             |  241 |        0.0249542   |
| stgcn_diffusion          | WNA             | ENA             |  522 |        0.145713    |
| stgcn_diffusion          | WNA             | MED             |  328 |        0.0104775   |
| stgcn_diffusion          | WNA             | NCA             |  144 |        0.00218511  |
| stgcn_diffusion          | WNA             | NEU             | 1000 |        0.0182392   |
| stgcn_diffusion          | WNA             | NWN             |  183 |        0.0693217   |
| stgcn_diffusion          | WNA             | SAU             |  351 |        0.0184558   |
| stgcn_diffusion          | WNA             | WCE             | 1000 |        0.0221213   |

## KBS predictive comparison

| forecast_model           | feature_set         | cv_kind                 | estimator     |     n |   n_features |       mae |           r2 |
|:-------------------------|:--------------------|:------------------------|:--------------|------:|-------------:|----------:|-------------:|
| graphwavenet_transfer    | physical_knowledge  | leave_target_region_out | ridge         | 52920 |           12 | 0.0947246 |  0.0788495   |
| graphwavenet_transfer    | physical_knowledge  | leave_target_region_out | random_forest | 52920 |           12 | 0.0817047 |  0.168235    |
| graphwavenet_transfer    | generic_shift       | leave_target_region_out | ridge         | 52920 |           11 | 0.103683  | -0.111536    |
| graphwavenet_transfer    | generic_shift       | leave_target_region_out | random_forest | 52920 |           11 | 0.0954416 | -0.135326    |
| graphwavenet_transfer    | physical_plus_shift | leave_target_region_out | ridge         | 52920 |           23 | 0.0958463 |  0.0394615   |
| graphwavenet_transfer    | physical_plus_shift | leave_target_region_out | random_forest | 52920 |           23 | 0.076355  |  0.179281    |
| graphwavenet_transfer    | physical_knowledge  | group_by_cell           | ridge         | 52920 |           12 | 0.0939737 |  0.131032    |
| graphwavenet_transfer    | physical_knowledge  | group_by_cell           | random_forest | 52920 |           12 | 0.0759975 |  0.299126    |
| graphwavenet_transfer    | generic_shift       | group_by_cell           | ridge         | 52920 |           11 | 0.0922609 |  0.00391377  |
| graphwavenet_transfer    | generic_shift       | group_by_cell           | random_forest | 52920 |           11 | 0.0810409 |  0.130589    |
| graphwavenet_transfer    | physical_plus_shift | group_by_cell           | ridge         | 52920 |           23 | 0.0921738 |  0.124201    |
| graphwavenet_transfer    | physical_plus_shift | group_by_cell           | random_forest | 52920 |           23 | 0.0618042 |  0.392864    |
| linear_window            | physical_knowledge  | leave_target_region_out | ridge         | 52920 |           12 | 1.13404   | -0.00267156  |
| linear_window            | physical_knowledge  | leave_target_region_out | random_forest | 52920 |           12 | 1.18167   | -0.109547    |
| linear_window            | generic_shift       | leave_target_region_out | ridge         | 52920 |           11 | 1.13167   |  0.000215897 |
| linear_window            | generic_shift       | leave_target_region_out | random_forest | 52920 |           11 | 1.13479   | -0.00286465  |
| linear_window            | physical_plus_shift | leave_target_region_out | ridge         | 52920 |           23 | 1.133     | -0.00111457  |
| linear_window            | physical_plus_shift | leave_target_region_out | random_forest | 52920 |           23 | 1.18037   | -0.106931    |
| linear_window            | physical_knowledge  | group_by_cell           | ridge         | 52920 |           12 | 1.13485   | -0.0063637   |
| linear_window            | physical_knowledge  | group_by_cell           | random_forest | 52920 |           12 | 1.20341   | -0.239564    |
| linear_window            | generic_shift       | group_by_cell           | ridge         | 52920 |           11 | 1.13184   | -0.000169831 |
| linear_window            | generic_shift       | group_by_cell           | random_forest | 52920 |           11 | 1.13846   | -0.0186027   |
| linear_window            | physical_plus_shift | group_by_cell           | ridge         | 52920 |           23 | 1.13445   | -0.0047739   |
| linear_window            | physical_plus_shift | group_by_cell           | random_forest | 52920 |           23 | 1.20405   | -0.245523    |
| patchtst_small           | physical_knowledge  | leave_target_region_out | ridge         | 52920 |           12 | 1.13846   | -0.00253458  |
| patchtst_small           | physical_knowledge  | leave_target_region_out | random_forest | 52920 |           12 | 1.18649   | -0.11287     |
| patchtst_small           | generic_shift       | leave_target_region_out | ridge         | 52920 |           11 | 1.13603   |  0.000298103 |
| patchtst_small           | generic_shift       | leave_target_region_out | random_forest | 52920 |           11 | 1.13913   | -0.00269345  |
| patchtst_small           | physical_plus_shift | leave_target_region_out | ridge         | 52920 |           23 | 1.13749   | -0.00100648  |
| patchtst_small           | physical_plus_shift | leave_target_region_out | random_forest | 52920 |           23 | 1.18523   | -0.107853    |
| patchtst_small           | physical_knowledge  | group_by_cell           | ridge         | 52920 |           12 | 1.13962   | -0.00668704  |
| patchtst_small           | physical_knowledge  | group_by_cell           | random_forest | 52920 |           12 | 1.21049   | -0.253949    |
| patchtst_small           | generic_shift       | group_by_cell           | ridge         | 52920 |           11 | 1.13631   | -0.000157989 |
| patchtst_small           | generic_shift       | group_by_cell           | random_forest | 52920 |           11 | 1.14305   | -0.0182706   |
| patchtst_small           | physical_plus_shift | group_by_cell           | ridge         | 52920 |           23 | 1.13914   | -0.00506183  |
| patchtst_small           | physical_plus_shift | group_by_cell           | random_forest | 52920 |           23 | 1.21005   | -0.253758    |
| regional_doy_climatology | physical_knowledge  | leave_target_region_out | ridge         | 52920 |           12 | 0.70672   | -0.0360981   |
| regional_doy_climatology | physical_knowledge  | leave_target_region_out | random_forest | 52920 |           12 | 0.723393  | -0.0592895   |
| regional_doy_climatology | generic_shift       | leave_target_region_out | ridge         | 52920 |           11 | 0.632229  |  0.0565138   |
| regional_doy_climatology | generic_shift       | leave_target_region_out | random_forest | 52920 |           11 | 0.801308  | -0.496146    |
| regional_doy_climatology | physical_plus_shift | leave_target_region_out | ridge         | 52920 |           23 | 0.547805  |  0.215609    |
| regional_doy_climatology | physical_plus_shift | leave_target_region_out | random_forest | 52920 |           23 | 0.70311   | -0.363274    |
| regional_doy_climatology | physical_knowledge  | group_by_cell           | ridge         | 52920 |           12 | 0.663286  |  0.039971    |
| regional_doy_climatology | physical_knowledge  | group_by_cell           | random_forest | 52920 |           12 | 0.667155  |  0.0317011   |
| regional_doy_climatology | generic_shift       | group_by_cell           | ridge         | 52920 |           11 | 0.446366  |  0.415134    |
| regional_doy_climatology | generic_shift       | group_by_cell           | random_forest | 52920 |           11 | 0.107231  |  0.967862    |
| regional_doy_climatology | physical_plus_shift | group_by_cell           | ridge         | 52920 |           23 | 0.40148   |  0.57598     |
| regional_doy_climatology | physical_plus_shift | group_by_cell           | random_forest | 52920 |           23 | 0.108528  |  0.878324    |
| spatial_knn_ridge        | physical_knowledge  | leave_target_region_out | ridge         | 52920 |           12 | 0.0714407 | -0.16255     |
| spatial_knn_ridge        | physical_knowledge  | leave_target_region_out | random_forest | 52920 |           12 | 0.0688816 | -0.0154241   |
| spatial_knn_ridge        | generic_shift       | leave_target_region_out | ridge         | 52920 |           11 | 0.0722827 | -0.146829    |
| spatial_knn_ridge        | generic_shift       | leave_target_region_out | random_forest | 52920 |           11 | 0.0927249 | -0.886751    |
| spatial_knn_ridge        | physical_plus_shift | leave_target_region_out | ridge         | 52920 |           23 | 0.070951  | -0.273266    |
| spatial_knn_ridge        | physical_plus_shift | leave_target_region_out | random_forest | 52920 |           23 | 0.088037  | -0.829303    |
| spatial_knn_ridge        | physical_knowledge  | group_by_cell           | ridge         | 52920 |           12 | 0.0658537 |  0.0453283   |
| spatial_knn_ridge        | physical_knowledge  | group_by_cell           | random_forest | 52920 |           12 | 0.0600773 |  0.295383    |
| spatial_knn_ridge        | generic_shift       | group_by_cell           | ridge         | 52920 |           11 | 0.0569698 |  0.214503    |
| spatial_knn_ridge        | generic_shift       | group_by_cell           | random_forest | 52920 |           11 | 0.0291642 |  0.653273    |
| spatial_knn_ridge        | physical_plus_shift | group_by_cell           | ridge         | 52920 |           23 | 0.056051  |  0.168265    |
| spatial_knn_ridge        | physical_plus_shift | group_by_cell           | random_forest | 52920 |           23 | 0.0211773 |  0.809839    |
| stgcn_diffusion          | physical_knowledge  | leave_target_region_out | ridge         | 52920 |           12 | 0.0719404 |  0.0765239   |
| stgcn_diffusion          | physical_knowledge  | leave_target_region_out | random_forest | 52920 |           12 | 0.0646832 |  0.111177    |
| stgcn_diffusion          | generic_shift       | leave_target_region_out | ridge         | 52920 |           11 | 0.0772087 | -0.0382852   |
| stgcn_diffusion          | generic_shift       | leave_target_region_out | random_forest | 52920 |           11 | 0.0721789 | -0.114317    |
| stgcn_diffusion          | physical_plus_shift | leave_target_region_out | ridge         | 52920 |           23 | 0.0764842 |  0.053017    |
| stgcn_diffusion          | physical_plus_shift | leave_target_region_out | random_forest | 52920 |           23 | 0.0684769 |  0.0050375   |
| stgcn_diffusion          | physical_knowledge  | group_by_cell           | ridge         | 52920 |           12 | 0.069348  |  0.128198    |
| stgcn_diffusion          | physical_knowledge  | group_by_cell           | random_forest | 52920 |           12 | 0.0616811 |  0.195526    |
| stgcn_diffusion          | generic_shift       | group_by_cell           | ridge         | 52920 |           11 | 0.073193  |  0.00437408  |
| stgcn_diffusion          | generic_shift       | group_by_cell           | random_forest | 52920 |           11 | 0.0637226 |  0.0527925   |
| stgcn_diffusion          | physical_plus_shift | group_by_cell           | ridge         | 52920 |           23 | 0.0696692 |  0.135854    |
| stgcn_diffusion          | physical_plus_shift | group_by_cell           | random_forest | 52920 |           23 | 0.0463176 |  0.324485    |
