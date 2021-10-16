import xmltodict, json

o = xmltodict.parse("../data/FG-GML-543613-AdmArea-20191001-0001.xml")

json_dumps = json.dumps(o)

print(json_dumps)
