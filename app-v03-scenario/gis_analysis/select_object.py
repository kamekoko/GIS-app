from shapely.geometry import Point
from shapely.ops import transform
import geopandas as gpd
import pyproj
import sys

def get_project():

    wgs84 = pyproj.CRS('EPSG:4326')
    utm = pyproj.CRS('EPSG:3857')

    return pyproj.Transformer.from_crs(wgs84, utm, always_xy=True).transform

def select_nearest(gdf, wgs84_pt_lng, wgs84_pt_lat):
    
    wgs84_pt = Point(wgs84_pt_lng, wgs84_pt_lat)
    project = get_project()
    utm_pt = transform(project, wgs84_pt)
    gdf.geometry = gdf.geometry.to_crs(3857)

    dist_list = gdf.geometry.distance(utm_pt)

    min = sys.float_info.max
    minIndex = 0
    for i in range(len(dist_list)):
        if min > dist_list[i]:
            min = dist_list[i]
            minIndex = i

    length = len(gdf.geometry)
    gdf_r = gdf
    for i in range(length):
        if i == minIndex:
            None
        else:
            gdf_r = gdf_r.drop(i)

    gdf_r.geometry = gdf_r.geometry.to_crs(4326)

    return gdf_r
