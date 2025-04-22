def bellman_ford(graph, src):
    distance = [float('inf')] * graph.V
    distance[src] = 0  
    
    for _ in range(graph.V - 1):
        for u in range(graph.V):
            for v, w in graph.adj[u]:
                if distance[u] != float('inf') and distance[u] + w < distance[v]:
                    distance[v] = distance[u] + w

    # Check for negative-weight cycles
    has_negative_cycle = False
    for u in range(graph.V):
        for v, w in graph.adj[u]:
            if distance[u] != float('inf') and distance[u] + w < distance[v]:
                has_negative_cycle = True
                break
        if has_negative_cycle:
            break

    return distance, has_negative_cycle