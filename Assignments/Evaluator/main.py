# Author: Jordan Taranto
# CS461 Assignment 1

from parse_data import parse_adjacencies, parse_coordinates
from algos import RouteFinder

def main():
    # Parse data
    locations = parse_adjacencies('data/adjacencies.txt')
    parse_coordinates('data/coordinates.csv', locations)

    # create instance of the routefinder class
    route_finder = RouteFinder(locations)

    # user interface
    while True:
        start_city = input("Enter the start city: ").strip()
        if start_city not in locations:
            print("City not found. Please try again.")
            continue

        end_city = input("Enter the destination city: ").strip()
        if end_city not in locations:
            print("City not found. Please try again.")
            continue

        print("\nSelect search method:")
        print("1. Breadth-First Search")
        print("2. Depth-First Search")
        print("3. Iterative Deepening DFS")
        print("4. Best-First Search")
        print("5. A* Search")
        method = input("Enter the number of the search method: ").strip()

        if method == '1':
            path = route_finder.bfs(start_city, end_city)
            metrics = route_finder.metrics.get('bfs')
        elif method == '2':
            path = route_finder.dfs(start_city, end_city)
            metrics = route_finder.metrics.get('dfs')
        elif method == '3':
            path = route_finder.iddfs(start_city, end_city)
            metrics = route_finder.metrics.get('iddfs')
        elif method == '4':
            path = route_finder.best_first_search(start_city, end_city)
            metrics = route_finder.metrics.get('best_first')
        elif method == '5':
            path = route_finder.a_star_search(start_city, end_city)
            metrics = route_finder.metrics.get('a_star')
        else:
            print("Invalid selection. Please try again.")
            continue

        # Display results
        if path:
            print("\nPath found:")
            print(" -> ".join(path))
            print("\nMetrics:")
            print(f"Total distance: {metrics['total_distance']:.4f}")
            print(f"Execution time: {metrics['time']:.6f} seconds")
            print(f"Nodes expanded: {metrics['nodes_expanded']}")
            if 'max_depth' in metrics:
                print(f"Maximum depth reached: {metrics['max_depth']}")
        else:
            print("No path found.")

        # do another? 
        another = input("\nDo you want to perform another search? (y/n): ").strip()
        if another.lower() != 'y':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
