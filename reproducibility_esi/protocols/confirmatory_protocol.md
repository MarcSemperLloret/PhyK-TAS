# Protocolo congelado para la confirmación de acciones realizadas

**Congelado:** 22/08/2026, antes de evaluar outcomes 2023–2025.  
**Estado al congelar:** los outcomes confirmatorios 2023–2025 no se han abierto.  
**Propósito:** confirmar o refutar la asignación de reentrenamiento bajo capacidad limitada observada durante desarrollo.

## 1. Datos y bloques temporales

- Source training: 2005–2012.
- Source validation: 2013–2015.
- Target adaptation train: 2013–2014.
- Target adaptation validation: 2015.
- Development outcomes ya utilizados: 2020–2022.
- Confirmatory outcomes bloqueados hasta este protocolo: 2023–2025.
- Regiones: NEU, WCE, WNA, ENA, CNA, SAU, MED, EAU, NWN, NCA y EAS.
- Familias: spatial kNN-ridge, PatchTST small y Graph WaveNet transfer.
- Unidad de decisión: combinación modelo/source region/target region; 330 decisiones.

## 2. Acciones congeladas

- `deploy`: reutilizar el modelo source sin ajuste.
- `adapt`, spatial: calibración afín positiva en log1p ajustada con historia target.
- `adapt`, PatchTST: backbone congelado; ajustar solo la cabeza, 3 épocas, learning rate 5e-4.
- `adapt`, Graph WaveNet: backbone y bloques congelados; ajustar solo el módulo de salida, 3 épocas, learning rate 5e-4.
- `retrain`: modelo de la misma familia entrenado en el target con el protocolo source/target ya implementado.

No se modificarán arquitecturas, épocas, learning rate, ventanas, semillas, rasgos o presupuestos tras observar 2023–2025.

## 3. Política congelada

Se estiman por separado:

- beneficio de adapt frente a deploy;
- beneficio de retrain frente a deploy.

Cada estimador es `StandardScaler + Ridge`. El alpha se elige dentro de los datos de entrenamiento mediante `GroupKFold` por target y la rejilla fija `logspace(-3, 4, 15)`. Para cada target confirmatorio, el estimador se ajusta con outcomes 2020–2022 de los otros diez targets. No usa outcomes 2020–2022 del target retenido ni ningún outcome 2023–2025.

Los 62 predictores congelados son:

- 11 medidas pre-deployment de shift/distribución y distancia geográfica;
- para 12 descriptores físicos, valor source, valor target, delta con signo y delta absoluto;
- 3 indicadores de familia de modelo.

La acción barata es adapt si su beneficio predicho es positivo; en caso contrario, deploy. El score de asignación es el beneficio predicho de retrain respecto a la acción barata.

## 4. Evaluación bajo presupuesto

Para cada target hay 30 decisiones. Se evaluará la curva completa de presupuestos enteros de 0 a 30 reentrenamientos. Para cada presupuesto, la política asigna retrain a las decisiones con mayor score; las restantes reciben su acción barata.

No se seleccionará un presupuesto preferido después de observar confirmación. La métrica primaria es el promedio discreto del MAE sobre toda la curva de presupuesto, calculado primero dentro de cada target y después comparado de forma pareada entre targets.

## 5. Baselines congelados

- asignación aleatoria esperada;
- ranking por MMD;
- ranking por Wasserstein;
- ranking por distancia geográfica;
- ranking por shift de la media;
- ranking por KL source→target;
- oráculo restringido, solo como límite superior;
- always-retrain, reportado únicamente como endpoint sin restricción, no como competidor bajo presupuesto.

## 6. Hipótesis y regla de éxito

Hipótesis primaria direccional: el AUC de MAE de action-value es menor que el de asignación aleatoria esperada.

- Test primario: Wilcoxon pareado unilateral sobre los 11 AUC target-level, alpha 0.05.
- Efecto primario: diferencia media y mediana de AUC action-value menos random.
- Estabilidad mínima: action-value debe mejorar a random en al menos 8/11 targets.
- Comparación secundaria: action-value frente a MMD; se reportará como secundaria y con corrección por multiplicidad junto con los demás baselines shift-only.
- Se reportarán resultados por familia, worst-target y fracción del gap random–oracle cerrada.

**GO confirmatorio:** p primario <0.05, efecto medio favorable, mejora en al menos 8/11 targets y ausencia de un fallo catastrófico concentrado en una familia.  
**NO-GO:** cualquier incumplimiento de esos criterios o evidencia de leakage/inconsistencia.

## 7. Claims permitidos

Si hay GO, se permite afirmar que PhyK-TAS mejora la asignación de capacidad limitada de reentrenamiento frente a reglas aleatorias y shift-only en el benchmark estudiado. No se permite afirmar mejora universal de forecasting, superioridad frente a always-retrain sin restricción ni novedad arquitectónica de los forecasters.

