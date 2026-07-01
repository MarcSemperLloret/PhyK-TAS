# Decision v1: nucleo operativo del paper

## Decision

No se replantea la pregunta cientifica ni el framing metodologico. Se replantea el nucleo operativo para reducir riesgo de cobertura, solapamiento entre fuentes y falta de estabilidad longitudinal.

## Nucleo principal

Usar:

- `global_ghcnd_01`
- `eur_ecad_01`

Condiciones:

- variable diaria `precip_mm`;
- regiones IPCC AR6 europeas como particion primaria;
- interseccion temporal estable;
- deduplicacion entre fuentes antes de entrenar o reportar n efectivo;
- evaluacion por estacion y celda 5 x 5 con dependencia jerarquica.

## Validacion fuerte

Usar despues del nucleo:

- `deu_dwd_cdc_01`
- `che_meteoswiss_01`

Rol:

- comprobar robustez frente a proveedor dentro de Europa;
- no mezclar con el nucleo sin deduplicacion;
- no usarlas para inflar el n principal.

## Validacion limitada

Usar con alcance restringido:

- `esp_aemet_daily_hist_01`: validacion reciente o sensibilidad mediterranea; no nucleo longitudinal si el bloque historico queda bajo.
- `esp_avamet_01`: sensibilidad 2019-2025/2020-2025; no argumento central del paper.
- `can_eccc_climate_stations_01`: replicacion externa opcional; no cuarta region principal salvo que el n efectivo post-filtros lo justifique.

## Umbral de cobertura

No se fija todavia 80% o 95% como principal.

Regla:

- calcular primero conteos post-AR6, post-deduplicacion e interseccion temporal estable;
- si las regiones principales conservan n efectivo suficiente a 95%, usar 95% como principal;
- si alguna region principal cae por debajo de 300 estaciones unicas a 95% pero supera 300 a 80%, usar 80% con mascara explicita como principal y 95% como sensibilidad;
- si una region queda por debajo de 300 tambien a 80%, no usarla como region principal sin agrupar o redefinir el diseno.

## Proximo paso

Implementar la tabla final de viabilidad:

- asignacion de estaciones a regiones IPCC AR6;
- interseccion temporal estable;
- deduplicacion entre `global_ghcnd_01`, `eur_ecad_01` y redes nacionales;
- conteos por region AR6, celda 5 x 5, fuente y umbral 80/95.

El preregistro solo puede congelarse despues de esa tabla.

