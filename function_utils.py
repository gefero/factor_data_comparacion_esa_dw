import xarray as xr
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from typing import Dict, Union, List, Tuple
from pathlib import Path

import numpy as np
import xarray as xr
from pathlib import Path
from typing import List, Union, Tuple
import matplotlib.pyplot as plt
import seaborn as sns

def compare_multiple_dw(
        datasets: List[Union[str, Path, xr.Dataset]],
        names: List[str],
        data_var: str = 'label',
        figsize: Tuple[int, int] = (8, 6),
        title: str = ''
) -> None:
    """
    Compares multiple Dynamic World maps, calculating accuracy between all pairs
    using confusion matrices.

    Parameters
    ----------
    datasets : List[Union[str, Path, xr.Dataset]]
        List of Dynamic World datasets to compare
    names : List[str]
        Names to identify each dataset in the visualization
    data_var : str
        Name of the variable to compare in each dataset
    figsize : Tuple[int, int]
        Size of the figure
    """
    if len(datasets) != len(names):
        raise ValueError("Number of datasets must match number of names")

    # Dynamic World classes dictionary
    dw_classes = {
        0: 'Water',
        1: 'Trees',
        2: 'Grass',
        3: 'Flooded vegetation',
        4: 'Crops',
        5: 'Shrub & scrub',
        6: 'Built',
        7: 'Bare',
        8: 'Snow & ice'
    }

    # Load datasets
    def load_dataset(ds):
        if isinstance(ds, (str, Path)):
            return xr.open_dataset(ds)
        return ds

    loaded_datasets = [load_dataset(ds) for ds in datasets]

    # Create accuracy matrix
    n_datasets = len(datasets)
    accuracy_matrix = np.zeros((n_datasets, n_datasets))
    labels = sorted(dw_classes.keys())

    # Calculate accuracies using confusion matrices
    for i in range(n_datasets):
        for j in range(n_datasets):
            if i != j:
                # Create confusion matrix
                conf_matrix = np.zeros((len(labels), len(labels)), dtype=int)

                for k, label1 in enumerate(labels):
                    for l, label2 in enumerate(labels):
                        conf_matrix[k, l] = np.sum(
                            (loaded_datasets[i][data_var].values == label1) &
                            (loaded_datasets[j][data_var].values == label2)
                        )

                # Calculate overall accuracy from confusion matrix
                accuracy = np.sum(np.diag(conf_matrix)) / np.sum(conf_matrix)
                accuracy_matrix[i, j] = accuracy
            else:
                accuracy_matrix[i, j] = 1.0  # Diagonal elements

    # Create visualization
    plt.figure(figsize=figsize)
    sns.heatmap(accuracy_matrix,
                annot=True,
                fmt='.2%',
                xticklabels=names,
                yticklabels=names,
                cmap='YlOrRd',
                vmin=0,
                vmax=1)
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()

    # Print intermediate values for the last comparison
    print("Valores intermedios compare_multiple:")
    print(f"Suma diagonal: {np.sum(np.diag(conf_matrix))}")
    print(f"Suma total matriz: {np.sum(conf_matrix)}")
    print(f"Accuracy: {accuracy:.2%}")

def compare_dw_maps(
        dataset1: Union[str, Path, xr.Dataset],
        dataset2: Union[str, Path, xr.Dataset],
        data_var1: str = 'label',
        data_var2: str = 'label',
        title_prefix: str = 'Dynamic World Comparison',
        labels1_name: str = 'Map 1',
        labels2_name: str = 'Map 2',
        figsize: Tuple[int, int] = (10, 8),
        cmap: str = 'Blues',
) -> dict:
    """
    Compara dos mapas de Dynamic World, calculando matriz de confusión y métricas.

    Parameters
    ----------
    dataset1, dataset2 : Union[str, Path, xr.Dataset]
        Datasets de Dynamic World a comparar
    data_var1, data_var2 : str
        Nombres de las variables a comparar en cada dataset
    title_prefix : str
        Prefijo para el título del gráfico
    labels1_name, labels2_name : str
        Nombres para identificar cada mapa
    figsize : Tuple[int, int]
        Tamaño de la figura
    cmap : str
        Colormap para la matriz de confusión

    Returns
    -------
    dict
        Diccionario con matriz de confusión y métricas
    """
    # Diccionario de clases de Dynamic World
    dw_classes = {
        0: 'Water',
        1: 'Trees',
        2: 'Grass',
        3: 'Flooded vegetation',
        4: 'Crops',
        5: 'Shrub & scrub',
        6: 'Built',
        7: 'Bare',
        8: 'Snow & ice'
    }

    def load_dataset(ds):
        if isinstance(ds, (str, Path)):
            return xr.open_dataset(ds)
        return ds

    ds1 = load_dataset(dataset1)
    ds2 = load_dataset(dataset2)

    # Verificar forma
    if ds1[data_var1].shape != ds2[data_var2].shape:
        raise ValueError(f"Los datasets deben tener la misma forma. "
                         f"Se obtuvo {ds1[data_var1].shape} y {ds2[data_var2].shape}")

    # Crear matriz de confusión
    labels = sorted(dw_classes.keys())
    conf_matrix = np.zeros((len(labels), len(labels)), dtype=int)

    for i, label1 in enumerate(labels):
        for j, label2 in enumerate(labels):
            conf_matrix[i, j] = np.sum((ds1[data_var1].values == label1) &
                                       (ds2[data_var2].values == label2))

    # Calcular métricas
    overall_accuracy = np.sum(np.diag(conf_matrix)) / np.sum(conf_matrix)

    # Crear etiquetas legibles
    readable_labels = [dw_classes[i] for i in labels]

    # Plotear
    plt.figure(figsize=figsize)
    sns.heatmap(conf_matrix, annot=True, fmt='g', cmap=cmap,
                xticklabels=readable_labels, yticklabels=readable_labels)
    plt.title(f'{title_prefix}: {labels1_name} vs {labels2_name}')
    plt.xlabel(labels2_name)
    plt.ylabel(labels1_name)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()

    print(f"Precisión general: {overall_accuracy:.2%}")

    return {
        'confusion_matrix': conf_matrix,
        'labels': labels,
        'readable_labels': readable_labels,
        'overall_accuracy': overall_accuracy
    }



import xarray as xr
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from typing import Tuple, Union, Optional, Dict
from pathlib import Path

def compare_dw_esa(
        dw_dataset: Union[str, Path, xr.Dataset],
        esa_dataset: Union[str, Path, xr.Dataset],
        dw_var: str = 'label',
        esa_var: str = 'Map',
        custom_mapping: Dict[int, int] = None,
        title: str = 'Dynamic World vs ESA Land Cover',
        figsize: Tuple[int, int] = (12, 10),
        cmap: str = 'YlOrRd'
) -> dict:
    """
    Compara mapas de Dynamic World y ESA, creando matrices de confusión y calculando métricas.

    Parameters
    ----------
    dw_dataset : Union[str, Path, xr.Dataset]
        Dataset de Dynamic World
    esa_dataset : Union[str, Path, xr.Dataset]
        Dataset de ESA
    dw_var : str
        Nombre de la variable en el dataset de DW
    esa_var : str
        Nombre de la variable en el dataset de ESA
    custom_mapping : Dict[int, int], opcional
        Mapeo personalizado de clases ESA -> DW. Si no se proporciona, se usa el mapeo por defecto
    title : str
        Título para los gráficos
    figsize : Tuple[int, int]
        Tamaño de la figura
    cmap : str
        Colormap para las matrices de confusión

    Returns
    -------
    dict
        Diccionario con matrices de confusión y métricas
    """
    # Definición de clases
    DW_CLASSES = {
        0: 'Water',
        1: 'Trees',
        2: 'Grass',
        3: 'Flooded vegetation',
        4: 'Crops',
        5: 'Shrub & scrub',
        6: 'Built',
        7: 'Bare',
        8: 'Snow & ice'
    }

    ESA_CLASSES = {
        10: 'Tree cover',
        20: 'Shrubland',
        30: 'Grassland',
        40: 'Cropland',
        50: 'Built-up',
        60: 'Bare / sparse vegetation',
        70: 'Snow and ice',
        80: 'Permanent water bodies',
        90: 'Herbaceous wetland',
        95: 'Mangroves',
        100: 'Moss and lichen'
    }

    # Mapeo por defecto ESA -> DW
    DEFAULT_MAPPING = {
        10: 1,    # Tree cover -> Trees
        20: 5,    # Shrubland -> Shrub & scrub
        30: 2,    # Grassland -> Grass
        40: 4,    # Cropland -> Crops
        50: 6,    # Built-up -> Built
        60: 7,    # Bare/sparse -> Bare
        70: 8,    # Snow and ice -> Snow & ice
        80: 0,    # Water bodies -> Water
        90: 3,    # Herbaceous wetland -> Flooded vegetation
        95: 3,    # Mangroves -> Flooded vegetation
        100: 2    # Moss and lichen -> Grass
    }

    # Usar mapeo personalizado si se proporciona
    class_mapping = custom_mapping if custom_mapping is not None else DEFAULT_MAPPING

    def load_dataset(ds):
        if isinstance(ds, (str, Path)):
            return xr.open_dataset(ds)
        return ds

    ds1 = load_dataset(dw_dataset)
    ds2 = load_dataset(esa_dataset)

    # Verificar forma
    if ds1[dw_var].shape != ds2[esa_var].shape:
        raise ValueError(f"Los datasets deben tener la misma forma. "
                         f"Se obtuvo {ds1[dw_var].shape} y {ds2[esa_var].shape}")

    # Matriz de confusión original
    labels_dw = sorted(DW_CLASSES.keys())
    labels_esa = sorted(ESA_CLASSES.keys())

    conf_matrix = np.zeros((len(labels_dw), len(labels_esa)), dtype=int)

    for i, label1 in enumerate(labels_dw):
        for j, label2 in enumerate(labels_esa):
            conf_matrix[i, j] = np.sum((ds1[dw_var].values == label1) &
                                       (ds2[esa_var].values == label2))

    # Plotear matriz original
    plt.figure(figsize=figsize)
    sns.heatmap(conf_matrix, annot=True, fmt='g', cmap=cmap,
                xticklabels=[ESA_CLASSES[i] for i in labels_esa],
                yticklabels=[DW_CLASSES[i] for i in labels_dw])
    plt.title(f'{title}\nOriginal Confusion Matrix')
    plt.xlabel('ESA Land Cover')
    plt.ylabel('Dynamic World')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()

    # Crear array mapeado
    ds2_mapped = ds2[esa_var].values.copy()
    for esa_class, dw_class in class_mapping.items():
        ds2_mapped[ds2[esa_var].values == esa_class] = dw_class

    # Matriz de confusión mapeada
    mapped_labels = sorted(set(DW_CLASSES.keys()))
    conf_matrix_mapped = np.zeros((len(mapped_labels), len(mapped_labels)), dtype=int)

    for i, label1 in enumerate(mapped_labels):
        for j, label2 in enumerate(mapped_labels):
            conf_matrix_mapped[i, j] = np.sum((ds1[dw_var].values == label1) &
                                              (ds2_mapped == label2))

    # Calcular métricas
    overall_accuracy = np.sum(np.diag(conf_matrix_mapped)) / np.sum(conf_matrix_mapped)
    per_class_accuracy = {}
    for i, label in enumerate(mapped_labels):
        class_sum = np.sum(conf_matrix_mapped[i, :])
        if class_sum > 0:
            per_class_accuracy[label] = conf_matrix_mapped[i, i] / class_sum

    # Plotear matriz mapeada
    plt.figure(figsize=figsize)
    mapped_labels_names = [DW_CLASSES[i] for i in mapped_labels]
    sns.heatmap(conf_matrix_mapped, annot=True, fmt='g', cmap=cmap,
                xticklabels=mapped_labels_names,
                yticklabels=mapped_labels_names)
    plt.title(f'{title}\nMapped Classes Confusion Matrix')
    plt.xlabel('ESA (mapped to DW classes)')
    plt.ylabel('Dynamic World')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()

    print(f"\nOverall Accuracy: {overall_accuracy:.2%}")
    print("\nPer-class Accuracy:")
    for label, acc in per_class_accuracy.items():
        print(f"{DW_CLASSES[label]}: {acc:.2%}")

    return {
        'original_confusion_matrix': conf_matrix,
        'mapped_confusion_matrix': conf_matrix_mapped,
        'overall_accuracy': overall_accuracy,
        'per_class_accuracy': per_class_accuracy,
        'dw_classes': DW_CLASSES,
        'esa_classes': ESA_CLASSES,
        'class_mapping_used': class_mapping
    }

import numpy as np
import xarray as xr
from pathlib import Path
from typing import List, Dict, Union, Tuple
import matplotlib.pyplot as plt
import seaborn as sns

def compare_multiple_dw_esa(
        dw_datasets: List[Union[str, Path, xr.Dataset]],
        esa_dataset: Union[str, Path, xr.Dataset],
        dw_names: List[str],
        dw_var: str = 'label',
        esa_var: str = 'Map',
        custom_mapping: Dict[int, int] = None,
        title: str = 'Dynamic World vs ESA Comparison',
        figsize: Tuple[int, int] = (8, 6),
        cmap: str = 'YlOrRd'
) -> Dict:
    """
    Compares multiple Dynamic World maps against a single ESA map.

    Parameters
    ----------
    dw_datasets : List[Union[str, Path, xr.Dataset]]
        List of Dynamic World datasets to compare
    esa_dataset : Union[str, Path, xr.Dataset]
        ESA dataset to compare against
    dw_names : List[str]
        Names to identify each DW dataset
    dw_var : str
        Name of the variable in DW datasets
    esa_var : str
        Name of the variable in ESA dataset
    custom_mapping : Dict[int, int], optional
        Custom mapping of ESA -> DW classes
    title : str
        Title for the visualization
    figsize : Tuple[int, int]
        Size of the figure
    cmap : str
        Colormap for the heatmap

    Returns
    -------
    Dict
        Dictionary with accuracy matrix and detailed results per dataset
    """
    if len(dw_datasets) != len(dw_names):
        raise ValueError("Number of datasets must match number of names")

    # Class definitions
    DW_CLASSES = {
        0: 'Water',
        1: 'Trees',
        2: 'Grass',
        3: 'Flooded vegetation',
        4: 'Crops',
        5: 'Shrub & scrub',
        6: 'Built',
        7: 'Bare',
        8: 'Snow & ice'
    }

    ESA_CLASSES = {
        10: 'Tree cover',
        20: 'Shrubland',
        30: 'Grassland',
        40: 'Cropland',
        50: 'Built-up',
        60: 'Bare / sparse vegetation',
        70: 'Snow and ice',
        80: 'Permanent water bodies',
        90: 'Herbaceous wetland',
        95: 'Mangroves',
        100: 'Moss and lichen'
    }

    # Default ESA -> DW mapping
    DEFAULT_MAPPING = {
        10: 1,    # Tree cover -> Trees
        20: 5,    # Shrubland -> Shrub & scrub
        30: 2,    # Grassland -> Grass
        40: 4,    # Cropland -> Crops
        50: 6,    # Built-up -> Built
        60: 7,    # Bare/sparse -> Bare
        70: 8,    # Snow and ice -> Snow & ice
        80: 0,    # Water bodies -> Water
        90: 3,    # Herbaceous wetland -> Flooded vegetation
        95: 3,    # Mangroves -> Flooded vegetation
        100: 2    # Moss and lichen -> Grass
    }

    class_mapping = custom_mapping if custom_mapping is not None else DEFAULT_MAPPING

    # Load datasets
    def load_dataset(ds):
        if isinstance(ds, (str, Path)):
            return xr.open_dataset(ds)
        return ds

    dw_loaded = [load_dataset(ds) for ds in dw_datasets]
    esa_loaded = load_dataset(esa_dataset)

    # Create mapped ESA array
    esa_mapped = esa_loaded[esa_var].values.copy()
    for esa_class, dw_class in class_mapping.items():
        esa_mapped[esa_loaded[esa_var].values == esa_class] = dw_class

    # Initialize results
    n_datasets = len(dw_datasets)
    accuracy_matrix = np.zeros(n_datasets)
    detailed_results = []

    # Calculate accuracies
    for i in range(n_datasets):
        # Verify shapes
        if dw_loaded[i][dw_var].shape != esa_loaded[esa_var].shape:
            raise ValueError(f"Dataset {dw_names[i]} shape {dw_loaded[i][dw_var].shape} "
                             f"doesn't match ESA shape {esa_loaded[esa_var].shape}")

        # Create confusion matrix
        labels = sorted(set(DW_CLASSES.keys()))
        conf_matrix = np.zeros((len(labels), len(labels)), dtype=int)

        for j, label1 in enumerate(labels):
            for k, label2 in enumerate(labels):
                conf_matrix[j, k] = np.sum(
                    (dw_loaded[i][dw_var].values == label1) & (esa_mapped == label2)
                )

        # Calculate metrics
        overall_accuracy = np.sum(np.diag(conf_matrix)) / np.sum(conf_matrix)
        accuracy_matrix[i] = overall_accuracy

        # Calculate per-class accuracy
        per_class_accuracy = {}
        for j, label in enumerate(labels):
            class_sum = np.sum(conf_matrix[j, :])
            if class_sum > 0:
                per_class_accuracy[label] = conf_matrix[j, j] / class_sum

        detailed_results.append({
            'name': dw_names[i],
            'confusion_matrix': conf_matrix,
            'overall_accuracy': overall_accuracy,
            'per_class_accuracy': per_class_accuracy
        })

    # Create visualization
    plt.figure(figsize=figsize)
    sns.barplot(x=dw_names, y=accuracy_matrix)
    plt.title(f'{title}')
    plt.xlabel('Dynamic World Datasets')
    plt.ylabel('Accuracy')
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, 1)
    for i, v in enumerate(accuracy_matrix):
        plt.text(i, v, f'{v:.2%}', ha='center', va='bottom')
    plt.tight_layout()
    plt.show()

    # Print detailed results
    for result in detailed_results:
        print(f"\n=== {result['name']} ===")
        print(f"Overall Accuracy: {result['overall_accuracy']:.2%}")
        print("\nPer-class Accuracy:")
        for label, acc in result['per_class_accuracy'].items():
            print(f"{DW_CLASSES[label]}: {acc:.2%}")

    return {
        'accuracy_matrix': accuracy_matrix,
        'detailed_results': detailed_results,
        'dw_classes': DW_CLASSES,
        'esa_classes': ESA_CLASSES,
        'class_mapping_used': class_mapping
    }



import ee
import geemap
import wxee
import xarray as xr
from typing import Union, Literal, Dict

def initialize_gee(project_id: str, opt_url: str = 'https://earthengine-highvolume.googleapis.com') -> None:
    """Initialize Google Earth Engine with authentication"""
    ee.Authenticate()
    ee.Initialize(project=project_id, opt_url=opt_url)


import ee
from typing import List
import numpy as np
from time import sleep

def chunk_geometry(geometry: ee.Geometry, initial_max_size: int = 15000000, min_chunk_size: int = 1000000) -> List[ee.Geometry]:
    """Split geometry into smaller chunks with adaptive size reduction on memory errors.

    Args:
        geometry: Earth Engine geometry to split
        initial_max_size: Initial maximum chunk size in bytes
        min_chunk_size: Minimum chunk size to try before giving up

    Returns:
        List of geometry chunks

    Raises:
        RuntimeError: If chunking fails even at minimum chunk size
    """
    def try_chunking(max_size: int) -> List[ee.Geometry]:
        bounds = geometry.bounds().getInfo()['coordinates'][0]
        x_min, y_min = bounds[0][0], bounds[0][1]
        x_max, y_max = bounds[2][0], bounds[2][1]

        total_area = abs((x_max - x_min) * (y_max - y_min))
        n_chunks = int(np.ceil(total_area * (50331648 / max_size)))

        n_rows = int(np.ceil(np.sqrt(n_chunks)))
        n_cols = n_rows

        x_steps = np.linspace(x_min, x_max, n_cols + 1)
        y_steps = np.linspace(y_min, y_max, n_rows + 1)

        chunks = []
        for i in range(n_rows):
            for j in range(n_cols):
                chunk = ee.Geometry.Rectangle([
                    x_steps[j], y_steps[i],
                    x_steps[j+1], y_steps[i+1]
                ])
                intersection = chunk.intersection(geometry)
                if intersection.area().getInfo() > 0:
                    chunks.append(intersection)
        return chunks

    current_max_size = initial_max_size
    while current_max_size >= min_chunk_size:
        try:
            return try_chunking(current_max_size)
        except ee.EEException as e:
            if "Total request size" in str(e):
                current_max_size = int(current_max_size * 0.5)  # Reduce chunk size by half
                sleep(1)  # Add small delay to avoid rate limiting
                continue
            raise  # Re-raise if it's a different type of EEException

    raise RuntimeError(f"Failed to chunk geometry even with minimum chunk size of {min_chunk_size} bytes")

def process_worldcover(aoi: ee.Geometry, output_path: str, scale: int = 30) -> None:
    try:
        worldcover = ee.ImageCollection("ESA/WorldCover/v100").first()
        worldcover_clipped = worldcover.clip(aoi)
        ds = worldcover_clipped.wx.to_xarray(region=ee.Feature(aoi).geometry(), scale=scale)

    except ee.ee_exception.EEException as e:
        if "Total request size" in str(e):
            print("Area too large, processing in chunks...")
            chunks = chunk_geometry(aoi)

            worldcover = ee.ImageCollection("ESA/WorldCover/v100").first()
            worldcover_clipped = worldcover.clip(chunks[0])
            ds = worldcover_clipped.wx.to_xarray(region=ee.Feature(chunks[0]).geometry(), scale=scale)

            for i, chunk in enumerate(chunks[1:], 1):
                print(f"Processing chunk {i+1}/{len(chunks)}...")
                worldcover_clipped = worldcover.clip(chunk)
                chunk_ds = worldcover_clipped.wx.to_xarray(
                    region=ee.Feature(chunk).geometry(),
                    scale=scale
                )
                ds = xr.merge([ds, chunk_ds])
        else:
            raise e

    ds = ds.fillna(-1)
    ds = ds.clip(min=-128, max=127)
    ds["Map"] = ds["Map"].astype("int8")
    ds["x"] = ds["x"].astype("float32")
    ds["y"] = ds["y"].astype("float32")

    ds.to_netcdf(output_path)


def chunk_geometry_adaptive(geometry: ee.Geometry, initial_max_size: int = 5000000, min_chunk_size: int = 500000) -> List[ee.Geometry]:
    """Split geometry with aggressive initial chunking and adaptive resizing."""
    def try_chunking(max_size: int) -> List[ee.Geometry]:
        bounds = geometry.bounds().getInfo()['coordinates'][0]
        x_min, y_min = bounds[0][0], bounds[0][1]
        x_max, y_max = bounds[2][0], bounds[2][1]

        total_area = abs((x_max - x_min) * (y_max - y_min))
        n_chunks = int(np.ceil(total_area * (50331648 / max_size)))

        # Use more chunks initially to prevent memory issues
        n_rows = int(np.ceil(np.sqrt(n_chunks * 1.5)))
        n_cols = n_rows

        x_steps = np.linspace(x_min, x_max, n_cols + 1)
        y_steps = np.linspace(y_min, y_max, n_rows + 1)

        chunks = []
        for i in range(n_rows):
            for j in range(n_cols):
                chunk = ee.Geometry.Rectangle([
                    x_steps[j], y_steps[i],
                    x_steps[j+1], y_steps[i+1]
                ])
                intersection = chunk.intersection(geometry)
                if intersection.area().getInfo() > 0:
                    chunks.append(intersection)
        return chunks

    current_max_size = initial_max_size
    last_error = None

    while current_max_size >= min_chunk_size:
        try:
            chunks = try_chunking(current_max_size)
            # Validate first chunk with a small computation
            test_img = ee.Image(1).clip(chunks[0])
            _ = test_img.getDownloadURL({'scale': 10, 'region': chunks[0].getInfo()})
            return chunks
        except ee.EEException as e:
            if "Total request size" in str(e):
                current_max_size = int(current_max_size * 0.4)  # More aggressive reduction
                last_error = e
                sleep(1)
                continue
            raise

    raise RuntimeError(f"Failed to chunk geometry. Last error: {str(last_error)}")

def process_dynamic_world_chunk(
        chunk: ee.Geometry,
        processing_type: str,
        scale: int,
        start_date: str,
        end_date: str,
        retry_count: int = 3
) -> Optional[xr.Dataset]:
    """Process a single chunk with retries."""
    CLASS_NAMES = ['water', 'trees', 'grass', 'flooded_vegetation', 'crops',
                   'shrub_and_scrub', 'built', 'bare', 'snow_and_ice']
    CLASS_NUMBER = ee.List.sequence(0, 8)

    for attempt in range(retry_count):
        try:
            dw_chunk = wxee.TimeSeries("GOOGLE/DYNAMICWORLD/V1") \
                .filterDate(start_date, end_date) \
                .filterBounds(chunk) \
                .map(lambda img: img.clip(chunk))

            if processing_type == 'mode':
                ts = dw_chunk.select("label").aggregate_time("year", ee.Reducer.mode())
            elif processing_type in ['mode_pooled', 'mean_pooled']:
                reducer = ee.Reducer.mode() if processing_type == 'mode_pooled' else ee.Reducer.mean()
                ts = dw_chunk.select("label" if processing_type == 'mode_pooled' else CLASS_NAMES) \
                    .aggregate_time("year", reducer) \
                    .map(lambda img: img.setDefaultProjection('EPSG:4326', None, scale) \
                         .reduceResolution(
                    reducer=reducer,
                    maxPixels=65535,
                    bestEffort=True
                ).reproject(crs='EPSG:4326', scale=scale))
            else:  # mean_unpooled
                ts = dw_chunk.aggregate_time("year", ee.Reducer.mean())
                ts = ts.map(
                    lambda image:
                    image.select(CLASS_NAMES)
                    .reduce(ee.Reducer.max())
                    .eq(image.select(CLASS_NAMES))
                    .multiply(ee.Image.constant(CLASS_NUMBER))
                    .reduce(ee.Reducer.sum())
                    .rename('label')
                    .uint8()
                    .copyProperties(image, ['system:time_start'])
                )

            return ts.wx.to_xarray(region=chunk, scale=scale)

        except ee.EEException as e:
            if attempt < retry_count - 1:
                sleep(2 ** attempt)  # Exponential backoff
                continue
            if "Total request size" in str(e):
                return None  # Signal need for smaller chunks
            raise
    return None

def process_dynamic_world(
        aoi: ee.Geometry,
        processing_type: str,
        output_path: str,
        scale: int = 30,
        start_date: str = "2020-01-01",
        end_date: str = "2021-01-01",
        include_probabilities: bool = False
) -> None:
    """Process each band separately and merge at the end."""

    def process_band(chunk: ee.Geometry, band: str, is_probability: bool) -> Optional[xr.Dataset]:
        for attempt in range(3):
            try:
                dw_chunk = wxee.TimeSeries("GOOGLE/DYNAMICWORLD/V1") \
                    .filterDate(start_date, end_date) \
                    .filterBounds(chunk) \
                    .map(lambda img: img.clip(chunk)) \
                    .select(band)

                # Remove fill values
                dw_chunk = dw_chunk.map(lambda img: img.updateMask(img.neq(-32768)))

                # Always use mean for probabilities, mode for label (only in mode cases)
                reducer = ee.Reducer.mean() if is_probability else ee.Reducer.mode()

                ts = dw_chunk.aggregate_time("year", reducer)
                if processing_type in ['mode_pooled', 'mean_pooled']:
                    ts = ts.map(lambda img: img.setDefaultProjection('EPSG:4326', None, scale)
                                .reduceResolution(
                        reducer=ee.Reducer.mean(),  # Always mean for spatial reduction
                        maxPixels=65535,
                        bestEffort=True
                    ).reproject(crs='EPSG:4326', scale=scale))

                return ts.wx.to_xarray(region=chunk, scale=scale)
            except ee.EEException as e:
                if "Total request size" in str(e) and attempt < 2:
                    sleep(2 ** attempt)
                    continue
                raise
        return None

    try:
        CLASS_NAMES = ['water', 'trees', 'grass', 'flooded_vegetation', 'crops',
                       'shrub_and_scrub', 'built', 'bare', 'snow_and_ice']

        merged_ds = None

        # Only process label for mode-based methods
        if 'mode' in processing_type:
            print("Processing label band")
            try:
                label_ds = process_band(aoi, 'label', is_probability=False)
                merged_ds = label_ds
            except ee.EEException:
                print("Area too large for label, processing in chunks...")
                chunks = chunk_geometry_adaptive(aoi)

                for i, chunk in enumerate(chunks, 1):
                    print(f"Processing chunk {i}/{len(chunks)} for label...")
                    try:
                        chunk_ds = process_band(chunk, 'label', is_probability=False)
                        if chunk_ds is not None:
                            merged_ds = chunk_ds if merged_ds is None else xr.merge([merged_ds, chunk_ds])
                    except Exception as e:
                        print(f"Error processing chunk {i} for label: {str(e)}")
                        continue

        # Process probability bands
        include_probabilities = include_probabilities or 'mean' in processing_type
        if include_probabilities:
            for band in CLASS_NAMES:
                print(f"Processing probability band: {band}")
                try:
                    band_ds = process_band(aoi, band, is_probability=True)
                    merged_ds = xr.merge([merged_ds, band_ds]) if merged_ds is not None else band_ds
                except ee.EEException:
                    print(f"Area too large for {band}, processing in chunks...")
                    chunks = chunk_geometry_adaptive(aoi)

                    for i, chunk in enumerate(chunks, 1):
                        print(f"Processing chunk {i}/{len(chunks)} for {band}...")
                        try:
                            chunk_ds = process_band(chunk, band, is_probability=True)
                            if chunk_ds is not None:
                                merged_ds = xr.merge([merged_ds, chunk_ds])
                        except Exception as e:
                            print(f"Error processing chunk {i} for {band}: {str(e)}")
                            continue

        if merged_ds is None:
            raise RuntimeError("Failed to process any data successfully")

        # Post-processing
        merged_ds = merged_ds.fillna(-1)

        # Calculate label from probability bands for mean-based methods
        if 'mean' in processing_type:
            # Stack all probability bands
            prob_array = np.stack([merged_ds[class_name].values for class_name in CLASS_NAMES], axis=-1)
            # Get argmax along class dimension
            label_array = np.argmax(prob_array, axis=-1)
            # Add label to dataset
            merged_ds['label'] = (('time', 'y', 'x'), label_array)

        merged_ds["label"] = merged_ds["label"].clip(min=-128, max=127).astype("int8")

        if include_probabilities:
            for class_name in CLASS_NAMES:
                if class_name in merged_ds:
                    merged_ds[class_name] = merged_ds[class_name].clip(0, 1).astype("float32")

        merged_ds["x"] = merged_ds["x"].astype("float32")
        merged_ds["y"] = merged_ds["y"].astype("float32")
        merged_ds["time"] = merged_ds["time"].dt.strftime("%Y-%m")

        merged_ds.to_netcdf(output_path)

    except Exception as e:
        print(f"Error during processing: {str(e)}")
        raise

def visualize_areas(areas: Dict[str, ee.Geometry.Polygon],
                    colors: Dict[str, Dict[str, str]] = None) -> geemap.Map:
    """
    Creates a map visualizing study areas with customizable colors

    Args:
        areas: Dictionary of area names and their geometries
        colors: Dictionary of area styling. If None, uses default colors
               Format: {'area_name': {'color': 'hex_color', 'fillColor': 'hex_color_with_alpha'}}
    """
    Map = geemap.Map(center=[-27, -62], zoom=6)

    if colors is None:
        colors = {name: {'color': 'FF0000', 'fillColor': 'FF000088'}
                  for name in areas.keys()}

    for area_name, area in areas.items():
        style = colors.get(area_name, {'color': 'FF0000', 'fillColor': 'FF000088'})
        Map.addLayer(area, style, area_name)

    return Map