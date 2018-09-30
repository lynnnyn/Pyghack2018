import pandas as pd
import googlemaps
import sys
import gasbuddy

API_KEY = "AIzaSyCO6xWAy1F4WEAAArjT8qgEgFjZc77B7ds"

def generate_route(client, origin, destination, waypoint = None): 
	""" Pings the Google Maps API to generate directions between two locations """
	# Need to extend this to using waypoints using *args
	
	if waypoint != None: 
		try: 
			return client.directions(origin, destination)
		except: 
			print("Couldn't establish connection with the Google Maps API") # Probably change this later 
	else:
		try: 
			return client.directions(origin, destination, mode = "driving", waypoints = waypoint)
		except:
			print("Couldn't establish connection with the Google Maps API")

def get_total_route_distance(route): 
	""" Returns the total route distance between in a route encoded in a json
	
	Assumes the JSON file follows Google Maps' route format 
	"""
	total_distance = route[0]["legs"][0]["distance"]
	total_duration = route[0]["legs"][0]["duration"]
	return total_distance, total_duration

def get_lat_long_rect(route): 
	""" Returns the latitudes and longitudes that bound the area we will be driving """
	latitude_ne = route[0]["bounds"]["northeast"]["lat"]
	longitude_ne = route[0]["bounds"]["northeast"]["lng"]
	latitude_sw = route[0]["bounds"]["southwest"]["lat"]
	longitude_sw = route[0]["bounds"]["southwest"]["lng"]
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

	df = pd.read_csv("../data/address_location.csv")	
	out = list() 
	for address, latitude, longitude in zip(df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2]):
		if latitude < latitude_ne and latitude > latitude_sw and longitude < longitude_ne and longitude > longitude_sw: 
			out.append(address)
	return out

if __name__ == "__main__": 
	input_origin = input("Enter your starting point: ")
	input_destination = input("Enter your destination: ")
	input_optimize = input("Optimize for cost or speed?")
	input_fuel_type = input("Fuel Type: ")
	input_remaining_gas = input("Remaining Gas Types: ")

	gmaps = googlemaps.Client(key = API_KEY)

	route = generate_route(gmaps, input_origin, input_destination)
	northeast, southwest = get_lat_long_rect(route)
	waypoints = get_gas_stations(northeast, southwest)
	if len(waypoints) == 0: # Couldn't find any prospective gas stations 
		print("There are no gas stations between your start and end locations")
		sys.exit(0)

	# print(waypoints)
	route_ranking = list() 
	for waypoint in gas_stations: 
		rt = generate_route(gmaps, input_origin, input_destination, waypoint)
		# Pull price for waypoint using the zip code -> waiting for jianzhang 
		# Calculate ranking -> waiting for terry/zhaowin
		# Put it into the ranking list 
	# Return the best ranking list 