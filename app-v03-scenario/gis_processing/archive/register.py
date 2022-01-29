# def register(name_str, owner_str, application_field, geojson):
# 	with get_connection("geomdb") as conn:
# 		with conn.cursor() as cur:
# 			query_str = "INSERT INTO " + application_field + "(name, owner, geom) VALUES ('" + name_str + "', '" + owner_str + "', ST_GeomFromText(ST_AsText(ST_GeomFromGeoJSON('" + json.dumps(geojson) + "'))))"
# 			cur.execute(query_str)
# 			query_str2 = "SELECT max(id) FROM " + application_field
# 			cur.execute(query_str2)
# 			maxid = cur.fetchone()[0]
# 			print(maxid)
# 			query_str3 = "SELECT * FROM " + application_field + " WHERE id=" + str(maxid)
# 			r = cur.execute(query_str3)
#
# 	return r
