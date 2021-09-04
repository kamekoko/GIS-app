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

def xy2ll(inputPath: Path, outputPath: Path):
    json_open = open(inputPath, 'r')
    json_load = json.load(json_open)

    with open(outputPath, 'w') as f:
        ls = []
        features = []

        for elem in json_load['features']:
            newCoordinates = []

            for val in elem['geometry']['coordinates']:
                newCoordinate = []

                if val[0][0] > minLng and val[0][0] < maxLng and val[0][1] > minLat and val[0][1] < maxLat:
                    for lnglat in val:
                        newCoordinate.append(lnglat)

                    newCoordinates.append(newCoordinate)


            if len(newCoordinates) >= 1:
                featureStr = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": newCoordinates
                    },
                    "properties": elem['properties']
                }
                features.insert(len(ls), featureStr)

        featureCollection = {
            "type": "FeatureCollection",
            "features": features
        }
        featureCollection = json.dumps(featureCollection, indent=4, ensure_ascii=False)
        ls.insert(len(ls), featureCollection)

        f.writelines(ls)

def main():
    outputPath = Path(__file__).parent/'../../data/out-forest-7-limited.geojson'
    inputPath = Path(__file__).parent/'../../data/out-forest-7-edited.geojson'
    xy2ll(inputPath, outputPath)

if __name__ == '__main__':
    main()
