import networkx as nx
import matplotlib.pyplot as plt

# Sample points and their connections (predefined path)
points = {
    "Point A": {"Point B", "Point C"},
    "Point B": {"Point A", "Point D"},
    "Point C": {"Point A", "Point D"},
    "Point D": {"Point B", "Point C", "Point E"},
    "Point E": {"Point D", "Point F"},
    "Point F": {"Point E"}
}

# Create a grid-based representation of the points and connections
grid_points = {
    "Point A": (0, 0),
    "Point B": (2, 0),
    "Point C": (0, 2),
    "Point D": (2, 2),
    "Point E": (4, 2),
    "Point F": (4, 4)
}

# Function to calculate Manhattan distance between two points in the grid
def calculate_distance(u, v):
    x1, y1 = grid_points[u]
    x2, y2 = grid_points[v]
    return abs(x2 - x1) + abs(y2 - y1)

# Function to find the shortest path between points using grid-based movement
def find_shortest_path(grid, start, end):
    shortest_path = nx.shortest_path(grid, start, end, weight=lambda u, v, d: calculate_distance(u, v))
    return shortest_path

# Create a graph based on the grid points
grid_G = nx.Graph()
for point, connections in points.items():
    for connection in connections:
        grid_G.add_edge(point, connection)

# Example usage
current_point = "Point A"  # Replace this with the current point scanned by the robot
final_point = "Point F"    # Replace this with the final point selected by the user

if current_point in points.keys() and final_point in points.keys():
    shortest_path = find_shortest_path(grid_G, current_point, final_point)
    print(f"The shortest path from {current_point} to {final_point} is: {shortest_path}")
else:
    print("Invalid points detected or selected.")
