from hashlib import md5
from queue import PriorityQueue


def l1_maker(target):
    def result(start):
        diff = start - target
        return int(abs(diff.real) + abs(diff.imag))

    return result


def search(passcode, start, goal, distance, x_bounds, y_bounds, find_longest):
    # distance, coord, previous
    weight = -1 if find_longest else 1
    Q = PriorityQueue()
    Q.put((weight * distance(start), passcode, start))
    directions = {"U": -1j, "D": 1j, "L": -1, "R": 1}
    xmin, xmax = x_bounds
    ymin, ymax = y_bounds
    best = None

    while Q.qsize():
        _, chars, coord = Q.get()
        # print(coord, chars)
        if coord == goal:
            if best is None:
                best = chars
            else:
                if find_longest:
                    best = max(best, chars, key=len)
                else:
                    best = min(best, chars, key=len)
            continue
        if (best and not find_longest) and len(chars) >= len(best):
            continue

        open = check_doors(get_hash(chars))

        for char, shift in directions.items():
            if open[char]:
                new = coord + shift
                if xmin <= new.real <= xmax and ymin <= new.imag <= ymax:
                    Q.put((weight * distance(new), chars + char, new))

    return best


# True if door open: up, down, left, right
def check_doors(hash):
    return dict(zip("UDLR", (char in set("bcdef") for char in hash[:4])))


def get_hash(chars):
    return md5(chars.encode("utf-8")).hexdigest()


def parse(lines):
    start = goal = None
    xmax = (len(lines[0]) - 2) // 2
    ymax = (len(lines) - 2) // 2

    for j, line in enumerate(lines[1:]):
        if "S" in line:
            start = complex(line[1 : (xmax + 1)].find("S"), j // 2)
        elif line[-1] == "|":
            goal = complex(xmax, j // 2)
    return start, goal, xmax, ymax


raw_input = """#########
#S| | | #
#-#-#-#-#
# | | | #
#-#-#-#-#
# | | | #
#-#-#-#-#
# | | |
####### V
"""
lines = raw_input.splitlines()
passcode = "rrrbmfta"
index = len(passcode)
start, goal, xmax, ymax = parse(lines)
distance = l1_maker(goal)
part1 = search(passcode, start, goal, distance, (0, xmax), (0, ymax), False)
if part1:
    print(part1[index:])

part2 = search(passcode, start, goal, distance, (0, xmax), (0, ymax), True)
if part2:
    print(len(part2[index:]))
