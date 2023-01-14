from collections import defaultdict
from functools import cache
from itertools import permutations
from math import inf
from queue import PriorityQueue

# Parse data
# Identify coords of goal nodes
# Create map
# Only node 5 might lie on shortest path between two others
# All others in dead ends
# Start at 0:
# Map blocked spaces bordering open to False
# For each node pair, find shortest path, including any other nodes traversed
# Brute-force shortest tour, since only 9! possibilities


def neighbor_finder(xmin, xmax, ymin, ymax, graph):
    @cache
    def inner(coord):
        result = set()
        if coord.real > xmin and graph[(target := coord - 1)] >= 0:
            result.add(target)
        if coord.real < xmax and graph[(target := coord + 1)] >= 0:
            result.add(target)
        if coord.imag > ymin and graph[(target := coord - 1j)] >= 0:
            result.add(target)
        if coord.imag < ymax and graph[(target := coord + 1j)] >= 0:
            result.add(target)
        return result

    return inner


def l1(x, y):
    return abs(x.real - y.real) + abs(x.imag - y.imag)


def parse(lines):
    result = defaultdict(lambda: 10)
    nodes = {}
    xmax = len(lines[0]) - 1
    ymax = len(lines) - 1
    xmin = ymin = 0
    closed = "#"

    for j, line in enumerate(lines):
        for i, char in enumerate(line):
            if char == closed:
                result[complex(i, j)] = -1
            elif char.isdigit():
                digit = int(char)
                coord = complex(i, j)
                nodes[digit] = coord
                result[coord] = digit
    return result, nodes, xmin, xmax, ymin, ymax


def find_path(start, end):
    f_score = defaultdict(lambda: inf)
    f_score[start] = l1(start, end)
    g_score = defaultdict(lambda: inf)
    g_score[start] = 0

    Q = PriorityQueue()
    Q.put((f_score[start], hash(start), start), block=False)

    while Q.qsize():
        _, _, current_node = Q.get(block=False)
        if current_node == end:
            continue

        for neighbor in neighbors(current_node):
            # Since neighbors are directly connected
            candidate_g_score = g_score[current_node] + 1
            if candidate_g_score < g_score[neighbor]:
                estimate = l1(neighbor, end)
                # came_from[neighbor] = current_node
                g_score[neighbor] = candidate_g_score
                f_score[neighbor] = candidate_g_score + estimate
                # if neighbor not in visited:
                Q.put((estimate, hash(neighbor), neighbor), block=False)

    return g_score[end]


def shortest_tour(paths):
    perms = permutations(k for k in paths.keys() if k > 0)
    part1 = part2 = inf
    distance = i = 0
    iterations = range(len(paths) - 2)

    for perm in perms:
        distance += paths[0][perm[0]]
        for i in iterations:
            distance += paths[perm[i]][perm[i + 1]]

        part1 = min(part1, distance)
        distance += paths[perm[i + 1]][0]
        part2 = min(part2, distance)
        # if distance < best:
        #     best = distance
        #     best_tour = perm
        distance = 0
    return part1, part2  # , best_tour


with open("inputs/day24.txt") as f:
    raw_input = f.read().splitlines()

graph, nodes, xmin, xmax, ymin, ymax = parse(raw_input)
neighbors = neighbor_finder(xmin, xmax, ymin, ymax, graph)

shortest = defaultdict(lambda: {})
done = set()
for start_node, start in nodes.items():
    for end_node, end in nodes.items():
        if start_node != end_node and (start_node, end_node) not in done:
            distance = find_path(start, end)
            shortest[start_node][end_node] = shortest[end_node][start_node] = distance
            done.add((start_node, end_node))
            done.add((end_node, start_node))

part1, part2 = shortest_tour(shortest)
print(part1)
print(part2)
