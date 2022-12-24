from collections import defaultdict
from functools import cache

favorite = 10
# Default to
map = defaultdict(lambda k: Node(k[0], k[1], favorite, map))

start = (1, 1)
goal = (7, 4)


class Node:
    def __init__(self, x, y, favorite, map) -> None:
        self.x = x
        self.y = y
        self.favorite = favorite
        self.is_open = self.open(self.x, self.y)
        self.map = map
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
        candidate = self.map[coord]
        if candidate.open:
            self.neighbors.add(candidate)

    def coord_sum(self, x, y):
        return (x**2 + 3 * x + 2 * x * y + y + y**2) + self.favorite

    @staticmethod
    def count_ones(num):
        return bin(num).count("1")

    def open(self, x, y):
        return not bool(__class__.count_ones(self.coord_sum(x, y)) % 2)


map[start] = Node(*start, favorite, map)
map[goal] = Node(*goal, favorite, map)
