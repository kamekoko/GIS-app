''' Calclation geometry area or length '''
''' area => https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoSeries.area.html '''
''' length => https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoSeries.length.html '''

import geopandas as gpd

def calc_bq(gdf_data, bq_name):
    gdf = gdf_data
    gdf.geometry = gdf.geometry.to_crs(3857)

    if bq_name == 'area':
        bq = gdf.geometry.area
        for i in range(len(gdf.geometry)):
            gdf.loc[i, 'area'] = bq[i]
    else:
        bq = gdf.geometry.length
        for i in range(len(gdf.geometry)):
            gdf.loc[i, 'length'] = bq[i]

    gdf.geometry = gdf.geometry.to_crs(4326)

    return gdf
