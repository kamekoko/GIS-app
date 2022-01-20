from sqlalchemy import *
import geopandas as gpd
import json

def edit_sql_by_time_range(sql, time_range_param, column_name_list, isFirstWhere):

    if 'existence' in column_name_list:
        if isFirstWhere is True:
            sql = sql + " WHERE"
        else:
            sql = sql + " AND"
        sql = sql + " existence=1"

    return sql

def get_data_from_postgis(conn, table_name, spatial_range, time_range, attribute):

    # default
    sql = "SELECT * FROM %s" % (table_name)

    isFirstWhere = True

    # data requirements
    if spatial_range is None:
        None
    else:
        isFirstWhere = False
        param = json.loads(spatial_range)
        if param.get('left') is None:
            #spatial_range is circle
            buffer_area = "SRID=4326;POINT(%s %s)" \
                % (str(param['lng']), str(param['lat']))
            sql = sql + " WHERE ST_Intersects(ST_Transform(geom, 4326), ST_Buffer(ST_GeomFromText('%s')::geography,%s,'quad_segs=8'))" \
                % (buffer_area, str(param['radius']))
        else:
            #spatial_range is bbox
            bbox = "SRID=4326;POLYGON((%s %s,%s %s,%s %s,%s %s,%s %s))" \
                % (str(param['left']), str(param['bottom']), str(param['left']), str(param['top']), \
                   str(param['right']), str(param['top']), str(param['right']), str(param['bottom']), \
                   str(param['left']), str(param['bottom']))
            sql = sql + " WHERE ST_Intersects(ST_Transform(geom, 4326), ST_GeomFromText('%s')::geography)" \
                % (bbox)

    if time_range is None:
        None
    else:
        time_range_param = json.loads(time_range)
        column_name_list = Table(table_name, MetaData(), autoload_with=conn).c.keys()
        sql = edit_sql_by_time_range(sql, time_range_param, column_name_list, isFirstWhere)

    if attribute is None:
        None
    else:
        None # work...

    # run sql
    gdf = gpd.GeoDataFrame.from_postgis(sql, conn)
    if gdf.crs is None:
        print("Data from postgresql is not have crs")
        sql2 = "SELECT ST_SRID(geom) FROM %s LIMIT 1" % (table_name)
        crs_val = conn.execute(sql2).fetchone()[0]
        gdf = gdf.set_crs("epsg:%s" % (crs_val))
        print("crs check (by sql) ... %s" % (crs_val))
    gdf.geometry = gdf.geometry.to_crs(4326)

    return gdf
