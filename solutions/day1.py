from collections import defaultdict


def count_up(start, end):
    return range(start + 1, end + 1, 1)


def count_down(start, end):
    return range(start - 1, end - 1, -1)


# l1 norm
def l1(x):
    return sum([abs(el) for el in x])


def segment_intersection(seg1, seg2):
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


with open("inputs/day1.txt") as f:
    raw_input = f.read().split(", ")

# starting east, going counterclockwise
directions = {0: [1, 0], 1: [0, 1], 2: [-1, 0], 3: [0, -1]}
modulus = len(directions)
translations = {"R": -1, "L": 1}

start = (0, 0)
position = list(start)
direction = 1

visited = defaultdict(lambda: False)
old_position = start
visited[start] = part2_undone = True
part2 = None


for i, instr in enumerate(raw_input):
    direction = (direction + translations[instr[0]]) % modulus
    distance = int(instr[1:])
    position[0] += directions[direction][0] * distance
    position[1] += directions[direction][1] * distance
    new_position = tuple(position)
    this_point = start

    if part2_undone:
        if old_position[0] == new_position[0]:
            fixed = old_position[0]
            new_point = lambda fixed, i: (fixed, i)
            if old_position[1] < new_position[1]:
                rng = count_up(old_position[1], new_position[1])
            else:
                rng = count_down(old_position[1], new_position[1])
        # Horizontal (constant y-value)
        else:
            fixed = old_position[1]
            new_point = lambda fixed, i: (i, fixed)
            if old_position[0] < new_position[0]:
                rng = count_up(old_position[0], new_position[0])
            else:
                rng = count_down(old_position[0], new_position[0])
        for i in rng:
            this_point = new_point(fixed, i)
            if visited[this_point]:
                part2 = l1(this_point)
                part2_undone = False
                break
            else:
                visited[this_point] = True
        else:
            old_position = this_point


part1 = l1(position)
print(part1)
print(part2)
