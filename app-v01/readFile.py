import readShp as rs
import readGeojson as rg

def read_shp(path):
    return rs.zipped_shp_to_geojson(path)

def read_geojson(path):
    return rg.read_geojson(path)
