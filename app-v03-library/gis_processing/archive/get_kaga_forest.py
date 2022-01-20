import psycopg2
import json

from gis_processing import connect_db as cd

def create_kaga_forest_responce(data):
    features = []
    for i in range(len(data)):
        for j in range(len(data[i])):
            geometry = json.loads(data[i][j])
            feature = {'type': 'Feature', 'geometry': geometry, 'properties': {}}
            features.append(feature)
    return {"type": "FeatureCollection","features": features}

def get_kaga_forest():
    with cd.connect() as conn:
        with conn.cursor() as cur:
            query = "SELECT ST_AsGeoJSON(ST_Transform(a.geom,4326)) FROM %s a, %s b WHERE ST_Intersects(ST_Transform(a.geom, 4326), ST_Transform(b.geom, 4326))" % ('forest', 'gyousei_kaga')
            cur.execute(query)
            data = cur.fetchall()
            # r = create_responce(data)
            r = create_kaga_forest_responce(data)

    return r
