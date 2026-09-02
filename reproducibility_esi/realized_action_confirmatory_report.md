# Evaluacion confirmatoria de acciones realizadas

**Outcomes:** 2023-2025.  
**Predicciones/rankings:** congelados desde desarrollo 2020-2022.  
**Targets:** 11; **decisiones:** 330; **acciones realizadas:** 990.  
**Metrica primaria:** AUC discreto de MAE sobre presupuestos 0-30.

## Veredicto: GO CONFIRMATORIO

p primario=0.000977; diferencia media=-0.003452; targets favorables=10/11; sin deterioro medio por familia=True.

## AUC de la curva de presupuesto

| policy | mean_budget_curve_auc | mean_excess_auc_vs_oracle |
|---|---|---|
| oracle | 2.542837 | 0.000000 |
| action_value | 2.547325 | 0.004488 |
| mmd | 2.549983 | 0.007146 |
| wasserstein | 2.550384 | 0.007548 |
| distance | 2.550526 | 0.007690 |
| mean_shift | 2.550740 | 0.007904 |
| random_expected | 2.550777 | 0.007940 |
| kl_source_target | 2.551237 | 0.008401 |

Action-value cambia el AUC frente a random en -0.003452 MAE-AUC y cierra el 43.5% del gap random-oracle.

## Test primario y comparaciones secundarias

| baseline | mean_auc_difference | median_auc_difference | targets_action_value_better | targets_total | wilcoxon_one_sided_p | wilcoxon_two_sided_p | holm_adjusted_p |
|---|---|---|---|---|---|---|---|
| kl_source_target | -0.003912 | -0.001972 | 10.000000 | 11.000000 | 0.003418 | 0.006836 | 0.010254 |
| random_expected | -0.003452 | -0.001608 | 10.000000 | 11.000000 | 0.000977 | 0.001953 | nan |
| mean_shift | -0.003415 | -0.001402 | 10.000000 | 11.000000 | 0.000977 | 0.001953 | 0.004883 |
| distance | -0.003202 | -0.001865 | 10.000000 | 11.000000 | 0.002441 | 0.004883 | 0.009766 |
| wasserstein | -0.003059 | -0.001699 | 9.000000 | 11.000000 | 0.003418 | 0.006836 | 0.010254 |
| mmd | -0.002658 | -0.001832 | 10.000000 | 11.000000 | 0.004883 | 0.009766 | 0.010254 |

El test frente a random es el unico primario. Los p-valores Holm corresponden solo a los cinco baselines shift-only secundarios.

El test primario preespecificado es unilateral. La columna `wilcoxon_two_sided_p` es una comprobacion de robustez posterior a la confirmacion: no redefine el estimando, no entra en la regla GO/NO-GO y no se corrige por multiplicidad.

## Diagnostico por familia

| model | mean_auc_difference | targets_better | targets_total | worst_target_difference |
|---|---|---|---|---|
| graphwavenet_transfer | -0.001617 | 8.000000 | 11.000000 | 0.001839 |
| patchtst_small | -0.001858 | 8.000000 | 11.000000 | 0.000677 |
| spatial_knn_ridge | -0.000846 | 9.000000 | 11.000000 | 0.000535 |

## Heterogeneidad de acciones confirmatorias

| model | adapt_improves_deploy | n | best_deploy | best_adapt | best_retrain | mean_adapt_minus_deploy | mean_retrain_minus_deploy |
|---|---|---|---|---|---|---|---|
| graphwavenet_transfer | 106.000000 | 110.000000 | 1.000000 | 10.000000 | 99.000000 | -0.029446 | -0.079631 |
| patchtst_small | 103.000000 | 110.000000 | 3.000000 | 14.000000 | 93.000000 | -0.023374 | -0.041677 |
| spatial_knn_ridge | 71.000000 | 110.000000 | 36.000000 | 24.000000 | 50.000000 | -0.030537 | -0.038933 |

Oraculo global: deploy=40, adapt=48, retrain=242.

## Puntos de la curva agregada

| budget_retrains | action_value | mmd | oracle | random_expected |
|---|---|---|---|---|
| 0.000000 | 2.563612 | 2.563612 | 2.563612 | 2.563612 |
| 5.000000 | 2.555865 | 2.557194 | 2.550180 | 2.559334 |
| 10.000000 | 2.550143 | 2.552504 | 2.542314 | 2.555055 |
| 15.000000 | 2.545211 | 2.549166 | 2.539095 | 2.550777 |
| 20.000000 | 2.542085 | 2.546518 | 2.537431 | 2.546499 |
| 25.000000 | 2.539222 | 2.542508 | 2.537090 | 2.542220 |
| 30.000000 | 2.537942 | 2.537942 | 2.537942 | 2.537942 |

## Interpretacion permitida

El resultado solo respalda asignacion de capacidad limitada de reentrenamiento si el veredicto es GO. No respalda superioridad frente a always-retrain sin restriccion, mejora universal del forecaster ni novedad arquitectonica.
