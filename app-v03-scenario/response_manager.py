from strage_info.get_data_info import get_data_info
from postgresql_operation.connect import connect_to_postgis
from postgresql_operation.get_data import get_data_from_postgis
from processing import processing
import geopandas as gpd
import json

def create_response(processes):

    for i in range(len(processes)):
        processes[i] = json.loads(processes[i])

    conn = connect_to_postgis()

    # process
    output_gdf = []
    for process in processes:
        input_gdf_set = [None, None]
        for i, data_name in enumerate(process['data']):
            if type(data_name) is int:
                input_gdf_set[i] = output_gdf[data_name - 1]
            else:
                data_info = get_data_info(data_name)
                if data_info == None:
                    return {"request error": "No such data", "data name": data_name}
                else:
                    search_option = process['search_option'][i] if 'search_option' in process else None
                    input_gdf_set[i] = get_data_from_postgis(conn, data_info['data_tablename'], search_option)

        if 'processing' in process:
            processing_val = process['processing_val'] if 'processing_val' in process else None
            gdf = processing(conn, process['processing'], processing_val, input_gdf_set[0], input_gdf_set[1])
        else:
            gdf = input_gdf_set[0]

        output_gdf.append(gdf)

    response = json.loads(output_gdf[len(output_gdf) - 1].to_json())

    return response
