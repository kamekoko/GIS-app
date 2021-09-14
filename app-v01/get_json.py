import json
from pathlib import Path

def get_json(path):
    inputPath = Path(__file__).parent/path
    json_open = open(inputPath, 'r')
    json_load = json.load(json_open)
    return json_load
