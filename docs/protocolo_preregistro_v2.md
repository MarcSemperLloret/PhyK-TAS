# Protocolo preregistro v2

## Estado

Este documento consolida las decisiones operativas tomadas despues de las fases de viabilidad AR6, cobertura temporal, deduplicacion y potencia preliminar.

No es todavia un preregistro publico. Queda pendiente subirlo a OSF o equivalente junto con los artefactos reproducibles.

## Pregunta cientifica

Evaluar si la degradacion out-of-region de modelos espaciotemporales de precipitacion diaria puede anticiparse mediante descriptores fisicos preregistrados del regimen destino, y si esos descriptores aportan informacion por encima de metricas genericas de distribution shift.

## Enfoque para Knowledge-Based Systems

El articulo se orienta a Knowledge-Based Systems como un sistema inteligente de evaluacion de transferibilidad, no como un paper puramente climatologico.

Nombre operativo del marco:

- `PhyK-TAS`: Physically informed Knowledge-based Transferability Assessment System.

Componentes:

- capa de conocimiento regional: IPCC AR6, jerarquia region/celda/estacion, metadatos de estacion;
- capa de conocimiento fisico: descriptores preregistrados de intermitencia, estacionalidad, extremos, dependencia espacial y orografia;
- capa de shift generico: KL, Wasserstein, MMD, shift temporal y controles geograficos;
- capa de evaluacion de modelos: climatologia, persistencia, PatchTST y ST-GNN;
- capa de inferencia de degradacion: modelo jerarquico o bootstrap bloqueado;
- capa de decision: estimacion de riesgo de fallo, recomendacion deploy/retrain/adapt y explicacion por descriptores.

Contribucion principal para KBS:

- un marco knowledge-based para predecir fallo de modelos antes del despliegue out-of-region;
- una representacion explicita de conocimiento fisico como base de decision;
- una comparacion preregistrada contra metricas genericas de distribution shift;
- evidencia de robustez o limitacion de ese conocimiento fisico bajo diferentes arquitecturas.

## Variable

- Variable principal: `precip_mm`.
- Resolucion: diaria.
- Horizonte subdiario: excluido del nucleo del paper.

## Fuentes

### Nucleo principal

- `global_ghcnd_01`
- `eur_ecad_01`

Estas dos fuentes definen el benchmark principal. Se usan solo despues de:

- asignacion a regiones IPCC AR6 land;
- interseccion temporal estable;
- deduplicacion entre fuentes;
- filtrado de cobertura.

### Validacion fuerte

- `deu_dwd_cdc_01`
- `che_meteoswiss_01`

Rol: comprobar robustez frente a proveedor en Europa. No inflan el n principal.

### Validacion limitada

- `esp_aemet_daily_hist_01`: sensibilidad mediterranea o validacion reciente.
- `esp_avamet_01`: sensibilidad 2019-2025/2020-2025, no nucleo.
- `can_eccc_climate_stations_01`: replicacion externa opcional, no region principal.

## Regiones

Particion primaria:

- IPCC AR6 land regions via `regionmask.defined_regions.ar6.land`.

Regiones principales:

- `MED`
- `WCE`
- `NEU`

Artefactos:

- `stations_ar6.csv`
- `stations_ar6_summary.csv`
- `stations_ar6_map.png`

Revision visual:

- aceptada;
- el mapa no muestra claramente el contorno de Europa, pero la forma de la nube de estaciones y los limites AR6 permiten verificar la asignacion;
- no se observaron anomalias sistematicas.

## Periodo temporal

Decision operativa:

- inicio historico: 2005.

Bloques:

- train historico: 2005-2012;
- validacion historica: 2013-2015;
- validacion/despliegue intermedio: 2016-2019;
- test reciente: 2020-2025.

Justificacion:

- con inicio 2000, `MED` queda por debajo del umbral operativo a 95%;
- con inicio 2005, `MED` supera por poco el umbral a 95% y queda mucho mas solido a 80%;
- `WCE` y `NEU` son robustas bajo ambos inicios.

## Cobertura

Regla final candidata:

- `WCE`: principal a 95%;
- `NEU`: principal a 95%;
- `MED`: principal a 80% con mascara explicita de missingness; sensibilidad estricta a 95%.

Conteos post-deduplicacion para fuentes nucleares, inicio 2005:

| region | n80 | n95 | decision |
|---|---:|---:|---|
| MED | 913 | 311 | principal 80%, sensibilidad 95% |
| WCE | 4705 | 4100 | principal 95% |
| NEU | 2704 | 2345 | principal 95% |

## Deduplicacion

Regla aplicada:

- identidad por WMO ID;
- identidad por `candidate_duplicate_key`;
- union espacial entre fuentes a <= 1 km solo con metadatos compatibles: nombre normalizado, WMO o elevacion dentro de +/- 10 m;
- no se deduplican estaciones de la misma fuente solo por proximidad.

Artefactos:

- `dedup_log.csv`;
- `viability_post_dedup.csv`;
- `viability_dedup_comparison.md`;
- `dedup_audit_sample_with_correlations.csv`;
- `dedup_audit_report.md`.

Auditoria automatizada:

- muestra de 30 pares;
- correlacion diaria 2005-2025 >= 0.9997 en todos los pares muestreados;
- miles de dias solapados en todos los pares muestreados.

Decision de auditoria:

- aceptada para candidato de preregistro;
- 30 pares muestreados con correlacion diaria >= 0.9997;
- no se identificaron falsos positivos plausibles en esta etapa.

## Unidad estadistica

Unidad primaria:

- estacion destino post-deduplicacion.

Unidad secundaria:

- celda espacial 5 x 5 grados dentro de region AR6.

Inferencia:

- no se asumira independencia IID por estacion;
- se usaran modelos jerarquicos o bootstrap por bloques con estructura estacion/celda/region/fuente.

## Potencia preliminar

Artefacto:

- `power_analysis.md`.
- `pilot_light_power.md`.
- `pilot_light_degradation.csv`.

Resultado:

- WCE y NEU tienen n suficiente por estacion y mejor soporte por celdas;
- MED es viable por estaciones, pero es la region limitante por celdas 5 x 5;
- se ejecuto un piloto ligero con climatologia regional diaria para estimar varianza inicial de degradacion.

Piloto ligero:

- hasta 300 estaciones post-dedup por region;
- train 2005-2012;
- test 2020-2025;
- degradacion = MAE de climatologia media out-region menos MAE de climatologia in-region.

Resumen del piloto:

| region | n_station | n_cell5 | mean_degradation | sd_degradation | median_ratio |
|---|---:|---:|---:|---:|---:|
| MED | 300 | 17 | 0.239514 | 0.050902 | 1.076247 |
| NEU | 300 | 23 | -0.078177 | 0.032644 | 0.971809 |
| WCE | 300 | 12 | 0.028432 | 0.045151 | 1.009435 |

Uso en preregistro:

- el piloto justifica mantener analisis jerarquico y no asumir independencia por estacion;
- el signo negativo en NEU bajo baseline simple se reporta como advertencia contra conclusiones post-hoc;
- el piloto no sustituye el analisis principal con modelos y baselines preregistrados.

## Hipotesis principal

Los descriptores fisicos preregistrados explican la degradacion out-of-region mejor que baselines genericos de distribution shift.

Metrica primaria:

- log-loss out-of-fold para degradacion ordinal o binaria severa/no severa;
- folds bloqueados por region AR6;
- incertidumbre mediante bootstrap por bloques.

Metricas secundarias:

- RMSE/MAE out-of-fold para degradacion continua;
- ranking loss para ordenar estaciones/celdas por dificultad;
- peor-caso regional.

## Baselines de distribution shift

Baselines preregistrados:

- divergencia KL de distribuciones marginales discretizadas de `precip_mm`;
- distancia de Wasserstein;
- MMD sobre ocurrencia, intensidad, percentiles, rachas secas y estacionalidad mensual;
- shift temporal en media, varianza, fraccion de dias humedos y percentiles altos;
- distancia geografica y diferencia de elevacion como controles.

Artefactos iniciales:

- `distribution_shift_baselines.csv`;
- `distribution_shift_baselines_report.md`.

Resultado descriptivo inicial:

- MED se separa claramente de WCE/NEU por KL, Wasserstein, MMD y diferencias de fraccion humeda;
- WCE y NEU son mucho mas cercanas entre si;
- esto confirma que los baselines genericos contienen senal fuerte, por lo que el contraste contra conocimiento fisico no sera trivial.

## Descriptores fisicos

Descriptores calculados en la capa de conocimiento fisico:

- fraccion de dias humedos;
- intensidad condicional en dias humedos;
- coeficiente de variacion;
- amplitud anual de climatologia mensual;
- concentracion estacional en los tres meses mas humedos;
- autocorrelacion de ocurrencia;
- autocorrelacion de intensidad;
- longitud media y percentil 95 de rachas secas;
- P95/P99 de precipitacion humeda;
- tail index o aproximacion robusta de cola;
- escala espacial de correlacion;
- gradiente orografico.

Artefactos:

- `physical_descriptors_station.csv`;
- `physical_descriptors_cell5.csv`;
- `physical_descriptors_region.csv`;
- `physical_descriptors_report.md`.

Resumen regional inicial, periodo 2005-2012:

| region | n_stations | wet_day_fraction | wet_intensity | dry_spell_p95 | wet_p99 | top3_fraction |
|---|---:|---:|---:|---:|---:|---:|
| MED | 913 | 0.199131 | 9.965448 | 24.0 | 51.1130 | 0.401968 |
| NEU | 2345 | 0.342048 | 6.451232 | 13.0 | 29.0600 | 0.363421 |
| WCE | 4100 | 0.321971 | 6.471139 | 13.0 | 30.5085 | 0.362017 |

Interpretacion preregistrada:

- MED muestra menor frecuencia de lluvia, mayor intensidad condicional y rachas secas mas largas;
- NEU y WCE son mas humedas/frecuentes y con menor intensidad extrema diaria mediana;
- estos patrones justifican que la capa fisica sea central para el sistema PhyK-TAS, pero no garantizan que supere a los baselines genericos.

Si el analisis de potencia final exige reducir dimensionalidad, se congelara un subconjunto antes de entrenar modelos profundos.

## Modelos

Baselines:

- climatologia/persistencia;
- modelo temporal local por estacion;
- modelo espacial simple.

Capa ligera ya generada:

- `light_degradation_station.csv`;
- `light_degradation_pair_summary.csv`;
- `light_degradation_matrix_report.md`.

Modelo ligero actual:

- climatologia diaria regional entrenada en 2005-2012;
- baseline local: climatologia mensual por estacion;
- evaluacion: 2020-2025.

Resultado cualitativo inicial:

- transferir climatologias de WCE/NEU hacia MED degrada fuertemente el MAE;
- transferir MED hacia WCE/NEU no siempre degrada el MAE en este baseline simple;
- el comportamiento asimetrico confirma que la matriz origen-destino es necesaria y que no basta con una distancia simetrica entre regiones.

Modelos principales:

- Graph WaveNet o AGCRN como ST-GNN;
- PatchTST como baseline temporal no-grafo.

Experimento forecasting inicial:

- `forecast_dataset_operational_sample.npz`;
- `forecast_dataset_operational_sample_metadata.csv`;
- `forecast_baseline_station_metrics.csv`;
- `forecast_baseline_pair_summary.csv`;
- `forecast_persistence_station_metrics.csv`;
- `forecast_baseline_report.md`;
- `forecast_spatial_baseline_station_metrics.csv`;
- `forecast_spatial_baseline_pair_summary.csv`;
- `forecast_spatial_baseline_report.md`;
- `forecast_stgnn_station_metrics.csv`;
- `forecast_stgnn_pair_summary.csv`;
- `forecast_stgnn_report.md`;
- `forecast_graphwavenet_station_metrics.csv`;
- `forecast_graphwavenet_pair_summary.csv`;
- `forecast_graphwavenet_report.md`;
- `forecast_patchtst_station_metrics.csv`;
- `forecast_patchtst_pair_summary.csv`;
- `forecast_patchtst_report.md`.

Diseno:

- muestra operacional de 300 estaciones por region;
- lookback 30 dias;
- horizonte t+1;
- train 2005-2012;
- validation 2013-2015;
- test 2020-2025;
- modelos: `regional_doy_climatology`, `station_persistence`, `spatial_knn_ridge`, `linear_window`, `patchtst_small`, `stgcn_diffusion`, `graphwavenet_transfer`.

Resultado inicial:

- la degradacion out-of-region en modelos temporales es mucho menor que en climatologia regional;
- la climatologia regional transferida confirma una asimetria fuerte cuando NEU/WCE se despliegan sobre MED;
- `station_persistence` queda documentado como baseline meteorologico sin transferencia regional;
- `spatial_knn_ridge` cubre el baseline espacial simple previo a ST-GNN completo;
- `stgcn_diffusion` introduce el primer modelo espaciotemporal de grafo transferible entre regiones, sin embeddings especificos de estacion;
- `graphwavenet_transfer` implementa una variante transferible de Graph WaveNet con convoluciones temporales dilatadas y difusion sobre soportes kNN forward/backward;
- `patchtst_small` reduce la degradacion en varias transferencias, aunque no en todas;
- estos resultados no sustituyen al experimento final, pero validan el pipeline de forecasting.

Comparacion KBS sobre modelos temporales:

- `kbs_forecast_model_comparison_results.csv`;
- `kbs_forecast_model_comparison_predictions.csv`;
- `kbs_forecast_model_comparison_report.md`.

Resultado inicial:

- para `linear_window`, `physical_plus_shift` con random forest obtiene el mejor resultado en group-by-cell;
- para `patchtst_small`, `physical_plus_shift` con random forest tambien obtiene el mejor resultado en group-by-cell;
- para `regional_doy_climatology`, `physical_plus_shift` con random forest obtiene el resultado mas fuerte en group-by-cell;
- para `spatial_knn_ridge`, `physical_plus_shift` con random forest obtiene el resultado mas fuerte en group-by-cell;
- para `stgcn_diffusion`, `physical_plus_shift` con random forest obtiene el resultado mas fuerte en group-by-cell, mientras que leave-target-region-out sigue siendo el caso mas exigente;
- para `graphwavenet_transfer`, `physical_plus_shift` con random forest tambien obtiene el mejor resultado en group-by-cell, mientras que `generic_shift` es mas competitivo en leave-target-region-out;
- en leave-target-region-out, `generic_shift` con random forest queda ligeramente mejor que las alternativas en estos modelos temporales;
- esto refuerza el enfoque integrador de PhyK-TAS: conocimiento fisico y shift generico deben combinarse en la capa de decision.

Experimento caro ST-GNN:

- dataset grande:
  - `forecast_dataset_large.npz`;
  - `forecast_dataset_large_metadata.csv`;
  - `forecast_dataset_large_report.md`;
- tamano efectivo:
  - MED: 913 estaciones;
  - WCE: 1000 estaciones;
  - NEU: 1000 estaciones;
- modelos:
  - `stgcn_diffusion`;
  - `graphwavenet_transfer`;
- artefactos:
  - `forecast_stgnn_large_station_metrics.csv`;
  - `forecast_stgnn_large_pair_summary.csv`;
  - `forecast_stgnn_large_report.md`;
  - `forecast_graphwavenet_large_station_metrics.csv`;
  - `forecast_graphwavenet_large_pair_summary.csv`;
  - `forecast_graphwavenet_large_report.md`;
  - `kbs_forecast_model_comparison_large_results.csv`;
  - `kbs_forecast_model_comparison_large_predictions.csv`;
  - `kbs_forecast_model_comparison_large_report.md`.

Resultado caro:

- `graphwavenet_transfer` mantiene degradacion baja en la mayoria de pares, con mayor riesgo en WCE -> NEU;
- `stgcn_diffusion` confirma el mismo patron general con menor coste computacional;
- en la comparacion KBS large, `physical_plus_shift` con random forest es el mejor en group-by-cell para ambos ST-GNN:
  - Graph WaveNet: R2 aproximado 0.72;
  - STGCN diffusion: R2 aproximado 0.70;
- en leave-target-region-out, `generic_shift` sigue siendo mas competitivo, lo que se interpretara como evidencia de que la extrapolacion completa a una region no vista requiere senales globales de shift ademas del conocimiento fisico local.

Robustez multi-semilla:

- semillas large:
  - 20260524;
  - 20260525;
  - 20260526;
- artefactos:
  - `large_seed_pair_summary_all.csv`;
  - `large_seed_pair_uncertainty.csv`;
  - `large_seed_kbs_results_all.csv`;
  - `large_seed_kbs_uncertainty.csv`;
  - `large_seed_uncertainty_report.md`;
  - `large_seed_transfer_decisions.csv`;
  - `large_seed_transfer_decision_report.md`.

Resultado multi-semilla:

- `physical_plus_shift` es el mejor predictor KBS en group-by-cell para los dos ST-GNN large:
  - Graph WaveNet: R2 medio aproximado 0.62, desviacion aproximada 0.09;
  - STGCN diffusion: R2 medio aproximado 0.66, desviacion aproximada 0.04;
- los pares con mayor riesgo conservador son los despliegues hacia NEU, especialmente WCE -> NEU y MED -> NEU;
- la capa de decision usa el limite superior del intervalo entre semillas para clasificar `deploy`, `adapt` o `retrain`.

Cierre experimental:

- tablas finales:
  - `final_model_kbs_summary.csv`;
  - `final_pair_risk_summary.csv`;
  - `final_experimental_summary_report.md`;
- ablacion fisica:
  - `physical_group_ablation_results_all.csv`;
  - `physical_group_ablation_summary.csv`;
  - `physical_group_ablation_report.md`;
- sensibilidad de decisiones:
  - `decision_threshold_sensitivity.csv`;
  - `decision_threshold_sensitivity_details.csv`;
  - `decision_threshold_sensitivity_report.md`.

Resultado de cierre:

- los grupos fisicos individuales mas informativos son ocurrencia e intensidad;
- `physical_all` supera a grupos fisicos individuales, y `physical_plus_shift` supera a `physical_all`;
- `shift_only` no explica bien la variacion group-by-cell, aunque es competitivo en leave-target-region-out;
- las decisiones conservadoras son sensibles al umbral, pero el ranking de riesgo se mantiene: los despliegues hacia NEU concentran la mayor preocupacion.

## Resultado nulo

Si los descriptores fisicos no superan a los baselines estadisticos:

- no se reinterpretara post-hoc como exito parcial;
- se reportara como resultado negativo del benchmark;
- se identificara que baseline explica mejor la degradacion;
- se separara el fallo por Bloque B y Bloque C.

## Comparacion piloto knowledge vs shift

Artefactos:

- `knowledge_vs_shift_pilot_results.csv`;
- `knowledge_vs_shift_pilot_report.md`.

Diseno:

- variable objetivo: degradacion del piloto ligero por estacion;
- feature set 1: descriptores fisicos por estacion;
- feature set 2: baselines genericos de shift por region destino;
- feature set 3: combinacion;
- validacion: leave-one-region-out.

Resultado piloto:

| feature_set | n | n_features | ridge_logo_mae | ridge_logo_r2 | rf_logo_mae | rf_logo_r2 |
|---|---:|---:|---:|---:|---:|---:|
| physical_knowledge | 900 | 12 | 0.125412 | -0.728213 | 0.141907 | -0.355495 |
| generic_shift | 900 | 11 | 0.260493 | -2.736262 | 0.190947 | -1.551223 |
| physical_plus_shift | 900 | 23 | 0.229940 | -2.046380 | 0.178424 | -1.318441 |

Interpretacion preregistrada:

- en este piloto, la capa de conocimiento fisico mejora MAE frente al shift generico bajo leave-one-region-out;
- los R2 negativos indican que el split por region es muy exigente y que el piloto no debe tratarse como evidencia final;
- el resultado apoya seguir con el enfoque KBS, pero no permite reclamar aun superioridad definitiva.

## Comparacion full-matrix knowledge vs shift

Artefactos:

- `knowledge_vs_shift_full_matrix_results.csv`;
- `knowledge_vs_shift_full_matrix_predictions.csv`;
- `knowledge_vs_shift_full_matrix_report.md`.

Diseno:

- variable objetivo: `mae_out_minus_in` de la matriz ligera completa;
- solo transferencias out-of-region;
- feature set 1: conocimiento fisico del destino;
- feature set 2: shift generico del par origen-destino;
- feature set 3: combinacion;
- validaciones: leave-target-region-out y group-by-cell.

Resultado resumido:

| feature_set | cv_kind | model | mae | r2 |
|---|---|---|---:|---:|
| physical_knowledge | leave_target_region_out | ridge | 0.107061 | -0.365649 |
| physical_knowledge | leave_target_region_out | random_forest | 0.107030 | -0.321287 |
| generic_shift | leave_target_region_out | ridge | 0.178708 | -4.927750 |
| generic_shift | leave_target_region_out | random_forest | 0.146830 | -1.455924 |
| physical_plus_shift | leave_target_region_out | random_forest | 0.138841 | -1.188811 |
| physical_knowledge | group_by_cell | random_forest | 0.066535 | 0.494157 |
| generic_shift | group_by_cell | random_forest | 0.040666 | 0.770395 |
| physical_plus_shift | group_by_cell | random_forest | 0.028397 | 0.886725 |

Interpretacion preregistrada:

- bajo leave-target-region-out, el conocimiento fisico generaliza mejor que el shift generico;
- bajo group-by-cell, el shift generico y la combinacion son superiores;
- esto sugiere que el conocimiento fisico aporta extrapolacion entre regiones, mientras que las metricas de shift capturan bien variacion dentro de regiones/celdas;
- esta tension es central para el paper KBS y debe reportarse aunque los modelos profundos cambien la magnitud.

## Decision Layer

Artefactos:

- `transfer_risk_classifier_results.csv`;
- `transfer_risk_predictions.csv`;
- `transfer_risk_decisions.csv`;
- `transfer_risk_decision_layer_report.md`.

Definicion de riesgo:

- `safe`: degradacion <= 0;
- `moderate`: degradacion positiva hasta el percentil 75 de degradacion positiva;
- `high`: degradacion superior al percentil 75 positivo.

Politica de decision:

- `retrain` si `p_high >= 0.5`;
- `adapt` si `p_high >= 0.25` o `p_safe < 0.4`;
- `deploy` en el resto.

Modelo de decision actual:

- feature set: `physical_plus_shift`;
- clasificador: random forest;
- validacion usada para probabilidades: group-by-cell.

Resumen por par origen-destino:

| source | target | mean_p_high | retrain_rate | adapt_rate | deploy_rate | observed_degradation |
|---|---|---:|---:|---:|---:|---:|
| MED | NEU | 0.019704 | 0.000000 | 0.005117 | 0.994883 | -0.092230 |
| MED | WCE | 0.031033 | 0.002683 | 0.190244 | 0.807073 | -0.036271 |
| NEU | MED | 0.975289 | 1.000000 | 0.000000 | 0.000000 | 0.284396 |
| NEU | WCE | 0.076637 | 0.061707 | 0.938293 | 0.000000 | 0.080758 |
| WCE | MED | 0.882001 | 0.992333 | 0.007667 | 0.000000 | 0.177910 |
| WCE | NEU | 0.019692 | 0.000000 | 0.121109 | 0.878891 | -0.041644 |

Interpretacion:

- el sistema recomienda `retrain` casi siempre cuando el destino es MED y el origen es WCE/NEU;
- recomienda `deploy` mayoritariamente para MED -> NEU y MED -> WCE;
- recomienda `adapt` para NEU -> WCE, donde la degradacion es positiva pero no tan extrema como hacia MED;
- esto convierte el benchmark en un sistema de soporte a decision, que es el nucleo del enfoque KBS.

## Artefactos para OSF

Adjuntar:

- `protocolo_preregistro_v2.md`;
- `stations_ar6.csv`;
- `viability_pre_dedup.csv`;
- `viability_post_dedup.csv`;
- `region_decisions.md`;
- `power_analysis.md`;
- `physical_descriptors_station.csv`;
- `physical_descriptors_cell5.csv`;
- `physical_descriptors_region.csv`;
- `physical_descriptors_report.md`;
- `distribution_shift_baselines.csv`;
- `distribution_shift_baselines_report.md`;
- `knowledge_vs_shift_pilot_results.csv`;
- `knowledge_vs_shift_pilot_report.md`;
- `knowledge_vs_shift_full_matrix_results.csv`;
- `knowledge_vs_shift_full_matrix_predictions.csv`;
- `knowledge_vs_shift_full_matrix_report.md`;
- `light_degradation_station.csv`;
- `light_degradation_pair_summary.csv`;
- `light_degradation_matrix_report.md`;
- `transfer_risk_classifier_results.csv`;
- `transfer_risk_predictions.csv`;
- `transfer_risk_decisions.csv`;
- `transfer_risk_decision_layer_report.md`;
- `dedup_audit_report.md`;
- scripts en `Paper1/scripts/`.

## Pendiente antes de congelar

- crear repositorio o tag reproducible;
- subir preregistro a OSF y obtener URL/DOI.
