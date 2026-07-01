# Cobertura preliminar por bloques temporales

Consulta realizada sobre `Data/harmonized/precip_daily/source_id=*/year=*/part-*.parquet`.

Los conteos son previos a asignacion AR6, deduplicacion entre fuentes y filtros espaciales. Por tanto, son una cota superior operativa, no el tamano final del benchmark.

## Conteo basico de observaciones

| source_id | periodo | rows | stations | non_null_rows |
|---|---:|---:|---:|---:|
| global_ghcnd_01 | 2000-2012 | 83416580 | 37007 | 74720403 |
| global_ghcnd_01 | 2013-2015 | 25789599 | 31596 | 21489866 |
| global_ghcnd_01 | 2016-2019 | 35568305 | 34189 | 29276878 |
| global_ghcnd_01 | 2020-2025 | 55914747 | 37626 | 46281665 |
| eur_ecad_01 | 2000-2012 | 76754769 | 17196 | 56541554 |
| eur_ecad_01 | 2013-2015 | 18915077 | 17350 | 13144557 |
| eur_ecad_01 | 2016-2019 | 25426595 | 17450 | 17063873 |
| eur_ecad_01 | 2020-2025 | 38430714 | 17606 | 24117902 |
| deu_dwd_cdc_01 | 2000-2012 | 13172274 | 4478 | 13167504 |
| deu_dwd_cdc_01 | 2013-2015 | 2300642 | 2196 | 2299543 |
| deu_dwd_cdc_01 | 2016-2019 | 3088711 | 2266 | 3082881 |
| deu_dwd_cdc_01 | 2020-2025 | 4756913 | 2388 | 4742018 |
| che_meteoswiss_01 | 2000-2012 | 1663492 | 377 | 1663362 |
| che_meteoswiss_01 | 2013-2015 | 417401 | 387 | 417236 |
| che_meteoswiss_01 | 2016-2019 | 565562 | 388 | 564053 |
| che_meteoswiss_01 | 2020-2025 | 848350 | 389 | 844573 |
| esp_aemet_daily_hist_01 | 2000-2012 | 2049760 | 812 | 1956048 |
| esp_aemet_daily_hist_01 | 2013-2015 | 889397 | 868 | 861680 |
| esp_aemet_daily_hist_01 | 2016-2019 | 1238992 | 896 | 1206761 |
| esp_aemet_daily_hist_01 | 2020-2025 | 1909169 | 909 | 1854442 |
| esp_avamet_01 | 2000-2012 | 0 | 0 | 0 |
| esp_avamet_01 | 2013-2015 | 0 | 0 | 0 |
| esp_avamet_01 | 2016-2019 | 82038 | 250 | 73915 |
| esp_avamet_01 | 2020-2025 | 860521 | 579 | 808056 |
| can_eccc_climate_stations_01 | 2000-2012 | 9535572 | 2877 | 7103995 |
| can_eccc_climate_stations_01 | 2013-2015 | 1685935 | 1645 | 1247616 |
| can_eccc_climate_stations_01 | 2016-2019 | 2120264 | 1632 | 1502228 |
| can_eccc_climate_stations_01 | 2020-2025 | 3004908 | 1500 | 2103133 |

## Estaciones con cobertura no nula suficiente

`ge80` y `ge95` indican estaciones con al menos 80% o 95% de dias con `precip_mm` no nulo en el bloque.

| source_id | periodo | dias | any | ge80 | ge95 |
|---|---:|---:|---:|---:|---:|
| global_ghcnd_01 | 2000-2012 | 4749 | 37005 | 9487 | 6467 |
| global_ghcnd_01 | 2013-2015 | 1095 | 31590 | 14892 | 10383 |
| global_ghcnd_01 | 2016-2019 | 1461 | 34189 | 14793 | 10074 |
| global_ghcnd_01 | 2020-2025 | 2192 | 37625 | 14099 | 9163 |
| eur_ecad_01 | 2000-2012 | 4749 | 14968 | 9816 | 8634 |
| eur_ecad_01 | 2013-2015 | 1095 | 12560 | 11651 | 11056 |
| eur_ecad_01 | 2016-2019 | 1461 | 12412 | 11222 | 9969 |
| eur_ecad_01 | 2020-2025 | 2192 | 11953 | 10553 | 8988 |
| deu_dwd_cdc_01 | 2000-2012 | 4749 | 4478 | 1663 | 1445 |
| deu_dwd_cdc_01 | 2013-2015 | 1095 | 2196 | 2034 | 1965 |
| deu_dwd_cdc_01 | 2016-2019 | 1461 | 2264 | 2021 | 1899 |
| deu_dwd_cdc_01 | 2020-2025 | 2192 | 2383 | 2032 | 1942 |
| che_meteoswiss_01 | 2000-2012 | 4749 | 377 | 348 | 344 |
| che_meteoswiss_01 | 2013-2015 | 1095 | 387 | 376 | 373 |
| che_meteoswiss_01 | 2016-2019 | 1461 | 388 | 386 | 385 |
| che_meteoswiss_01 | 2020-2025 | 2192 | 387 | 385 | 380 |
| esp_aemet_daily_hist_01 | 2000-2012 | 4749 | 811 | 186 | 109 |
| esp_aemet_daily_hist_01 | 2013-2015 | 1095 | 867 | 767 | 542 |
| esp_aemet_daily_hist_01 | 2016-2019 | 1461 | 888 | 810 | 662 |
| esp_aemet_daily_hist_01 | 2020-2025 | 2192 | 896 | 834 | 685 |
| esp_avamet_01 | 2000-2012 | 4749 | 0 | 0 | 0 |
| esp_avamet_01 | 2013-2015 | 1095 | 0 | 0 | 0 |
| esp_avamet_01 | 2016-2019 | 1461 | 240 | 0 | 0 |
| esp_avamet_01 | 2020-2025 | 2192 | 568 | 251 | 0 |
| esp_avamet_01 | 2019-2025 | 2557 | 569 | 209 | 38 |
| can_eccc_climate_stations_01 | 2000-2012 | 4749 | 2807 | 817 | 485 |
| can_eccc_climate_stations_01 | 2013-2015 | 1095 | 1519 | 897 | 480 |
| can_eccc_climate_stations_01 | 2016-2019 | 1461 | 1414 | 824 | 454 |
| can_eccc_climate_stations_01 | 2020-2025 | 2192 | 1269 | 705 | 438 |

## Lectura preliminar

- El nucleo `global_ghcnd_01` + `eur_ecad_01` es viable en 2000-2025 antes de deduplicar y recortar por region AR6.
- `deu_dwd_cdc_01` y `che_meteoswiss_01` son fuertes para validacion por proveedor, especialmente desde 2013.
- `esp_aemet_daily_hist_01` tiene cobertura amplia en anos recientes, pero el bloque 2000-2012 cae mucho bajo umbral 95%; conviene tratarlo con filtros por cobertura o usarlo como validacion reciente.
- `esp_avamet_01` no sirve para el protocolo 2000-2015; solo es sensibilidad 2019-2025/2020-2025 y no sostiene 95% de cobertura salvo pocas estaciones.
- `can_eccc_climate_stations_01` es viable como validacion externa, pero el umbral 95% reduce bastante el numero de estaciones.

## Decision operativa tras estos conteos

El diseno no se replantea, pero el nucleo operativo queda restringido.

Nucleo principal:

- `global_ghcnd_01` + `eur_ecad_01`;
- regiones IPCC AR6 europeas;
- deduplicacion obligatoria antes de declarar n efectivo;
- decision final 80% vs 95% basada en conteos post-AR6 y post-deduplicacion, no en conteos brutos.

Validacion fuerte:

- `deu_dwd_cdc_01`;
- `che_meteoswiss_01`.

Validacion limitada:

- `esp_aemet_daily_hist_01`, preferiblemente reciente o sensibilidad mediterranea;
- `esp_avamet_01`, solo sensibilidad 2019-2025/2020-2025;
- `can_eccc_climate_stations_01`, solo replicacion externa opcional.

Regla provisional:

- si una region AR6 principal queda por debajo de 300 estaciones unicas post-deduplicacion a 95%, el analisis principal usara 80% con mascara explicita y 95% quedara como sensibilidad estricta;
- si tambien queda por debajo de 300 a 80%, esa region no se usara como region principal sin agrupar o redefinir el diseno.

## Interseccion temporal estable

Estas cifras cuentan estaciones que cumplen el umbral de cobertura en todos los bloques temporales principales: 2000-2012, 2013-2015, 2016-2019 y 2020-2025. Esta es una aproximacion mas realista para los analisis longitudinales que los conteos por bloque aislado.

| source_id | any_block | all4_ge80 | all4_ge95 | train_val_test_ge95 | train_val_test_ge80 |
|---|---:|---:|---:|---:|---:|
| global_ghcnd_01 | 60435 | 5099 | 3240 | 3353 | 5204 |
| eur_ecad_01 | 15540 | 7694 | 6480 | 6580 | 7755 |
| deu_dwd_cdc_01 | 4855 | 1289 | 1089 | 1119 | 1303 |
| che_meteoswiss_01 | 388 | 346 | 340 | 340 | 346 |
| esp_aemet_daily_hist_01 | 918 | 166 | 94 | 97 | 167 |
| esp_avamet_01 | 569 | 0 | 0 | 0 | 0 |
| can_eccc_climate_stations_01 | 3077 | 246 | 93 | 101 | 261 |

Lectura:

- El n real longitudinal es bastante menor que el conteo por bloque.
- `global_ghcnd_01` queda en 3240 estaciones estables a 95% en los cuatro bloques.
- `eur_ecad_01` queda en 6480 estaciones estables a 95% en los cuatro bloques.
- `esp_aemet_daily_hist_01` y `can_eccc_climate_stations_01` quedan demasiado reducidos a 95% para tratarlos como nucleo longitudinal completo; son mas defendibles como validaciones/sensibilidades.

## Sensibilidad del inicio historico

Si el bloque historico comienza en 2005 en lugar de 2000, la interseccion estable mejora de forma moderada en algunas fuentes.

| source_id | all4_ge80_start2005 | all4_ge95_start2005 |
|---|---:|---:|
| global_ghcnd_01 | 5761 | 3681 |
| eur_ecad_01 | 8361 | 6817 |
| deu_dwd_cdc_01 | 1488 | 1260 |
| che_meteoswiss_01 | 346 | 337 |
| esp_aemet_daily_hist_01 | 259 | 103 |
| can_eccc_climate_stations_01 | 307 | 107 |

Lectura:

- Empezar en 2005 aumenta estabilidad, pero no cambia cualitativamente el diseno.
- La mejora es clara para GHCN-D, ECA&D y DWD.
- AEMET apenas mejora a 95%, por lo que no resuelve su debilidad en el bloque historico.

## Piloto de deduplicacion mediterranea aproximada

Este piloto no usa todavia regiones IPCC AR6 oficiales. Usa un proxy geografico mediterraneo europeo: latitud 34-46 N y longitud 10 W-20 E, con `global_ghcnd_01`, `eur_ecad_01` y `esp_aemet_daily_hist_01`.

Regla aplicada:

- solo estaciones estables en los cuatro bloques;
- deduplicacion por WMO/candidate key;
- union espacial entre fuentes a <= 1 km solo si hay evidencia de identidad de metadatos: WMO, nombre normalizado o elevacion a +/- 10 m;
- no se deduplican estaciones de la misma fuente solo por cercania espacial.

| threshold | scope | pre_stations | post_components | removed_or_grouped |
|---|---|---:|---:|---:|
| all4_ge80 | esp_aemet_daily_hist_01 | 148 | 148 | 0 |
| all4_ge80 | eur_ecad_01 | 347 | 347 | 0 |
| all4_ge80 | global_ghcnd_01 | 77 | 77 | 0 |
| all4_ge80 | combined_core_sources | 572 | 344 | 228 |
| all4_ge95 | esp_aemet_daily_hist_01 | 85 | 85 | 0 |
| all4_ge95 | eur_ecad_01 | 147 | 147 | 0 |
| all4_ge95 | global_ghcnd_01 | 38 | 38 | 0 |
| all4_ge95 | combined_core_sources | 270 | 167 | 103 |

Lectura:

- La deduplicacion reduce sustancialmente el n efectivo en el proxy mediterraneo.
- Con umbral 95%, este proxy queda por debajo de 300 estaciones unicas; con 80%, queda por encima de 300.
- Esta tabla no decide el protocolo final, pero confirma que el conteo post-deduplicacion y post-AR6 debe calcularse antes de congelar el preregistro.
