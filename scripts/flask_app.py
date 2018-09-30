from gmaps_interface import *

input_origin = 'carle hospital'
input_destination = '1509e university ave,urbana,il'
input_remaining_miles = 10
input_optimize = 'cost'
input_fuel_type = 1
optimal_gas_station = calculate_optimal_gas_station(input_origin, input_destination, input_optimize, input_fuel_type, input_remaining_miles)
embed = get_embed_string(input_origin, input_destination, optimal_gas_station)
print(embed)