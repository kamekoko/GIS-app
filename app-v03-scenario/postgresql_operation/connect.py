from sqlalchemy import create_engine, exc
from postgresql_operation.config import config

def connect_to_postgis():
    """ Connect to the PostgreSQL database server by sqlalchemy """

    conn = None
    try:
        params = config() # section='postgresql'
        print('Connecting to the PostgreSQL database...')
        db_connection_url = "postgresql://%s:%s@%s:5432/%s" \
            % (params['user'], params['password'], params['host'], params['database'])
        conn = create_engine(db_connection_url)
    except:
        raise exc.DisconnectionError()

    return conn
