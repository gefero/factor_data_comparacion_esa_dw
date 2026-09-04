validacion_descarga_dw: Descarga de las imágenes Dynamic World de la frontera Chaco-Santiago y el Delta del Paraná para validación

validacion_descarga_ESA: Descarga de las imágenes ESA WorldCover V100 de la frontera Chaco-Santiago y el Delta del Paraná para validación

Validación_Descarga: Une los archivos validacion_descarga_dw y validacion_descarga_ESA en un único archivo de descargas.

validación_test: Cruce de las distintas imagenes para validar método de descarga.

# function_utils.py

## Descripción General
Colección de funciones de utilidad para procesar y analizar datos de cobertura terrestre usando Google Earth Engine, especialmente para Dynamic World y ESA World Cover.

## Funciones

### initialize_gee
```python
initialize_gee(project_id: str, opt_url: str = 'https://earthengine-highvolume.googleapis.com')
```
Inicializa la autenticación de Google Earth Engine.
- **project_id**: ID del proyecto GCP
- **opt_url**: URL del servidor GEE (opcional)

### chunk_geometry
```python
chunk_geometry(geometry: ee.Geometry, initial_max_size: int = 15000000, min_chunk_size: int = 1000000)
```
Divide una geometría en fragmentos más pequeños para procesamiento.
- **geometry**: Geometría a dividir
- **initial_max_size**: Tamaño máximo inicial del fragmento
- **min_chunk_size**: Tamaño mínimo del fragmento
- **Retorna**: Lista de geometrías fragmentadas

### process_worldcover
```python
process_worldcover(aoi: ee.Geometry, output_path: str, scale: int = 30)
```
Procesa datos de ESA World Cover.
- **aoi**: Área de interés
- **output_path**: Ruta de salida del archivo
- **scale**: Resolución en metros

### process_dynamic_world
```python
process_dynamic_world(
    aoi: ee.Geometry,
    processing_type: str,
    output_path: str,
    scale: int = 30,
    start_date: str = "2020-01-01",
    end_date: str = "2021-01-01",
    include_probabilities: bool = False
)
```
Procesa datos de Dynamic World.
- **aoi**: Área de interés
- **processing_type**: Tipo de procesamiento ('mode', 'mode_pooled', 'mean_pooled', 'mean_unpooled')
- **output_path**: Ruta de salida del archivo
- **scale**: Resolución en metros
- **start_date**: Fecha inicial
- **end_date**: Fecha final
- **include_probabilities**: Incluir bandas de probabilidad

### compare_dw_maps
```python
compare_dw_maps(
    dataset1: Union[str, Path, xr.Dataset],
    dataset2: Union[str, Path, xr.Dataset],
    data_var1: str = 'label',
    data_var2: str = 'label',
    title_prefix: str = 'Dynamic World Comparison'
)
```
Compara dos mapas de Dynamic World.
- **dataset1, dataset2**: Datasets a comparar
- **data_var1, data_var2**: Variables a comparar
- **title_prefix**: Prefijo del título
- **Retorna**: Diccionario con matriz de confusión y métricas

### compare_dw_esa
```python
compare_dw_esa(
    dw_dataset: Union[str, Path, xr.Dataset],
    esa_dataset: Union[str, Path, xr.Dataset],
    dw_var: str = 'label',
    esa_var: str = 'Map'
)
```
Compara mapas de Dynamic World y ESA World Cover.
- **dw_dataset**: Dataset de Dynamic World
- **esa_dataset**: Dataset de ESA
- **dw_var**: Variable de Dynamic World
- **esa_var**: Variable de ESA
- **Retorna**: Diccionario con matrices de confusión y métricas

### visualize_areas
```python
visualize_areas(areas: Dict[str, ee.Geometry.Polygon], colors: Dict[str, Dict[str, str]] = None)
```
Crea un mapa interactivo de áreas de estudio.
- **areas**: Diccionario de áreas y geometrías
- **colors**: Diccionario de estilos de visualización
- **Retorna**: Objeto geemap.Map

## Dependencias
- earthengine-api
- geemap
- wxee
- xarray
- numpy
- seaborn
- matplotlib

## Notas
- Las funciones manejan automáticamente áreas grandes mediante fragmentación
- Incluye manejo de errores y reintentos
- Soporta diferentes tipos de procesamiento para Dynamic World