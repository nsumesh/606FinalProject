import time
import tracemalloc

def bellman_ford(graph, src):
    """
    Bellman-Ford algorithm to find the shortest path from a source node to all other nodes in a graph.
    Args:
        graph (networkx.Graph): The input graph.
        src (int): The source node.
    Returns:
        distance (dict): A dictionary with nodes as keys and their shortest distance from the source as values.
        has_negative_cycle (bool): True if there is a negative-weight cycle in the graph, False otherwise.
        stats (dict): A dictionary containing memory and time usage statistics.
    """
    # Start memory and time tracking
    start_time = time.time()
    tracemalloc.start()

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

    # Stop memory and time tracking
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Create a dictionary for memory and time usage
    stats = {
        'current_memory': current / 10**3,  # Convert to KB
        'peak_memory': peak / 10**3,        # Convert to KB
        'execution_time': end_time - start_time # Time in seconds
    }


    return distance, has_negative_cycle, stats