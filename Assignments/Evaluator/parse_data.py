# Author: Jordan Taranto
# CS461 Assignment 1
import csv

class Location:
    def __init__(self, name, coordinates=None):
        self.name = name
        self.coordinates = coordinates 
        self.adjacencies = []

    def add_adjacency(self, adjacent_location):
        self.adjacencies.append(adjacent_location)

def parse_adjacencies(file_path):
    locations = {}
    with open(file_path, 'r') as f:
        for line in f:
            loc1, loc2 = line.strip().split()
            if loc1 not in locations:
                locations[loc1] = Location(loc1)
            if loc2 not in locations:
                locations[loc2] = Location(loc2)
            locations[loc1].add_adjacency(locations[loc2])
            locations[loc2].add_adjacency(locations[loc1])
    return locations

def parse_coordinates(file_path, locations):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            name, latitude, longitude = row[0], float(row[1]), float(row[2])
            if name in locations:
                locations[name].coordinates = (latitude, longitude)