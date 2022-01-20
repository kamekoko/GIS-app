import reverse_geocode as rg

def r_geocode(lng, lat):
	coordinates = tuple([lat, lng]),
	r = rg.search(coordinates)[0]
	return r
