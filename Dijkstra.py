#Implementing a heap for the Dijkstra
import time
import tracemalloc

class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, item):
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        if len(self.heap) == 0:
            return None
        self._swap(0, len(self.heap) - 1)
        min_item = self.heap.pop()
        self._sift_down(0)
        return min_item

    def _sift_up(self, index):
        parent = (index - 1) // 2
        while index > 0 and self.heap[index][0] < self.heap[parent][0]:
            self._swap(index, parent)
            index = parent
            parent = (index - 1) // 2

    def _sift_down(self, index):
        child = 2 * index + 1
        while child < len(self.heap):
            right = child + 1
            if right < len(self.heap) and self.heap[right][0] < self.heap[child][0]:
                child = right
            if self.heap[index][0] <= self.heap[child][0]:
                break
            self._swap(index, child)
            index = child
            child = 2 * index + 1

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def __len__(self):
        return len(self.heap)
# start = ox.distance.nearest_nodes(drive_map, landmarks["White House"][1], landmarks["White House"][0])
# end = ox.distance.nearest_nodes(drive_map, landmarks["Union Station"][1], landmarks["Union Station"][0])

### Djikstra takes starting point and end point
def dijkstra(graph, source, target):
    start_time = time.perf_counter()
    tracemalloc.start()
    ## The output will be path and shortest distance 
    dist = {node: float('inf') for node in graph.nodes}
    prev = {node: None for node in graph.nodes}
    dist[source] = 0

    heap = MinHeap()
    heap.push((0, source))

    while len(heap) > 0:
        curr_dist, u = heap.pop()

        if u == target:
            break

        if curr_dist > dist[u]:
            continue

        for v, edges in graph[u].items():
            min_edge = min(edges.values(), key=lambda x: x['weight'])
            alt = dist[u] + min_edge['weight']

            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                heap.push((alt, v))

    # path reconstruction
    path = []
    u = target
    while u is not None:
        path.insert(0, u)
        u = prev[u]
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_time = time.perf_counter()
    stats = {'execution_time': end_time-start_time,
        'current_memory': current / 10**3,
        'peak_memory': peak / 10**3}
    return path, dist[target], stats
