import json
from pathlib import Path

start = [36.39326604089627, 136.52501053249725];
end = [36.37429836513503, 136.52831501381425];

minLng = min([start[0], end[0]]) - 0.03;
maxLng = max([start[0], end[0]]) + 0.03;
minLat = min([start[1], end[1]]) - 0.03;
maxLat = max([start[1], end[1]]) + 0.03;

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

        count = 0

        for elem in json_load['features']:
            newCoordinates = []
            count = count + 1

            for lnglat in elem['geometry']['coordinates']:
                if count < 2:
                    print(lnglat)
                # if lnglat[0] > minLng and lnglat[0] < maxLng and lnglat[1] > minLat and lnglat[1] < maxLat:
                    newCoordinates.append(lnglat)

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
    outputPath = Path(__file__).parent/'../../data/out-farmland-limited.geojson'
    inputPath = Path(__file__).parent/'../../data/out-farmland-converted.geojson'
    xy2ll(inputPath, outputPath)

if __name__ == '__main__':
    main()
