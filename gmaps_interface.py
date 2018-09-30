import requests 
import pandas as pd
# Need python json library 

API_KEY = "AIzaSyCO6xWAy1F4WEAAArjT8qgEgFjZc77B7ds"

def generate_route(origin, destination): 
	""" Pings the Google Maps API to generate directions between two locations """
	# Need to extend this to using waypoints using *args
	no_comma_orig = origin.split(",") # Removing commas 
	no_comma_dest = destination.split(",") 

	orig = list()
	dest = list()
	for o in no_comma_orig: 
		orig.extend(o.split())
	for d in no_comma_dest:
		dest.extend(d.split())

	params = {"origin": "+".join(orig),
			  "destination": "+".join(dest),
			  "key": API_KEY}

	try: 
		r = requests.get("https://maps.googleapis.com/maps/api/directions/json", params = params, timeout = 30)
		return r.json()
	except: 
		print("Couldn't establish connection with the Google Maps API") # Probably change this later 
	

def get_total_route_distance(jsn): 
	""" Returns the total route distance between in a route encoded in a json
	
	Assumes the JSON file follows Google Maps' route format 
	"""
	total_distance = jsn["routes"][0]["legs"][0]["distance"]
	total_duration = jsn["routes"][0]["legs"][0]["duration"]
	return total_distance, total_duration

def get_lat_long_rect(jsn): 
	""" Returns the latitudes and longitudes that bound the area we will be driving """
	latitude_ne = jsn["routes"][0]["bounds"]["northeast"]["lat"]
	longitude_ne = jsn["routes"][0]["bounds"]["northeast"]["lng"]
	latitude_sw = jsn["routes"][0]["bounds"]["southwest"]["lat"]
	longitude_sw = jsn["routes"][0]["bounds"]["southwest"]["lng"]
	return (latitude_ne, longitude_ne), (latitude_sw, longitude_sw)

def get_gas_stations(northeast, southwest): 
	""" Returns a list of gas stations that lie within the bounds of the box defined by the northeast (lat, long) tuple 
		and the southwest (lat, long) tuple 

	Inputs: 
	northeast - a tuple of (latitude, longitude)
	southwest - a tuple of (latitude, longiude)

	Returns a list of gas station addresses 
	""" 
	latitude_ne = northeast[0]
	longitude_ne = northeast[1]
	latitude_sw = southwest[0]
	longitude_sw = southwest[1]

	df = pd.read_csv("data/address_location.csv")	
	out = list() 
	for address, latitude, longitude in zip(df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2]):
		if latitude < latitude_ne and latitude > latitude_sw and longitude < longitude_ne and longitude > longitude_sw: 
			out.append(address)
	return out

if __name__ == "__main__": 
	input_origin = input("Enter your starting point: ")
	input_destination = input("Enter your destination: ")

	jsn = generate_route(input_origin, input_destination)
	northeast, southwest = get_lat_long_rect(jsn)
	gas_stations = get_gas_stations(northeast, southwest)
	if len(gas_stations) == 0: # Couldn't find any prospective gas stations 
		print("There are no gas stations between your start and end locations")
		sys.exit(0)
	else:
		print(gas_stations)