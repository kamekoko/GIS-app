import psycopg2
import json
from sqlalchemy import create_engine

from gis_processing.config import config

def connect():
	""" Connect to the PostgreSQL database server by psycopg2 """

	conn = None
	try:
		params = config()
		print('Connecting to the PostgreSQL database...')
		conn = psycopg2.connect(**params)
		return conn
	except (Exception, psycopg2.DatabaseError) as error:
		return error


def connect_to_postgis():
	""" Connect to the PostgreSQL database server by sqlalchemy """

	params = config()
	db_connection_url = "postgresql://%s:%s@%s:5432/%s" \
		% (params['user'], params['password'], params['host'], params['database'])
	print('Connecting to the PostgreSQL database...')
	return create_engine(db_connection_url)
