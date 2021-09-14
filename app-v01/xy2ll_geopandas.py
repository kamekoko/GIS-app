import geopandas as gpd

def readGeojsonByGeopandas(path):
    gdf_test = gpd.read_file(path, encoding='cp932')

    # 変換後の座標系指定（平面直角座標13系(EPSG2455) → 緯度経度(EPSG4612)）
    dst_proj = 4612 # 変換後の座標系を指定

    # 座標変換
    gdf_test_transfer = gdf_test.to_crs(epsg=dst_proj)  # 変換式を作成

    ls = []
    for (i1, row1), (i2, row2) in zip(gdf_test.iterrows(), gdf_test_transfer.iterrows()):
        print(f'変換前ポリゴン位置 {row1["geometry"]}')  # 位置情報（座標変換前）
        print(f'変換後ポリゴン位置 {row2["geometry"]}')  # 位置情報（座標変換後）
        ls.append(row2["geometry"])

    return ls

def readShpByGeopandas(path):
    gdf_data = gpd.read_file(path, encoding='cp932')
    return gdf_data
