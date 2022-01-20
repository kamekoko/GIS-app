import psycopg2

from gis_processing.connect_db import connect

def get_area_size(table_name):
	with connect() as conn:
		with conn.cursor() as cur:
			query_str = "SELECT ST_Area(geom) FROM %s" % (table_name)
			cur.execute(query_str)
			sum = 0
			data = cur.fetchall()
			for row in data:
				sum = sum + row[0]
			r = {
				"source": table_name,
				"unit": "m^2",
				"data": data,
				"sum": sum
			}

	return r
