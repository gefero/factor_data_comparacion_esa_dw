import ee
import geemap
import wxee
import xarray as xr
from typing import Union, Literal, Dict

def get_study_areas() -> Dict[str, ee.Geometry.Polygon]:
    """Returns dictionary of predefined study areas"""
    areas = {
        'border_area': ee.Geometry.Polygon([
            [[-63.099021, -26.015639],
             [-63.099021, -25.632434],
             [-62.715816, -25.632434],
             [-62.715816, -26.015639]]
        ]),
        'parana_delta': ee.Geometry.Polygon([
            [[-59.29, -33.65],
             [-59.29, -33.95],
             [-59.01, -33.95],
             [-59.01, -33.65]]
        ])
    }
    return areas