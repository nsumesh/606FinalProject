import osmnx as ox
import matplotlib.pyplot as plt
from johnsons import johnsons
from Dijkstra import dijkstra
import networkx as nx
# Load full city graph (optional for visual reference)
print("🚀 Script started")

drive_map = ox.graph_from_place("Washington, District of Columbia, USA", network_type="drive")
drive_map = drive_map.subgraph(max(nx.strongly_connected_components(drive_map), key=len)).copy()

ox.plot_graph(drive_map, node_size=10, edge_color="#999999")

# Landmarks
landmarks = {
    "The Capitol": (38.8899, -77.0091),
    "White House": (38.8977, -77.0365),
    "Bullpen": (38.8677, -77.0076),
    "Georgetown University": (38.9076, -77.0723),
    "George Washington University": (38.8997, -77.0498),
    "Archives": (38.8922, -77.0228),
    "Smithsonian": (38.8881, -77.0260),
    "Mt Vernon Convention Center": (38.9041, -77.0227),
    "Nationals Park": (38.8730, -77.0075),
    "Union Station": (38.8971, -77.0064)
}

# Create a larger subgraph to ensure connectivity
# subgraph = ox.graph_from_point(landmarks["White House"], dist=2000, network_type="drive")

# # Add edge weights
for u, v, k, data in drive_map.edges(keys=True, data=True):
    data['weight'] = data.get('length', 1)

# Get node IDs
start = ox.distance.nearest_nodes(drive_map, landmarks["White House"][1], landmarks["White House"][0])
end = ox.distance.nearest_nodes(drive_map, landmarks["Smithsonian"][1], landmarks["Smithsonian"][0])

print("✅ Start node:", start)
print("✅ End node:", end)
print("✅ Start and end in graph:", start in drive_map.nodes, end in drive_map.nodes)

print("Is Smithsonian node in the graph?", end in drive_map.nodes)
path, distance = dijkstra(drive_map, start, end)
print("✅ Path found:", path[:5], "...", path[-5:])
print(f"✅ Total distance: {distance:.2f} meters")

fig, ax = ox.plot_graph_route(
    drive_map,
    path,
    route_color='red',
    route_linewidth=4,
    node_size=10,
    bgcolor='black'
)
plt.title(f"Custom Dijkstra: White House to Smithsonian ({distance:.2f} meters)", fontsize=12)
plt.tight_layout()
plt.show()

# Run Johnson’s algorithm
# print("⚙️ Running Johnson's algorithm...")
# all_paths = johnsons(drive_map, only_source=start)
# print("✅ Johnson's finished.")

# # Initialize the plot
# fig, ax = ox.plot_graph(subgraph, node_size=10, edge_color="#cccccc", show=False, close=False)
# print(f"Start node: {start}")
# print(f"End node: {end}")
# print("Paths from start:", all_paths[start][1].keys())
# print("Distance:", all_paths[start][0].get(end, 'N/A'))

# # Plot route only if a path exists
# if end in all_paths[start][1] and all_paths[start][0][end] != float('inf'):
#     print("entered if statement")
#     path = all_paths[start][1][end]
#     distance = all_paths[start][0][end]

#     x_vals = [subgraph.nodes[n]['x'] for n in path]
#     y_vals = [subgraph.nodes[n]['y'] for n in path]
#     ax.plot(x_vals, y_vals, color='red', linewidth=2, label='Johnson path')

#     plt.title(f"Johnson's Path from White House to Smithsonian: {distance:.2f} meters")
# else:
#     print("❌ No valid Johnson path found from White House to Smithsonian.")
#     plt.title("❌ No valid Johnson path from White House to Smithsonian")

# # Plot landmarks
# for name, (lat, lon) in landmarks.items():
#     try:
#         node = ox.distance.nearest_nodes(subgraph, lon, lat)
#         x, y = subgraph.nodes[node]['x'], subgraph.nodes[node]['y']
#         ax.plot(x, y, 'o', markersize=5, color='blue')
#         ax.text(x, y, name, fontsize=8, color='black', ha='right')
#     except:
#         continue

# plt.legend()
# plt.tight_layout()
# plt.show()
