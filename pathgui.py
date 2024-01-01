import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

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

# Create a Tkinter application
def find_shortest_path_gui():
    root = tk.Tk()
    root.title("Shortest Path Finder")

    # Create initial figure and canvas
    plt.figure()
    pos = {point: grid_points[point] for point in points.keys()}
    nx.draw(grid_G, pos, with_labels=True, node_size=500, node_color='red', font_weight='bold')
    plt.title('Shortest Path')
    canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def calculate_shortest_path():
        current = current_point_var.get()
        final = final_point_var.get()

        plt.clf()  # Clear the previous plot
        nx.draw(grid_G, pos, with_labels=True, node_size=500, node_color='red', font_weight='bold')

        if current in points.keys() and final in points.keys():
            shortest_path = find_shortest_path(grid_G, current, final)
            shortest_path_label.config(text=f"The shortest path from {current} to {final} is: {shortest_path}")

            # Highlight the shortest path in green
            nx.draw_networkx_nodes(grid_G, pos, nodelist=shortest_path, node_color='green', node_size=700)
            nx.draw_networkx_edges(grid_G, pos, edgelist=[(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)], edge_color='green', width=4)
        else:
            shortest_path_label.config(text="Invalid points detected or selected.")

        plt.title('Shortest Path')
        canvas.draw()

    # Dropdown menu for current point selection
    current_point_var = tk.StringVar()
    current_point_label = ttk.Label(root, text="Select Current Point:")
    current_point_label.pack()
    current_point_dropdown = ttk.Combobox(root, textvariable=current_point_var, values=list(points.keys()))
    current_point_dropdown.pack()

    # Dropdown menu for final point selection
    final_point_var = tk.StringVar()
    final_point_label = ttk.Label(root, text="Select Final Point:")
    final_point_label.pack()
    final_point_dropdown = ttk.Combobox(root, textvariable=final_point_var, values=list(points.keys()))
    final_point_dropdown.pack()

    # Button to calculate the shortest path
    calculate_button = ttk.Button(root, text="Calculate Shortest Path", command=calculate_shortest_path)
    calculate_button.pack()

    # Label to display the shortest path result
    shortest_path_label = ttk.Label(root, text="")
    shortest_path_label.pack()

    root.mainloop()

# Run the GUI function
find_shortest_path_gui()
