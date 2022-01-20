''' geocoding =>  https://github.com/SaitoTsutomu/simple-geocoding ※__init__.py add getCalc() <= return tuple of answer '''
''' reverse_geocode => https://github.com/richardpenman/reverse_geocode/ '''

from shapely.geometry import Point
import geopandas as gpd
import simple_geocoding as sg
import reverse_geocode as rg

def geocode(gdf):
    ''' Address (str) data only '''

    if type(gdf['geom']) is str:
        gdf['geom'] = sg.getCalc(gdf['geom'])
    else :
        None # 本当はエラー処理（Geoseries型の空間情報にジオコーディング（住所→coordinate）しようとしています．的な）

    return gdf

def reverse_geocode(gdf):
    ''' Point (Shapely Point) only '''

    if gdf.geometry.crs != 4326:
        gdf.geometry.to_crs(4326)
    else:
        None
    if type(gdf['geom']) is gpd.geoseries.GeoSeries:
        gdf['address'] = None
        for i in range(len(gdf['geom'])):
            point = gdf['geom'][i]
            coordinates = tuple([Point(point).coords[0][1], Point(point).coords[0][0]]),
            gdf.loc[i, 'address'] = str(rg.search(coordinates)[0])
    else:
        None # 本当はエラー処理（Point型以外の空間情報に逆ジオコーディング（coordinate→住所）しようとしています．的な）

    return gdf
