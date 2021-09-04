import shapefile, io, zipfile, json
from pathlib import Path

def find_shpfile_inzip(zipped_shp):
    zip_infolist = zipped_shp.infolist()
    for info in zip_infolist:
        if not info.filename.startswith('__MACOSX/'):
            if info.filename.endswith('.shp'):
                return info.filename

def zipped_shp_to_geojson(zipped_shp):
    CODECS = ['utf-8', 'shift_jis']
    zipped_files = zipfile.ZipFile(zipped_shp)

    shp_name = find_shpfile_inzip(zipped_files)[:-4]

    try:
        shp_file_bytes = zipped_files.read(shp_name + '.shp')
        shx_file_bytes = zipped_files.read(shp_name + '.shx')
        dbf_file_bytes = zipped_files.read(shp_name + '.dbf')
    except:
        print("Imported file was not apropriate Shape-Zip-File.")
        return None

    geojson = dict(type="FeatureCollection", features=[])

    for codec in CODECS:
        try:
            reader = shapefile.Reader(shp=io.BytesIO(shp_file_bytes),
                                        shx = io.BytesIO(shx_file_bytes),
                                        dbf = io.BytesIO(dbf_file_bytes),
                                        encoding=codec)
            fields = reader.fields[1:]
            field_names = [field[0] for field in fields]
            for sr in reader.shapeRecords():
                atr = dict(zip(field_names, sr.record))
                geom = sr.shape.__geo_interface__
                geojson['features'].append(dict(type="Feature", \
                 geometry=geom, properties=atr))
            print(codec + ' encoding is correct.')
            break
        except UnicodeDecodeError:
            print(codec + ' is not suitable for this file.')
            continue
    return geojson

def json_make(path: Path, obj: dict) -> None:
    ls = None
    with open(path, 'r+') as f:
        ls = f.readlines()
        if ls == []:
            ls.append('[\n')
        if ls[-1] == ']':
            ls[-1] = ','
        ls.insert(len(ls), f'{json.dumps(obj, ensure_ascii=False)}')
        ls.insert(len(ls), '\n]')
    with open(path, 'w') as f:
        f.writelines(ls)

def main():
    path = Path(__file__).parent/'../../data/out-forest-9.geojson'
    geojson = zipped_shp_to_geojson(Path(__file__).parent/'../../data/A13-15_17_GML_9.zip')
    json_make(path, geojson)

if __name__ == '__main__':
    main()
