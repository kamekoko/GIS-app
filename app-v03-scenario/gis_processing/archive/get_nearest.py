import os
import psycopg2
from shapely import wkb
import re
import geopandas as gpd

def get_connection(db_name):
	dsn = "dbname=" + db_name + " user=kosukekameda host=localhost password=test"
	return psycopg2.connect(dsn)

def get_nearest_data(num, point_data):
	
	featureCol = []
	with get_connection("geomdb") as conn:
		with conn.cursor() as cur:
			queryStr = "SELECT name, geom FROM test ORDER BY ST_Distance(geom, ST_GeomFromText('POINT(" + str(point_data[0]) + " " + str(point_data[1]) + ")')) LIMIT " + str(num)
			cur.execute(queryStr)
			geom = cur.fetchall()
			for elem in geom:
				text = wkb.loads(elem[1], hex=True)
				json = gpd.GeoSeries([text]).__geo_interface__
				json['features'][0]['properties']['name'] = elem[0]
				featureCol.append(json)

	features = []
	count = 0
	for elem in featureCol:
		elem['features'][0]['id'] = str(count)
		features.append(elem['features'][0])
		count = count + 1

	featureCollection = {
		"type": "FeatureCollection",
		"features": features	
	}

	return featureCollection

def get_nearest_refuge(num, point):
	featureCol = []
	with get_connection("pointdb") as conn:
		with conn.cursor() as cur:
			queryStr = "SELECT * FROM wellpoints ORDER BY ST_Distance(geometry, ST_GeomFromText('POINT(" + str(point[0]) + " " + str(point[1]) + ")', 4326)) LIMIT " + str(num)
			cur.execute(queryStr)
			geom = cur.fetchall()
			colnames = [col.name for col in cur.description]
			for elem in geom:
				count = 0
				properties = {}
				for val in elem:
					if colnames[count] != 'geometry':
						properties[colnames[count]] = val
						count = count + 1
					else:
						text = wkb.loads(val, hex=True)
						json = gpd.GeoSeries([text]).__geo_interface__
				json['features'][0]['properties'] = properties
				json['features'][0]['geometry']['coordinates'] = list(json['features'][0]['geometry']['coordinates'])
				featureCol.append(json)
	
	features = []
	count = 0
	for elem in featureCol:
		elem['features'][0]['id'] = str(count)
		features.append(elem['features'][0])
		count = count + 1

	featureCollection = {
		"type": "FeatureCollection",
		"features": features
	}

	return featureCollection
