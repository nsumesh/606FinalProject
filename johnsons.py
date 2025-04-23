from bellmanford import bellman_ford
from Dijkstra import dijkstra
import networkx as nx
import heapq

def johnsons(G):
    s = 'dummy'
    graph = G.copy()
    graph.add_node(s)
    for node in graph.nodes:
        if node!=s:
            graph.add_edge(s, node, weight=0)
    bellman_ford_graph, has_negative_cycle = bellman_ford(graph,s)

    if(not has_negative_cycle):
        raise Exception('Negative cycle present in graph')
    
    new_graph = nx.MultiDiGraph()
    for u, v, key, data in graph.edges(data=True):
        weight = data['weight']
        new_weight = weight + bellman_ford_graph[u]-bellman_ford_graph[v]
        new_graph.add_edge(u, v, key=key, weight=new_weight, original_weight = weight)

    pairs = {}
    for node in graph.nodes:
        path, distance = {},{}
        for t in graph.nodes:
            if t==node:
                path[t] = [node]
                distance[t] = 0
            else:
                result, d = dijkstra(new_graph, node, t)
                path[t] = result
                distance[t] = d - bellman_ford_graph[node] + bellman_ford_graph[t]
        pairs[node] = (distance, path)
    return pairs