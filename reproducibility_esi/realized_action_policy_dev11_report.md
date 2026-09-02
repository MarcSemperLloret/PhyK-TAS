# Desarrollo de la politica de acciones realizadas

**Bloque evaluado:** 2020-2022 (desarrollo).  
**Bloque confirmatorio:** 2023-2025 no abierto.  
**Validacion externa interna:** leave-one-target-region-out (11 folds).  
**Muestra:** 330 combinaciones modelo/source/target.  
**Predictores:** 62 rasgos pre-deployment de shift fisico/climatico y familia de modelo.

## Comparacion de politicas

| policy | mean_mae | mean_regret | median_regret | mean_normalized_regret | oracle_action_accuracy |
|---|---|---|---|---|---|
| retrain | 2.563786 | 0.007542 | 0.000000 | 0.002805 | 0.703030 |
| action-value ridge | 2.566529 | 0.010286 | 0.000000 | 0.003820 | 0.630303 |
| adapt | 2.588099 | 0.031855 | 0.011407 | 0.012843 | 0.172727 |
| deploy | 2.613018 | 0.056774 | 0.031057 | 0.026288 | 0.124242 |

El regret es la diferencia de MAE respecto a la mejor accion realizada para cada par. Un valor menor es mejor.

## Acciones elegidas

Politica ridge: deploy=10, adapt=40, retrain=280.  
Oraculo observado: deploy=41, adapt=57, retrain=232.

## Resultado por target retenido

| target_region | n_pairs | mean_policy_regret | median_policy_regret | action_accuracy |
|---|---|---|---|---|
| CNA | 30.000000 | 0.002204 | 0.000000 | 0.900000 |
| EAS | 30.000000 | 0.018735 | 0.004415 | 0.433333 |
| EAU | 30.000000 | 0.006653 | 0.000000 | 0.566667 |
| ENA | 30.000000 | 0.028995 | 0.000000 | 0.566667 |
| MED | 30.000000 | 0.007396 | 0.002881 | 0.333333 |
| NCA | 30.000000 | 0.000653 | 0.000000 | 0.933333 |
| NEU | 30.000000 | 0.014783 | 0.000000 | 0.700000 |
| NWN | 30.000000 | 0.011158 | 0.000000 | 0.633333 |
| SAU | 30.000000 | 0.003964 | 0.000000 | 0.666667 |
| WCE | 30.000000 | 0.015577 | 0.000225 | 0.466667 |
| WNA | 30.000000 | 0.003024 | 0.000000 | 0.733333 |

## Diagnostico

La politica action-value no supera always-retrain: su regret medio es 0.002744 MAE mayor. No hay base para abrir el bloque confirmatorio con esta politica; primero debe revisarse el diseno sin usar 2023-2025.

Esta prueba no incorpora costes elegidos post hoc. Evalua solo calidad predictiva y utiliza rasgos calculados antes del periodo de despliegue. No constituye evidencia confirmatoria ni debe presentarse como resultado principal sin la evaluacion 2023-2025 previamente congelada.

## Hiperparametros por fold

| held_out_target | outcome | best_alpha | inner_cv_mae |
|---|---|---|---|
| CNA | benefit_adapt | 10000.000000 | 0.036420 |
| CNA | benefit_retrain | 10000.000000 | 0.054768 |
| EAS | benefit_adapt | 3162.277660 | 0.035404 |
| EAS | benefit_retrain | 316.227766 | 0.055226 |
| EAU | benefit_adapt | 10000.000000 | 0.037103 |
| EAU | benefit_retrain | 10000.000000 | 0.060806 |
| ENA | benefit_adapt | 10000.000000 | 0.036089 |
| ENA | benefit_retrain | 0.316228 | 0.049135 |
| MED | benefit_adapt | 0.316228 | 0.036553 |
| MED | benefit_retrain | 3.162278 | 0.057275 |
| NCA | benefit_adapt | 10000.000000 | 0.033202 |
| NCA | benefit_retrain | 10000.000000 | 0.056279 |
| NEU | benefit_adapt | 3162.277660 | 0.036642 |
| NEU | benefit_retrain | 10000.000000 | 0.058701 |
| NWN | benefit_adapt | 3162.277660 | 0.035646 |
| NWN | benefit_retrain | 0.316228 | 0.051960 |
| SAU | benefit_adapt | 10000.000000 | 0.037430 |
| SAU | benefit_retrain | 10000.000000 | 0.060278 |
| WCE | benefit_adapt | 3162.277660 | 0.037547 |
| WCE | benefit_retrain | 10000.000000 | 0.059187 |
| WNA | benefit_adapt | 10000.000000 | 0.037431 |
| WNA | benefit_retrain | 10000.000000 | 0.060512 |
