import re
from collections import defaultdict
from functools import cache
from math import inf
from math import log2
from queue import PriorityQueue


iter_floors = (4, 3, 2)


def display(num, elements, player_bit):
    fill_digits = int(log2(player_bit))
    if num.bit_length() >= fill_digits:
        num ^= player_bit
        has_player = True
    else:
        has_player = False
    digits = (bin(num)[2:]).zfill(fill_digits)
    if has_player:
        print("Has player")
    print("".join(elements))
    print("MG" * ((fill_digits - 1) // 2))
    print(digits)


def parse(raw):
    values = {"generator": 0, "microchip": 1}
    elements = sorted(re.findall(r"[a-z]+(?:ium|gen|alt)", raw))
    filtered = []
    for el in elements:
        if el not in filtered:
            filtered.append(el)

    raw = re.sub("-compatible", "", raw)
    raw = raw.splitlines()
    raw.reverse()
    elements = dict(zip(filtered, range(len(elements))))
    result = {k: 0 for k in range(len(raw))}

    for floor, line in enumerate(raw):
        if "ium" in line or "ogen" in line:
            line = re.sub("(?=[a-z]) and ", ", ", line)
            parts = line.rstrip(".").split(", ")
            for part in parts:
                element, component = part.split(" ")[-2:]
                result[floor] |= 2 ** ((elements[element] * 2) + values[component])
    # Leftmost bit representing player on floor
    result[max(result.keys())] |= 2 ** (max(elements.values()) * 2 + 2)
    return result, elements


def h(state):
    # Reminder: A* is correct IFF h never overestimates
    s = running = 0
    for k in iter_floors:
        this_floor = state[(k - 1)]
        this_floor ^= player_bit * (this_floor >= player_bit)
        this_floor = this_floor.bit_count()
        running += this_floor
        if running > 0:
            s += 2 * max(running - 2, 0) + 1
    return s


def make_hash(state):
    return hash(
        "".join(
            bin(v)[2:].zfill(11) + str(k)
            for k, v in sorted(state.items(), key=lambda k: k[0])
        )
    )


@cache
def validate(num):
    # Chip lacking own RTG while other RTG present, even if that RTG connected.
    lone_generators = set()
    lone_microchips = set()
    element = 0
    num ^= (num >= player_bit) * player_bit

    while num:
        remainder = num % 4
        # OK if generator and microchip both present
        if remainder == 1:
            lone_generators.add(element)
        elif remainder == 2:
            lone_microchips.add(element)
        if lone_generators and lone_microchips:
            return False
        num >>= 2
    return True


def A_star(start, n_elements, h):
    # bottom floor has max value
    visited = set()
    start_hash = make_hash(start)
    f_score = defaultdict(lambda: inf)
    f_score[start_hash] = h(start)
    g_score = defaultdict(lambda: inf)
    g_score[start_hash] = 0

    bottom = max(start.keys())
    top = min(start.keys())
    goal = 2 ** (n_elements * 2 + 1) - 1
    goal_state = {k: 0 for k in start.keys()}
    goal_state[top] = goal
    goal_hash = make_hash(goal_state)
    # Floor above/below each
    possibilities = {
        floor: (floor - 1,)
        if floor == bottom
        else (floor + 1,)
        if floor == top
        else (floor - 1, floor + 1)
        for floor in start.keys()
    }

    Q = PriorityQueue()
    visited.add(start_hash)
    Q.put((f_score[start_hash], start_hash, start), block=False)

    while Q.qsize():
        h_score, current_hash, current_state = Q.get(block=False)
        if (
            h_score + g_score[current_hash] >= g_score[goal_hash]
            or current_state[top] == goal
        ):
            # breakpoint()
            continue
        # current_hash = make_hash(current_state)
        # Since it has leading bit
        current_floor, current_floor_num = max(
            current_state.items(), key=lambda x: x[1]
        )

        # Strip player bit, since we're moving
        # assert current_floor_num > player_bit
        current_floor_num ^= player_bit
        element = 0
        targets = possibilities[current_floor]
        # unchanged = {k: v for k, v in current_state.items() if k not in targets}

        generators = set()
        microchips = set()
        element = 0

        # Illegal if chip on same floor as other element's RTG, but chip lacks own RTG
        copy = current_floor_num
        while copy:
            if copy % 2 == 1:
                generators.add(element)
            copy >>= 1
            if copy % 2 == 1:
                microchips.add(element)
            copy >>= 1
            element += 1

        neighbors = []
        # If multiple chip-RTG pairs can be moved, pick 1
        # If several chips need moving each have RTGs on target floor, pick 1
        # Better h function
        # Remove player bit
        for gen in generators:
            generator_num = 2 ** (gen * 2)
            new_current_floor_num = current_floor_num ^ generator_num
            if validate(new_current_floor_num):
                # new_current_floor = {current_floor: new_current_floor_num_num}
                for target_floor in targets:
                    unchanged = {
                        floor: num
                        for floor, num in current_state.items()
                        if floor != current_floor and floor != target_floor
                    }
                    new_target_floor_num = player_bit | (
                        current_state[target_floor] | generator_num
                    )
                    # Add state if both new current floor and target floor state after move are legal
                    if validate(new_target_floor_num):
                        neighbors.append(
                            {
                                **unchanged,
                                current_floor: new_current_floor_num,
                                target_floor: new_target_floor_num,
                            }
                        )

        for chip in microchips:
            microchip_num = 2 ** (chip * 2 + 1)
            new_current_floor_num = current_floor_num ^ microchip_num
            if validate(new_current_floor_num):
                # new_current_floor = {current_floor: new_current_floor_num_num}
                for target_floor in targets:
                    unchanged = {
                        floor: num
                        for floor, num in current_state.items()
                        if floor != current_floor and floor != target_floor
                    }
                    new_target_floor_num = player_bit | (
                        current_state[target_floor] | microchip_num
                    )
                    # Add state if both new current floor and target floor state after move are legal
                    if validate(new_target_floor_num):
                        neighbors.append(
                            {
                                **unchanged,
                                current_floor: new_current_floor_num,
                                target_floor: new_target_floor_num,
                            }
                        )
        # Combinations
        if generators and microchips:
            moved_pair = False
            for generator in generators:
                for chip in microchips:
                    if generator == chip:
                        if moved_pair:
                            continue
                        moved_pair = True
                    combined_num = 2 ** (generator * 2) + 2 ** (chip * 2 + 1)
                    new_current_floor_num = current_floor_num ^ combined_num
                    if validate(new_current_floor_num):
                        for target_floor in targets:
                            unchanged = {
                                floor: num
                                for floor, num in current_state.items()
                                if floor != current_floor and floor != target_floor
                            }
                            new_target_floor_num = player_bit | (
                                current_state[target_floor] | combined_num
                            )
                            # Add state if both new current floor and target floor state after move are legal
                            if validate(new_target_floor_num):
                                neighbors.append(
                                    {
                                        **unchanged,
                                        current_floor: new_current_floor_num,
                                        target_floor: new_target_floor_num,
                                    }
                                )
        # assert len(neighbors) == len(set(make_hash(x) for x in neighbors))
        # breakpoint()
        for neighbor in neighbors:
            neighbor_hash = make_hash(neighbor)
            candidate_g_score = g_score[current_hash] + 1
            if candidate_g_score < g_score[neighbor_hash]:
                estimate = h(neighbor)
                # Abandon if impossible to beat best known path
                if candidate_g_score + (estimate // 2) >= g_score[goal_hash]:
                    continue
                g_score[neighbor_hash] = candidate_g_score
                f_score[neighbor_hash] = candidate_g_score + estimate
                Q.put((estimate, neighbor_hash, neighbor), block=False)
    return g_score[goal_hash]


with open("inputs/day11.txt") as f:
    raw_input = f.read()

start, elements = parse(raw_input)
player_bit = 2 ** (len(elements.keys()) * 2)

part1 = A_star(start, len(elements.keys()), h)
# part1 = h(start)
print(part1)

new_line = "an elerium generator, an elerium-compatible microchip, a dilithium generator, a dilithium-compatible microchip, and a"
raw_input = raw_input.replace(
    "and a",
    new_line,
    1,
)
start, elements = parse(raw_input)
player_bit = 2 ** (len(elements.keys()) * 2)
# part2 = A_star(start, len(elements.keys()), h)
part2 = h(start)
print(part2)
