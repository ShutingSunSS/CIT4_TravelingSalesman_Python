# File:        cities.py
# Programmer:  Shuting Sun
# Time:        Sep 25, 2016
# Description: CIT 590, Assignment 4.
#              A traveling salesman wishes to visit every city exactly once, then return to his starting point.
#              However, the salesman also wishes to minimize the total distance that must be traveled.
#              This is a classic computer science problem, known as the Traveling Salesman problem.

from math import *
from random import *

def distance(lat1degrees, long1degrees, lat2degrees, long2degrees):
    """ The earth is not planar, the function returns
        the distance between two points on the globe (Great-circle distance)."""
    earth_radius = 3956  # miles
    lat1 = radians(lat1degrees)
    long1 = radians(long1degrees)
    lat2 = radians(lat2degrees)
    long2 = radians(long2degrees)
    lat_difference = lat2 - lat1
    long_difference = long2 - long1
    sin_half_lat = sin(lat_difference / 2)
    sin_half_long = sin(long_difference / 2)
    a = sin_half_lat ** 2 + cos(lat1) * cos(lat2) * sin_half_long ** 2
    c = 2 * atan2(sqrt(a), sqrt(1.0 - a))
    return earth_radius * c

def read_cities(file_name):
    """ Read in the cities from the given file_name, and return them
        as a list of four-tuples: [(state, city, latitude, longitude), ...]
        Use this as initial road_map:
        the cycle Alabama → Alaska → Arizona → ... → Wyoming → Alabama."""
    with open(file_name, "r") as file:
        res = []
        for line in file:
            line = line.strip()
            elements = line.split("\t")
            res.append(elements)
        return res

def print_cities(road_map):
    """Prints a list of cities, along with their locations.
       Print only two digits after the decimal point."""
    # Do I need to add road_map[0] as the last one? Actually I don't like the idea.
    for i in range (0, len(road_map)):
        alt = float(road_map[i][2])
        lat = float(road_map[i][3])
        print(road_map[i][1].ljust(16), '(','{:5.2f}, {:8.2f}'.format(alt, lat), ')')
    

def compute_total_distance(road_map):
    """Returns, as a floating point number, the sum of the distances of all the connections in the road_map.
       Remember that it's a cycle, so that (for example) in the initial road_map, Wyoming connects to Alabama.."""
    if (len(road_map) == 1):
        return 0
    else:
        total = 0
        for i in range(0, len(road_map)):
            next_index = (i + 1) % len(road_map)
            total = total + \
            distance(float(road_map[i][2]), float(road_map[i][3]), float(road_map[next_index][2]), float(road_map[next_index][3]))
        return total
        
def swap_adjacent_cities(road_map, index):
    """Take the city at location index in the road_map,
       and the city at location index+1 (or at 0, if index refers to the last element in the list),
       swap their positions in the road_map,
       compute the new total distance, and return the tuple (new_road_map, new_total_distance)."""
    next_index = (index + 1) % len(road_map)
    return (swap_cities(road_map, index, next_index))

def swap_cities(road_map, index1, index2):
    """Take the city at location index in the road_map,
       and the city at location index2, swap their positions in the road_map,
       compute the new total distance, and return the tuple (new_road_map, new_total_distance).
       Allow the possibility that index1=index2, and handle this case correctly."""
    new_road_map = road_map[:] # Copy the road_map to a new list
    temporary = new_road_map[index1]
    new_road_map[index1] = new_road_map[index2]
    new_road_map[index2] = temporary
    new_total_distance = compute_total_distance(new_road_map)
    tup = [new_road_map, new_total_distance]
    return tup

def find_best_cycle(road_map):
    """Using a combination of swap_cities and swap_adjacent_cities,
       try 10000 swaps, and each time keep the best cycle found so far.
       After 10000 swaps, return the best cycle found so far."""
    tup = swap_cities(road_map, 0, 0) # Genearte the tup of the initial road_map

    for i in range (0, 5000):
        temp = swap_adjacent_cities(road_map, randint(0, len(road_map) - 1))
        if temp[1] < tup[1]:
            tup = temp
        else:
            tup = tup
    
    for i in range (0, 5000):
        temp = swap_cities(tup[0], randint(0, len(road_map) - 1), randint(0, len(road_map) - 1))
        if temp[1] < tup[1]:
            tup = temp
        else:
            tup = tup
    return tup[0]

def print_map(road_map):
    """Prints in an easily understandable format, the cities and their connections,
       along with the distance for each connection and the total distance."""
    total_distance = 0
    the_distance = 0
    for i in range(0, len(road_map)):
        next_index = (i + 1) % len(road_map)
        the_distance = distance(float(road_map[i][2]), float(road_map[i][3]), float(road_map[next_index][2]), float(road_map[next_index][3]))
        print("The", i + 1, "stop: ", road_map[i][1], "to", road_map[next_index][1], "\nThe distance (miles): ", the_distance)
        total_distance = total_distance + the_distance
        print()
    print("The total distance (miles):", total_distance)
      
def main():
    road_map = read_cities("city-data.txt")
    print("The original cities, with latitude and altitude:")
    print_cities(road_map)
    best_cycle = find_best_cycle(road_map)
    print("\nThe 'best' cycle:\n")
    print_map(best_cycle)
    
if __name__ == "__main__":
    main()
