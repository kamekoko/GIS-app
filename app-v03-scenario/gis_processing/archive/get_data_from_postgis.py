import geopandas as gpd
import json

from gis_processing.connect_db import connect
from gis_processing.create_responce import create_geojson

def get_data(table_name, spatial_range):
	with connect() as conn:
		with conn.cursor() as cur:
			if spatial_range is None:
				query ="SELECT row_to_json(%s), ST_AsGeoJSON(ST_Transform(geom,4326)) FROM %s" % (table_name, table_name)
			else:
				parameter = json.loads(spatial_range)
				if parameter.get('left') is None:
					buffer_area = "SRID=4326;POINT(%s %s)" \
						% (str(parameter['lng']), str(parameter['lat']))
					query = "SELECT row_to_json(%s), ST_AsGeoJSON(ST_Transform(geom,4326)) FROM %s WHERE ST_Intersects(ST_Transform(geom, 4326), ST_Buffer(ST_GeomFromText('%s')::geography,%s,'quad_segs=8'))" \
						% (table_name, table_name, buffer_area, str(parameter['radius']))
				else:
					bbox = "SRID=4326;POLYGON((%s %s,%s %s,%s %s,%s %s,%s %s))" \
						% (str(parameter['left']), str(parameter['bottom']), str(parameter['left']), str(parameter['top']), \
						   str(parameter['right']), str(parameter['top']), str(parameter['right']), str(parameter['bottom']), \
						   str(parameter['left']), str(parameter['bottom']))
					query = "SELECT row_to_json(%s), ST_AsGeoJSON(ST_Transform(geom,4326)) FROM %s WHERE ST_Intersects(ST_Transform(geom, 4326), ST_GeomFromText('%s')::geography)" \
						% (table_name, table_name, bbox)
			cur.execute(query)
			data = cur.fetchall()
			r = create_geojson(data)
	return r

def get_data_by_geopandas(table_name, conn):
    sql = "SELECT geom FROM %s" % (table_name)
    df = gpd.GeoDataFrame.from_postgis(sql, conn)
    r = df.to_crs(4326)
    return r
