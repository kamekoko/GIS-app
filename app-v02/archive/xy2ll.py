import json
from pathlib import Path
import numpy as np

origins = [
    [36.0, 137.166666666666667]
]

def calc_lat_lon(x, y, phi0_deg, lambda0_deg):
    """ 平面直角座標を緯度経度に変換する
    - input:
        (x, y): 変換したいx, y座標[m]
        (phi0_deg, lambda0_deg): 平面直角座標系原点の緯度・経度[度]（分・秒でなく小数であることに注意）
    - output:
        latitude:  緯度[度]
        longitude: 経度[度]
        * 小数点以下は分・秒ではないことに注意
    """
    # 平面直角座標系原点をラジアンに直す
    phi0_rad = np.deg2rad(phi0_deg)
    lambda0_rad = np.deg2rad(lambda0_deg)

    # 補助関数
    def A_array(n):
        A0 = 1 + (n**2)/4. + (n**4)/64.
        A1 = -     (3./2)*( n - (n**3)/8. - (n**5)/64. )
        A2 =     (15./16)*( n**2 - (n**4)/4. )
        A3 = -   (35./48)*( n**3 - (5./16)*(n**5) )
        A4 =   (315./512)*( n**4 )
        A5 = -(693./1280)*( n**5 )
        return np.array([A0, A1, A2, A3, A4, A5])

    def beta_array(n):
        b0 = np.nan # dummy
        b1 = (1./2)*n - (2./3)*(n**2) + (37./96)*(n**3) - (1./360)*(n**4) - (81./512)*(n**5)
        b2 = (1./48)*(n**2) + (1./15)*(n**3) - (437./1440)*(n**4) + (46./105)*(n**5)
        b3 = (17./480)*(n**3) - (37./840)*(n**4) - (209./4480)*(n**5)
        b4 = (4397./161280)*(n**4) - (11./504)*(n**5)
        b5 = (4583./161280)*(n**5)
        return np.array([b0, b1, b2, b3, b4, b5])

    def delta_array(n):
        d0 = np.nan # dummy
        d1 = 2.*n - (2./3)*(n**2) - 2.*(n**3) + (116./45)*(n**4) + (26./45)*(n**5) - (2854./675)*(n**6)
        d2 = (7./3)*(n**2) - (8./5)*(n**3) - (227./45)*(n**4) + (2704./315)*(n**5) + (2323./945)*(n**6)
        d3 = (56./15)*(n**3) - (136./35)*(n**4) - (1262./105)*(n**5) + (73814./2835)*(n**6)
        d4 = (4279./630)*(n**4) - (332./35)*(n**5) - (399572./14175)*(n**6)
        d5 = (4174./315)*(n**5) - (144838./6237)*(n**6)
        d6 = (601676./22275)*(n**6)
        return np.array([d0, d1, d2, d3, d4, d5, d6])

    # 定数 (a, F: 世界測地系-測地基準系1980（GRS80）楕円体)
    m0 = 0.9999
    a = 6378137.
    F = 298.257222101

    # (1) n, A_i, beta_i, delta_iの計算
    n = 1. / (2*F - 1)
    A_array = A_array(n)
    beta_array = beta_array(n)
    delta_array = delta_array(n)

    # (2), S, Aの計算
    A_ = ( (m0*a)/(1.+n) )*A_array[0]
    S_ = ( (m0*a)/(1.+n) )*( A_array[0]*phi0_rad + np.dot(A_array[1:], np.sin(2*phi0_rad*np.arange(1,6))) )

    # (3) xi, etaの計算
    xi = (x + S_) / A_
    eta = y / A_

    # (4) xi', eta'の計算
    xi2 = xi - np.sum(np.multiply(beta_array[1:],
                                  np.multiply(np.sin(2*xi*np.arange(1,6)),
                                              np.cosh(2*eta*np.arange(1,6)))))
    eta2 = eta - np.sum(np.multiply(beta_array[1:],
                                   np.multiply(np.cos(2*xi*np.arange(1,6)),
                                               np.sinh(2*eta*np.arange(1,6)))))

    # (5) chiの計算
    chi = np.arcsin( np.sin(xi2)/np.cosh(eta2) ) # [rad]
    latitude = chi + np.dot(delta_array[1:], np.sin(2*chi*np.arange(1, 7))) # [rad]

    # (6) 緯度(latitude), 経度(longitude)の計算
    longitude = lambda0_rad + np.arctan( np.sinh(eta2)/np.cos(xi2) ) # [rad]

    # ラジアンを度になおしてreturn
    return np.rad2deg(latitude), np.rad2deg(longitude) # [deg]

def xy2ll(inputPath: Path):
    json_open = open(inputPath, 'r')
    json_load = json.load(json_open)

    ls = []

    for obj in json_load:
        features = []

        for elem in obj['features']:
            newCoordinates = []

            for val in elem['geometry']['coordinates']:
                newCoordinate = []

                for xy in val:
                    lat, lng = calc_lat_lon(xy[1], xy[0], origins[0][0], origins[0][1])
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

    return ls[0]
