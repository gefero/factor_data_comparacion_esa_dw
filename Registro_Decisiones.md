# Registro de Decisiones del Proyecto

## 2024-27-11
### Esquema de muestreo estratificado

**Estado:** Pausado

**Contexto rápido:**
- Necesitamos establecer sistema de muestreo estratificado para validar DW de forma representativa
- Estratificación basada en ecoregiones según conversaciones con Germán

**Decisiones clave:**
- Usar base de datos WWF para ecoregiones ([fuente](https://www.worldwildlife.org/publications/terrestrial-ecoregions-of-the-world))

**Próximos pasos:**
- [ ] Cruzar ecoregiones con índice espacial (H3 o S2)
- [ ] Decidir entre H3 o S2
- [ ] Definir criterios para áreas fronterizas
- [ ] Revisar área de estudio (criterio ecoregiones vs político)

---

## 2024-28-11
### Descarga de imágenes para workflow de validación

**Estado:** Completado

**Contexto rápido:**
- Descarga de imágenes ESA y DW (30m y 50m) en Chaco y Delta del Paraná
- Objetivo: establecer proceso de validación para aplicar en muestreo estratificado

**Decisiones clave:**
- Foco en resoluciones de 30m y 50m
- Implementación de 4 métodos de descarga (moda, moda pooleada, media y media pooleada)

**Notas adicionales:**
- Alternativas pendientes de evaluar:
  - Resolución a 10m
  - Otras áreas de estudio
  - Descarga de imágenes Sentinel-2 crudas

---

## 2024-30-11
### Validación interna métodos de descarga

**Estado:** Completo

**Contexto rápido:**
- Comparación de diferentes métodos de agregación temporal y espacial de DW
- Desarrollo de funciones de comparación: compare_dw_maps() y compare_multiple_dw_maps()

**Decisiones clave:**
- Implementación de dos enfoques de comparación:
  1. Agregación total por clases con matriz de confusión
  2. Comparación a nivel pixel

**Notas adicionales:**
- Resultados divergentes entre funciones - requiere investigación
- Hipótesis: método de probabilidades y recomputo de clase predominante podría ser más robusto

---

## 2024-7-12
### [Replanteo del esquema de validación]

**Estado:** [En progreso]

**Contexto rápido:**
- Este paper establece un workflow de validación de DW contra WC y ESRI bien establecido y replicable [Paper](https://www.mdpi.com/2072-4292/14/16/4101)
- [Punto 2]

**Decisiones clave:**
- Aplico la metodología del paper. Extraje los héxagonos de H3 a resolución de 3 y 4 que intersectan sobre toda la Argentina.
  La idea es poder dentro de cada héxagono utilizar la metodología del paper para evaluar DW. 
  Básicamente se hace un conteo del total de los pixeles que caen dentro del héxagono y se examina las diferencias en totales entre las dos fuentes de datos.
- También crucé los héxagonos de H3 con el mapa de ecoregiones. Me gustaría también incluir variables sociodemográficas y productivas para analizar si el error posee patrones.

**Próximos pasos:**
- [ ] Explorar la posibilidad de validar contra una ground-truth como el dataset original generado para entrenar DW.
- [ ] Explorar algún método que incluya las probabilidades en el esquema de validación.
- [ ] Explorar el uso de índices de diferencia normalizada para la validación.
- [ ] Encontrar otras fuentes de datos contra las que explorar la correlación del error.


**Notas adicionales:**
- [Notas opcionales]

---

## 2026-04-09
### Comparación DW vs ESA completada a escala nacional; foco actual en explicar la divergencia

**Estado:** Completado (comparación) / En progreso (análisis de divergencia)

**Contexto rápido:**
- Entrada retroactiva: registra el estado real del proyecto relevado a partir del repo (código y datos), que había quedado desactualizado desde la última entrada (2024-7-12).
- La comparación DW vs ESA WorldCover, planteada como "en progreso" en la entrada anterior, ya está terminada para toda Argentina, no solo para las áreas piloto de Chaco y Delta del Paraná.

**Decisiones clave:**
- `Testeo_validacion_metodología_paper.ipynb` implementó el pipeline completo por hexágono H3 (resolución 4, con checkpointing en `DW_Validado_Resolution_4_checkpoint.pkl`/`.csv`): histograma de frecuencia de píxeles ESA (reclasificado a las 9 clases DW) vs DW (`mode()` anual) por hexágono, con precision/recall/f1 por clase y accuracy/precision/recall/f1 agregados por hexágono.
- El resultado consolidado, a resolución H3 6 y ya con `js_divergence` y `kappa` agregados, quedó en `Data/Geo/landcover_analysis_results_resolution_6.csv` (el script que agrega esas dos métricas no está commiteado en el repo).
- `R/0_proc_prods_h3.R` cruza esa divergencia con datos de productores agropecuarios (dataset externo `CONICET_estr_agrarias_h3/oede_naf.geojson`: tamaño de empleo y rama de actividad por hexágono), con imputación a hexágonos vecinos sin dato de productores. Genera los geojson `divergence_overall_*`, `divergence_byclasses_*` y sus versiones `_imput_*`.
- `R/01_estimate_gw_statistcs.R` corre Geographically Weighted Statistics (`gwss`, paquete GWmodel) entre `js_divergence` y las variables productivas, probando varios anchos de banda (bw2, bw3, bw4, bw6) — resultados en `outputs/*.rds`.
- Se sumaron datos censales (`Data/Geo/poblaciones_CNPyV22_indicadores_hogares_radio.csv` y `..._personas_radio.csv`), en línea con la idea original de incorporar variables sociodemográficas al análisis de patrones de error.

**Próximos pasos:**
- [ ] Documentar/commitear el script que calcula `js_divergence` y `kappa` a resolución H3 6 (no está en el repo actualmente).
- [ ] Incorporar formalmente las variables censales (CNPyV22) al modelo GWR, no solo las de productores agropecuarios.
- [ ] Sistematizar los hallazgos de correlación espacial (`Corr_js_divergence.*`, `Spearman_rho_js_divergence.*`) explorados de forma ad hoc en `.Rhistory` en un notebook o script reproducible.
- [ ] Retomar los próximos pasos pendientes de la entrada anterior (ground-truth de DW, uso de probabilidades, índices de diferencia normalizada) si siguen vigentes para el paper.

**Notas adicionales:**
- Este relevamiento se hizo revisando fechas de modificación de archivos (`landcover_analysis_results_resolution_6.csv` de abril 2025; geojson de divergencia y datos censales de oct. 2025) y el `.Rhistory`, ya que la bitácora no se había actualizado desde diciembre de 2024.

---

## 2026-04-09 (cont.)
### Bug en dw_pixels por clase + cruce con ecoregiones y censo

**Estado:** Completado (este avance) / En progreso (el análisis de fondo)

**Contexto rápido:**
- Se instaló R + `sp`/`sf`/`data.table` en el devcontainer para poder leer los `.rds` de GWSS (`outputs/*.rds`) directamente.
- Al intentar validar la fórmula de `js_divergence`/`kappa` contra los datos crudos, se detectó que `dw_pixels`/`dw_proportion` están en 0 en el 100% de las 848.934 filas de `Data/Geo/landcover_analysis_results_resolution_6.csv` (verificado con todo el archivo, no una muestra).

**Decisiones clave:**
- `matched_pixels`, `class_recall`, `hexagon_overall_*`, `js_divergence` y `kappa` de ese CSV sí son válidos (se verificaron contra sus fórmulas). Lo que **no** es usable de ese archivo: `dw_pixels`, `dw_proportion`, `class_precision`, `proportion_difference`.
- Causa probable: mismatch de formato de clave (`'0'` vs `'0.0'`) al leer el histograma de frecuencias de DW en el script que generó ese CSV (no commiteado, distinto de la versión actual de `Testeo_validacion_metodología_paper.ipynb`).
- Se agregó `compute_hexagon_divergence_metrics()` a `function_utils.py`: reconstruye `js_divergence` (Jensen-Shannon, bits) y `kappa` (desde marginales: `po`=accuracy, `pe`=Σ p_esa·p_dw) con parsing robusto de claves. Validada exactamente contra un hexágono real de `Data/Geo/DW_Validado_Resolution_4.csv` (que sí tiene `dw_pixels` correctos).
- Cruce con ecoregiones WWF (`Data/Geo/official/wwf_terr_ecos.shp`): la divergencia promedio por ecoregión va de 0.19 (Humid Pampas) a ~0.40-0.50 (Patagonian steppe, Valdivian temperate forests, Southern Andean steppe) — gradiente árido/estepa vs. húmedo/agrícola muy claro. El signo de la correlación agricultura(-)/ganadería(+) con divergencia se mantiene en casi todas las ecoregiones.
- Cruce con censo (CNPyV22, `%NBI` por hexágono vía centroides de radio censal): correlación de Spearman positiva moderada (0.29, *pooled*) entre `js_divergence` y % hogares con NBI. **Corregido más abajo: esto era confusión espacial, no una relación real.**
- Scripts nuevos, versionados y probados de punta a punta: `R/02_plot_gwss_maps.R` (genera los 5 mapas puntuales de GWSS) y `R/03_ecoregion_census_crossing.R` (cruce con ecoregiones + censo, con el control de confusión de abajo). Ambos escriben a `outputs/figuras/`.

**Corrección (misma sesión, después de controlar por ecoregión):**
- La correlación pooled (+0.29) entre `js_divergence` y `%NBI` es un caso de paradoja de Simpson: dentro de cada ecoregión la correlación es mayormente **negativa o nula** (Dry Chaco -0.35, Southern Andean Yungas -0.40, Humid Pampas -0.04; solo Espinal +0.23 y Humid Chaco +0.21 son positivas), y la correlación parcial controlando por ecoregión (residuos, n=8.590) es **-0.13 (Spearman) / -0.17 (Pearson)** — signo invertido respecto al pooled.
- Conclusión revisada: **no hay evidencia de que la pobreza estructural explique la divergencia DW/ESA** una vez controlado por ecoregión. La correlación positiva agregada solo refleja que Patagonia/Chaco árido son a la vez más pobres y más divergentes por aridez. El patrón agricultura(-)/ganadería(+) sigue firme (se sostiene ecoregión por ecoregión).

**Próximos pasos:**
- [ ] Correr `compute_hexagon_divergence_metrics()` contra GEE para regenerar `landcover_analysis_results_resolution_6.csv` con `dw_pixels`/`dw_proportion` correctos (no se pudo ejecutar acá por falta de credenciales GEE en este entorno).
- [ ] Considerar un GWR formal (`gwr.basic`, no solo `gwss`) si se quiere una superficie de coeficientes con significancia estadística.
- [ ] Si se quiere seguir la pista censal, probar otros indicadores (no solo NBI) y otra estrategia de control (p. ej. densidad poblacional continua en vez de dummies de ecoregión).

**Notas adicionales:**
- Figuras versionadas en `outputs/figuras/`: `map_js_lm.png`, `map_corr_agricult.png`, `map_corr_ganaderia.png`, `map_corr_sinasal.png`, `map_corr_totalexp.png`, `barplot_ecoregion.png`.

---

## 2026-04-09 (cont. 2)
### GWR formal + control de confusión censal con densidad continua

**Estado:** Completado

**Contexto rápido:**
- Se cerraron los dos pendientes que quedaban abiertos: (1) correr un GWR formal (no solo `gwss`), (2) volver a probar la pista censal con otro control (densidad poblacional continua) y otros indicadores además de `%NBI`.

**Decisiones clave — GWR formal:**
- Se instaló `GWmodel` desde CRAN (no está empaquetado en apt; hubo que instalar además `liblapack-dev`/`libblas-dev`/`gfortran` para poder linkear).
- `gwr.basic(js_divergence ~ prop_agricult + prop_ganaderia)` sobre las ~21.592 hexágonos "core" **no corre en este entorno**: la matriz de distancias n×n pesa ~3.7 GB, prácticamente toda la RAM del contenedor (3.7 GB total) — el proceso se cuelga por swapping. Se resolvió ajustando sobre una submuestra aleatoria de 6.000 hexágonos (semilla fija).
- Bandwidth elegido por AICc en una grilla {300, 500, 800, 1200} (adaptativo, kernel bisquare): AICc empeora monótonamente al agrandar bw, así que **bw=300** es el óptimo explorado (evitando el régimen inestable de bw muy chico, ~80-150, donde los coeficientes locales explotan y el R² ajustado se vuelve negativo).
- Resultado: R² global (OLS) = 0.068, R² local (GWR) ajustado = **0.50** — la relación entre uso del suelo y divergencia es fuertemente no estacionaria espacialmente; casi todo el poder explicativo es local.
- Solo 16.7% de los hexágonos tiene coeficiente de `prop_agricult` significativo (|t|≥1.96) y 22.4% para `prop_ganaderia` — el efecto es real pero geográficamente acotado, no nacional. R² local más alto en Buenos Aires y Chaco/Formosa; más bajo en Patagonia.
- Script versionado: `R/04_gwr_formal.R`. Figuras: `outputs/figuras/gwr_coef_agricult.png`, `gwr_coef_ganaderia.png`, `gwr_local_r2.png`. Modelo guardado en `outputs/gwr_formal_agricult_ganaderia_bw300.rds`.

**Decisiones clave — censo, segunda vuelta:**
- Se probaron 5 indicadores (NBI, hacinamiento, sin agua de red, combustible garrafa/leña, computadora) con 3 estrategias de control: ecoregión (dummies), densidad poblacional continua (log, spline), y ambas.
- **La densidad poblacional NO es un control equivalente a la ecoregión**: controlar solo por densidad apenas mueve la correlación de NBI (0.29→0.26), mientras que ecoregión la invierte (0.29→-0.13). El confusor real es el bioma/aridez, no "denso vs. disperso".
- **Hallazgo nuevo:** `% hogares sin agua de red pública` es el único indicador robusto en las 4 especificaciones (siempre negativo, -0.15 a -0.28) — a diferencia de NBI/hacinamiento (marcadores de asentamiento informal periurbano), este es un marcador de ruralidad genuina (pozo/tanque), y correlaciona con **menor** divergencia: el campo extensivo "de verdad" se clasifica más consistente que las zonas periurbanas mixtas.

**Próximos pasos:**
- [ ] Correr `compute_hexagon_divergence_metrics()` contra GEE para regenerar `landcover_analysis_results_resolution_6.csv` con `dw_pixels`/`dw_proportion` correctos (sigue bloqueado por falta de credenciales GEE en este entorno).
- [ ] Si se quiere GWR sobre el dataset completo (21.592 o 53.028 hexágonos), correrlo en una máquina con más RAM (>8 GB recomendado) en vez de este devcontainer.
- [ ] Profundizar la pista de "% sin agua de red" como proxy de ruralidad genuina — es la señal censal más consistente encontrada hasta ahora.

**Notas adicionales:**
- Ninguno de los pendientes registrados en la entrada anterior queda abierto salvo el que depende de credenciales GEE.
- Importante para quien retome esto: la imposibilidad de correr `gwr.basic` sobre los 21.592/53.028 hexágonos completos en este devcontainer **se verificó empíricamente** (se lanzó el proceso, se lo dejó corriendo varios minutos, y hubo que matarlo por consumo de swap) — no es que falte probar un bandwidth más chico o esperar más tiempo. No tiene sentido reintentarlo en este entorno sin más RAM; el resultado sobre la submuestra de 6.000 (bw=300, `R/04_gwr_formal.R`) es el entregable válido hasta que se corra en una máquina con más memoria.

---

<!-- Template para nuevas entradas -->
## [FECHA]
### [NOMBRE BREVE DE LA TAREA]

**Estado:** [En progreso/Completado/Pausado]

**Contexto rápido:**
- [Punto 1]
- [Punto 2]

**Decisiones clave:**
- [Decisión 1]
- [Decisión 2]

**Próximos pasos:**
- [ ] [Tarea 1]
- [ ] [Tarea 2]

**Notas adicionales:**
- [Notas opcionales]
