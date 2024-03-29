from collections import defaultdict
from collections import deque
from functools import cache
from math import inf
from queue import PriorityQueue


def A_star(start, graph, h):
    came_from = {}
    visited = set()
    f_score = defaultdict(lambda: inf)
    f_score[start] = h(start)
    g_score = defaultdict(lambda: inf)
    g_score[start] = 0

    Q = PriorityQueue()
    Q.put((f_score[start], start), block=False)

    while Q.qsize():
        _, current_node = Q.get(block=False)

        for neighbor in graph[current_node].find_neighbors():
            # Since neighbors are directly connected
            candidate_g_score = g_score[current_node] + 1
            if candidate_g_score < g_score[neighbor]:
                estimate = h(neighbor)
                came_from[neighbor] = current_node
                g_score[neighbor] = candidate_g_score
                f_score[neighbor] = candidate_g_score + estimate
                if neighbor not in visited:
                    Q.put((estimate, neighbor), block=False)

    return came_from


def reconstruct_path(came_from, current):
    S = deque([current])
    while current in came_from.keys():
        current = came_from[current]
        S.appendleft(current)
    return S


def l1_maker(dest):
    @cache
    def result(start):
        return sum(abs(start[i] - dest[i]) for i in range(len(start)))

    return result


class Graph:
    def __init__(self):
        self.map = {}

    def __setitem__(self, k, v):
        self.map[k] = v

    def __getitem__(self, k):
        if len(k) != 2:
            raise ValueError
        if k not in self.map.keys():
            self.__setitem__(k, Node(*k, FAVORITE, self))
        return self.map[k]


class Node:
    def __init__(self, x, y, FAVORITE, graph) -> None:
        self.x = x
        self.y = y
        self.FAVORITE = FAVORITE
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
            self.neighbors.add((candidate.x, candidate.y))

    def coord_sum(self, x, y):
        return ((x**2) + (3 * x) + (2 * x * y) + y + (y**2)) + self.FAVORITE

    def open(self, x, y):
        return (self.coord_sum(x, y).bit_count() % 2) == 0


FAVORITE = 1362

start = (1, 1)
goal = (31, 39)
graph = Graph()
graph[start] = Node(*start, FAVORITE, graph)
graph[goal] = Node(*goal, FAVORITE, graph)
h = l1_maker(goal)

came_from = A_star(start, graph, h)
part1 = len(reconstruct_path(came_from, goal)) - 1
print(part1)

accessible = set()
cutoff = 50 + 1
for node in came_from.keys():
    if node not in accessible:
        path = list(reconstruct_path(came_from, node))
        accessible.update(path[: min(cutoff, len(path))])

print(len(accessible))
