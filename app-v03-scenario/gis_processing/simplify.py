import geopandas as gpd

def simplify(gdf, tolerance):
    gdf_r = gdf
    gdf.geometry = gdf.geometry.to_crs(3857)
    gdf_r.geometry = gdf.geometry.simplify(tolerance)
    gdf_r.geometry = gdf_r.geometry.to_crs(4326)

    return gdf_r
