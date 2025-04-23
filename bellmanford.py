def bellman_ford(graph, src):
    distance = {node : float('inf') for node in graph.nodes}
    distance[src] = 0  

    for _ in range(len(graph.nodes) - 1):
        for u, v, data in graph.edges(data=True):
            w = data.get('weight',1)
            if distance[u] != float('inf') and distance[u] + w < distance[v]:
                distance[v] = distance[u] + w

    # Check for negative-weight cycles
    has_negative_cycle = False
    for u, v, data in graph.edges(data=True):
        w = data.get('weight',1)        
        if distance[u] != float('inf') and distance[u] + w < distance[v]:
            has_negative_cycle = True
            break

    return distance, has_negative_cycle