from bellmanford import bellman_ford
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
