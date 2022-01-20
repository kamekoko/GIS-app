import json
import geopandas as gpd

from strage_info.get_data_info import get_data_info
from postgresql_operation.get_data import get_data_from_postgis
from postgresql_operation.connect import connect_to_postgis
from processing import processing

def create_response(data_name, spatial_range, time_range, attribute, processing_name):

    data_info = get_data_info(data_name)
    conn = connect_to_postgis()
    df_data = get_data_from_postgis(conn, data_info['data_tablename'], spatial_range, time_range, attribute)
    response = json.loads(df_data.to_json())

    return response


def create_response_with_processing(data_creation_process, spatial_range, time_range, attribute):

    # data shape
    for i in range(len(data_creation_process)):
        data_creation_process[i] = json.loads(data_creation_process[i])

    conn = connect_to_postgis()

    # process...
    pre_output_df = None
    for process in data_creation_process:
        input_df_set = [None, None]
        for i, data_name in enumerate(process['data_name']):
            data_info = get_data_info(data_name)
            if data_info['data_name'] == 'output':
                input_df_set[i] = pre_output_df
            else:
                input_df_set[i] = get_data_from_postgis(conn, data_info['data_tablename'], spatial_range, time_range, attribute)

        processing_val = process['processing_val'] if 'processing_val' in process else None
        print(processing_val)
        df = processing(conn, process['processing_name'], processing_val, input_df_set[0], input_df_set[1])
        pre_output_df = df

    response = json.loads(df.to_json())

    return response
