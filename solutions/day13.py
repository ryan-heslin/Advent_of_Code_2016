from collections import defaultdict
from collections import deque
from functools import cache
from math import inf

favorite = 10
# Default to
graph = defaultdict(lambda k: Node(k[0], k[1], favorite, graph))

start = (1, 1)
goal = (7, 4)


def dijkstra(start, graph):
    dist = defaultdict(lambda: inf)
    prev = defaultdict(lambda: None)
    dist[start] = 0

    Q = deque([start])
    visited = set()

    while Q:
        current = Q.popleft()
        if current == goal:
            break
        visited.add(current)

        for node in graph[current].find_neighbors():
            alt = dist[current] + 1
            if alt < dist[node]:
                dist[node] = alt
                prev[node] = current

    return dist, prev


def reconstruct_path(target, prev):
    S = deque([])
    u = target
    while u:
        S.appendleft(u)
        u = prev[u]
    return S


def l1(x, y):
    return sum(abs(x[i] - y[i]) for i in range(len(x)))


class Node:
    def __init__(self, x, y, favorite, graph) -> None:
        self.x = x
        self.y = y
        self.favorite = favorite
        self.is_open = self.open(self.x, self.y)
        self.graph = graph
        self.neighbors = set()
        self.neighbors_found = False

    @cache
    def find_neighbors(self):
        if not self.neighbors_found:
            self.verify_neighbor((self.x + 1, self.y))
            self.verify_neighbor((self.x, self.y + 1))
            if self.x > 0:
                self.verify_neighbor((self.x - 1, self.y))
            if self.y > 0:
                self.verify_neighbor((self.x, self.y - 1))
            self.neighbors_found = True
        return self.neighbors

    def verify_neighbor(self, coord):
        candidate = self.graph[coord]
        if candidate.is_open:
            self.neighbors.add(candidate)

    def coord_sum(self, x, y):
        return (x**2 + 3 * x + 2 * x * y + y + y**2) + self.favorite

    @staticmethod
    def count_ones(num):
        return bin(num).count("1")

    def open(self, x, y):
        return not (self.coord_sum(x, y).bit_count() % 2)


graph[start] = Node(*start, favorite, graph)
graph[goal] = Node(*goal, favorite, graph)
