from db_connect import connect as cn
from gis_processing import get_data as gd
import json

def merge_test():
    conn = cn.connect_to_postgis()

    df_refuge = gd.get_data_by_geopandas("refuge", conn)
    df_bus_stop = gd.get_data_by_geopandas("bus_stop", conn)
    df_joined = df_refuge.append(df_bus_stop)

    return json.loads(df_joined.to_json())

def merge(df_1, df_2): #get_dataは別で実行，ここではGeoDataFrameに対する処理を行う方がいい
    df_joined = df_1.append(df_2)
    return json.loads(df_joined.to_json())
