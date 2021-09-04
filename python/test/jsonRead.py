import json

json_open = open('./test-data.json', 'r')
json_load = json.load(json_open)

print(json_load)
