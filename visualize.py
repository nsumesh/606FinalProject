import numpy as np
import osmnx as ox

import folium
from folium.plugins import AntPath

from astar import astar

def visualize(G, start, end, pathfinder, start_label=None, end_label=None, save_location=None):
    """
    Visualize the graph and the shortest path between two nodes

    Args:
        G (NetworkX MutiDiGraph): input graph
        s (int): start node
        t (int): target node
        pathfinder (func): pathfinding algorithm
        s_label (str): label for start node
        t_label (str): label for target node
        save_location (str): path to save the map
    """

    # NOTE: hack for when pathfinder is not astar (explicitly set weights)
    if pathfinder != astar:
        for _, _, _, data in G.edges(keys=True, data=True):
            data['weight'] = data.get('length', np.inf)


    path, distance, _ = pathfinder(G, start, end)
    if start_label is None:
        start_label = "START"
    if end_label is None:
        end_label = "END"

    start_coords = (G.nodes[start]['y'], G.nodes[start]['x'])
    end_coords = (G.nodes[end]['y'], G.nodes[end]['x'])

    path_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in path]
    map_center = np.mean(path_coords, axis=0)

    route_map = folium.Map(location=map_center, zoom_start=14, tiles="OpenStreetMap")

    # start node marker
    folium.Marker(
        location=list(start_coords),
        tooltip=folium.Tooltip(start_label, permanent=True, style="font-size: 16px;"),
        icon=folium.Icon(color='green', icon='play')
    ).add_to(route_map)

    # end node marker
    folium.Marker(
        location=list(end_coords),
        tooltip=folium.Tooltip(end_label, permanent=True, style="font-size: 16px;"),
        icon=folium.Icon(color='red', icon='stop')
    ).add_to(route_map)

    # path
    path_locations = path_coords

    folium.PolyLine(
        locations=path_locations,
        color="blue",
        weight=5,
        opacity=0.7,
        tooltip=f"Path Distance: {distance:.2f} m",
    ).add_to(route_map)

    # animate path
    AntPath(
        locations=path_locations,
        delay=500,
        dash_array=[10, 20], # dash and gap lengths
        color='darkblue',
        weight=3,
        pulse_color='lightblue'
    ).add_to(route_map)


    if save_location is not None:
        route_map.save(save_location)
    
    route_map.show_in_browser()
    

if __name__ == "__main__":
    # example usage
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

    drive_map = ox.load_graphml("maps/drive_map.graphml")
    start = ox.distance.nearest_nodes(
        drive_map, landmarks["Georgetown University"][1], landmarks["Georgetown University"][0]
    )

    end = ox.distance.nearest_nodes(
        drive_map, landmarks["Smithsonian"][1], landmarks["Smithsonian"][0]
    )
    
    visualize(
        drive_map,
        start,
        end,
        astar,
        "Georgetown University",
        "Smithsonian",
        "plots/drive_map.html"
    )
