import math
import heapq # NOTE: use custom priority queue implementation instead?

class PriorityQueue():
    def __init__(self):
        self.elements = []
    def push(self, k, v):
        heapq.heappush(self.elements, (k, v))
    def pop(self):
        return heapq.heappop(self.elements)[1]
    def empty(self):
        return not self.elements
  
# an admissible heuristic function (does not overestimate distance to target=>optimal sol)

def astar(G, s: int, t: int) -> tuple[list[int], float]: 
    """
    A* algorithm for finding the shortest path between two nodes in a graph

    Parameters:
        G (NetworkX MutiDiGraph): input graph
        s (int): start node
        t (int): target node

    Returns:
        path (list[int]): list of nodes in the shortest path from s to t
        dist (float): distance of the shortest path from s to t
    """

    t_x, t_y = G[t]['x'], G[t]['y'] # target coordinates

    def heuristic(v): 
        # L2 distance between nodes u and target node t

        v_x, v_y = G[v]['x'], G[v]['y']
        return math.sqrt((v_x - t_x)**2 + (v_y - t_y)**2)

    frontier = PriorityQueue()
    dist = {}
    prev = {}

    dist[s] = 0
    prev[s] = -1
    frontier.push(heuristic(s), s)
    while not frontier.empty():
        u = frontier.pop()
        if u == t: # target found
            break
        for v, data in G[u].items():
            # FIXME: assumes only one edge exists b/w u and v but G is multi digraph
            d = dist[u] + data[0]['length']
            if (v not in dist) or (d < dist[v]):
                dist[v] = d
                prev[v] = u
                priority = dist[v] + heuristic(v)
                frontier.push(priority, v)

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

    return path, dist[t]