import time
import tracemalloc

import osmnx as ox
import numpy as np
import matplotlib.pyplot as plt

from astar import astar


def benchmark_memory(G, landmarks):

    def get_osm_memory(G, s: int, t: int):
        tracemalloc.reset_peak()
        tracemalloc.start()

        _ = ox.shortest_path(G, s, t, weight='length')

        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return peak

    osm_memory = []
    astar_memory = []

    for u, u_coords in landmarks.items():
        for v, v_coords in landmarks.items():
            if u == v:
                continue

            start = ox.distance.nearest_nodes(G, u_coords[1], u_coords[0])
            end = ox.distance.nearest_nodes(G, v_coords[1], v_coords[0])

            osm_mem = get_osm_memory(G, start, end)
            _, _, stat_astar = astar(G, start, end)

            osm_memory.append(osm_mem)
            astar_memory.append(stat_astar['execution_time'])

    avg_memory_osm = np.mean(osm_memory)
    avg_memory_astar = np.mean(astar_memory)

    plt.figure(figsize=(10, 6))
    plt.bar(['OSMnx', 'A*'], [avg_memory_osm, avg_memory_astar])
    plt.ylabel('Memory Usage (in KB)')
    plt.title('Average Memory Usage: A* vs OSMnx (90 Queries)')
    plt.show()


def benchmark_time(G, landmarks):

    def get_osm_time(G, s: int, t: int):
        start_time = time.perf_counter()
        _ = ox.shortest_path(G, s, t, weight='length')
        end_time = time.perf_counter()

        return end_time - start_time

    osm_time = []
    astar_time = []

    for u, u_coords in landmarks.items():
        for v, v_coords in landmarks.items():
            if u == v:
                continue

            start = ox.distance.nearest_nodes(G, u_coords[1], u_coords[0])
            end = ox.distance.nearest_nodes(G, v_coords[1], v_coords[0])

            osm_t = get_osm_time(G, start, end)
            _, _, stat_astar = astar(G, start, end)

            osm_time.append(osm_t)
            astar_time.append(stat_astar['execution_time'])


    # percentage difference plot
    percentage_diff_astar = [
        (osm - astar) / osm * 100 for osm, astar in zip(osm_time, astar_time)
    ]

    avg_percentage_diff_astar = np.mean(percentage_diff_astar)

    plt.figure(figsize=(10, 6))

    colors = ['red' if x < 0 else 'skyblue' for x in percentage_diff_astar]
    plt.bar(range(len(percentage_diff_astar)), percentage_diff_astar, color=colors)

    plt.title('Percentage Difference in Execution Time: A* vs OSMnx')
    plt.xlabel('Query')
    plt.ylabel('Percentage Difference (%)')
    plt.axhline(
        y=avg_percentage_diff_astar, 
        color='green',
        linestyle='--', 
        label=f'Average: {avg_percentage_diff_astar:.2f}%'
    )
    plt.legend()
    plt.show()

    # total execution time plot
    total_time_osmnx = sum(osm_time)
    total_time_astar = sum(astar_time)

    plt.figure(figsize=(10, 6))
    plt.bar(['OSMnx', 'A*'], [total_time_osmnx, total_time_astar])
    plt.ylabel('Total Execution Time (in seconds)')
    plt.title('Total Execution Time: A* vs OSMnx (90 Queries)')
    plt.show()

def main(graph_path='maps/drive_map.graphml', landmarks=None):

    G = ox.io.load_graphml(graph_path)
    if landmarks is None:
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

    print("Running memory benchmark...")
    benchmark_memory(G, landmarks)
    print("Memory benchmark complete.")

    print("Running time benchmark...")
    benchmark_time(G, landmarks)
    print("Time benchmark complete.")

if __name__ == "__main__":
    main()