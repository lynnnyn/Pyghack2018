import pandas as pd
import googlemaps
import sys
from gasbuddy import get_from_gasbuddy
from queue import PriorityQueue
import math

API_KEY = "AIzaSyCO6xWAy1F4WEAAArjT8qgEgFjZc77B7ds"

def generate_route(client, origin, destination, waypoint = None):
	""" Pings the Google Maps API to generate directions between two locations """
	# Need to extend this to using waypoints using *args

	if waypoint == None:
		try:
			return client.directions(origin, destination, mode = "driving")
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

	Currently only works for single destination routes - need to extend it to waypoints
	"""
	total_distance = 0

	for i in range(len(route[0]["legs"])):
		total_distance += route[0]["legs"][i]["distance"]["value"]

	return total_distance

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

	df = pd.read_csv("./data/address_location.csv")
	out = list()
	for address, latitude, longitude in zip(df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2]):
		if latitude < latitude_ne and latitude > latitude_sw and longitude < longitude_ne and longitude > longitude_sw:
			out.append(address)
	return out

def calculate_gas_station_score(route, price, original_dist):
	""" Calculates the score used to rank gas stations """
	distance = get_total_route_distance(route)
	diff = math.fabs(distance - original_dist)
	return price - price * diff

def calculate_optimal_gas_station(origin, destination, optimization_target, fuel_type, remaining_miles):
	""" Generates all of the gas stations between origin and destination, ranks them, and determines which one is the best given our optimization target """
	gmaps = googlemaps.Client(key = API_KEY)
	direct_route = generate_route(gmaps, origin, destination)
	direct_distance = get_total_route_distance(direct_route)
	bounding_ne, bounding_sw = get_lat_long_rect(direct_route)
	gas_stations = get_gas_stations(bounding_ne, bounding_sw)

	# We couldn't find any prospective gas stations along the route
	if len(gas_stations) == 0:
		print("There are no gas stations between your start and end locations")
		sys.exit(0)

	gb = get_from_gasbuddy(fuel_type)

	station_ranking = PriorityQueue()

	for station in gas_stations: # Go through each gas station and rank them
		station_address = station[:-11] # Try not to hard code this
		print(station_address)
		station_price = gb.get_price(station_address)

		if station_price != set(): # Found the gas station and it sells the fuel type that we are looking for
			price = station_price.pop()
			station_route = generate_route(gmaps, origin, destination, station_address)
			if optimization_target.strip().lower() == "cost":
				station_ranking.put((calculate_gas_station_score(station_route, price, direct_distance), price, station_address))
			elif optimization_target.strip().lower() == "speed":
				station_ranking.put((get_total_route_distance(station_route), calculate_gas_station_score(station_route, price, direct_distance), price, station_address))

	if optimization_target.strip().lower() == "cost":
		return station_ranking.get()[2]
	elif optimization_target.strip().lower() == "speed":
		nearest = list()
		for i in range(5):
			nearest.append(station_ranking.get())
		return min(nearest, key = lambda x: x[1])[3]
	else:
		print(optimization_target)
		return "Optimization Target Wrong " # No optimization target

def get_embed_string(origin, destination, waypoint):
	""" Returns the string used to embed a google maps visual in an iframe """
	embed = "https://www.google.com/maps/embed/v1/directions?"
	embed = embed + "key=" + API_KEY
	embed = embed + "&origin=" + "+".join(origin.split())
	embed = embed + "&destination=" + "+".join(destination.split())
	embed = embed + "&waypoints=" + "+".join(waypoint.split())
	return embed

if __name__ == "__main__":
	input_origin = input("Enter your starting point: ")
	input_destination = input("Enter your destination: ")
	input_optimize = input("Optimize for cost or speed? ")
	input_fuel_type = input("Fuel Type: ")
	input_remaining_miles = input("Remaining Miles before Empty Tank: ")

	optimal_gas_station = calculate_optimal_gas_station(input_origin, input_destination, input_optimize, input_fuel_type, input_remaining_miles)
	print("Best Gas Station: ", optimal_gas_station)
	embed = get_embed_string(input_origin, input_destination, optimal_gas_station)

