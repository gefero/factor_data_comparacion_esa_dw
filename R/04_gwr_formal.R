library(sf)
library(sp)
library(GWmodel)

## GWR formal (GWmodel::gwr.basic) de js_divergence ~ prop_agricult + prop_ganaderia,
## a diferencia de R/01_estimate_gw_statistcs.R que solo corre gwss (estadística
## resumen/correlación local, sin coeficientes ni significancia).
##
## Nota de escala: con los ~21.592 hexágonos del set "core" (sin imputar a vecinos),
## gwr.basic necesita una matriz de distancias n x n (~3.7 GB) que excede la RAM
## disponible en este entorno (contenedor con 3.7 GB). Se ajusta sobre una
## submuestra aleatoria de 6.000 hexágonos (semilla fija = reproducible), que sí
## entra en memoria.
##
## bw=300 (n° de vecinos, kernel bisquare adaptativo) se eligió por menor AICc en
## una grilla {300, 500, 800, 1200} corrida sobre la misma submuestra: a mayor bw,
## peor AICc de forma monótona (-7740 a -6407), así que 300 es el óptimo dentro de
## la grilla explorada sin caer en el régimen inestable de bw muy chico (<150) que
## produce coeficientes locales extremos y R² ajustado negativo.

sf_use_s2(FALSE)

div <- st_read('./Data/Geo/divergence_overall_prods_h3_res6.geojson', quiet = TRUE)
vars <- c('js_divergence', 'prop_agricult', 'prop_ganaderia')
d <- suppressWarnings(st_centroid(div[, vars]))
sp_d <- as(d, 'Spatial')

set.seed(42)
sub <- sp_d[sample(nrow(sp_d), 6000), ]

fit <- gwr.basic(js_divergence ~ prop_agricult + prop_ganaderia,
                  data = sub, bw = 300, adaptive = TRUE, kernel = 'bisquare')
print(fit)
saveRDS(fit, './outputs/gwr_formal_agricult_ganaderia_bw300.rds')

sdf <- fit$SDF@data
coords <- coordinates(fit$SDF)
sig_agricult <- abs(sdf$prop_agricult_TV) >= 1.96
sig_ganaderia <- abs(sdf$prop_ganaderia_TV) >= 1.96
cat('% hexágonos con coef. prop_agricult significativo (|t|>=1.96):',
    round(100 * mean(sig_agricult), 1), '\n')
cat('% hexágonos con coef. prop_ganaderia significativo (|t|>=1.96):',
    round(100 * mean(sig_ganaderia), 1), '\n')

plot_coef <- function(v, sig, title, file) {
  png(file, width = 900, height = 1000, res = 120)
  pal <- colorRampPalette(c('#2c7bb6', '#ffffbf', '#d7191c'))(100)
  brks <- seq(min(v), max(v), length.out = 101)
  cols <- pal[cut(v, breaks = brks, include.lowest = TRUE)]
  plot(coords, col = cols, pch = ifelse(sig, 16, 1), cex = ifelse(sig, 0.6, 0.4),
       main = title, xlab = 'Lon', ylab = 'Lat', asp = 1)
  legend('bottomleft', legend = c('significativo (|t|>=1.96)', 'no significativo'),
         pch = c(16, 1), cex = 0.7, bty = 'n')
  dev.off()
}

plot_coef(sdf$prop_agricult, sig_agricult,
          'GWR: coeficiente local de % agricultura sobre js_divergence',
          './outputs/figuras/gwr_coef_agricult.png')
plot_coef(sdf$prop_ganaderia, sig_ganaderia,
          'GWR: coeficiente local de % ganadería sobre js_divergence',
          './outputs/figuras/gwr_coef_ganaderia.png')

png('./outputs/figuras/gwr_local_r2.png', width = 900, height = 1000, res = 120)
pal <- colorRampPalette(c('#2c7bb6', '#ffffbf', '#d7191c'))(100)
brks <- seq(min(sdf$Local_R2), max(sdf$Local_R2), length.out = 101)
cols <- pal[cut(sdf$Local_R2, breaks = brks, include.lowest = TRUE)]
plot(coords, col = cols, pch = 16, cex = 0.4, main = 'GWR: R² local',
     xlab = 'Lon', ylab = 'Lat', asp = 1)
dev.off()

cat('Mapas guardados en ./outputs/figuras\n')
