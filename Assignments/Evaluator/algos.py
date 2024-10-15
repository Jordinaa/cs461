# Author: Jordan Taranto
# CS461 Assignment 1

import heapq
import math
import time
from collections import deque

# ChatGPT Response: 
# write me these 5 algorithims that take in a parsed data
class RouteFinder:
    def __init__(self, locations):
        self.locations = locations
        self.metrics = {}

    def calculate_distance(self, coord1, coord2):
        """
        Calculates the Euclidean distance between two points in 2D space.
        """
        x1, y1 = coord1
        x2, y2 = coord2

        # euclidian distance 
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distance

    def calculate_total_distance(self, path):
        """
        Calculates the total distance of a path given a list of city names.
        """
        total_distance = 0.0
        for i in range(len(path) - 1):
            coord1 = self.locations[path[i]].coordinates
            coord2 = self.locations[path[i+1]].coordinates
            total_distance += self.calculate_distance(coord1, coord2)
        return total_distance

    def bfs(self, start_name, goal_name):
        """
        Performs Breadth-First Search from start to goal.
        """
        start_time = time.time()
        start_node = self.locations[start_name]
        goal_node = self.locations[goal_name]

        visited = set()
        queue = deque()
        queue.append((start_node, [start_node.name]))
        nodes_expanded = 0

        while queue:
            current_node, path = queue.popleft()
            nodes_expanded += 1

            if current_node.name == goal_name:
                end_time = time.time()
                total_distance = self.calculate_total_distance(path)
                self.metrics['bfs'] = {
                    'time': end_time - start_time,
                    'path_length': len(path),
                    'nodes_expanded': nodes_expanded,
                    'total_distance': total_distance
                }
                return path

            visited.add(current_node.name)
            for neighbor in current_node.adjacencies:
                if neighbor.name not in visited:
                    visited.add(neighbor.name)
                    queue.append((neighbor, path + [neighbor.name]))

        end_time = time.time()
        self.metrics['bfs'] = {
            'time': end_time - start_time,
            'path_length': None,
            'nodes_expanded': nodes_expanded,
            'total_distance': None
        }
        return None 

    def dfs(self, start_name, goal_name):
        """
        Performs Depth-First Search from start to goal.
        """
        start_time = time.time()
        start_node = self.locations[start_name]
        goal_node = self.locations[goal_name]

        visited = set()
        stack = []
        stack.append((start_node, [start_node.name]))
        nodes_expanded = 0

        while stack:
            current_node, path = stack.pop()
            nodes_expanded += 1

            if current_node.name == goal_name:
                end_time = time.time()
                total_distance = self.calculate_total_distance(path)
                self.metrics['dfs'] = {
                    'time': end_time - start_time,
                    'path_length': len(path),
                    'nodes_expanded': nodes_expanded,
                    'total_distance': total_distance
                }
                return path

            if current_node.name not in visited:
                visited.add(current_node.name)
                for neighbor in reversed(current_node.adjacencies):
                    if neighbor.name not in visited:
                        stack.append((neighbor, path + [neighbor.name]))

        end_time = time.time()
        self.metrics['dfs'] = {
            'time': end_time - start_time,
            'path_length': None,
            'nodes_expanded': nodes_expanded,
            'total_distance': None
        }
        return None

    def iddfs(self, start_name, goal_name):
        """
        Performs Iterative Deepening Depth-First Search from start to goal.
        """
        start_time = time.time()
        max_depth = 0
        nodes_expanded = 0

        while True:
            visited = set()
            result, expanded = self.dls(start_name, goal_name, max_depth, visited, [start_name])
            nodes_expanded += expanded

            if result:
                end_time = time.time()
                total_distance = self.calculate_total_distance(result)
                self.metrics['iddfs'] = {
                    'time': end_time - start_time,
                    'path_length': len(result),
                    'nodes_expanded': nodes_expanded,
                    'total_distance': total_distance,
                    'max_depth': max_depth
                }
                return result

            max_depth += 1
            if max_depth > len(self.locations):
                break

        end_time = time.time()
        self.metrics['iddfs'] = {
            'time': end_time - start_time,
            'path_length': None,
            'nodes_expanded': nodes_expanded,
            'total_distance': None,
            'max_depth': max_depth
        }
        return None

    def best_first_search(self, start_name, goal_name):
        """
        Performs Best-First Search from start to goal using a heuristic.
        """
        start_time = time.time()
        start_node = self.locations[start_name]
        goal_node = self.locations[goal_name]

        open_list = []
        heuristic = self.calculate_distance(start_node.coordinates, goal_node.coordinates)
        heapq.heappush(open_list, (heuristic, start_node, [start_node.name]))
        visited = set()
        nodes_expanded = 0

        while open_list:
            _, current_node, path = heapq.heappop(open_list)
            nodes_expanded += 1

            if current_node.name == goal_name:
                end_time = time.time()
                total_distance = self.calculate_total_distance(path)
                self.metrics['best_first'] = {
                    'time': end_time - start_time,
                    'path_length': len(path),
                    'nodes_expanded': nodes_expanded,
                    'total_distance': total_distance
                }
                return path

            visited.add(current_node.name)
            for neighbor in current_node.adjacencies:
                if neighbor.name not in visited:
                    heuristic = self.calculate_distance(
                        neighbor.coordinates, goal_node.coordinates)
                    heapq.heappush(open_list, (heuristic, neighbor, path + [neighbor.name]))
                    visited.add(neighbor.name)

        end_time = time.time()
        self.metrics['best_first'] = {
            'time': end_time - start_time,
            'path_length': None,
            'nodes_expanded': nodes_expanded,
            'total_distance': None
        }
        return None 

    def a_star_search(self, start_name, goal_name):
        """
        Performs A* Search from start to goal using both actual cost and heuristic.
        """
        start_time = time.time()
        start_node = self.locations[start_name]
        goal_node = self.locations[goal_name]

        open_list = []
        g = 0 
        h = self.calculate_distance(start_node.coordinates, goal_node.coordinates)
        f = g + h
        heapq.heappush(open_list, (f, start_node, [start_node.name], g))
        visited = {}
        nodes_expanded = 0

        while open_list:
            f, current_node, path, g = heapq.heappop(open_list)
            nodes_expanded += 1

            if current_node.name == goal_name:
                end_time = time.time()
                total_distance = g
                self.metrics['a_star'] = {
                    'time': end_time - start_time,
                    'path_length': len(path),
                    'nodes_expanded': nodes_expanded,
                    'total_distance': total_distance
                }
                return path

            if current_node.name in visited and visited[current_node.name] <= g:
                continue

            visited[current_node.name] = g

            for neighbor in current_node.adjacencies:
                distance = self.calculate_distance(
                    current_node.coordinates, neighbor.coordinates)
                g_new = g + distance
                h_new = self.calculate_distance(
                    neighbor.coordinates, goal_node.coordinates)
                f_new = g_new + h_new
                heapq.heappush(open_list, (f_new, neighbor, path + [neighbor.name], g_new))

        end_time = time.time()
        self.metrics['a_star'] = {
            'time': end_time - start_time,
            'path_length': None,
            'nodes_expanded': nodes_expanded,
            'total_distance': None
        }
        return None
