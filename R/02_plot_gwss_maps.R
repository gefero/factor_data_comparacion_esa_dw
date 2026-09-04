library(sp)
library(sf)

## Genera mapas puntuales de los resultados GWSS (outputs/*.rds) guardados
## por R/01_estimate_gw_statistcs.R. Cada punto es un hexágono H3 res6.

plot_var <- function(sdf_data, coords, varname, title, file) {
  v <- sdf_data[[varname]]
  png(file, width = 900, height = 1000, res = 120)
  pal <- colorRampPalette(c('#2c7bb6', '#ffffbf', '#d7191c'))(100)
  brks <- seq(min(v, na.rm = TRUE), max(v, na.rm = TRUE), length.out = 101)
  cols <- pal[cut(v, breaks = brks, include.lowest = TRUE)]
  plot(coords, col = cols, pch = 16, cex = 0.35, main = title,
       xlab = 'Lon', ylab = 'Lat', asp = 1)
  dev.off()
}

out_dir <- './outputs/figuras'

## bw6, imputado: js_divergence local + correlación con agricultura/ganadería
gwss_bw6 <- readRDS('./outputs/gwr_imput_descr_usotierra_bw6.rds')
d6 <- gwss_bw6$SDF@data
coords6 <- coordinates(gwss_bw6$SDF)

plot_var(d6, coords6, 'js_divergence_LM',
         'JS divergence (media local, bw6)',
         file.path(out_dir, 'map_js_lm.png'))

plot_var(d6, coords6, 'Corr_js_divergence.prop_agricult',
         'Corr. local: JS divergence x % agricultura',
         file.path(out_dir, 'map_corr_agricult.png'))

plot_var(d6, coords6, 'Corr_js_divergence.prop_ganaderia',
         'Corr. local: JS divergence x % ganadería',
         file.path(out_dir, 'map_corr_ganaderia.png'))

## bw2, imputado: correlación con % sin asalariados y densidad de productores
gwss_bw2 <- readRDS('./outputs/gwr_imput_descr_tamanio_bw2.rds')
d2 <- gwss_bw2$SDF@data
coords2 <- coordinates(gwss_bw2$SDF)

plot_var(d2, coords2, 'Corr_js_divergence.prop_sin_asal',
         'Corr. local: JS divergence x % sin asalariados (bw2)',
         file.path(out_dir, 'map_corr_sinasal.png'))

plot_var(d2, coords2, 'Corr_js_divergence.total_exp',
         'Corr. local: JS divergence x densidad de productores (bw2)',
         file.path(out_dir, 'map_corr_totalexp.png'))

cat('Mapas guardados en', out_dir, '\n')
