# Desarrollo: asignacion de reentrenamiento bajo presupuesto

**Periodo de outcomes:** 2020-2022.  
**Periodo confirmatorio 2023-2025:** no abierto.  
**Unidad de validacion:** target region retenida (11 folds).  
**Decisiones:** 330 combinaciones modelo/source/target.  
**Presupuesto:** curva completa de 0 a 30 reentrenamientos por target; no se selecciona post hoc un unico coste.

La accion barata se elige entre deploy y adapt con predicciones out-of-target. La politica ordena el beneficio esperado de retrain y asigna el presupuesto a los primeros casos.

## AUC de la curva de presupuesto

| policy | mean_budget_curve_auc | mean_excess_auc_vs_oracle |
|---|---|---|
| oracle | 2.568055 | 0.000000 |
| action_value | 2.572433 | 0.004378 |
| mmd | 2.575208 | 0.007153 |
| wasserstein | 2.575381 | 0.007326 |
| distance | 2.575588 | 0.007534 |
| mean_shift | 2.575755 | 0.007700 |
| random_expected | 2.575972 | 0.007918 |
| kl_source_target | 2.576020 | 0.007965 |

Frente a asignacion aleatoria, action-value reduce el AUC de MAE en 0.003539 y cierra el 44.7% de la distancia entre random y el oraculo restringido.

## Comparaciones pareadas por target

| baseline | mean_auc_difference | targets_action_value_better | targets_total | wilcoxon_one_sided_p |
|---|---|---|---|---|
| kl_source_target | -0.003587 | 9.000000 | 11.000000 | 0.004883 |
| random_expected | -0.003539 | 10.000000 | 11.000000 | 0.001465 |
| mean_shift | -0.003322 | 10.000000 | 11.000000 | 0.000977 |
| distance | -0.003155 | 9.000000 | 11.000000 | 0.003418 |
| wasserstein | -0.002948 | 10.000000 | 11.000000 | 0.003418 |
| mmd | -0.002775 | 9.000000 | 11.000000 | 0.006836 |

Los p-valores son exploratorios, unilaterales y no corregidos; el bloque se uso para desarrollar la politica.

## Puntos de la curva agregada

| budget_retrains | action_value | mmd | oracle | random_expected |
|---|---|---|---|---|
| 0.000000 | 2.588159 | 2.588159 | 2.588159 | 2.588159 |
| 5.000000 | 2.580812 | 2.582033 | 2.575445 | 2.584097 |
| 10.000000 | 2.574878 | 2.577551 | 2.567542 | 2.580035 |
| 15.000000 | 2.570144 | 2.574416 | 2.564100 | 2.575972 |
| 20.000000 | 2.567291 | 2.572084 | 2.562592 | 2.571910 |
| 25.000000 | 2.564829 | 2.567909 | 2.562577 | 2.567848 |
| 30.000000 | 2.563786 | 2.563786 | 2.563786 | 2.563786 |

## Veredicto de desarrollo

GO condicionado para congelar la politica budget-aware y evaluarla en 2023-2025. La politica supera a random en 10/11 targets y a MMD en 9/11, pero no supera always-retrain cuando no existe restriccion. Por tanto, el claim defendible es asignacion de reentrenamiento bajo capacidad limitada, no mejora universal de MAE.

Antes de abrir el bloque confirmatorio deben congelarse: rasgos, ridge, validacion, definicion de accion barata, curva de presupuestos y estadisticos. No se permite seleccionar tras la confirmacion un presupuesto o una metrica diferente.
