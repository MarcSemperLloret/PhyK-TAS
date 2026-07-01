# Protocolo v1: benchmark multi-regional de robustez bajo cambio de regimen climatico

## Objetivo

Evaluar si modelos espaciotemporales de precipitacion aprenden patrones transferibles entre regimenes climaticos fisicamente distintos o si su rendimiento fuera de region esta dominado por artefactos locales de red, cobertura y calidad de observacion.

La contribucion metodologica no sera "entrenar en muchos datasets", sino definir un sistema knowledge-based reproducible para medir transferencia entre regiones climaticas definidas ex ante, representar conocimiento fisico del regimen destino y usarlo para anticipar degradacion de modelos antes del despliegue.

Orientacion de venue:

- Knowledge-Based Systems.
- El paper se presentara como un sistema inteligente de soporte a decision para despliegue de modelos espaciotemporales bajo cambio de regimen climatico.
- La contribucion central sera la representacion e inferencia de conocimiento fisico para predecir riesgo de fallo, no una nueva arquitectura meteorologica.

## Variable y resolucion

Decision principal: el benchmark nuclear sera diario y univariante sobre `precip_mm`.

Justificacion:

- Es la variable comun armonizada con mayor cobertura entre fuentes.
- La capa armonizada existente contiene `Data/harmonized/precip_daily/source_id=*/year=*/part-*.parquet`.
- Temperatura y otras variables no tienen una capa comun equivalente en el estado actual del repositorio.
- AVAMET se usara solo como validacion de sensibilidad diaria, no como ventaja subhoraria principal.

Implicacion para AVAMET:

- AVAMET no define el nucleo del paper.
- Su resolucion subdiaria se agrega a diario cuando se compare con GHCN-D, ECA&D o AEMET.
- La ventaja diferencial de AVAMET en este paper sera densidad regional y proveedor independiente dentro del Mediterraneo, no resolucion temporal.
- Un paper subdiario queda separado porque actualmente no hay suficientes regiones terrestres comparables a 10-15 minutos.

## Nucleo operativo revisado

El paper no se replantea metodologicamente. Se replantea el nucleo operativo para que la inferencia principal dependa solo de fuentes con cobertura longitudinal suficiente y comparabilidad diaria.

### Nucleo principal

- `global_ghcnd_01`: red global diaria, precipitacion armonizada, estaciones con coordenadas.
- `eur_ecad_01`: red europea diaria, precipitacion armonizada, estaciones con coordenadas.

Estas fuentes se usaran por recortes climaticos/regionales, no como regiones por si mismas.

Alcance:

- base del benchmark principal;
- asignacion a regiones IPCC AR6;
- interseccion temporal estable obligatoria;
- deduplicacion estricta antes de cualquier split;
- analisis principal en regiones `MED`, `WCE` y `NEU` si superan el n efectivo minimo post-deduplicacion.

### Validacion fuerte por proveedor

- `deu_dwd_cdc_01`: Europa continental, diario.
- `che_meteoswiss_01`: region alpina/centroeuropea, diario.

Alcance:

- validacion por proveedor dentro de regiones europeas;
- no forman el nucleo principal porque solapan con GHCN-D/ECA&D y deben evaluarse despues de deduplicar;
- se usan para comprobar si las conclusiones sobreviven al cambio de proveedor en regiones con cobertura fuerte.

### Validacion limitada y sensibilidad mediterranea

- `esp_aemet_daily_hist_01`: Mediterraneo/Iberia, diario.
- `esp_avamet_01`: Mediterraneo oriental iberico, subdiario agregado a diario.

Alcance:

- AEMET no se usara como fuente longitudinal nuclear si el bloque 2000-2012 queda por debajo del minimo efectivo;
- AEMET es preferible como validacion reciente o sensibilidad mediterranea desde 2013;
- AVAMET queda fuera del nucleo principal y no sostiene la justificacion del paper;
- AVAMET se conserva solo como sensibilidad 2019-2025/2020-2025, centrada en densidad regional y proveedor independiente, no en resolucion subdiaria.

Estas fuentes no se mezclaran sin deduplicacion con GHCN-D/ECA&D, porque pueden compartir estaciones o series equivalentes.

### Validacion externa opcional

- `can_eccc_climate_stations_01`: continental/frio, diario, gran cobertura.

Alcance:

- no entra como cuarta region principal;
- se usara solo como replicacion externa opcional si el n efectivo post-filtros es suficiente;
- a 95% de cobertura longitudinal se considera marginal para inferencia con el mismo rigor que el nucleo europeo.

### Regla de avance

Antes de entrenar modelos, el nucleo operativo debe pasar una tabla de viabilidad final:

- estaciones unicas post-deduplicacion por region AR6;
- estaciones unicas por celda 5 x 5;
- conteos para umbrales 80% y 95%;
- interseccion temporal estable;
- desglose por fuente antes y despues de deduplicar.

Si `MED`, `WCE` o `NEU` quedan por debajo del minimo efectivo preregistrado a 95%, el diseno principal pasara a 80% con mascara explicita y 95% quedara como sensibilidad estricta.

## Definicion ex ante de regiones

No se dibujaran regiones manualmente por intuicion geografica. Se adoptara una clasificacion climatica estandar antes de calcular resultados.

Opcion primaria: regiones terrestres IPCC AR6.

Justificacion:

- Son una convencion climatica actual y reconocible para revisores.
- Evitan parte de la circularidad de Koppen-Geiger, que se define directamente a partir de temperatura y precipitacion.
- Permiten reportar resultados con etiquetas climaticas/geograficas estandar sin dibujar limites manuales.

Regiones iniciales candidatas:

- `MED`: Mediterraneo.
- `WCE`: Western and Central Europe.
- `NEU`: Northern Europe.
- Extension opcional si se usa validacion transcontinental: regiones AR6 norteamericanas que cubran Canada/ECCC.

Opcion secundaria para sensibilidad: Koppen-Geiger actualizado.

Koppen-Geiger no sera la particion primaria porque sus clases incorporan precipitacion y temperatura en la definicion. Si se usa como sensibilidad, no se interpretara como evidencia independiente de descriptores climaticos marginales. En ese caso, el analisis dara mas peso a descriptores no triviales respecto a Koppen:

- escala espacial de correlacion;
- tail index de extremos;
- intermitencia subestacional;
- autocorrelacion de ocurrencia;
- estructura de rachas secas y humedas.

Agregaciones propuestas:

- Mediterraneo seco/calido: clases `Csa`, `Csb` y, como sensibilidad separada, bordes `BSk` mediterraneos.
- Oceanico/Atlantico templado: clases `Cfb` y `Cfc` en fachada europea occidental.
- Continental templado/frio: clases `Dfb`, `Dfc`, `Dfa` y transicion interior europea segun disponibilidad.
- Alpino/orografico: no se define como region "dificil" a priori. Solo se incluye si queda objetivamente identificado por clase climatica/elevacion bajo regla preregistrada.

Regla de preregistro:

- La clasificacion climatica y la tabla de agregacion se fijaran antes de entrenar modelos.
- Cada estacion recibira una etiqueta de region por interseccion entre coordenadas y mapa climatico.
- Las estaciones sin coordenadas exactas o sin clase climatica asignable se excluyen del benchmark principal.

## Unidad estadistica de transferencia

La inferencia no dependera solo de 3-4 regiones agregadas, porque eso produce muy pocas unidades para relacionar descriptores fisicos y degradacion de rendimiento.

Unidad primaria:

- estacion destino;
- cada estacion conserva su region AR6 como etiqueta interpretable;
- los descriptores locales se calculan a partir de la estacion y/o de su vecindario espacial de entrenamiento definido ex ante.

Unidad secundaria:

- subregion espacial de 5 x 5 grados dentro de cada region AR6;
- se usa para analisis agregado y visualizacion;
- solo se conserva una celda si supera un minimo preregistrado de estaciones validas.

Ventaja:

- la unidad estacion permite miles de observaciones de degradacion;
- las regiones AR6 siguen siendo el marco para reportar transferencia entre regimenes;
- se evita ajustar regresiones con `n=12` pares region-origen/destino.

Dependencia estadistica:

- las estaciones no se trataran como observaciones independientes simples;
- el analisis explicativo modelara dependencia espacial y de proveedor;
- la estructura minima sera estacion anidada en celda 5 x 5 grados, celda anidada en region AR6, con proveedor/fuente como efecto adicional o estrato de bootstrap;
- los intervalos de confianza se calcularan con bootstrap por bloques o modelos jerarquicos, no con errores estandar IID por estacion;
- se reportara el numero efectivo de unidades por region/celda/fuente, ademas del numero bruto de estaciones.

## Deduplicacion entre fuentes

La deduplicacion es obligatoria antes de separar entrenamiento, validacion y test.

Fases:

1. Identidad exacta o casi exacta por metadatos:
   - mismo WMO ID cuando exista;
   - misma `candidate_duplicate_key` del registro si procede;
   - mismo nombre normalizado y distancia geografica pequena.

2. Identidad espacial:
   - candidatos si la distancia entre estaciones es <= 1 km;
   - candidatos secundarios si distancia <= 5 km y elevacion similar.

3. Identidad por serie:
   - para pares candidatos, calcular correlacion diaria de precipitacion en el periodo comun;
   - marcar como duplicado fuerte solo si correlacion diaria > 0.95, solape temporal suficiente y existe evidencia de identidad de metadatos;
   - evidencia de identidad de metadatos: mismo WMO ID, mismo nombre normalizado, misma elevacion a +/- 10 m, o clave de identidad compatible;
   - marcar como duplicado probable si correlacion > 0.90, distancia <= 1 km y metadatos compatibles.

Restriccion importante:

- La correlacion alta no sera condicion suficiente para deduplicar.
- Dos estaciones cercanas pueden ser legitimas y muy correlacionadas en el mismo valle o bajo el mismo regimen sinoptico.
- En redes densas como AVAMET y MeteoSwiss se conservara densidad real salvo evidencia de identidad de estacion.

Regla experimental:

- Un grupo de duplicados no puede aparecer simultaneamente en train y test.
- Para el nucleo GHCN-D/ECA&D, si dos fuentes contienen la misma estacion, se conserva una representacion canonica por region y periodo.
- Las redes nacionales usadas como validacion se filtraran para excluir estaciones ya presentes en el entrenamiento nuclear o para evaluarlas como "misma estacion/proveedor distinto" en un experimento separado.

## Criterios de inclusion por estacion

Los filtros se aplican igual en todas las regiones para evitar confundir regimen climatico con calidad de red.

Periodo candidato principal:

- 2000-2025 para el benchmark diario amplio.
- 2019-2025 como sensibilidad que permite incluir AVAMET.
- opcion de sensibilidad temporal: iniciar el bloque historico en 2005 si la interseccion estable de estaciones mejora materialmente sin debilitar la pregunta cientifica.

Criterios minimos por estacion:

- coordenadas disponibles y `position_kind` aceptable;
- soporte de precipitacion (`precip_supported=True` o presencia efectiva en `precip_daily`);
- al menos 80% de dias observados en el periodo de entrenamiento;
- al menos 80% de dias observados en el periodo de test;
- no mas de 30 dias consecutivos sin observacion durante ventanas usadas para entrenar/evaluar;
- excluir valores negativos o fisicamente imposibles ya marcados por QC;
- aplicar el mismo tratamiento de trazas y nulos en todas las fuentes.

Sensibilidad:

- repetir resultados con umbral de cobertura del 70% y 90%;
- reportar numero de estaciones por region tras cada filtro;
- no cambiar umbrales tras ver rendimiento de modelos.

Decision 80% vs 95%:

- la decision final no se tomara con conteos brutos por fuente;
- se tomara con la tabla post-asignacion AR6, post-deduplicacion y con interseccion temporal estable;
- el analisis principal de modelos profundos usara 95% si cada region principal conserva suficiente n efectivo;
- si una region principal cae por debajo del minimo preregistrado, se usara un diseno dual: 95% para modelos profundos en regiones con cobertura suficiente y 80% con mascara explicita para analisis de sensibilidad;
- la decision y el minimo de estaciones/celdas por region se congelaran antes del entrenamiento final.

Gaps e imputacion:

- no se permitira imputacion silenciosa;
- el analisis principal usara estaciones con cobertura suficiente para construir ventanas de entrenamiento sin romper la arquitectura temporal;
- umbral inicial para modelos profundos: 95% de dias disponibles en cada bloque usado por el modelo;
- umbral inicial para analisis descriptivo y modelos ligeros: 80%, manteniendo mascara de observacion;
- si se imputa, el metodo se preregistrara antes de entrenar y se reportara como sensibilidad, no como resultado principal;
- metodos de imputacion permitidos para sensibilidad: climatologia diaria por estacion, mediana de vecinos cercanos dentro de la misma region/celda, o modelo simple entrenado solo en periodo de entrenamiento;
- la mascara de valores imputados se incorporara como covariable o se excluiran esos puntos de las metricas, segun el modelo.

## Descriptores fisicos definidos ex ante

Los descriptores se calculan solo con datos de entrenamiento o climatologia previa al periodo de test.

Descriptores por region:

- fraccion de dias humedos: `P(precip_mm > 1 mm)`;
- intensidad media condicional en dias humedos;
- coeficiente de variacion de precipitacion diaria;
- estacionalidad: amplitud anual de la climatologia mensual;
- concentracion estacional: proporcion de precipitacion anual acumulada en los tres meses mas humedos;
- autocorrelacion temporal de ocurrencia de lluvia;
- autocorrelacion temporal de intensidad en dias humedos;
- intermitencia: longitud media y percentil 95 de rachas secas;
- extremos: percentiles 95/99 de precipitacion diaria humeda;
- tail index o aproximacion robusta de cola extrema, definido antes del analisis final;
- escala espacial: distancia a la que cae la correlacion diaria por debajo de umbrales predefinidos, por ejemplo 0.5 y 0.2;
- gradiente orografico: distribucion de elevacion y rango intercuartil de elevacion de estaciones.

Hipotesis principal:

La degradacion out-of-region de los modelos se explica mejor por estos descriptores fisicos que por metricas genericas de distribution shift calculadas directamente sobre distribuciones marginales.

Baselines preregistrados de distribution shift:

- divergencia KL entre distribuciones marginales discretizadas de `precip_mm`;
- distancia de Wasserstein entre distribuciones de precipitacion diaria;
- MMD (maximum mean discrepancy) sobre features basicos: ocurrencia, intensidad, percentiles, rachas secas y estacionalidad mensual;
- shift temporal simple: cambio en media, varianza, fraccion de dias humedos y percentiles altos entre periodos;
- distancia geografica y diferencia de elevacion como controles no climaticos.

Criterio de soporte de la hipotesis:

- metrica primaria: log-loss out-of-fold de un modelo jerarquico que predice degradacion ordinal o binaria severa/no severa, con folds bloqueados por region AR6;
- metricas secundarias: RMSE/MAE out-of-fold para degradacion continua y ranking loss para ordenar estaciones/celdas por dificultad esperada;
- los descriptores fisicos deben mejorar la prediccion de degradacion frente a estos baselines bajo el mismo protocolo de validacion;
- "mejor" significa menor log-loss out-of-fold en la metrica primaria, evaluado con folds por region y reportado con incertidumbre por bootstrap de bloques;
- se reportaran tambien resultados por region y peor-caso regional, aunque la decision primaria se basa en la metrica global bloqueada;
- la mejora se reportara con intervalos de confianza o bootstrap por estaciones/subregiones;
- si solo superan a un baseline debil, no se considerara evidencia suficiente.

## Validacion temporal y espacial

Se separaran explicitamente transferencia espacial, deriva temporal y su combinacion.

Un unico split 2000-2015 / 2016-2019 / 2020-2025 no basta para atribuir degradacion, porque mezcla cambio de region y deriva temporal. Por tanto, el diseno principal sera cruzado.

Bloques temporales:

- Periodo historico temprano: 2000-2012.
- Periodo historico de validacion: 2013-2015.
- Periodo intermedio de validacion/despliegue: 2016-2019.
- Periodo reciente/test: 2020-2025.

### Bloque A: deriva temporal pura

- Train: region origen, 2000-2012.
- Validation: region origen, 2013-2015.
- Test: misma region origen, 2020-2025.
- Interpretacion: degradacion por cambio temporal dentro de la misma region.

### Bloque B: transferencia espacial pura

- Train: region origen, 2000-2012.
- Validation: region origen, 2013-2015 para hiperparametros.
- Test: region destino, 2000-2015.
- Interpretacion: degradacion por cambio de regimen espacial manteniendo periodo historico.

Restricciones del Bloque B:

- no se usaran datos posteriores a 2015 para elegir hiperparametros del Bloque B;
- el test destino 2000-2015 se evaluara con desglose por anos para comprobar si eventos sinopticos continentales compartidos inflan rendimiento;
- como sensibilidad, se repetira con separacion pares/impares o con bloques temporales no solapados si la correlacion sinoptica continental resulta dominante;
- si se usa un gap temporal, este se fijara antes del entrenamiento final y se aplicara simetricamente a todas las regiones.

### Bloque C: despliegue fuera de region y futuro

- Train: region origen, 2000-2012.
- Validation: region origen, 2013-2015 o 2016-2019 segun el experimento preregistrado.
- Test: region destino, 2020-2025.
- Interpretacion: degradacion combinada por transferencia espacial y deriva temporal.

### Descomposicion

La degradacion del Bloque C se reportara junto a A y B para evitar atribuir a regimen climatico lo que pueda ser deriva temporal. La contribucion principal solo se sostendra si los descriptores fisicos explican degradacion espacial en B y aportan informacion adicional en C.

Para el experimento AVAMET:

- Train/validation/test restringido a 2019-2025.
- Se reporta como sensibilidad, no como evidencia principal de deriva climatica de largo plazo.

Reglas:

- El test temporal no se usa para elegir regiones, descriptores, filtros ni hiperparametros.
- Las regiones destino se mantienen cerradas antes de entrenar.
- Si el periodo comun reduce demasiado estaciones en alguna region, se reporta y se excluye esa region bajo regla objetiva, no por rendimiento.

## Modelos

El benchmark debe comparar al menos:

- persistencia/climatologia regional como baseline;
- modelo temporal local por estacion;
- modelo espacial simple;
- Graph WaveNet o AGCRN como ST-GNN representativo;
- PatchTST como baseline temporal competitivo no basado en grafo;
- variante con descriptores fisicos como contexto o predictor de degradacion, si procede.

Seleccion minima:

- Graph WaveNet si se prioriza una arquitectura ST-GNN ampliamente reconocible;
- AGCRN si la adaptacion de grafos aprendidos resulta mas adecuada para redes de estaciones heterogeneas;
- PatchTST como control fuerte para distinguir efecto de arquitectura grafica frente a modelado temporal por estacion.

Regla de interpretacion:

- si la relacion entre descriptores fisicos y degradacion aparece en Graph WaveNet/AGCRN y PatchTST, la conclusion es robusta al tipo de modelo;
- si aparece solo en ST-GNN, se reportara como sensibilidad especifica de arquitectura;
- si aparece solo en PatchTST, no se atribuira a estructura espacial aprendida.

La parte metodologica clave no es proponer necesariamente una nueva arquitectura, sino demostrar si la transferibilidad puede anticiparse con descriptores fisicos preregistrados.

## Potencia estadistica

Antes de entrenar modelos definitivos se realizara un analisis de potencia.

Objetivo:

- estimar que tamano de efecto minimo puede detectarse con alpha = 0.05 y poder = 0.8;
- decidir si el diseno tiene suficientes unidades de transferencia;
- evitar iniciar un experimento que solo pueda detectar efectos enormes.

Unidades consideradas:

- estacion destino como unidad primaria;
- celda 5 x 5 grados dentro de region AR6 como unidad secundaria;
- par origen-destino agregado solo como resumen descriptivo, no como base principal de inferencia.

Procedimiento:

- usar una muestra piloto de estaciones y modelos ligeros para estimar varianza de degradacion;
- simular asociaciones entre descriptores y degradacion bajo distintos tamanos de efecto;
- repetir con clustering por region/fuente para no sobreestimar independencia;
- fijar el numero minimo de estaciones/celdas por region antes del entrenamiento final.

Criterio de viabilidad:

- si el poder estadistico solo permite detectar efectos muy grandes, se ampliaran unidades mediante mas celdas/estaciones o se reducira la dimensionalidad de descriptores;
- si aun asi el poder es insuficiente, el paper se reformulara como benchmark descriptivo con inferencia limitada.
- la potencia se recalculara con el n efectivo post-AR6 y post-deduplicacion, no con conteos brutos por fuente.

## Metricas

Para precipitacion diaria, reportar por region y por estacion:

- MAE/RMSE para cantidad diaria;
- Brier score o F1 para ocurrencia de lluvia;
- error en percentiles altos, por ejemplo P95/P99;
- skill relativo frente a climatologia y persistencia;
- degradacion out-of-region: diferencia o ratio entre rendimiento in-region y out-of-region.

La variable dependiente para el analisis de transferibilidad sera la degradacion normalizada del modelo respecto a su rendimiento in-region y a los baselines.

## Analisis principal

1. Construir regiones climaticas con criterio estandar.
2. Aplicar filtros de estaciones y deduplicacion.
3. Entrenar modelos con separacion temporal estricta.
4. Medir degradacion out-of-region.
5. Calcular descriptores fisicos solo con datos permitidos.
6. Ajustar modelos explicativos de degradacion con dependencia explicita:
   - modelo jerarquico o efectos mixtos con estacion/celda/region y fuente;
   - regresion regularizada solo como sensibilidad predictiva;
   - ranking/prediccion ordinal de estaciones o celdas dificiles;
   - comparacion contra metricas genericas de distribution shift.
7. Evaluar si los descriptores fisicos predicen mejor la degradacion que los baselines estadisticos.

## Resultado nulo o contrario a la hipotesis

Si los descriptores fisicos no superan a los baselines estadisticos preregistrados, el resultado no se reinterpretara post-hoc como exito parcial.

Plan de reporte:

- reportar que los descriptores fisicos no aportan informacion predictiva suficiente bajo este diseno;
- identificar que baselines estadisticos explican mejor la degradacion, si alguno;
- separar si el fallo ocurre en Bloque B, Bloque C o ambos;
- discutir si la limitacion proviene de resolucion diaria, ruido de estaciones, deduplicacion, cobertura o arquitectura;
- mantener el valor del paper como benchmark negativo/reproducible de transferibilidad bajo regimenes climaticos.

La conclusion fuerte solo se hara si la metrica primaria preregistrada apoya la hipotesis. Las metricas secundarias se usaran para interpretacion, no para cambiar la conclusion principal.

## Preregistro verificable

Antes de entrenar modelos definitivos se congelara una version del protocolo.

Condicion previa:

- no se congelara el preregistro hasta disponer de la tabla de estaciones por region AR6 despues de filtros de cobertura, interseccion temporal y deduplicacion;
- si alguna region principal queda por debajo del minimo efectivo preregistrado, se ajustara el diseno antes del preregistro, no despues.

Artefactos aceptables:

- registro publico en OSF o AsPredicted;
- release publico de repositorio con DOI;
- commit firmado y timestamped en repositorio publico, preferiblemente acompanado de DOI.

Contenido minimo del preregistro:

- regiones AR6 y agregaciones;
- fuentes incluidas y excluidas;
- filtros de estaciones y cobertura;
- reglas de deduplicacion;
- splits temporales;
- descriptores fisicos;
- baselines de distribution shift;
- metrica primaria y metricas secundarias;
- plan para resultado nulo.

## Riesgos y mitigaciones

- Pocas regiones efectivas: subdividir por clases climaticas y subregiones objetivas, no por rendimiento observado.
- Solapamiento de fuentes: deduplicacion obligatoria y grupos de identidad cerrados.
- Calidad desigual: filtros comunes de cobertura y QC.
- Circularidad alpina/extremos: regiones definidas por clasificacion externa, no por dificultad esperada.
- AVAMET subdiario: sensibilidad diaria; no mezclar como evidencia subdiaria multi-regional.
- Licencias: documentar restricciones de ECA&D y Weather2K si se usaran; el nucleo inicial evita depender de Weather2K.

## Entregables inmediatos

- Tabla de regiones climaticas preregistradas.
- Script de asignacion estacion-region desde `station_registry_v1.csv`.
- Script de deduplicacion entre fuentes.
- Tabla de cobertura tras filtros por region/fuente/periodo.
- Tabla de interseccion temporal estable por fuente y region.
- Tabla post-deduplicacion por region AR6, celda 5 x 5 y fuente.
- Documento de preregistro congelado antes de entrenar modelos.
