from sqlalchemy import *
import geopandas as gpd
import json

def edit_sql_by_spatial_range(sql, spatial_range):

    if spatial_range is None:
        return False
    else:
        if spatial_range.get('left') is None:
            # circle spatial range
            buffer_area = "SRID=4326;POINT(%s %s)" \
                % (str(spatial_range['lng']), str(spatial_range['lat']))
            sql[0] = sql[0] + " WHERE ST_Intersects(ST_Transform(geom, 4326), ST_Buffer(ST_GeomFromText('%s')::geography,%s,'quad_segs=8'))" \
                % (buffer_area, str(spatial_range['radius']))
        else:
            # bbox spatial range
            bbox = "SRID=4326;POLYGON((%s %s,%s %s,%s %s,%s %s,%s %s))" \
                % (str(spatial_range['left']), str(spatial_range['bottom']), str(spatial_range['left']), str(spatial_range['top']), \
                   str(spatial_range['right']), str(spatial_range['top']), str(spatial_range['right']), str(spatial_range['bottom']), \
                   str(spatial_range['left']), str(spatial_range['bottom']))
            sql[0] = sql[0] + " WHERE ST_Intersects(ST_Transform(geom, 4326), ST_GeomFromText('%s')::geography)" \
                % (bbox)

    return True

def edit_sql_by_time_range(sql, time_range, isFirstWhereSyntax):

    if time_range is None:
        return False
    else:
        if isFirstWhereSyntax is True:
            sql[0] = sql[0] + " WHERE"
        else:
            sql[0] = sql[0] + " AND"

        sql[0] = sql[0] + (" timestamp BETWEEN '%s' AND '%s'" % (time_range['start_at'], time_range['end_at']))

    return True

def edit_sql_by_attribute(sql, attribute, isFirstWhereSyntax):

    if attribute is None:
        return False
    else:
        for key in attribute.keys():
            if isFirstWhereSyntax is True:
                sql[0] = sql[0] + " WHERE"
                isFirstWhere = False
            else:
                sql[0] = sql[0] + " AND"

            sql[0] = sql[0] + (" %s = '%s'" % (key, attribute[key]))

    return True

def get_data_from_postgis(conn, table_name, search_option):

    # default sql
    sql = ["SELECT * FROM %s" % (table_name)] # ※参照渡ししたいからmutableな型のリストにしてる

    # edit sql by search option
    if search_option is None:
        None
    else:
        spatial_range = search_option['spatial_range'] if 'spatial_range' in search_option else None
        time_range = search_option['time_range'] if 'time_range' in search_option else None
        attribute = search_option['attribute'] if 'attribute' in search_option else None

        isFirstWhereSyntax = False if edit_sql_by_spatial_range(sql, spatial_range) else True
        isFirstWhereSyntax = False if edit_sql_by_time_range(sql, time_range, isFirstWhereSyntax) else isFirstWhereSyntax
        edit_sql_by_attribute(sql, attribute, isFirstWhereSyntax)

    # run sql
    print("Info: get data [SQL: %s]" % (sql[0]))
    gdf = gpd.GeoDataFrame.from_postgis(sql[0], conn)

    # crs check
    if gdf.crs is None:
        # print("Info: get data [Data from postgresql is not have crs]")
        sql2 = "SELECT ST_SRID(geom) FROM %s LIMIT 1" % (table_name)
        crs_val = conn.execute(sql2).fetchone()[0]
        gdf = gdf.set_crs("epsg:%s" % (crs_val))
        # print("Info: get data [crs check (by sql) ... %s]" % (crs_val))
    else:
        None

    gdf.geometry = gdf.geometry.to_crs(4326) #geojsonで返すので，どうしても地理座標系にする必要がある．元データを変更することになるけど．

    # if "Multi" in gdf.geom_type[0]: # multipolygonなどがなぜかclipできない．geojsonに変換できないのかも．
    #     gdf = gdf.explode(index_parts=False, ignore_index=True)
    #     # gdf['geom'] = gdf.geometry
    # else:
    #     None

    print("Info: get data <%s> complete" % (table_name))

    return gdf
