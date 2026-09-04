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
