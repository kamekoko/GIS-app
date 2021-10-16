import json, pyproj

def transform(path, epsgIn, epsgOut):
    json_open = open(path, 'r')
    json_load = json.load(json_open)
    
    epsgInStr = "epsg:" + str(epsgIn)
    epsgOutStr = "epsg:" + str(epsgOut)

    transformer = pyproj.Transformer.from_crs(epsgInStr, epsgOutStr, always_xy=True)

    features = []
    for elem in json_load['features']:
        newCoordinates = []
        for val in elem['geometry']['coordinates']:
            newCoordinate = []
            for xy in val:
                lng, lat = transformer.transform(xy[0], xy[1])
                newCoordinate.append([lng, lat])
            newCoordinates.append(newCoordinate)
        featureStr = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": newCoordinates
            },
            "properties": elem['properties']
        }
        features.append(featureStr)
    featureCollection = {
        "type": "FeatureCollection",
        "features": features
    }

    return featureCollection
