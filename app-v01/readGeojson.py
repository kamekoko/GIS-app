import json

def read_geojson(path):
    json_open = open(inputPath, 'r')
    json_load = json.load(json_open)
    return json_load
