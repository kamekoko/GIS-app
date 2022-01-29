'''Processing to GeoDataFrame(input)'''
'''Output is GeoDataFrame too'''

import geopandas as gpd

import gis_processing.geocoding as gis_p_g
import gis_processing.simplify as gis_p_s
import gis_analysis.calc_basic_quantity as cbq
import gis_analysis.select_object as gis_a_so

def processing(conn, processing_name, processing_val, gdf_data_1, gdf_data_2):

    print("Info: start processing <%s>" % (processing_name))

    # preprocessing
    if gdf_data_1 is not None:
        gdf_data_1.geometry = gdf_data_1.geometry.to_crs(4326)
    if gdf_data_2 is not None:
        gdf_data_2.geometry = gdf_data_2.geometry.to_crs(4326)

    # processing
    gdf = None

    # 1 GISデータ処理
    # 1.1 座標系変換
    if processing_name == 'set_crs':
        gdf = gdf_data_1
        gdf.geometry = gdf.geometry.to_crs(processing_val)

    # 1.2 ジオコーディング・逆ジオコーディング
    elif processing_name == 'geocode':
        gdf = gis_p_g.geocode(gdf_data_1)
    elif processing_name == 'reverse_geocode':
        gdf = gis_p_g.reverse_geocode(gdf_data_1)

    # 1.3 解像度・空間構成単位の変換 ：simplification
    elif processing_name == 'simplify':
        gdf = gis_p_s.simplify(gdf_data_1, processing_val)

    # 1.3 解像度・空間構成単位の変換：aggregation (=dissolve)
    elif processing_name == 'dissolve':
        gdf = gdf_data_1.dissolve(by=processing_val['by'], aggfunc=processing_val['aggfunc'])

    # 2 GISデータ分析
    # 2.1 空間解析：基本量の測定
    elif processing_name == 'area' or processing_name == 'length':
        gdf = cbq.calc_bq(gdf_data_1, processing_name)

    # 2.2 空間解析：オブジェクト選択：最近隣データ取得
    elif processing_name == 'nearest':
        gdf = gis_a_so.select_nearest(gdf_data_1, processing_val['lng'], processing_val['lat'])

    # 2.2 空間解析：オーバーレイ
    elif processing_name == 'erase':
        gdf = gdf_data_1.overlay(gdf_data_2, how='difference')
    elif processing_name == 'union':
        gdf = gdf_data_1.overlay(gdf_data_2, how='union')
    elif processing_name == 'intersection':
        gdf = gdf_data_1.overlay(gdf_data_2, how='intersection')
    elif processing_name == 'symmetric_difference':
        gdf = gdf_data_1.overlay(gdf_data_2, how='symmetric_difference')
    elif processing_name == 'difference':
        gdf = gdf_data_1.overlay(gdf_data_2, how='difference')
    elif processing_name == 'identity':
        gdf = gdf_data_1.overlay(gdf_data_2, how='identity')

    # 2.2 空間解析：その他データ操作（clipは gdf_data_1 cliped by gdf_data_2）
    elif processing_name == 'merge':
        gdf = gdf_data_1.append(gdf_data_2)
    elif processing_name == 'clip':
        gdf = gpd.clip(gdf_data_1, gdf_data_2)


    # 2.3 領域分析（バッファリング）
    elif processing_name == 'buffer':
        gdf = gdf_data_1
        gdf.geometry = gdf.geometry.to_crs(3857) #Googlemapなどで採用されているWebメルカトル法の平面直交座標
        gdf.geometry = gdf.geometry.buffer(processing_val['buffer_area'])
        gdf.geometry = gdf.geometry.to_crs(4326)

    elif processing_name == 'contains':
        gdf = gdf_data_1.geometry.contains(gdf_data_2.geometry)

    print("Info: end processing <%s>" % (processing_name))

    return gdf
