import heapq
import osmnx as ox

import time
import tracemalloc

class PriorityQueue():
    def __init__(self):
        self.elements = []
    def push(self, k, v):
        heapq.heappush(self.elements, (k, v))
    def pop(self):
        return heapq.heappop(self.elements)[1]
    def empty(self):
        return not self.elements
  

def astar(G, s: int, t: int) -> tuple[list[int], float, dict[str, float]]: 
    """
    A* algorithm for finding the shortest path between two nodes in a graph

    Args:
        G (NetworkX MutiDiGraph): input graph
        s (int): start node
        t (int): target node

    Returns:
        path (list[int]): list of nodes in the shortest path from s to t
        dist (float): distance of the shortest path from s to t (in meters)
        stats (dict): dictionary containing execution time (in s) and memory usage (in KB)
    """

    tracemalloc.start()
    start_time = time.perf_counter()

    t_x, t_y = G.nodes[t]['x'], G.nodes[t]['y'] # target coordinates

    def heuristic(v): 
        # L2 distance between node v and target node t

        v_x, v_y = G.nodes[v]['x'], G.nodes[v]['y'] # (lat, lon) coordinates
        return ox.distance.euclidean(v_y, v_x, t_y, t_x)

    Q = PriorityQueue()
    dist = {}
    prev = {}

    dist[s] = 0
    prev[s] = -1

    Q.push(heuristic(s), s)
    while not Q.empty():
        u = Q.pop()
        if u == t: # target found
            break

        for v, data_dict in G[u].items():
            # traverse all edges from u to v (G is a multi digraph)
            for _, data in data_dict.items():
                d = dist[u] + data.get('length', float('inf')) # assume non-traversable path by default
                if d == float('inf'):
                    continue

                if (v not in dist) or (d < dist[v]):
                    dist[v] = d
                    prev[v] = u
                    priority = dist[v] + heuristic(v)
                    Q.push(priority, v)

    # get path
    if t not in prev: # no path to t
        return [], -1

    path = []
    u = t
    while u != s:
        path.append(u)
        u = prev[u]
    path.append(s)
    path.reverse()

    end_time = time.perf_counter()
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    stats = {
        'execution_time': end_time - start_time,
        'current_memory': current / 10**3,
        'peak_memory': peak / 10**3
    } 

    return path, dist[t], stats