from bellmanford import bellman_ford
from Dijkstra import dijkstra
import networkx as nx
import heapq

def johnsons(graph, only_source=None):
    dummy = 'DUMMY'
    G = graph.copy()
    G.add_node(dummy)
    for node in graph.nodes:
        G.add_edge(dummy, node, weight=0)

    h, has_neg = bellman_ford(G, dummy)
    if has_neg:
        raise Exception("Negative weight cycle detected")

    reweighted = nx.MultiDiGraph()
    for u, v, key, data in graph.edges(keys=True, data=True):
        w = data['weight']
        w_prime = w + h[u] - h[v]
        reweighted.add_edge(u, v, key=key, weight=w_prime, original_weight=w)

    all_pairs = {}
    sources = [only_source] if only_source else graph.nodes
    for u in sources:
        dist_u = {}
        path_u = {}
        for v in graph.nodes:
            # path, d = dijkstra(reweighted, u, v)
            # if d != float('inf'):
            #     dist_u[v] = d - h[u] + h[v]
            #     path_u[v] = path
            try:
                path = nx.shortest_path(reweighted, u, v, weight='weight')
                d = nx.shortest_path_length(reweighted, u, v, weight='weight')
            except nx.NetworkXNoPath:
                path = []
                d = float('inf')
        all_pairs[u] = (dist_u, path_u)
    return all_pairs
