import json

def create_geojson(data):
    if len(data) == 0:
        return {"data": None}
    else:
        features = []
        for i in range(len(data)):
            for j in range(len(data[i])):
                if type(data[i][j]) == dict: # row_to_json
                    properties = {}
                    for elem in data[i][j]:
                        if elem == 'geom':
                            None
                        else:
                            properties[elem] = data[i][j][elem]
                else: # translated geometry
                    geometry = json.loads(data[i][j])

            feature = {'type': 'Feature', 'geometry': geometry, 'properties': properties}
            features.append(feature)

        return {"type": "FeatureCollection","features": features}

def set_features(features, df_json):
    j = json.loads(df_json)
    for i in j['features']:
        features.append(i)

def merge_geojson(df1_geojson, df2_geojson):
    if len(df1_geojson) == 0:
        return df2_geojson
    elif len(df2_geojson) == 0:
        return df1_geojson
    else:
        features = []
        set_features(features, df1_geojson)
        set_features(features, df2_geojson)
        return {"type": "FeatureCollection","features": features}
