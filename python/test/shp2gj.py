import shapefile
import zipfile
# from pathlib import Path
from json import dumps

def shp2gj():
    reader = shapefile.Reader('farmland-komatsu.shp')
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", \
         geometry=geom, properties=atr))

    geojson = open("pyshp-demo.json", "w")
    geojson.write(dumps({"type": "FeatureCollection",\
     "features": buffer}, indent=2) + "\n")
    geojson.close()

def main():
    # path = '../../data/input/farmland-komatsu.shp'
    shp2gj()

if __name__ == '__main__':
    main()
