def floyd_warshall(graph):
    n = len(graph.nodes)
    
    dist = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0  
    
    # Initialize distances with direct edges
    for u, v, data in graph.edges(data=True):
        w = data.get('weight', 1)
        if w < dist[u][v]:  
            dist[u][v] = w
    
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    # Check for negative-weight cycles
    has_negative_cycle = any(dist[i][i] < 0 for i in range(n))
    
    return dist, has_negative_cycle