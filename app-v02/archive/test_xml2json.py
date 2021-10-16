import xml.etree.ElementTree as ET
import json

tree = ET.parse('../data/FG-GML-543613-AdmArea-20191001-0001.xml')
root = tree.getroot()

coordinatesStr = root[3][5][0][0][0][0][0][0][0][0][0][0].text

coordinatesStrSpl = coordinatesStr.split()

count = 1
lat = 0
lng = 0

print(len(coordinatesStrSpl))

for val in coordinatesStrSpl:
    if count % 2 == 1:
        lat = float(val)
    else:
        lng = float(val)
        print(lat, lng)
    count = count + 1

