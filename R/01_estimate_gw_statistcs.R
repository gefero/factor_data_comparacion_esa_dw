library(tidyverse)
library(sf)
library(GWmodel)

in_file <- './Data/Geo/divergence_overall_prods_h3_res6.geojson'


cat("Loading data...")

div_df <- read_sf(in_file)
bandwidth <- round(nrow(div_df) * .005, 0)

vars_select <- c("js_divergence", 
                 "total_exp",
                 "prop_sin_asal",
                 "prop_agricult",
                 "prop_ganaderia")

calculate_gwstats <- function(sf_object, vars, var_na_filter=2, bwidth, adapt,
                              quant){
  centroids <- st_centroid(sf_object)
  
  centroids <- centroids %>%
    select(all_of(vars_select)) %>%
    filter(!is.na(!!sym(vars_select[var_na_filter]))) %>%
    as("Spatial")
    
  gwstats <- gwss(centroids,
             vars=vars_select,
             adaptive = adapt,
             quantile = quant,
             bw = bwidth
  )
  return(gwstats)
}

cat("Calculating GW stats...")
tictoc::tic()
gw_stats <- calculate_gwstats(sf_object = div_df,
                              vars = vars_select,
                              adapt=TRUE,
                              quant=TRUE,
                              bwidth = bandwidth)
tictoc::toc()

out_file <- paste0('./outputs/gwr_descr_usotierra_tamanio_bw', bandwidth,'.rds')

cat("Saving GW stats...")
gw_stats %>% write_rds(out_file)
cat("Done.")