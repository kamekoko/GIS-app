import osmnx as ox
import geopandas as gpd
from shapely.geometry import LineString, MultiLineString

def getPaths(num, sLat, sLng, eLat, eLng):
		
	bbox = [max(sLat, eLat)+0.01, min(sLat, eLat)-0.01, max(sLng, eLng)+0.01, min(sLng, eLng)-0.01]
	
	G = ox.graph_from_bbox(bbox[0], bbox[1], bbox[2], bbox[3], network_type='drive')
	
	start_node = ox.nearest_nodes(G, sLng, sLat)
	end_node = ox.nearest_nodes(G, eLng, eLat)	
	
	paths = ox.distance.k_shortest_paths(G, start_node, end_node, num)

	nodes, edges = ox.graph_to_gdfs(G)

	pre_lines = []
	for route in paths:
		sub_line = []
		for i in range(0, len(route)-1, 2):
			line = edges.loc[route[i], route[i+1]]['geometry']
			json = gpd.GeoSeries(line).__geo_interface__
			sub_line.append(json)
		pre_lines.append(sub_line)

	features = []
	# for route in paths:
		# route_nodes = nodes.loc[route]
		# route_line = LineString(route_nodes['geometry'].tolist())
		# json = gpd.GeoSeries([route_line]).__geo_interface__

		# newCoordinates = []
		# for coordinate in json['features'][0]['geometry']['coordinates']:
		# 	lng, lat = coordinate[0], coordinate[1]
		# 	newCoordinates.append([lng, lat])

		# route_edges = edges.loc[route]
		# route_line = route_edges['geometry']
		# son = gpd.GeoSeries(route_line).__geo_interface__

		# newCoordinates = []
		# for feature in json['features']:
		# 	for coordinate in feature['geometry']['coordinates']:
		# 		val = [coordinate[0], coordinate[1]]
		# 		newCoordinates.append(val)
	
	for route in pre_lines:
		newCoordinates = []
		for elem in route:
			for coordinate in elem['features'][0]['geometry']['coordinates']:
				newCoordinates.append([coordinate[0], coordinate[1]])
		
		featureStr = {
			"type": "Feature",
			"geometry": {
				"type": "LineString",
				"coordinates": newCoordinates
			},
			"properties": {}
		}
		features.append(featureStr)
	
	featureCollection = {
		"type": "FeatureCollection",
		"features": features
	}

	return featureCollection
