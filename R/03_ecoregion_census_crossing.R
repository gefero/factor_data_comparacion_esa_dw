library(sp)
library(sf)
library(data.table)

sf_use_s2(FALSE)

## Cruza los resultados GWSS (js_divergence por hexágono H3 res6) con:
## 1) ecoregiones WWF, para ver si la divergencia DW/ESA sigue un patrón
##    árido/estepa vs. húmedo/agrícola.
## 2) indicadores censales CNPyV22 (%NBI), controlando por ecoregión para
##    evitar confundir "más pobre" con "más árido/rural" (paradoja de Simpson:
##    la correlación pooled es positiva pero se invierte dentro de cada
##    ecoregión).

gwss <- readRDS('./outputs/gwr_imput_descr_usotierra_bw6.rds')
d <- gwss$SDF@data
coords <- coordinates(gwss$SDF)
pts <- st_as_sf(data.frame(coords, d), coords = c('coords.x1', 'coords.x2'), crs = 4326)

hex <- st_make_valid(st_read('./Data/Geo/Hexagonos_H3_Argentina_Resolution_6.geojson', quiet = TRUE))

eco <- st_read('./Data/Geo/official/wwf_terr_ecos.shp', quiet = TRUE)
bbox_arg <- st_bbox(c(xmin = -80, ymin = -56, xmax = -50, ymax = -20), crs = st_crs(eco))
eco_arg <- st_make_valid(suppressWarnings(st_crop(eco, bbox_arg)))

j1 <- st_join(pts, hex, join = st_intersects, left = TRUE)
j2 <- st_join(j1, eco_arg[, c('ECO_NAME', 'BIOME')], join = st_intersects, left = TRUE)
jd <- st_drop_geometry(j2)
setDT(jd)
jd <- unique(jd, by = 'index')

## --- 1) Divergencia por ecoregión ---
agg <- aggregate(js_divergence_LM ~ ECO_NAME, data = jd, FUN = mean)
n_by_eco <- table(jd[['ECO_NAME']])
agg$n <- as.integer(n_by_eco[agg$ECO_NAME])
agg <- agg[agg$n >= 100, ]
agg <- agg[order(agg$js_divergence_LM), ]

png('./outputs/figuras/barplot_ecoregion.png', width = 1000, height = 700, res = 120)
par(mar = c(5, 15, 3, 2))
barplot(agg$js_divergence_LM, names.arg = agg$ECO_NAME, horiz = TRUE, las = 1,
        col = colorRampPalette(c('#2c7bb6', '#d7191c'))(nrow(agg)),
        xlab = 'JS divergence promedio (local mean, bw6)',
        main = 'Divergencia DW-ESA por ecoregión (n>=100 hexágonos)')
dev.off()
cat('=== JS divergence promedio por ecoregión ===\n')
print(agg[order(-agg$n), ])

## --- 2) Cruce con censo (CNPyV22), controlando por ecoregión ---
census_cols <- c('Código de radio.', 'Total de hogares',
                  'Hogares con al menos un indicador NBI', 'Población total',
                  'Latitud del centroide', 'Longitud del centroide')
census <- fread('./Data/Geo/poblaciones_CNPyV22_indicadores_hogares_radio.csv',
                 select = census_cols, encoding = 'UTF-8')
setnames(census, census_cols, c('radio', 'hogares', 'hogares_nbi', 'poblacion', 'lat', 'lon'))
census <- census[!is.na(lat) & !is.na(lon)]
census_pts <- st_as_sf(census, coords = c('lon', 'lat'), crs = 4326)

census_joined <- st_drop_geometry(st_join(census_pts, hex, join = st_intersects, left = TRUE))
setDT(census_joined)
census_joined <- census_joined[!is.na(index)]
census_by_hex <- census_joined[, .(hogares = sum(hogares, na.rm = TRUE),
                                    hogares_nbi = sum(hogares_nbi, na.rm = TRUE),
                                    poblacion = sum(poblacion, na.rm = TRUE)), by = index]
census_by_hex[, prop_nbi := hogares_nbi / hogares]

m <- merge(jd, census_by_hex, by = 'index')
m <- m[hogares >= 20 & is.finite(prop_nbi) & !is.na(ECO_NAME)]

cat('\n=== Correlación global (pooled), n =', nrow(m), '===\n')
cat('Spearman(js_divergence_LM, prop_nbi):',
    round(cor(m$js_divergence_LM, m$prop_nbi, method = 'spearman'), 3), '\n')

cat('\n=== Correlación dentro de cada ecoregión (n>=100) ===\n')
by_eco <- m[, .(n = .N, spearman = round(cor(js_divergence_LM, prop_nbi, method = 'spearman'), 3)),
            by = ECO_NAME]
print(by_eco[n >= 100][order(-n)])

cat('\n=== Correlación parcial controlando por ecoregión (residuos) ===\n')
m[, eco_f := factor(ECO_NAME)]
res_js <- residuals(lm(js_divergence_LM ~ eco_f, data = m))
res_nbi <- residuals(lm(prop_nbi ~ eco_f, data = m))
cat('Spearman (residuos):', round(cor(res_js, res_nbi, method = 'spearman'), 3), '\n')
cat('Pearson (residuos):', round(cor(res_js, res_nbi), 3), '\n')
