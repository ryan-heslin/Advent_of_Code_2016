from itertools import combinations
from math import inf


def neighbor_finder(xmin, xmax, ymin, ymax):
    def inner(coord):
        result = set()
        if coord[0] > xmin:
            result.add((coord[0] - 1, coord[1]))
        if coord[0] < xmax:
            result.add((coord[0] + 1, coord[1]))

        if coord[1] > ymin:
            result.add((coord[0], coord[1] - 1))
        if coord[1] < ymax:
            result.add((coord[0], coord[1] + 1))
        return result

    return inner


class Node:
    def __init__(self, coords, size, used, available) -> None:
        self.coords = coords
        self.size = size
        self.used = used
        self.available = available
        self.neighbors = None
        self.empty = self.used == 0
        self.full = self.available == 0

    def add_neighbors(self, func):
        self.neighbors = func(self.coords)
        return self

    def __repr__(self) -> str:
        return f"{self.coords} size: {self.size} used : {self.used}"

    def can_move(self, other):
        return other.available >= self.used


def parse(lines):
    result = []
    xmin = ymin = inf
    xmax = ymax = -inf
    for line in lines:
        if line[0] == "/":
            parts = line.split()
            node = parts[0]
            coords = tuple(int(x[1:]) for x in node.split("-")[1:])
            xmin = min(xmin, coords[0])
            xmax = max(xmax, coords[0])
            ymin = min(ymin, coords[1])
            ymax = max(ymax, coords[1])

            args = (int(x.rstrip("T")) for x in parts[1:4])
            result.append(Node(coords, *args))
    return result, {"xmin": xmin, "xmax": xmax, "ymin": ymin, "ymax": ymax}


def find_pairs(nodes):
    combos = combinations(nodes.values(), 2)
    return sum(
        (0 < combo[0].used <= combo[1].available)
        + (0 < combo[1].used <= combo[0].available)
        for combo in combos
    )


with open("inputs/day22.txt") as f:
    raw_input = f.read().splitlines()

nodes, extents = parse(raw_input)
add_neighbors = neighbor_finder(**extents)
nodes = {node.coords: node.add_neighbors(add_neighbors) for node in nodes}

part1 = find_pairs(nodes)
print(part1)

free = next(filter(lambda x: x.empty, nodes.values())).coords

can_move = {
    key: {coord: node.can_move(nodes[coord])}
    for key, node in nodes.items()
    for coord in node.neighbors
}

# too_small = 0
# for i in range(free[0] + 1, extents["xmax"]):
#     too_small += nodes[(i - 1, free[1])].size < nodes[(i, free[1])].used
#
# for j in range(free[1] + 1, extents["ymin"] - 1):
#     too_small += (
#         nodes[(extents["xmax"] - 1, j - 1)].size
#         < nodes[(extents["xmax"] - 1, j)].used.used
#     )
# # TODO count "full" nodes; there should be five to add to total tiles
# for i in range(1, extents["xmax"]):
#     too_small += nodes[(i - 1, 0)].size < nodes[(i, 0)].used
#
goal = (extents["xmin"], extents["ymin"])
target = (extents["xmax"], extents["ymin"])
# TODO: figure out whether this is just accidentally right

full = list(filter(lambda k: nodes[k].used > 100, nodes.keys()))

part2 = 0
xes = [coord[0] for coord in filter(lambda coord: coord[1] < free[1], full)]
if free[0] in xes:
    left_deviation = right_deviation = 2
    for i in range(free[0] - 1, min(xes) - 1, -1):
        if not i in xes:
            break
        left_deviation += 2
    for i in range(free[0] + 1, max(xes) + 1):
        if not i in xes:
            break
        right_deviation += 2
    part2 += min((left_deviation, right_deviation))

too_small_top = list(
    filter(
        lambda k: k[1] == 0 and nodes[k].size < nodes[(k[0], 1)].used < 10, nodes.keys()
    )
)
part2 += (
    abs(free[0] - target[0])
    # Initial shift down and left to clear node left of target, plus initial movement left of target
    + abs(free[1] - target[1])
    # Five moves for each subsequent movement, including onto goal node
    + (5 * (abs(goal[0] - target[0]) - 1))
)

# while cur.x > goal do
#  if nodes[]
target_size = nodes[target].size
assert all(
    nodes[(x, 0)].size <= target_size for x in range(extents["xmin"], extents["xmax"])
)

print(part2)
# Must be 3 in the way
# Just add 6 to correct formula?
