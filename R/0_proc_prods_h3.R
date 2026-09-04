library(tidyverse)
library(sf)
library(GWmodel)

# Funciones Auxiliares
## Funciones de actividación
soft_sign_func <- function(x){ x / (1 + abs(x))  }
soft_plus_func <- function(x){ log(1 + exp(x))}
logistic_func <- function(x){1 / (1 + exp(-x))}
tanh_func <- function(x){tanh(x)}
arc_tan_func <- function(x){atan(x)}
rec_lu_func <- function(x){ ifelse(x < 0 , 0, x )}

## Función para obtener vecinos de celdas H3
library(h3r)

get_cell_nei <- function(cells_vector, k=1){
  center_nei <- list()
  for (center in cells_vector){
    center_nei[[center]] <- gridRingUnsafe(center, k=1)[[1]]
  } 
  
  matrix <- do.call(rbind, center_nei)
  colnames(matrix) <- paste0("V",1:ncol(matrix))
  tibble <- as_tibble(matrix, rownames="center") %>%
    pivot_longer(V1:V6, values_to = "nei") %>%
    select(-name)
  return(tibble)
}

## Carga de datos 1
prods <- read_sf("../../CONICET_estr_agrarias_h3/data/proc/oede_naf.geojson") %>%
  mutate(tam_empleo = case_when(
    tam_empleo == "a. 0" ~ 'sin_asal',
    tam_empleo == "a. 1-9" ~ 'peq_patrones',
    TRUE ~ 'med_grandes_patrones'
  )) 

geo <- read_sf('./Data/Geo/Hexagonos_H3_Argentina_Resolution_6.geojson') %>%
  rename(h3_address = index)

data <- read_csv('./Data/Geo/landcover_analysis_results_resolution_6.csv')

overall <- data %>% filter(dw_class_name == "Overall")
data <- data %>% filter(dw_class_name != "Overall")

## Join espacial
prods <- prods %>%
  st_join(geo, join = st_intersects) %>% 
  filter(!is.na(h3_address))

prods_agg_empleo <- prods %>%
  st_drop_geometry() %>%
  group_by(h3_address, tam_empleo) %>%
  summarise(n=n()) %>%
  ungroup() %>%
  pivot_wider(names_from = c(tam_empleo),
              values_from = n, 
              values_fill = 0
              ) %>%
  janitor::clean_names() %>%
  mutate(total_exp = sin_asal + peq_patrones + med_grandes_patrones) %>%
  mutate(prop_sin_asal = sin_asal / total_exp,
         prop_peq_patrones = peq_patrones / total_exp,
         prop_med_grandes_patrones = med_grandes_patrones/total_exp,
         )

prods_agg_rama <- prods %>%
  st_drop_geometry() %>%
  group_by(h3_address, clae_naf_ag) %>%
  summarise(n=n()) %>%
  ungroup() %>%
  pivot_wider(names_from = c(clae_naf_ag),
              values_from = n, 
              values_fill = 0
  ) %>%
  janitor::clean_names() %>%
  mutate(total_exp_rama = agricultura + ganaderia + forestal + mixta) %>%
  mutate(prop_agricult = agricultura / total_exp_rama,
         prop_ganaderia = ganaderia / total_exp_rama,
         prop_forestal = forestal/total_exp_rama,
         prop_mixta = mixta/total_exp_rama
  )

prods_agg <- prods_agg_empleo %>%
  left_join(prods_agg_rama)

### Genero datasets sin imputar

prods_agg %>%
  left_join(overall) %>%
  left_join(geo) %>%
  st_as_sf() %>%
  write_sf('./Data/Geo/divergence_overall_prods_h3_res6.geojson')
  

prods_agg %>%
  left_join(overall) %>%
  left_join(geo) %>%
  st_as_sf() %>%
  write_sf('./Data/Geo/divergence_byclasses_prods_h3_res6.geojson')


### Identifico h3 vecinos de productor

prods_nei <- get_cell_nei(prods_agg$h3_address, k=1)

### Selecciono los que tienen dato de DW y ESA pero no de
### productores

h3_sin_prod_data <- overall %>%
  left_join(prods_agg) %>%
  filter(is.na(total_exp)) %>%
  select(h3_address) %>% pull()

### Filtro de los vecinos los que no tienen data 
### de productores
prods_nei_input <-  prods_nei %>%
  filter(nei %in% h3_sin_prod_data)

prods_nei_input <- prods_nei_input %>%
  distinct(nei, .keep_all = TRUE)

### Imputo el valor del centro a los vecinos
prods_nei_input <- prods_nei_input %>%
  left_join(prods_agg %>% rename(center=h3_address))

prods_nei_input <- prods_nei_input %>%
  rename(h3_address = nei) %>%
  select(-center) %>%
  bind_rows(
    prods_agg
  ) %>% left_join(geo) %>%
  st_as_sf()

### Resultado final
prods_nei_input %>%
  ggplot() + 
    geom_sf(aes(fill=soft_sign_func(prop_med_grandes_patrones+prop_peq_patrones)),
            color=NA) + 
    scale_fill_viridis_c()

###
overall <- overall %>%
  left_join(prods_nei_input %>%
              st_set_geometry(NULL)) %>%
  left_join(geo) %>%
  st_as_sf()

data <- data %>%
  left_join(geo) %>%
  st_as_sf()
data <- data %>%
  left_join(prods_agg)


write_sf(data, './Data/Geo/divergence_imput_byclasses_prods_h3_res6.geojson')
write_sf(overall, './Data/Geo/divergence_imput_aggregate_prods_h3_res6.geojson')

