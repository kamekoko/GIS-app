import json
from pathlib import Path

start = [36.39326604089627, 136.52501053249725];
end = [36.37429836513503, 136.52831501381425];

minLat = min([start[0], end[0]]) - 0.01;
maxLat = max([start[0], end[0]]) + 0.03;
minLng = min([start[1], end[1]]) - 0.03;
maxLng = max([start[1], end[1]]) + 0.03;

bbox = [
  [minLng, maxLng],
  [minLat, maxLat]
];

def integrate(farmlandPath: Path, forestPath: Path, outputPath: Path):
    json_open_farmland = open(farmlandPath, 'r')
    json_load_farmland = json.load(json_open_farmland)

    json_open_forest = open(forestPath, 'r')
    json_load_forest = json.load(json_open_forest)

    ls = []
    integratedFeatures = []

    multiPoint = {
        "type": "Feature",
        "properties": { },
        "geometry": {
        "type": "MultiPoint",
        "coordinates": [start, end]
    }}
    integratedFeatures.append(multiPoint)

    for elem in json_load_farmland['features']:
        integratedFeatures.append(elem)

    for elem in json_load_forest['features']:
        integratedFeatures.append(elem)

    featureCollection = {
        "type": "FeatureCollection",
        "features": integratedFeatures
    }
    featureCollection = json.dumps(featureCollection, indent=4, ensure_ascii=False)
    ls.insert(len(ls), featureCollection)

    with open(outputPath, 'w') as f:
        f.writelines(ls)

def main():
    farmlandPath = Path(__file__).parent/'../../data/out-farmland-limited.geojson'
    forestPath = Path(__file__).parent/'../../data/out-forest-7-limited.geojson'
    outputPath = Path(__file__).parent/'../../data/out-farmland-forest-integrated.geojson'
    integrate(farmlandPath, forestPath, outputPath)

if __name__ == '__main__':
    main()
