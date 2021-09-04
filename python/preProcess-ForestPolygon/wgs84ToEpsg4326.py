import json
from pathlib import Path

def cnvWGS84ToTokyo(lng,lat):
    latAns = lat + lat*0.00010696 - lng*0.000017467 - 0.0046020
    lngAns = lng + lat*0.000046047 + lng*0.000083049 - 0.010041
    return lngAns, latAns


def wgs84ToEpsg4326(inputPath: Path, outputPath: Path):
    json_open = open(inputPath, 'r')
    json_load = json.load(json_open)

    with open(outputPath, 'w') as f:
        ls = []

        for obj in json_load:
            features = []

            for elem in obj['features']:
                newCoordinates = []

                for val in elem['geometry']['coordinates']:
                    newCoordinate = []

                    for lnglat in val:
                        if type(lnglat[0]) == type([1, 2]):

                            for lnglat2 in lnglat:
                                lng, lat = cnvWGS84ToTokyo(lnglat2[0], lnglat2[1])
                                newCoordinate.append([lng, lat])
                        else:
                            lng, lat = cnvWGS84ToTokyo(lnglat[0], lnglat[1])
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
                features.insert(len(ls), featureStr)

            featureCollection = {
                "type": "FeatureCollection",
                "features": features
            }
            featureCollection = json.dumps(featureCollection, indent=4, ensure_ascii=False)
            ls.insert(len(ls), featureCollection)

        f.writelines(ls)

def main():
    outputPath = Path(__file__).parent/'../../data/out-forest-7-edited.geojson'
    inputPath = Path(__file__).parent/'../../data/out-forest-7.geojson'
    wgs84ToEpsg4326(inputPath, outputPath)

if __name__ == '__main__':
    main()
