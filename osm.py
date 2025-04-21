import osmnx as ox
import matplotlib.pyplot as plt
drive_map = ox.graph_from_place("Washington, District of Columbia, USA", network_type="drive")
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

subgraph = ox.graph_from_point(landmarks["White House"], dist=1000, network_type="drive")
ox.plot_graph(subgraph, node_size=10, edge_color="#336699")
