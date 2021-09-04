import json
from pathlib import Path

# angle units in degrees
def tky2wgs_approx(lon_tky, lat_tky, degree=2):
    L = lon_tky - 135
    B = lat_tky - 35
    if degree == 1:
        dL = -2.80641517e-3 - 4.98891541e-5*B - 8.33469263e-5*L
        dB =  3.20321021e-3 - 1.15452990e-4*B + 2.47032059e-5*L
    elif degree == 2:
        a00,a01,a02,a03,a04,a05,a10,a11,a12,a13,a14,a15 = -2.79648156e-03, -3.64571151e-05, -1.00958714e-06, -8.83091873e-05, -8.33002662e-07, 3.54561248e-07, 3.19774649e-03, -1.13997082e-04, -7.51313530e-07, 2.34640477e-05, 6.06731757e-07, 3.28340222e-07
        dL = a00+a01*B+a02*B**2+a03*L+a04*B*L+a05*L**2
        dB = a10+a11*B+a12*B**2+a13*L+a14*B*L+a15*L**2
    return lon_tky + dL, lat_tky + dB


def xy2ll(inputPath: Path, outputPath: Path):
    json_open = open(inputPath, 'r')
    json_load = json.load(json_open)

    with open(outputPath, 'w') as f:
        ls = []
        features = []

        for elem in json_load['features']:
            newCoordinates = []

            for lnglat in elem['geometry']['coordinates']:
                lng, lat = tky2wgs_approx(lnglat[0], lnglat[1], )
                newCoordinates.append([lng, lat])

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
    outputPath = Path(__file__).parent/'../../data/out-farmland-converted.geojson'
    inputPath = Path(__file__).parent/'../../data/out-farmland-edited.geojson'
    xy2ll(inputPath, outputPath)

if __name__ == '__main__':
    main()
