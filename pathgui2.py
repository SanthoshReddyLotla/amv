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

# Default initial distance values
distance_values = {f"{point1}-{point2}": 1 for point1 in points for point2 in points[point1]}

# Function to calculate Manhattan distance between two points in the grid
def calculate_distance(u, v):
    distance_key = f"{u}-{v}" if f"{u}-{v}" in distance_values else f"{v}-{u}"
    return distance_values.get(distance_key, 1)

# Function to find the shortest path between points using grid-based movement
def find_shortest_path(grid, start, end):
    shortest_path = nx.shortest_path(grid, start, end, weight=lambda u, v, d: calculate_distance(u, v))
    return shortest_path

# Load distance values from a file
def load_distance_values():
    try:
        with open('distance.txt', 'r') as file:
            data = file.readlines()
            for line in data:
                key, value = line.strip().split(':')
                distance_values[key] = int(value)
    except FileNotFoundError:
        print("File not found. Using default distances.")

# Save distance values to a file
def save_distance_values():
    with open('distance.txt', 'w') as file:
        for key, value in distance_values.items():
            file.write(f"{key}:{value}\n")

# Create a graph based on the grid points
grid_G = nx.Graph()
for point, connections in points.items():
    for connection in connections:
        grid_G.add_edge(point, connection)

# Create a Tkinter application
def find_shortest_path_gui():
    load_distance_values()  # Load distances from the file

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

    def set_distance_values():
        def update_distances():
            selected_point1 = point1_var.get()
            selected_point2 = point2_var.get()
            distance = int(distance_entry.get())
            distance_values[f"{selected_point1}-{selected_point2}"] = distance
            distance_values[f"{selected_point2}-{selected_point1}"] = distance
            distance_info_label.config(text=f"Distance updated between {selected_point1} and {selected_point2} to {distance}")

        distance_window = tk.Toplevel(root)
        distance_window.title("Set Distance Values")

        point1_var = tk.StringVar()
        point1_label = ttk.Label(distance_window, text="Select Point 1:")
        point1_label.pack()
        point1_dropdown = ttk.Combobox(distance_window, textvariable=point1_var, values=list(grid_points.keys()))
        point1_dropdown.pack()

        point2_var = tk.StringVar()
        point2_label = ttk.Label(distance_window, text="Select Point 2:")
        point2_label.pack()
        point2_dropdown = ttk.Combobox(distance_window, textvariable=point2_var, values=list(grid_points.keys()))
        point2_dropdown.pack()

        distance_label = ttk.Label(distance_window, text="Enter Distance:")
        distance_label.pack()
        distance_entry = ttk.Entry(distance_window)
        distance_entry.pack()

        update_button = ttk.Button(distance_window, text="Update Distance", command=update_distances)
        update_button.pack()

        distance_info_label = ttk.Label(distance_window, text="")
        distance_info_label.pack()

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

    # Button to set distance values
    set_distance_button = ttk.Button(root, text="Set Distance Values", command=set_distance_values)
    set_distance_button.pack()

    # Label to display the shortest path result
    shortest_path_label = ttk.Label(root, text="")
    shortest_path_label.pack()

    root.protocol("WM_DELETE_WINDOW", save_distance_values)  # Save distances when the window is closed
    root.mainloop()

# Run the GUI function
find_shortest_path_gui()
