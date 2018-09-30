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
	"""
	total_distance = route[0]["legs"][0]["distance"]["value"]
	
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

	df = pd.read_csv("../data/address_location.csv")	
	out = list() 
	for address, latitude, longitude in zip(df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2]):
		if latitude < latitude_ne and latitude > latitude_sw and longitude < longitude_ne and longitude > longitude_sw: 
			out.append(address)
	return out

def calculate_gas_station_score(route, price, original_dist):
	""" Calculates the score used to rank gas stations """ 
	distance = route[0]["legs"][0]["distance"]["value"] + route[0]["legs"][1]["distance"]["value"]
	diff = math.fabs(distance - original_dist)
	return price - price * diff

if __name__ == "__main__": 
	input_origin = input("Enter your starting point: ")
	input_destination = input("Enter your destination: ")
	input_optimize = input("Optimize for cost or speed? ")
	input_fuel_type = input("Fuel Type: ")
	input_remaining_gas = input("Remaining Miles before Empty Tank: ")

	gmaps = googlemaps.Client(key = API_KEY)

	route = generate_route(gmaps, input_origin, input_destination)
	distance = get_total_route_distance(route)
	northeast, southwest = get_lat_long_rect(route)
	waypoints = get_gas_stations(northeast, southwest)
	if len(waypoints) == 0: # Couldn't find any prospective gas stations 
		print("There are no gas stations between your start and end locations")
		sys.exit(0)

	for waypoint in waypoints: 
		address = waypoint[:-11]
		gb = get_from_gasbuddy(address, input_fuel_type)
		gb_df = gb.get_content()
		print(gb_df["adds"])
		print(address)

		# names = gb_df["names"]
		# addresses = gb_df["adds"]
		# prices = gb_df["price"]



	# Placeholder code to show calculations 
	""" 
	waypoint, address, prices = gb.get_content() 

	route_ranking = PriorityQueue()

	if input_optimize == "cost": 
		for i in range(len(waypoint)): 
			# In the future, it would be good to consider the remaining amount of gas 
			rt = generate_route(gmaps, input_origin, input_destination, waypoint[i])
			route_ranking.put((calculate_gas_station_score(rt, prices[i], distance), prices[i], address[i]))
		print(route_ranking.get()[2])

	elif input_optimize == "speed": 
		for i in range(len(waypoint)): 
			rt = generate_route(gmaps, input_origin, input_destination, waypoint[i])
			route_ranking.put((get_total_route_distance(rt), calculate_gas_station_score(rt, prices[i], distance), prices[i], address[i]))
		ans = list()
		for i in range(5): # This is arbitrary
			ans.append(route_ranking.get())
		print(min(ans, key = lambda x: x[1])[3])
	"""
	# print(route_ranking.get())


	# for waypoint in gas_stations: 
	# 	rt = generate_route(gmaps, input_origin, input_destination, waypoint)
		# Pull price for waypoint using the zip code -> waiting for jianzhang 
		# Calculate ranking -> waiting for terry/zhaowin
		# Put it into the ranking list 
	# Return the best ranking list 