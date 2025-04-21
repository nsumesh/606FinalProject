import osmnx as ox
import matplotlib.pyplot as plt
drive_map = ox.graph_from_place("Washington, District of Columbia, USA", network_type="drive")
ox.plot_graph(drive_map, node_size=10, edge_color="#999999")
white_house = (38.8977, -77.0365)
subgraph = ox.graph_from_point(white_house, dist=1000, network_type="drive")
ox.plot_graph(subgraph, node_size=10, edge_color="#336699")
