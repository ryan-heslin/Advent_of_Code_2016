with open("inputs/day1.txt") as f:
    raw_input = f.read().split(", ")

# starting east, going counterclockwise
directions = {0: [1, 0], 1: [0, 1], 2: [-1, 0], 3: [0, -1]}
modulus = len(directions)
translations = {"R": -1, "L": 1}

position = [0, 0]
direction = 1

visited = [tuple(position)]
part2_undone = True
part2 = None

# raw_input = ["R8", "R4", "R4", "R8"]

# TODO check if any old position between current position and position after current displacement
# Better: track xend-yend of each segment, check for intersections

# l1 norm
def l1(x):
    return sum([abs(el) for el in x])


def find_overlap(x, y):
    x = sorted(x)
    if y[0] < y[1]:
        rng = range(y[0], y[1] + 1, 1)
    else:
        rng = range(y[0], y[1] - 1, -1)
    for pos in rng:
        if x[0] <= pos <= x[1]:
            return pos
    return None


def segment_intersection(seg1, seg2):
    # breakpoint()

    # Find whether each segment is vertical or horizontal
    seg1_constant = 0 if seg1[0][0] == seg1[1][0] else 1
    seg2_constant = 0 if seg2[0][0] == seg2[1][0] else 1
    seg1_variable = (seg1_constant + 1) % 2
    seg2_variable = (seg2_constant + 1) % 2
    # vertical-vertical or horizontal-horizontal
    if seg1_constant == seg2_constant:
        if seg1[0][seg1_constant] == seg2[0][seg2_constant]:
            result = find_overlap(
                (seg1[0][seg1_variable], seg1[1][seg1_variable]),
                (seg2[0][seg2_variable], seg2[1][seg2_variable]),
            )
        else:
            # Parallel lines
            return None

        # Choice of segment to subset irrelevant here
        if result is not None:
            # Both vertical
            if seg1_constant == 0:
                return (seg1[0][seg1_constant], result)
            # Both horizontal
            else:
                return (result, seg1[0][seg1_constant])
        else:
            return result
    # vertical-horizontal or horizontal-vertical
    else:
        # horizontal-vertical
        # Candidate amounts to reading of solution of diagonal system of equations
        # Choice of endpoint is arbitrary, since these dimensions are constant
        if seg1_constant == 1 and seg2_constant == 0:
            candidate = (seg2[0][0], seg1[0][1])
        # vertical-horizontal
        elif seg1_constant == 0 and seg2_constant == 1:
            candidate = (seg1[0][0], seg2[0][1])
        # Verify possible intersection actually between both pairs of endpoints
        xes = [sorted((seg1[0][0], seg1[1][0])), sorted((seg2[0][0], seg2[1][0]))]
        ys = [sorted((seg1[0][1], seg1[1][1])), sorted((seg2[0][1], seg2[1][1]))]
        for i in range(len(xes)):
            if not (
                xes[i][0] <= candidate[0] <= xes[i][1]
                and ys[i][0] <= candidate[1] <= ys[i][1]
            ):
                return None
        return candidate


# Both horizontal
assert segment_intersection([(0, 0), (8, 0)], [(20, 0), (-2, 0)]) == (8, 0)
assert segment_intersection([(0, 0), (8, 0)], [(7, 0), (8, 0)]) == (7, 0)
assert segment_intersection([(0, 0), (8, 0)], [(8, 0), (999, 0)]) == (8, 0)
assert segment_intersection([(-999, 0), (8, 0)], [(999, 0), (8, 0)]) == (8, 0)
# Both vertical
assert segment_intersection([(0, 0), (0, 8)], [(0, 20), (0, -2)]) == (0, 8)
assert segment_intersection([(0, 0), (0, 8)], [(0, 20), (0, 8)]) == (0, 8)

assert segment_intersection([(0, 0), (8, 0)], [(4, -4), (4, -1)]) is None
assert find_overlap((3, 5), (9, 4)) == 5
assert find_overlap((3, 5), (10, 5)) == 5

assert segment_intersection([(0, 0), (8, 0)], [(4, -4), (4, 4)]) == (4, 0)
# Vertical-horizontal
assert segment_intersection([(0, 0), (0, 8)], [(-4, 4), (4, 4)]) == (0, 4)
assert segment_intersection([(0, 0), (0, 8)], [(-4, 4), (4, 0)]) == (0, 4)
# Parallel horizontal
assert segment_intersection([(0, 0), (8, 0)], [(8, -4), (4, -4)]) is None


# Checks if coordinate falls on line segment connecting two other coordinates
# def between(start, end, check):
#
#     constant_dim = 0 if start[0] == end[0] else 1
#     changed_dim = (constant_dim + 1) % 2
#
#     if start[constant_dim] == end[constant_dim] == check[constant_dim]:
#         result = (
#             start[changed_dim] <= check[changed_dim] <= end[changed_dim]
#             or end[changed_dim] <= check[changed_dim] <= start[changed_dim]
#         )
#     else:
#         result = False
#     return result
#
#
for i, instr in enumerate(raw_input):
    direction = (direction + translations[instr[0]]) % modulus
    distance = int(instr[1:])
    position[0] += directions[direction][0] * distance
    position[1] += directions[direction][1] * distance
    new_position = tuple(position)

    if part2_undone:
        old_position = visited[-1]

        if old_position[0] == new_position[0]:

        visited.append(new_position)
        new_segment = visited[-2:]
        print("\n\n\n")
        print("----------------")
        for i in range(0, len(visited) - 2):
            print([visited[i], visited[i + 1]])
            print(new_segment)
            print("\n")
            intersection = segment_intersection(
                [visited[i], visited[i + 1]], new_segment
            )
            if intersection is not None and intersection != new_segment[0]:
                print(intersection)
                part2 = l1(intersection)
                part2_undone = False
                break

# 126 low, but looks accurate - missed one before
part1 = l1(position)
print(part1)
print(part2)
