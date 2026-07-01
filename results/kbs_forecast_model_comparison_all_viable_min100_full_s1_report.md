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
| graphwavenet_transfer    | CNA             | EAS             |  110 |        0.182715    |
| graphwavenet_transfer    | CNA             | EAU             |  241 |        0.0356106   |
| graphwavenet_transfer    | CNA             | ENA             |  522 |        0.0343848   |
| graphwavenet_transfer    | CNA             | MED             |  328 |        0.0442502   |
| graphwavenet_transfer    | CNA             | NCA             |  144 |       -0.00810638  |
| graphwavenet_transfer    | CNA             | NEU             | 1000 |        0.12823     |
| graphwavenet_transfer    | CNA             | NWN             |  183 |        0.193982    |
| graphwavenet_transfer    | CNA             | SAU             |  351 |        0.0419677   |
| graphwavenet_transfer    | CNA             | WCE             | 1000 |        0.0693719   |
| graphwavenet_transfer    | CNA             | WNA             |  975 |        0.0977959   |
| graphwavenet_transfer    | EAS             | CNA             |  438 |        0.240295    |
| graphwavenet_transfer    | EAS             | EAU             |  241 |        0.0375726   |
| graphwavenet_transfer    | EAS             | ENA             |  522 |        0.332576    |
| graphwavenet_transfer    | EAS             | MED             |  328 |        0.0182156   |
| graphwavenet_transfer    | EAS             | NCA             |  144 |        0.0157567   |
| graphwavenet_transfer    | EAS             | NEU             | 1000 |        0.057158    |
| graphwavenet_transfer    | EAS             | NWN             |  183 |        0.093396    |
| graphwavenet_transfer    | EAS             | SAU             |  351 |        0.0362998   |
| graphwavenet_transfer    | EAS             | WCE             | 1000 |        0.049164    |
| graphwavenet_transfer    | EAS             | WNA             |  975 |        0.0375073   |
| graphwavenet_transfer    | EAU             | CNA             |  438 |        0.179814    |
| graphwavenet_transfer    | EAU             | EAS             |  110 |        0.00929778  |
| graphwavenet_transfer    | EAU             | ENA             |  522 |        0.25909     |
| graphwavenet_transfer    | EAU             | MED             |  328 |        0.00547806  |
| graphwavenet_transfer    | EAU             | NCA             |  144 |        0.00424555  |
| graphwavenet_transfer    | EAU             | NEU             | 1000 |        0.0471858   |
| graphwavenet_transfer    | EAU             | NWN             |  183 |        0.14458     |
| graphwavenet_transfer    | EAU             | SAU             |  351 |        0.0120396   |
| graphwavenet_transfer    | EAU             | WCE             | 1000 |        0.0256511   |
| graphwavenet_transfer    | EAU             | WNA             |  975 |        0.0628867   |
| graphwavenet_transfer    | ENA             | CNA             |  438 |        0.031487    |
| graphwavenet_transfer    | ENA             | EAS             |  110 |        0.170764    |
| graphwavenet_transfer    | ENA             | EAU             |  241 |        0.0506817   |
| graphwavenet_transfer    | ENA             | MED             |  328 |        0.0294941   |
| graphwavenet_transfer    | ENA             | NCA             |  144 |       -0.0138642   |
| graphwavenet_transfer    | ENA             | NEU             | 1000 |        0.104855    |
| graphwavenet_transfer    | ENA             | NWN             |  183 |        0.161109    |
| graphwavenet_transfer    | ENA             | SAU             |  351 |        0.0369432   |
| graphwavenet_transfer    | ENA             | WCE             | 1000 |        0.047975    |
| graphwavenet_transfer    | ENA             | WNA             |  975 |        0.0845786   |
| graphwavenet_transfer    | MED             | CNA             |  438 |        0.191971    |
| graphwavenet_transfer    | MED             | EAS             |  110 |       -0.0117052   |
| graphwavenet_transfer    | MED             | EAU             |  241 |        0.00981107  |
| graphwavenet_transfer    | MED             | ENA             |  522 |        0.263446    |
| graphwavenet_transfer    | MED             | NCA             |  144 |        0.00290734  |
| graphwavenet_transfer    | MED             | NEU             | 1000 |        0.0203032   |
| graphwavenet_transfer    | MED             | NWN             |  183 |        0.119107    |
| graphwavenet_transfer    | MED             | SAU             |  351 |        0.00365345  |
| graphwavenet_transfer    | MED             | WCE             | 1000 |        0.00522743  |
| graphwavenet_transfer    | MED             | WNA             |  975 |        0.0413586   |
| graphwavenet_transfer    | NCA             | CNA             |  438 |        0.167215    |
| graphwavenet_transfer    | NCA             | EAS             |  110 |        0.026667    |
| graphwavenet_transfer    | NCA             | EAU             |  241 |        0.0228164   |
| graphwavenet_transfer    | NCA             | ENA             |  522 |        0.230191    |
| graphwavenet_transfer    | NCA             | MED             |  328 |        0.0209162   |
| graphwavenet_transfer    | NCA             | NEU             | 1000 |        0.0955726   |
| graphwavenet_transfer    | NCA             | NWN             |  183 |        0.13821     |
| graphwavenet_transfer    | NCA             | SAU             |  351 |        0.0293224   |
| graphwavenet_transfer    | NCA             | WCE             | 1000 |        0.0775611   |
| graphwavenet_transfer    | NCA             | WNA             |  975 |        0.0527343   |
| graphwavenet_transfer    | NEU             | CNA             |  438 |        0.226793    |
| graphwavenet_transfer    | NEU             | EAS             |  110 |        0.0184829   |
| graphwavenet_transfer    | NEU             | EAU             |  241 |        0.031006    |
| graphwavenet_transfer    | NEU             | ENA             |  522 |        0.291839    |
| graphwavenet_transfer    | NEU             | MED             |  328 |        0.0135084   |
| graphwavenet_transfer    | NEU             | NCA             |  144 |        0.022976    |
| graphwavenet_transfer    | NEU             | NWN             |  183 |        0.0864619   |
| graphwavenet_transfer    | NEU             | SAU             |  351 |        0.0197794   |
| graphwavenet_transfer    | NEU             | WCE             | 1000 |        0.00400415  |
| graphwavenet_transfer    | NEU             | WNA             |  975 |        0.0406339   |
| graphwavenet_transfer    | NWN             | CNA             |  438 |        0.223749    |
| graphwavenet_transfer    | NWN             | EAS             |  110 |        0.103918    |
| graphwavenet_transfer    | NWN             | EAU             |  241 |        0.0918019   |
| graphwavenet_transfer    | NWN             | ENA             |  522 |        0.269653    |
| graphwavenet_transfer    | NWN             | MED             |  328 |        0.046827    |
| graphwavenet_transfer    | NWN             | NCA             |  144 |        0.01779     |
| graphwavenet_transfer    | NWN             | NEU             | 1000 |        0.0721681   |
| graphwavenet_transfer    | NWN             | SAU             |  351 |        0.0589402   |
| graphwavenet_transfer    | NWN             | WCE             | 1000 |        0.079655    |
| graphwavenet_transfer    | NWN             | WNA             |  975 |        0.0206435   |
| graphwavenet_transfer    | SAU             | CNA             |  438 |        0.184773    |
| graphwavenet_transfer    | SAU             | EAS             |  110 |        0.039295    |
| graphwavenet_transfer    | SAU             | EAU             |  241 |        0.0172851   |
| graphwavenet_transfer    | SAU             | ENA             |  522 |        0.24898     |
| graphwavenet_transfer    | SAU             | MED             |  328 |        0.00356421  |
| graphwavenet_transfer    | SAU             | NCA             |  144 |        0.00653412  |
| graphwavenet_transfer    | SAU             | NEU             | 1000 |        0.0259353   |
| graphwavenet_transfer    | SAU             | NWN             |  183 |        0.140918    |
| graphwavenet_transfer    | SAU             | WCE             | 1000 |        0.00515521  |
| graphwavenet_transfer    | SAU             | WNA             |  975 |        0.0664277   |
| graphwavenet_transfer    | WCE             | CNA             |  438 |        0.195472    |
| graphwavenet_transfer    | WCE             | EAS             |  110 |        0.0780553   |
| graphwavenet_transfer    | WCE             | EAU             |  241 |        0.0341714   |
| graphwavenet_transfer    | WCE             | ENA             |  522 |        0.254799    |
| graphwavenet_transfer    | WCE             | MED             |  328 |        0.00887338  |
| graphwavenet_transfer    | WCE             | NCA             |  144 |        0.0113537   |
| graphwavenet_transfer    | WCE             | NEU             | 1000 |        0.0361191   |
| graphwavenet_transfer    | WCE             | NWN             |  183 |        0.196107    |
| graphwavenet_transfer    | WCE             | SAU             |  351 |        0.0137812   |
| graphwavenet_transfer    | WCE             | WNA             |  975 |        0.09266     |
| graphwavenet_transfer    | WNA             | CNA             |  438 |        0.2079      |
| graphwavenet_transfer    | WNA             | EAS             |  110 |        0.0112808   |
| graphwavenet_transfer    | WNA             | EAU             |  241 |        0.0533649   |
| graphwavenet_transfer    | WNA             | ENA             |  522 |        0.262011    |
| graphwavenet_transfer    | WNA             | MED             |  328 |        0.0300997   |
| graphwavenet_transfer    | WNA             | NCA             |  144 |        0.00425855  |
| graphwavenet_transfer    | WNA             | NEU             | 1000 |        0.0263486   |
| graphwavenet_transfer    | WNA             | NWN             |  183 |        0.0367617   |
| graphwavenet_transfer    | WNA             | SAU             |  351 |        0.0500367   |
| graphwavenet_transfer    | WNA             | WCE             | 1000 |        0.0348581   |
| linear_window            | CNA             | EAS             |  110 |        0.410736    |
| linear_window            | CNA             | EAU             |  241 |        0.161024    |
| linear_window            | CNA             | ENA             |  522 |        0.101052    |
| linear_window            | CNA             | MED             |  328 |        0.00860045  |
| linear_window            | CNA             | NCA             |  144 |        0.0351868   |
| linear_window            | CNA             | NEU             | 1000 |        0.122114    |
| linear_window            | CNA             | NWN             |  183 |        0.226336    |
| linear_window            | CNA             | SAU             |  351 |        0.0270979   |
| linear_window            | CNA             | WCE             | 1000 |        0.0679311   |
| linear_window            | CNA             | WNA             |  975 |        0.0681452   |
| linear_window            | EAS             | CNA             |  438 |        0.101478    |
| linear_window            | EAS             | EAU             |  241 |       -0.0846546   |
| linear_window            | EAS             | ENA             |  522 |        0.103195    |
| linear_window            | EAS             | MED             |  328 |       -0.063035    |
| linear_window            | EAS             | NCA             |  144 |        0.0197212   |
| linear_window            | EAS             | NEU             | 1000 |       -0.0205136   |
| linear_window            | EAS             | NWN             |  183 |        0.00155912  |
| linear_window            | EAS             | SAU             |  351 |        0.115205    |
| linear_window            | EAS             | WCE             | 1000 |       -0.0400538   |
| linear_window            | EAS             | WNA             |  975 |        0.00891467  |
| linear_window            | EAU             | CNA             |  438 |        0.0363366   |
| linear_window            | EAU             | EAS             |  110 |       -0.247042    |
| linear_window            | EAU             | ENA             |  522 |       -0.0594674   |
| linear_window            | EAU             | MED             |  328 |        0.0124365   |
| linear_window            | EAU             | NCA             |  144 |        0.0661658   |
| linear_window            | EAU             | NEU             | 1000 |        0.0745652   |
| linear_window            | EAU             | NWN             |  183 |        0.0463797   |
| linear_window            | EAU             | SAU             |  351 |        0.157957    |
| linear_window            | EAU             | WCE             | 1000 |       -0.0591301   |
| linear_window            | EAU             | WNA             |  975 |        0.0382711   |
| linear_window            | ENA             | CNA             |  438 |        0.116692    |
| linear_window            | ENA             | EAS             |  110 |       -0.0682457   |
| linear_window            | ENA             | EAU             |  241 |        0.203948    |
| linear_window            | ENA             | MED             |  328 |       -0.0841659   |
| linear_window            | ENA             | NCA             |  144 |        0.0296768   |
| linear_window            | ENA             | NEU             | 1000 |        0.120085    |
| linear_window            | ENA             | NWN             |  183 |        0.014489    |
| linear_window            | ENA             | SAU             |  351 |        0.117359    |
| linear_window            | ENA             | WCE             | 1000 |       -0.0370053   |
| linear_window            | ENA             | WNA             |  975 |        0.0848873   |
| linear_window            | MED             | CNA             |  438 |        0.0921681   |
| linear_window            | MED             | EAS             |  110 |        0.239308    |
| linear_window            | MED             | EAU             |  241 |       -0.0381079   |
| linear_window            | MED             | ENA             |  522 |       -0.00692164  |
| linear_window            | MED             | NCA             |  144 |        0.0386423   |
| linear_window            | MED             | NEU             | 1000 |        0.0474235   |
| linear_window            | MED             | NWN             |  183 |       -0.0964381   |
| linear_window            | MED             | SAU             |  351 |        0.141546    |
| linear_window            | MED             | WCE             | 1000 |        0.0309787   |
| linear_window            | MED             | WNA             |  975 |        0.0315315   |
| linear_window            | NCA             | CNA             |  438 |        0.0206527   |
| linear_window            | NCA             | EAS             |  110 |        0.180228    |
| linear_window            | NCA             | EAU             |  241 |        0.089116    |
| linear_window            | NCA             | ENA             |  522 |        0.0730836   |
| linear_window            | NCA             | MED             |  328 |        0.0463176   |
| linear_window            | NCA             | NEU             | 1000 |        0.110109    |
| linear_window            | NCA             | NWN             |  183 |       -0.037522    |
| linear_window            | NCA             | SAU             |  351 |        0.101864    |
| linear_window            | NCA             | WCE             | 1000 |        0.0406302   |
| linear_window            | NCA             | WNA             |  975 |        0.0834347   |
| linear_window            | NEU             | CNA             |  438 |        0.194381    |
| linear_window            | NEU             | EAS             |  110 |       -0.343949    |
| linear_window            | NEU             | EAU             |  241 |        0.0214551   |
| linear_window            | NEU             | ENA             |  522 |        0.138318    |
| linear_window            | NEU             | MED             |  328 |       -0.0564013   |
| linear_window            | NEU             | NCA             |  144 |        0.097521    |
| linear_window            | NEU             | NWN             |  183 |       -0.00917919  |
| linear_window            | NEU             | SAU             |  351 |        0.0967583   |
| linear_window            | NEU             | WCE             | 1000 |        0.0174669   |
| linear_window            | NEU             | WNA             |  975 |       -0.00485446  |
| linear_window            | NWN             | CNA             |  438 |        0.111814    |
| linear_window            | NWN             | EAS             |  110 |       -0.728121    |
| linear_window            | NWN             | EAU             |  241 |       -0.121037    |
| linear_window            | NWN             | ENA             |  522 |        0.0887425   |
| linear_window            | NWN             | MED             |  328 |        0.0245217   |
| linear_window            | NWN             | NCA             |  144 |        0.0552657   |
| linear_window            | NWN             | NEU             | 1000 |        0.0111116   |
| linear_window            | NWN             | SAU             |  351 |        0.207985    |
| linear_window            | NWN             | WCE             | 1000 |        0.0118928   |
| linear_window            | NWN             | WNA             |  975 |       -0.0715041   |
| linear_window            | SAU             | CNA             |  438 |        0.0336376   |
| linear_window            | SAU             | EAS             |  110 |       -0.499918    |
| linear_window            | SAU             | EAU             |  241 |        0.120168    |
| linear_window            | SAU             | ENA             |  522 |        0.0583299   |
| linear_window            | SAU             | MED             |  328 |       -0.00336261  |
| linear_window            | SAU             | NCA             |  144 |        0.0332712   |
| linear_window            | SAU             | NEU             | 1000 |        0.0215254   |
| linear_window            | SAU             | NWN             |  183 |        0.0191605   |
| linear_window            | SAU             | WCE             | 1000 |       -0.0362966   |
| linear_window            | SAU             | WNA             |  975 |        0.0354757   |
| linear_window            | WCE             | CNA             |  438 |        0.0588579   |
| linear_window            | WCE             | EAS             |  110 |       -0.268679    |
| linear_window            | WCE             | EAU             |  241 |        0.086597    |
| linear_window            | WCE             | ENA             |  522 |        0.0103425   |
| linear_window            | WCE             | MED             |  328 |       -0.0041115   |
| linear_window            | WCE             | NCA             |  144 |        0.133291    |
| linear_window            | WCE             | NEU             | 1000 |        0.0353432   |
| linear_window            | WCE             | NWN             |  183 |        0.0648703   |
| linear_window            | WCE             | SAU             |  351 |        0.12354     |
| linear_window            | WCE             | WNA             |  975 |       -0.00270858  |
| linear_window            | WNA             | CNA             |  438 |        0.067267    |
| linear_window            | WNA             | EAS             |  110 |       -0.308162    |
| linear_window            | WNA             | EAU             |  241 |        0.0735979   |
| linear_window            | WNA             | ENA             |  522 |        0.0725304   |
| linear_window            | WNA             | MED             |  328 |       -0.0333312   |
| linear_window            | WNA             | NCA             |  144 |        0.128159    |
| linear_window            | WNA             | NEU             | 1000 |       -0.00208597  |
| linear_window            | WNA             | NWN             |  183 |       -0.0564258   |
| linear_window            | WNA             | SAU             |  351 |        0.196382    |
| linear_window            | WNA             | WCE             | 1000 |       -0.0308833   |
| patchtst_small           | CNA             | EAS             |  110 |        0.412975    |
| patchtst_small           | CNA             | EAU             |  241 |        0.149791    |
| patchtst_small           | CNA             | ENA             |  522 |        0.0944347   |
| patchtst_small           | CNA             | MED             |  328 |       -0.00605131  |
| patchtst_small           | CNA             | NCA             |  144 |        0.0332406   |
| patchtst_small           | CNA             | NEU             | 1000 |        0.124164    |
| patchtst_small           | CNA             | NWN             |  183 |        0.215533    |
| patchtst_small           | CNA             | SAU             |  351 |        0.0300812   |
| patchtst_small           | CNA             | WCE             | 1000 |        0.0626136   |
| patchtst_small           | CNA             | WNA             |  975 |        0.0596799   |
| patchtst_small           | EAS             | CNA             |  438 |        0.0705402   |
| patchtst_small           | EAS             | EAU             |  241 |       -0.104621    |
| patchtst_small           | EAS             | ENA             |  522 |        0.0665493   |
| patchtst_small           | EAS             | MED             |  328 |       -0.0880973   |
| patchtst_small           | EAS             | NCA             |  144 |        0.00475716  |
| patchtst_small           | EAS             | NEU             | 1000 |       -0.00228395  |
| patchtst_small           | EAS             | NWN             |  183 |       -0.0276665   |
| patchtst_small           | EAS             | SAU             |  351 |        0.105494    |
| patchtst_small           | EAS             | WCE             | 1000 |       -0.0352346   |
| patchtst_small           | EAS             | WNA             |  975 |        0.000459941 |
| patchtst_small           | EAU             | CNA             |  438 |        0.0243624   |
| patchtst_small           | EAU             | EAS             |  110 |       -0.139513    |
| patchtst_small           | EAU             | ENA             |  522 |       -0.0820514   |
| patchtst_small           | EAU             | MED             |  328 |        0.00381194  |
| patchtst_small           | EAU             | NCA             |  144 |        0.0628888   |
| patchtst_small           | EAU             | NEU             | 1000 |        0.107013    |
| patchtst_small           | EAU             | NWN             |  183 |        0.0889143   |
| patchtst_small           | EAU             | SAU             |  351 |        0.173755    |
| patchtst_small           | EAU             | WCE             | 1000 |       -0.0535081   |
| patchtst_small           | EAU             | WNA             |  975 |        0.0572877   |
| patchtst_small           | ENA             | CNA             |  438 |        0.126651    |
| patchtst_small           | ENA             | EAS             |  110 |       -0.0493792   |
| patchtst_small           | ENA             | EAU             |  241 |        0.204023    |
| patchtst_small           | ENA             | MED             |  328 |       -0.091085    |
| patchtst_small           | ENA             | NCA             |  144 |        0.0370453   |
| patchtst_small           | ENA             | NEU             | 1000 |        0.122566    |
| patchtst_small           | ENA             | NWN             |  183 |        0.0134206   |
| patchtst_small           | ENA             | SAU             |  351 |        0.126697    |
| patchtst_small           | ENA             | WCE             | 1000 |       -0.0409367   |
| patchtst_small           | ENA             | WNA             |  975 |        0.0866974   |
| patchtst_small           | MED             | CNA             |  438 |        0.0894717   |
| patchtst_small           | MED             | EAS             |  110 |        0.33405     |
| patchtst_small           | MED             | EAU             |  241 |       -0.0292423   |
| patchtst_small           | MED             | ENA             |  522 |       -0.0256383   |
| patchtst_small           | MED             | NCA             |  144 |        0.0499017   |
| patchtst_small           | MED             | NEU             | 1000 |        0.0883983   |
| patchtst_small           | MED             | NWN             |  183 |       -0.0412364   |
| patchtst_small           | MED             | SAU             |  351 |        0.165765    |
| patchtst_small           | MED             | WCE             | 1000 |        0.048094    |
| patchtst_small           | MED             | WNA             |  975 |        0.0647197   |
| patchtst_small           | NCA             | CNA             |  438 |        0.0246248   |
| patchtst_small           | NCA             | EAS             |  110 |        0.215957    |
| patchtst_small           | NCA             | EAU             |  241 |        0.0910283   |
| patchtst_small           | NCA             | ENA             |  522 |        0.0727776   |
| patchtst_small           | NCA             | MED             |  328 |        0.0387371   |
| patchtst_small           | NCA             | NEU             | 1000 |        0.123219    |
| patchtst_small           | NCA             | NWN             |  183 |       -0.0299181   |
| patchtst_small           | NCA             | SAU             |  351 |        0.111861    |
| patchtst_small           | NCA             | WCE             | 1000 |        0.0426919   |
| patchtst_small           | NCA             | WNA             |  975 |        0.0859376   |
| patchtst_small           | NEU             | CNA             |  438 |        0.184935    |
| patchtst_small           | NEU             | EAS             |  110 |       -0.35559     |
| patchtst_small           | NEU             | EAU             |  241 |        0.0101237   |
| patchtst_small           | NEU             | ENA             |  522 |        0.125174    |
| patchtst_small           | NEU             | MED             |  328 |       -0.07323     |
| patchtst_small           | NEU             | NCA             |  144 |        0.0878248   |
| patchtst_small           | NEU             | NWN             |  183 |       -0.0152339   |
| patchtst_small           | NEU             | SAU             |  351 |        0.0989806   |
| patchtst_small           | NEU             | WCE             | 1000 |        0.0145398   |
| patchtst_small           | NEU             | WNA             |  975 |       -0.0127562   |
| patchtst_small           | NWN             | CNA             |  438 |        0.096833    |
| patchtst_small           | NWN             | EAS             |  110 |       -0.8073      |
| patchtst_small           | NWN             | EAU             |  241 |       -0.132701    |
| patchtst_small           | NWN             | ENA             |  522 |        0.0648716   |
| patchtst_small           | NWN             | MED             |  328 |        0.005357    |
| patchtst_small           | NWN             | NCA             |  144 |        0.0485627   |
| patchtst_small           | NWN             | NEU             | 1000 |        0.0168834   |
| patchtst_small           | NWN             | SAU             |  351 |        0.205663    |
| patchtst_small           | NWN             | WCE             | 1000 |        0.00866679  |
| patchtst_small           | NWN             | WNA             |  975 |       -0.0799368   |
| patchtst_small           | SAU             | CNA             |  438 |        0.0270816   |
| patchtst_small           | SAU             | EAS             |  110 |       -0.501553    |
| patchtst_small           | SAU             | EAU             |  241 |        0.105967    |
| patchtst_small           | SAU             | ENA             |  522 |        0.0483128   |
| patchtst_small           | SAU             | MED             |  328 |       -0.0193024   |
| patchtst_small           | SAU             | NCA             |  144 |        0.0251711   |
| patchtst_small           | SAU             | NEU             | 1000 |        0.0250075   |
| patchtst_small           | SAU             | NWN             |  183 |        0.0152694   |
| patchtst_small           | SAU             | WCE             | 1000 |       -0.037015    |
| patchtst_small           | SAU             | WNA             |  975 |        0.0212505   |
| patchtst_small           | WCE             | CNA             |  438 |        0.0620363   |
| patchtst_small           | WCE             | EAS             |  110 |       -0.229963    |
| patchtst_small           | WCE             | EAU             |  241 |        0.0882301   |
| patchtst_small           | WCE             | ENA             |  522 |       -0.000656351 |
| patchtst_small           | WCE             | MED             |  328 |       -0.00872095  |
| patchtst_small           | WCE             | NCA             |  144 |        0.146893    |
| patchtst_small           | WCE             | NEU             | 1000 |        0.0500682   |
| patchtst_small           | WCE             | NWN             |  183 |        0.0828194   |
| patchtst_small           | WCE             | SAU             |  351 |        0.133965    |
| patchtst_small           | WCE             | WNA             |  975 |        0.00672306  |
| patchtst_small           | WNA             | CNA             |  438 |        0.0448027   |
| patchtst_small           | WNA             | EAS             |  110 |       -0.389932    |
| patchtst_small           | WNA             | EAU             |  241 |        0.0874268   |
| patchtst_small           | WNA             | ENA             |  522 |        0.0371024   |
| patchtst_small           | WNA             | MED             |  328 |       -0.0512718   |
| patchtst_small           | WNA             | NCA             |  144 |        0.123093    |
| patchtst_small           | WNA             | NEU             | 1000 |        0.0139366   |
| patchtst_small           | WNA             | NWN             |  183 |       -0.0561999   |
| patchtst_small           | WNA             | SAU             |  351 |        0.198572    |
| patchtst_small           | WNA             | WCE             | 1000 |       -0.0304504   |
| regional_doy_climatology | CNA             | EAS             |  110 |       -1.81385     |
| regional_doy_climatology | CNA             | EAU             |  241 |       -0.110242    |
| regional_doy_climatology | CNA             | ENA             |  522 |       -0.557076    |
| regional_doy_climatology | CNA             | MED             |  328 |        0.344803    |
| regional_doy_climatology | CNA             | NCA             |  144 |        0.893314    |
| regional_doy_climatology | CNA             | NEU             | 1000 |       -0.0148559   |
| regional_doy_climatology | CNA             | NWN             |  183 |       -0.19641     |
| regional_doy_climatology | CNA             | SAU             |  351 |        0.2294      |
| regional_doy_climatology | CNA             | WCE             | 1000 |       -0.0424347   |
| regional_doy_climatology | CNA             | WNA             |  975 |        0.1392      |
| regional_doy_climatology | EAS             | CNA             |  438 |        3.01123     |
| regional_doy_climatology | EAS             | EAU             |  241 |        3.12179     |
| regional_doy_climatology | EAS             | ENA             |  522 |        2.18762     |
| regional_doy_climatology | EAS             | MED             |  328 |        3.77667     |
| regional_doy_climatology | EAS             | NCA             |  144 |        4.29429     |
| regional_doy_climatology | EAS             | NEU             | 1000 |        2.97444     |
| regional_doy_climatology | EAS             | NWN             |  183 |        2.81549     |
| regional_doy_climatology | EAS             | SAU             |  351 |        3.27918     |
| regional_doy_climatology | EAS             | WCE             | 1000 |        2.91135     |
| regional_doy_climatology | EAS             | WNA             |  975 |        3.49015     |
| regional_doy_climatology | EAU             | CNA             |  438 |        0.282819    |
| regional_doy_climatology | EAU             | EAS             |  110 |       -1.33372     |
| regional_doy_climatology | EAU             | ENA             |  522 |       -0.351761    |
| regional_doy_climatology | EAU             | MED             |  328 |        0.468011    |
| regional_doy_climatology | EAU             | NCA             |  144 |        1.1281      |
| regional_doy_climatology | EAU             | NEU             | 1000 |        0.13233     |
| regional_doy_climatology | EAU             | NWN             |  183 |        0.01432     |
| regional_doy_climatology | EAU             | SAU             |  351 |        0.532103    |
| regional_doy_climatology | EAU             | WCE             | 1000 |        0.144564    |
| regional_doy_climatology | EAU             | WNA             |  975 |        0.160134    |
| regional_doy_climatology | ENA             | CNA             |  438 |        0.734675    |
| regional_doy_climatology | ENA             | EAS             |  110 |       -1.17278     |
| regional_doy_climatology | ENA             | EAU             |  241 |        0.48445     |
| regional_doy_climatology | ENA             | MED             |  328 |        1.03475     |
| regional_doy_climatology | ENA             | NCA             |  144 |        1.71267     |
| regional_doy_climatology | ENA             | NEU             | 1000 |        0.474722    |
| regional_doy_climatology | ENA             | NWN             |  183 |        0.377848    |
| regional_doy_climatology | ENA             | SAU             |  351 |        0.888504    |
| regional_doy_climatology | ENA             | WCE             | 1000 |        0.489044    |
| regional_doy_climatology | ENA             | WNA             |  975 |        0.696154    |
| regional_doy_climatology | MED             | CNA             |  438 |       -0.136096    |
| regional_doy_climatology | MED             | EAS             |  110 |       -1.65667     |
| regional_doy_climatology | MED             | EAU             |  241 |       -0.394873    |
| regional_doy_climatology | MED             | ENA             |  522 |       -0.684155    |
| regional_doy_climatology | MED             | NCA             |  144 |        0.644253    |
| regional_doy_climatology | MED             | NEU             | 1000 |       -0.232233    |
| regional_doy_climatology | MED             | NWN             |  183 |       -0.376459    |
| regional_doy_climatology | MED             | SAU             |  351 |        0.142412    |
| regional_doy_climatology | MED             | WCE             | 1000 |       -0.220427    |
| regional_doy_climatology | MED             | WNA             |  975 |       -0.212434    |
| regional_doy_climatology | NCA             | CNA             |  438 |       -0.677282    |
| regional_doy_climatology | NCA             | EAS             |  110 |       -2.21432     |
| regional_doy_climatology | NCA             | EAU             |  241 |       -0.780145    |
| regional_doy_climatology | NCA             | ENA             |  522 |       -1.08305     |
| regional_doy_climatology | NCA             | MED             |  328 |       -0.374613    |
| regional_doy_climatology | NCA             | NEU             | 1000 |       -0.519248    |
| regional_doy_climatology | NCA             | NWN             |  183 |       -0.750943    |
| regional_doy_climatology | NCA             | SAU             |  351 |       -0.362901    |
| regional_doy_climatology | NCA             | WCE             | 1000 |       -0.565099    |
| regional_doy_climatology | NCA             | WNA             |  975 |       -0.467222    |
| regional_doy_climatology | NEU             | CNA             |  438 |        0.204856    |
| regional_doy_climatology | NEU             | EAS             |  110 |       -1.57988     |
| regional_doy_climatology | NEU             | EAU             |  241 |       -0.0117633   |
| regional_doy_climatology | NEU             | ENA             |  522 |       -0.429559    |
| regional_doy_climatology | NEU             | MED             |  328 |        0.474462    |
| regional_doy_climatology | NEU             | NCA             |  144 |        1.05439     |
| regional_doy_climatology | NEU             | NWN             |  183 |       -0.127834    |
| regional_doy_climatology | NEU             | SAU             |  351 |        0.36199     |
| regional_doy_climatology | NEU             | WCE             | 1000 |        0.0352905   |
| regional_doy_climatology | NEU             | WNA             |  975 |        0.221867    |
| regional_doy_climatology | NWN             | CNA             |  438 |        0.374672    |
| regional_doy_climatology | NWN             | EAS             |  110 |       -1.44579     |
| regional_doy_climatology | NWN             | EAU             |  241 |        0.11023     |
| regional_doy_climatology | NWN             | ENA             |  522 |       -0.292863    |
| regional_doy_climatology | NWN             | MED             |  328 |        0.604575    |
| regional_doy_climatology | NWN             | NCA             |  144 |        1.2428      |
| regional_doy_climatology | NWN             | NEU             | 1000 |        0.108381    |
| regional_doy_climatology | NWN             | SAU             |  351 |        0.512798    |
| regional_doy_climatology | NWN             | WCE             | 1000 |        0.148107    |
| regional_doy_climatology | NWN             | WNA             |  975 |        0.320105    |
| regional_doy_climatology | SAU             | CNA             |  438 |       -0.227357    |
| regional_doy_climatology | SAU             | EAS             |  110 |       -1.92734     |
| regional_doy_climatology | SAU             | EAU             |  241 |       -0.3613      |
| regional_doy_climatology | SAU             | ENA             |  522 |       -0.75106     |
| regional_doy_climatology | SAU             | MED             |  328 |        0.0784903   |
| regional_doy_climatology | SAU             | NCA             |  144 |        0.582668    |
| regional_doy_climatology | SAU             | NEU             | 1000 |       -0.219642    |
| regional_doy_climatology | SAU             | NWN             |  183 |       -0.418267    |
| regional_doy_climatology | SAU             | WCE             | 1000 |       -0.240053    |
| regional_doy_climatology | SAU             | WNA             |  975 |       -0.091733    |
| regional_doy_climatology | WCE             | CNA             |  438 |        0.104918    |
| regional_doy_climatology | WCE             | EAS             |  110 |       -1.67852     |
| regional_doy_climatology | WCE             | EAU             |  241 |       -0.0770476   |
| regional_doy_climatology | WCE             | ENA             |  522 |       -0.499136    |
| regional_doy_climatology | WCE             | MED             |  328 |        0.419286    |
| regional_doy_climatology | WCE             | NCA             |  144 |        0.966576    |
| regional_doy_climatology | WCE             | NEU             | 1000 |        0.00234779  |
| regional_doy_climatology | WCE             | NWN             |  183 |       -0.149167    |
| regional_doy_climatology | WCE             | SAU             |  351 |        0.30092     |
| regional_doy_climatology | WCE             | WNA             |  975 |        0.195905    |
| regional_doy_climatology | WNA             | CNA             |  438 |        0.156543    |
| regional_doy_climatology | WNA             | EAS             |  110 |       -1.37559     |
| regional_doy_climatology | WNA             | EAU             |  241 |       -0.170542    |
| regional_doy_climatology | WNA             | ENA             |  522 |       -0.462289    |
| regional_doy_climatology | WNA             | MED             |  328 |        0.31725     |
| regional_doy_climatology | WNA             | NCA             |  144 |        1.00846     |
| regional_doy_climatology | WNA             | NEU             | 1000 |       -0.00467519  |
| regional_doy_climatology | WNA             | NWN             |  183 |       -0.0983048   |
| regional_doy_climatology | WNA             | SAU             |  351 |        0.432435    |
| regional_doy_climatology | WNA             | WCE             | 1000 |        0.0287172   |
| spatial_knn_ridge        | CNA             | EAS             |  110 |       -0.0230846   |
| spatial_knn_ridge        | CNA             | EAU             |  241 |       -0.0129018   |
| spatial_knn_ridge        | CNA             | ENA             |  522 |       -0.0858925   |
| spatial_knn_ridge        | CNA             | MED             |  328 |        0.0194666   |
| spatial_knn_ridge        | CNA             | NCA             |  144 |        0.114013    |
| spatial_knn_ridge        | CNA             | NEU             | 1000 |       -0.0585105   |
| spatial_knn_ridge        | CNA             | NWN             |  183 |        0.0731321   |
| spatial_knn_ridge        | CNA             | SAU             |  351 |       -0.0169311   |
| spatial_knn_ridge        | CNA             | WCE             | 1000 |       -0.0742674   |
| spatial_knn_ridge        | CNA             | WNA             |  975 |        0.0265251   |
| spatial_knn_ridge        | EAS             | CNA             |  438 |        0.153456    |
| spatial_knn_ridge        | EAS             | EAU             |  241 |        0.0889704   |
| spatial_knn_ridge        | EAS             | ENA             |  522 |        0.0668968   |
| spatial_knn_ridge        | EAS             | MED             |  328 |        0.127402    |
| spatial_knn_ridge        | EAS             | NCA             |  144 |        0.241549    |
| spatial_knn_ridge        | EAS             | NEU             | 1000 |       -0.00453622  |
| spatial_knn_ridge        | EAS             | NWN             |  183 |        0.0854261   |
| spatial_knn_ridge        | EAS             | SAU             |  351 |        0.0949758   |
| spatial_knn_ridge        | EAS             | WCE             | 1000 |        0.0127199   |
| spatial_knn_ridge        | EAS             | WNA             |  975 |        0.0776326   |
| spatial_knn_ridge        | EAU             | CNA             |  438 |        0.0339345   |
| spatial_knn_ridge        | EAU             | EAS             |  110 |       -0.0417018   |
| spatial_knn_ridge        | EAU             | ENA             |  522 |       -0.0501413   |
| spatial_knn_ridge        | EAU             | MED             |  328 |        0.0333557   |
| spatial_knn_ridge        | EAU             | NCA             |  144 |        0.135618    |
| spatial_knn_ridge        | EAU             | NEU             | 1000 |       -0.0574279   |
| spatial_knn_ridge        | EAU             | NWN             |  183 |        0.052676    |
| spatial_knn_ridge        | EAU             | SAU             |  351 |       -0.00111817  |
| spatial_knn_ridge        | EAU             | WCE             | 1000 |       -0.0635234   |
| spatial_knn_ridge        | EAU             | WNA             |  975 |        0.0232115   |
| spatial_knn_ridge        | ENA             | CNA             |  438 |        0.128853    |
| spatial_knn_ridge        | ENA             | EAS             |  110 |        0.0820629   |
| spatial_knn_ridge        | ENA             | EAU             |  241 |        0.102302    |
| spatial_knn_ridge        | ENA             | MED             |  328 |        0.152189    |
| spatial_knn_ridge        | ENA             | NCA             |  144 |        0.282963    |
| spatial_knn_ridge        | ENA             | NEU             | 1000 |        0.00635707  |
| spatial_knn_ridge        | ENA             | NWN             |  183 |        0.168616    |
| spatial_knn_ridge        | ENA             | SAU             |  351 |        0.091151    |
| spatial_knn_ridge        | ENA             | WCE             | 1000 |        0.000601824 |
| spatial_knn_ridge        | ENA             | WNA             |  975 |        0.139409    |
| spatial_knn_ridge        | MED             | CNA             |  438 |        0.00889744  |
| spatial_knn_ridge        | MED             | EAS             |  110 |       -0.0611087   |
| spatial_knn_ridge        | MED             | EAU             |  241 |       -0.0256161   |
| spatial_knn_ridge        | MED             | ENA             |  522 |       -0.0621207   |
| spatial_knn_ridge        | MED             | NCA             |  144 |        0.0937247   |
| spatial_knn_ridge        | MED             | NEU             | 1000 |       -0.0705233   |
| spatial_knn_ridge        | MED             | NWN             |  183 |        0.0264992   |
| spatial_knn_ridge        | MED             | SAU             |  351 |       -0.0229971   |
| spatial_knn_ridge        | MED             | WCE             | 1000 |       -0.0765248   |
| spatial_knn_ridge        | MED             | WNA             |  975 |       -0.00354329  |
| spatial_knn_ridge        | NCA             | CNA             |  438 |       -0.0647687   |
| spatial_knn_ridge        | NCA             | EAS             |  110 |       -0.11839     |
| spatial_knn_ridge        | NCA             | EAU             |  241 |       -0.0853752   |
| spatial_knn_ridge        | NCA             | ENA             |  522 |       -0.110387    |
| spatial_knn_ridge        | NCA             | MED             |  328 |       -0.0647036   |
| spatial_knn_ridge        | NCA             | NEU             | 1000 |       -0.0996923   |
| spatial_knn_ridge        | NCA             | NWN             |  183 |       -0.0146303   |
| spatial_knn_ridge        | NCA             | SAU             |  351 |       -0.0748668   |
| spatial_knn_ridge        | NCA             | WCE             | 1000 |       -0.110766    |
| spatial_knn_ridge        | NCA             | WNA             |  975 |       -0.0656461   |
| spatial_knn_ridge        | NEU             | CNA             |  438 |        0.15733     |
| spatial_knn_ridge        | NEU             | EAS             |  110 |        0.0374135   |
| spatial_knn_ridge        | NEU             | EAU             |  241 |        0.102643    |
| spatial_knn_ridge        | NEU             | ENA             |  522 |        0.0404054   |
| spatial_knn_ridge        | NEU             | MED             |  328 |        0.150348    |
| spatial_knn_ridge        | NEU             | NCA             |  144 |        0.284644    |
| spatial_knn_ridge        | NEU             | NWN             |  183 |        0.126943    |
| spatial_knn_ridge        | NEU             | SAU             |  351 |        0.0973727   |
| spatial_knn_ridge        | NEU             | WCE             | 1000 |        0.00597945  |
| spatial_knn_ridge        | NEU             | WNA             |  975 |        0.115966    |
| spatial_knn_ridge        | NWN             | CNA             |  438 |        0.129955    |
| spatial_knn_ridge        | NWN             | EAS             |  110 |       -0.00625909  |
| spatial_knn_ridge        | NWN             | EAU             |  241 |        0.0591864   |
| spatial_knn_ridge        | NWN             | ENA             |  522 |        0.10638     |
| spatial_knn_ridge        | NWN             | MED             |  328 |        0.067828    |
| spatial_knn_ridge        | NWN             | NCA             |  144 |        0.141888    |
| spatial_knn_ridge        | NWN             | NEU             | 1000 |       -0.0131737   |
| spatial_knn_ridge        | NWN             | SAU             |  351 |        0.072654    |
| spatial_knn_ridge        | NWN             | WCE             | 1000 |        0.0100192   |
| spatial_knn_ridge        | NWN             | WNA             |  975 |        0.00151608  |
| spatial_knn_ridge        | SAU             | CNA             |  438 |        0.0349628   |
| spatial_knn_ridge        | SAU             | EAS             |  110 |       -0.020991    |
| spatial_knn_ridge        | SAU             | EAU             |  241 |        0.00484886  |
| spatial_knn_ridge        | SAU             | ENA             |  522 |       -0.056889    |
| spatial_knn_ridge        | SAU             | MED             |  328 |        0.0377736   |
| spatial_knn_ridge        | SAU             | NCA             |  144 |        0.146386    |
| spatial_knn_ridge        | SAU             | NEU             | 1000 |       -0.0519868   |
| spatial_knn_ridge        | SAU             | NWN             |  183 |        0.0654791   |
| spatial_knn_ridge        | SAU             | WCE             | 1000 |       -0.063131    |
| spatial_knn_ridge        | SAU             | WNA             |  975 |        0.0378609   |
| spatial_knn_ridge        | WCE             | CNA             |  438 |        0.144707    |
| spatial_knn_ridge        | WCE             | EAS             |  110 |        0.0594805   |
| spatial_knn_ridge        | WCE             | EAU             |  241 |        0.101245    |
| spatial_knn_ridge        | WCE             | ENA             |  522 |        0.0181536   |
| spatial_knn_ridge        | WCE             | MED             |  328 |        0.150022    |
| spatial_knn_ridge        | WCE             | NCA             |  144 |        0.288121    |
| spatial_knn_ridge        | WCE             | NEU             | 1000 |        0.00187613  |
| spatial_knn_ridge        | WCE             | NWN             |  183 |        0.143919    |
| spatial_knn_ridge        | WCE             | SAU             |  351 |        0.0912289   |
| spatial_knn_ridge        | WCE             | WNA             |  975 |        0.129082    |
| spatial_knn_ridge        | WNA             | CNA             |  438 |        0.0518766   |
| spatial_knn_ridge        | WNA             | EAS             |  110 |       -0.0666356   |
| spatial_knn_ridge        | WNA             | EAU             |  241 |        0.00511311  |
| spatial_knn_ridge        | WNA             | ENA             |  522 |       -0.00521323  |
| spatial_knn_ridge        | WNA             | MED             |  328 |        0.0306563   |
| spatial_knn_ridge        | WNA             | NCA             |  144 |        0.114741    |
| spatial_knn_ridge        | WNA             | NEU             | 1000 |       -0.0488243   |
| spatial_knn_ridge        | WNA             | NWN             |  183 |        0.0236599   |
| spatial_knn_ridge        | WNA             | SAU             |  351 |        0.0186988   |
| spatial_knn_ridge        | WNA             | WCE             | 1000 |       -0.0377551   |
| stgcn_diffusion          | CNA             | EAS             |  110 |        0.745035    |
| stgcn_diffusion          | CNA             | EAU             |  241 |        0.13085     |
| stgcn_diffusion          | CNA             | ENA             |  522 |        0.0633677   |
| stgcn_diffusion          | CNA             | MED             |  328 |        0.10199     |
| stgcn_diffusion          | CNA             | NCA             |  144 |        0.0250245   |
| stgcn_diffusion          | CNA             | NEU             | 1000 |        0.0998095   |
| stgcn_diffusion          | CNA             | NWN             |  183 |        0.184426    |
| stgcn_diffusion          | CNA             | SAU             |  351 |        0.0710189   |
| stgcn_diffusion          | CNA             | WCE             | 1000 |        0.0665974   |
| stgcn_diffusion          | CNA             | WNA             |  975 |        0.121122    |
| stgcn_diffusion          | EAS             | CNA             |  438 |        0.12368     |
| stgcn_diffusion          | EAS             | EAU             |  241 |        0.028914    |
| stgcn_diffusion          | EAS             | ENA             |  522 |        0.183724    |
| stgcn_diffusion          | EAS             | MED             |  328 |        0.0159779   |
| stgcn_diffusion          | EAS             | NCA             |  144 |        0.0124404   |
| stgcn_diffusion          | EAS             | NEU             | 1000 |        0.0422626   |
| stgcn_diffusion          | EAS             | NWN             |  183 |        0.0701027   |
| stgcn_diffusion          | EAS             | SAU             |  351 |        0.0236555   |
| stgcn_diffusion          | EAS             | WCE             | 1000 |        0.0352904   |
| stgcn_diffusion          | EAS             | WNA             |  975 |        0.00998092  |
| stgcn_diffusion          | EAU             | CNA             |  438 |        0.072267    |
| stgcn_diffusion          | EAU             | EAS             |  110 |       -0.0328218   |
| stgcn_diffusion          | EAU             | ENA             |  522 |        0.122446    |
| stgcn_diffusion          | EAU             | MED             |  328 |        0.00171219  |
| stgcn_diffusion          | EAU             | NCA             |  144 |        0.000337697 |
| stgcn_diffusion          | EAU             | NEU             | 1000 |        0.0308494   |
| stgcn_diffusion          | EAU             | NWN             |  183 |        0.117173    |
| stgcn_diffusion          | EAU             | SAU             |  351 |        0.00247433  |
| stgcn_diffusion          | EAU             | WCE             | 1000 |        0.0109992   |
| stgcn_diffusion          | EAU             | WNA             |  975 |        0.024865    |
| stgcn_diffusion          | ENA             | CNA             |  438 |        0.0108596   |
| stgcn_diffusion          | ENA             | EAS             |  110 |        0.15447     |
| stgcn_diffusion          | ENA             | EAU             |  241 |        0.0790341   |
| stgcn_diffusion          | ENA             | MED             |  328 |        0.0489863   |
| stgcn_diffusion          | ENA             | NCA             |  144 |        0.00398034  |
| stgcn_diffusion          | ENA             | NEU             | 1000 |        0.0809931   |
| stgcn_diffusion          | ENA             | NWN             |  183 |        0.165298    |
| stgcn_diffusion          | ENA             | SAU             |  351 |        0.0438189   |
| stgcn_diffusion          | ENA             | WCE             | 1000 |        0.0407407   |
| stgcn_diffusion          | ENA             | WNA             |  975 |        0.0831236   |
| stgcn_diffusion          | MED             | CNA             |  438 |        0.0774605   |
| stgcn_diffusion          | MED             | EAS             |  110 |       -0.0477401   |
| stgcn_diffusion          | MED             | EAU             |  241 |        0.0104373   |
| stgcn_diffusion          | MED             | ENA             |  522 |        0.118226    |
| stgcn_diffusion          | MED             | NCA             |  144 |        0.00143091  |
| stgcn_diffusion          | MED             | NEU             | 1000 |        0.0312951   |
| stgcn_diffusion          | MED             | NWN             |  183 |        0.12497     |
| stgcn_diffusion          | MED             | SAU             |  351 |        0.000129453 |
| stgcn_diffusion          | MED             | WCE             | 1000 |        0.00471607  |
| stgcn_diffusion          | MED             | WNA             |  975 |        0.035405    |
| stgcn_diffusion          | NCA             | CNA             |  438 |        0.0643289   |
| stgcn_diffusion          | NCA             | EAS             |  110 |       -0.00457117  |
| stgcn_diffusion          | NCA             | EAU             |  241 |        0.00953237  |
| stgcn_diffusion          | NCA             | ENA             |  522 |        0.108934    |
| stgcn_diffusion          | NCA             | MED             |  328 |        0.00556233  |
| stgcn_diffusion          | NCA             | NEU             | 1000 |        0.0620738   |
| stgcn_diffusion          | NCA             | NWN             |  183 |        0.163989    |
| stgcn_diffusion          | NCA             | SAU             |  351 |        0.00877604  |
| stgcn_diffusion          | NCA             | WCE             | 1000 |        0.0227181   |
| stgcn_diffusion          | NCA             | WNA             |  975 |        0.0508891   |
| stgcn_diffusion          | NEU             | CNA             |  438 |        0.121788    |
| stgcn_diffusion          | NEU             | EAS             |  110 |       -0.00948034  |
| stgcn_diffusion          | NEU             | EAU             |  241 |        0.030341    |
| stgcn_diffusion          | NEU             | ENA             |  522 |        0.166494    |
| stgcn_diffusion          | NEU             | MED             |  328 |        0.0163353   |
| stgcn_diffusion          | NEU             | NCA             |  144 |        0.0233765   |
| stgcn_diffusion          | NEU             | NWN             |  183 |        0.0761143   |
| stgcn_diffusion          | NEU             | SAU             |  351 |        0.0225972   |
| stgcn_diffusion          | NEU             | WCE             | 1000 |        0.00980363  |
| stgcn_diffusion          | NEU             | WNA             |  975 |        0.0258153   |
| stgcn_diffusion          | NWN             | CNA             |  438 |        0.238282    |
| stgcn_diffusion          | NWN             | EAS             |  110 |        0.482311    |
| stgcn_diffusion          | NWN             | EAU             |  241 |        0.169155    |
| stgcn_diffusion          | NWN             | ENA             |  522 |        0.356902    |
| stgcn_diffusion          | NWN             | MED             |  328 |        0.0920833   |
| stgcn_diffusion          | NWN             | NCA             |  144 |        0.0470021   |
| stgcn_diffusion          | NWN             | NEU             | 1000 |        0.125826    |
| stgcn_diffusion          | NWN             | SAU             |  351 |        0.130118    |
| stgcn_diffusion          | NWN             | WCE             | 1000 |        0.140803    |
| stgcn_diffusion          | NWN             | WNA             |  975 |        0.0195863   |
| stgcn_diffusion          | SAU             | CNA             |  438 |        0.085021    |
| stgcn_diffusion          | SAU             | EAS             |  110 |       -0.0398002   |
| stgcn_diffusion          | SAU             | EAU             |  241 |        0.0158222   |
| stgcn_diffusion          | SAU             | ENA             |  522 |        0.124404    |
| stgcn_diffusion          | SAU             | MED             |  328 |        0.000945651 |
| stgcn_diffusion          | SAU             | NCA             |  144 |        0.00496014  |
| stgcn_diffusion          | SAU             | NEU             | 1000 |        0.0340681   |
| stgcn_diffusion          | SAU             | NWN             |  183 |        0.130063    |
| stgcn_diffusion          | SAU             | WCE             | 1000 |        0.00527636  |
| stgcn_diffusion          | SAU             | WNA             |  975 |        0.0424978   |
| stgcn_diffusion          | WCE             | CNA             |  438 |        0.0972737   |
| stgcn_diffusion          | WCE             | EAS             |  110 |       -0.0059573   |
| stgcn_diffusion          | WCE             | EAU             |  241 |        0.0340483   |
| stgcn_diffusion          | WCE             | ENA             |  522 |        0.128748    |
| stgcn_diffusion          | WCE             | MED             |  328 |        0.0125491   |
| stgcn_diffusion          | WCE             | NCA             |  144 |        0.0170096   |
| stgcn_diffusion          | WCE             | NEU             | 1000 |        0.0199373   |
| stgcn_diffusion          | WCE             | NWN             |  183 |        0.140688    |
| stgcn_diffusion          | WCE             | SAU             |  351 |        0.0100959   |
| stgcn_diffusion          | WCE             | WNA             |  975 |        0.0546018   |
| stgcn_diffusion          | WNA             | CNA             |  438 |        0.127533    |
| stgcn_diffusion          | WNA             | EAS             |  110 |       -0.0691345   |
| stgcn_diffusion          | WNA             | EAU             |  241 |        0.0444993   |
| stgcn_diffusion          | WNA             | ENA             |  522 |        0.18892     |
| stgcn_diffusion          | WNA             | MED             |  328 |        0.0272027   |
| stgcn_diffusion          | WNA             | NCA             |  144 |        0.0125525   |
| stgcn_diffusion          | WNA             | NEU             | 1000 |        0.0440578   |
| stgcn_diffusion          | WNA             | NWN             |  183 |        0.0498639   |
| stgcn_diffusion          | WNA             | SAU             |  351 |        0.0475261   |
| stgcn_diffusion          | WNA             | WCE             | 1000 |        0.0584507   |

## KBS predictive comparison

| forecast_model           | feature_set         | cv_kind                 | estimator     |     n |   n_features |       mae |           r2 |
|:-------------------------|:--------------------|:------------------------|:--------------|------:|-------------:|----------:|-------------:|
| graphwavenet_transfer    | physical_knowledge  | leave_target_region_out | ridge         | 52920 |           12 | 0.0928322 |  0.115498    |
| graphwavenet_transfer    | physical_knowledge  | leave_target_region_out | random_forest | 52920 |           12 | 0.0824801 |  0.191948    |
| graphwavenet_transfer    | generic_shift       | leave_target_region_out | ridge         | 52920 |           11 | 0.10565   | -0.108726    |
| graphwavenet_transfer    | generic_shift       | leave_target_region_out | random_forest | 52920 |           11 | 0.0948381 | -0.079033    |
| graphwavenet_transfer    | physical_plus_shift | leave_target_region_out | ridge         | 52920 |           23 | 0.0951218 |  0.0833423   |
| graphwavenet_transfer    | physical_plus_shift | leave_target_region_out | random_forest | 52920 |           23 | 0.0816962 |  0.178286    |
| graphwavenet_transfer    | physical_knowledge  | group_by_cell           | ridge         | 52920 |           12 | 0.0915342 |  0.154684    |
| graphwavenet_transfer    | physical_knowledge  | group_by_cell           | random_forest | 52920 |           12 | 0.0754853 |  0.333237    |
| graphwavenet_transfer    | generic_shift       | group_by_cell           | ridge         | 52920 |           11 | 0.0945899 |  0.00492562  |
| graphwavenet_transfer    | generic_shift       | group_by_cell           | random_forest | 52920 |           11 | 0.0805845 |  0.154694    |
| graphwavenet_transfer    | physical_plus_shift | group_by_cell           | ridge         | 52920 |           23 | 0.0916544 |  0.151311    |
| graphwavenet_transfer    | physical_plus_shift | group_by_cell           | random_forest | 52920 |           23 | 0.0623983 |  0.429584    |
| linear_window            | physical_knowledge  | leave_target_region_out | ridge         | 52920 |           12 | 1.1465    | -0.00443514  |
| linear_window            | physical_knowledge  | leave_target_region_out | random_forest | 52920 |           12 | 1.17507   | -0.054088    |
| linear_window            | generic_shift       | leave_target_region_out | ridge         | 52920 |           11 | 1.14513   | -0.000141581 |
| linear_window            | generic_shift       | leave_target_region_out | random_forest | 52920 |           11 | 1.147     | -0.00175601  |
| linear_window            | physical_plus_shift | leave_target_region_out | ridge         | 52920 |           23 | 1.14696   | -0.00477318  |
| linear_window            | physical_plus_shift | leave_target_region_out | random_forest | 52920 |           23 | 1.17464   | -0.0523437   |
| linear_window            | physical_knowledge  | group_by_cell           | ridge         | 52920 |           12 | 1.14752   | -0.00722478  |
| linear_window            | physical_knowledge  | group_by_cell           | random_forest | 52920 |           12 | 1.18612   | -0.107131    |
| linear_window            | generic_shift       | group_by_cell           | ridge         | 52920 |           11 | 1.14512   | -0.000332527 |
| linear_window            | generic_shift       | group_by_cell           | random_forest | 52920 |           11 | 1.14751   | -0.00636754  |
| linear_window            | physical_plus_shift | group_by_cell           | ridge         | 52920 |           23 | 1.14764   | -0.00735212  |
| linear_window            | physical_plus_shift | group_by_cell           | random_forest | 52920 |           23 | 1.18553   | -0.105715    |
| patchtst_small           | physical_knowledge  | leave_target_region_out | ridge         | 52920 |           12 | 1.15308   | -0.00404862  |
| patchtst_small           | physical_knowledge  | leave_target_region_out | random_forest | 52920 |           12 | 1.18087   | -0.0528477   |
| patchtst_small           | generic_shift       | leave_target_region_out | ridge         | 52920 |           11 | 1.15145   | -9.46195e-05 |
| patchtst_small           | generic_shift       | leave_target_region_out | random_forest | 52920 |           11 | 1.15429   | -0.00258584  |
| patchtst_small           | physical_plus_shift | leave_target_region_out | ridge         | 52920 |           23 | 1.15353   | -0.00431611  |
| patchtst_small           | physical_plus_shift | leave_target_region_out | random_forest | 52920 |           23 | 1.1804    | -0.0516455   |
| patchtst_small           | physical_knowledge  | group_by_cell           | ridge         | 52920 |           12 | 1.15385   | -0.00624107  |
| patchtst_small           | physical_knowledge  | group_by_cell           | random_forest | 52920 |           12 | 1.19095   | -0.098212    |
| patchtst_small           | generic_shift       | group_by_cell           | ridge         | 52920 |           11 | 1.15135   | -0.000210421 |
| patchtst_small           | generic_shift       | group_by_cell           | random_forest | 52920 |           11 | 1.15396   | -0.00604316  |
| patchtst_small           | physical_plus_shift | group_by_cell           | ridge         | 52920 |           23 | 1.15394   | -0.00629898  |
| patchtst_small           | physical_plus_shift | group_by_cell           | random_forest | 52920 |           23 | 1.1911    | -0.0986906   |
| regional_doy_climatology | physical_knowledge  | leave_target_region_out | ridge         | 52920 |           12 | 0.705195  | -0.0363335   |
| regional_doy_climatology | physical_knowledge  | leave_target_region_out | random_forest | 52920 |           12 | 0.722998  | -0.0599063   |
| regional_doy_climatology | generic_shift       | leave_target_region_out | ridge         | 52920 |           11 | 0.633075  |  0.0537091   |
| regional_doy_climatology | generic_shift       | leave_target_region_out | random_forest | 52920 |           11 | 0.796475  | -0.474359    |
| regional_doy_climatology | physical_plus_shift | leave_target_region_out | ridge         | 52920 |           23 | 0.544679  |  0.215932    |
| regional_doy_climatology | physical_plus_shift | leave_target_region_out | random_forest | 52920 |           23 | 0.691048  | -0.335463    |
| regional_doy_climatology | physical_knowledge  | group_by_cell           | ridge         | 52920 |           12 | 0.659955  |  0.0373194   |
| regional_doy_climatology | physical_knowledge  | group_by_cell           | random_forest | 52920 |           12 | 0.653518  |  0.0494774   |
| regional_doy_climatology | generic_shift       | group_by_cell           | ridge         | 52920 |           11 | 0.463086  |  0.388475    |
| regional_doy_climatology | generic_shift       | group_by_cell           | random_forest | 52920 |           11 | 0.107502  |  0.96509     |
| regional_doy_climatology | physical_plus_shift | group_by_cell           | ridge         | 52920 |           23 | 0.401527  |  0.567417    |
| regional_doy_climatology | physical_plus_shift | group_by_cell           | random_forest | 52920 |           23 | 0.126616  |  0.762438    |
| spatial_knn_ridge        | physical_knowledge  | leave_target_region_out | ridge         | 52920 |           12 | 0.0723575 | -0.142355    |
| spatial_knn_ridge        | physical_knowledge  | leave_target_region_out | random_forest | 52920 |           12 | 0.0700309 | -0.00414281  |
| spatial_knn_ridge        | generic_shift       | leave_target_region_out | ridge         | 52920 |           11 | 0.074349  | -0.168172    |
| spatial_knn_ridge        | generic_shift       | leave_target_region_out | random_forest | 52920 |           11 | 0.0973462 | -0.950425    |
| spatial_knn_ridge        | physical_plus_shift | leave_target_region_out | ridge         | 52920 |           23 | 0.0720928 | -0.252959    |
| spatial_knn_ridge        | physical_plus_shift | leave_target_region_out | random_forest | 52920 |           23 | 0.0912488 | -0.806675    |
| spatial_knn_ridge        | physical_knowledge  | group_by_cell           | ridge         | 52920 |           12 | 0.0678636 |  0.000997523 |
| spatial_knn_ridge        | physical_knowledge  | group_by_cell           | random_forest | 52920 |           12 | 0.0606231 |  0.31768     |
| spatial_knn_ridge        | generic_shift       | group_by_cell           | ridge         | 52920 |           11 | 0.0589933 |  0.198301    |
| spatial_knn_ridge        | generic_shift       | group_by_cell           | random_forest | 52920 |           11 | 0.0296106 |  0.653657    |
| spatial_knn_ridge        | physical_plus_shift | group_by_cell           | ridge         | 52920 |           23 | 0.0578301 |  0.131969    |
| spatial_knn_ridge        | physical_plus_shift | group_by_cell           | random_forest | 52920 |           23 | 0.0201502 |  0.838218    |
| stgcn_diffusion          | physical_knowledge  | leave_target_region_out | ridge         | 52920 |           12 | 0.0821516 |  0.0672701   |
| stgcn_diffusion          | physical_knowledge  | leave_target_region_out | random_forest | 52920 |           12 | 0.0745829 |  0.130483    |
| stgcn_diffusion          | generic_shift       | leave_target_region_out | ridge         | 52920 |           11 | 0.0916955 | -0.0661908   |
| stgcn_diffusion          | generic_shift       | leave_target_region_out | random_forest | 52920 |           11 | 0.0973999 | -0.353606    |
| stgcn_diffusion          | physical_plus_shift | leave_target_region_out | ridge         | 52920 |           23 | 0.0848351 |  0.0473097   |
| stgcn_diffusion          | physical_plus_shift | leave_target_region_out | random_forest | 52920 |           23 | 0.0779555 |  0.0601845   |
| stgcn_diffusion          | physical_knowledge  | group_by_cell           | ridge         | 52920 |           12 | 0.0814009 |  0.0747203   |
| stgcn_diffusion          | physical_knowledge  | group_by_cell           | random_forest | 52920 |           12 | 0.0726325 |  0.212144    |
| stgcn_diffusion          | generic_shift       | group_by_cell           | ridge         | 52920 |           11 | 0.0854548 | -0.00186672  |
| stgcn_diffusion          | generic_shift       | group_by_cell           | random_forest | 52920 |           11 | 0.0720159 |  0.072703    |
| stgcn_diffusion          | physical_plus_shift | group_by_cell           | ridge         | 52920 |           23 | 0.0819851 |  0.0780599   |
| stgcn_diffusion          | physical_plus_shift | group_by_cell           | random_forest | 52920 |           23 | 0.0559386 |  0.338396    |
