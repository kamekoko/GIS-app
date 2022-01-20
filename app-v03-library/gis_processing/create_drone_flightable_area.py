import geopandas as gpd
import json

from gis_processing.connect_db import connect_to_postgis
# from gis_processing.get_data_from_postgis import get_data_by_geopandas
# from gis_processing.create_responce import merge_geojson

def set_features(features, df_json):
    j = json.loads(df_json)
    for i in j['features']:
        features.append(i)

def merge_geojson(df1_geojson, df2_geojson):
    if len(df1_geojson) == 0:
        return df2_geojson
    elif len(df2_geojson) == 0:
        return df1_geojson
    else:
        features = []
        set_features(features, df1_geojson)
        set_features(features, df2_geojson)
        return {"type": "FeatureCollection","features": features}

def get_data_by_geopandas(table_name, con):
    sql = "SELECT geom FROM %s" % (table_name)
    df = gpd.GeoDataFrame.from_postgis(sql, con)
    df = df.to_crs(4326)
    return df

def get_drone_flightable_area(spatial_range):
    '''加賀市の配送ドローン飛行可能空域の導出'''
    # connect to postgis
    con = connect_to_postgis()

    # 森林地域データ（石川）から加賀市部分のみを抽出
    df_gyosei = get_data_by_geopandas("gyousei_kaga", con)
    df_forest = get_data_by_geopandas("forest_kaga", con)
    df_forest_kaga = df_gyosei.overlay(df_forest, how='intersection')
    print("1/5.....Forest.....")

    # 筆ポリゴン
    df_fude = get_data_by_geopandas("fude", con)
    print("2/5.....Fude Polygon.....")

    # flightless area を削除
    df_flightless = get_data_by_geopandas("my_drone_flightless_area", con)
    df_forest_kaga_flightable = df_forest_kaga.overlay(df_flightless, how='difference')
    df_fude_flightable = df_fude.overlay(df_flightless, how='difference')
    print("3/5.....Flightless Area.....")

    # dynamic flightless area を削除
    df_facilities = get_data_by_geopandas("facilities", con)
    df_facilities['geom'] = df_facilities['geom'].to_crs(6675)
    df_facilities['geom'] = df_facilities.geometry.buffer(100)
    df_facilities['geom'] = df_facilities['geom'].to_crs(4326)
    
    df_forest_kaga_flightable_dynamic = df_forest_kaga_flightable.overlay(df_facilities, how='difference')
    df_fude_flightable_dynamic = df_fude_flightable.overlay(df_facilities, how='difference')
    print("4/5.....Dynamic Flightless Area.....")



    # 結合
    r = merge_geojson(df_forest_kaga_flightable_dynamic.to_json(), df_fude_flightable_dynamic.to_json())
    print("5/5.....Merge.....")

    return r
