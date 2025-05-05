import osmnx as ox
import matplotlib.pyplot as plt
from johnsons import johnsons
from Dijkstra import dijkstra
from astar import astar
from bellmanford import bellman_ford
import networkx as nx
drive_map = ox.graph_from_place("Washington, District of Columbia, USA", network_type="drive")
drive_map = drive_map.subgraph(max(nx.strongly_connected_components(drive_map), key=len)).copy()
ox.plot_graph(drive_map, node_size=10, edge_color="#999999")
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

for u, v, k, data in drive_map.edges(keys=True, data=True):
    data['weight'] = data.get('length', 1)

start = ox.distance.nearest_nodes(drive_map, landmarks["Georgetown University"][1], landmarks["Georgetown University"][0])
end = ox.distance.nearest_nodes(drive_map, landmarks["Smithsonian"][1], landmarks["Smithsonian"][0])

print("Start node:", start)
print("End node:", end)
print("Start and end in graph:", start in drive_map.nodes, end in drive_map.nodes)

path_djikstra, distance_djikstra, stats_djikstra = dijkstra(drive_map, start, end)
print("Path found using Djikstra:", path_djikstra[:5], "...", path_djikstra[-5:])
print(f"Total distance using Djikstra: {distance_djikstra:.2f} meters")
print("Time taken by Djikstra:",stats_djikstra['execution_time'])
print("Peak Memory:",stats_djikstra['peak_memory'])
print("Current Memory:",stats_djikstra['current_memory'])
fig, ax = ox.plot_graph_route(
    drive_map,
    path_djikstra,
    route_color='red',
    route_linewidth=4,
    node_size=10,
    bgcolor='black'
)
print("\n")
path_astar, distance_astar, stats_astar = astar(drive_map, start, end)
print("Path found using A-Star:", path_astar[:5], "...", path_astar[-5:])
print(f"Total distance using A-Star: {distance_astar:.2f} meters")
print("Time taken by A-Star:",stats_astar['execution_time'])
print("Peak Memory:",stats_astar['peak_memory'])
print("Current Memory:",stats_astar['current_memory'])
fig, ax = ox.plot_graph_route(
    drive_map,
    path_astar,
    route_color='red',
    route_linewidth=4,
    node_size=10,
    bgcolor='black'
)
print("\n")
path_bf, distance_bf, stats_bf = bellman_ford(drive_map, start, end)
print("Path found using Bellman Ford:", path_bf[:5], "...", path_bf[-5:])
print(f"Total distance using Bellman Ford: {distance_bf:.2f} meters")
print("Time taken by Bellman Ford:",stats_bf['execution_time'])
print("Peak Memory:",stats_bf['peak_memory'])
print("Current Memory:",stats_bf['current_memory'])

fig, ax = ox.plot_graph_route(
    drive_map,
    path_bf,
    route_color='red',
    route_linewidth=4,
    node_size=10,
    bgcolor='black'
)
plt.show()

