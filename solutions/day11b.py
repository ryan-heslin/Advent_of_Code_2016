from collections import defaultdict
from math import inf
from queue import PriorityQueue

ELEMENTS = {
    "hydrogen",
    "helium",
    "lithium",
    "beryllium",
    "boron",
    "carbon",
    "nitrogen",
    "oxygen",
    "fluorine",
    "neon",
    "sodium",
    "magnesium",
    "aluminium",
    "silicon",
    "phosphorus",
    "sulfur",
    "chlorine",
    "argon",
    "potassium",
    "calcium",
    "scandium",
    "titanium",
    "vanadium",
    "chromium",
    "manganese",
    "iron",
    "cobalt",
    "nickel",
    "copper",
    "zinc",
    "gallium",
    "germanium",
    "arsenic",
    "selenium",
    "bromine",
    "krypton",
    "rubidium",
    "strontium",
    "yttrium",
    "zirconium",
    "niobium",
    "molybdenum",
    "technetium",
    "ruthenium",
    "rhodium",
    "palladium",
    "silver",
    "cadmium",
    "indium",
    "tin",
    "antimony",
    "tellurium",
    "iodine",
    "xenon",
    "caesium",
    "barium",
    "lanthanum",
    "cerium",
    "praseodymium",
    "neodymium",
    "promethium",
    "samarium",
    "europium",
    "gadolinium",
    "terbium",
    "dysprosium",
    "holmium",
    "erbium",
    "thulium",
    "ytterbium",
    "lutetium",
    "hafnium",
    "tantalum",
    "tungsten",
    "rhenium",
    "osmium",
    "iridium",
    "platinum",
    "gold",
    "mercury",
    "thallium",
    "lead",
    "bismuth",
    "polonium",
    "astatine",
    "radon",
    "francium",
    "radium",
    "actinium",
    "thorium",
    "protactinium",
    "uranium",
    "neptunium",
    "plutonium",
    "americium",
    "curium",
    "berkelium",
    "californium",
    "einsteinium",
    "fermium",
    "mendelevium",
    "nobelium",
    "lawrencium",
    "rutherfordium",
    "dubnium",
    "seaborgium",
    "bohrium",
    "hassium",
    "meitnerium",
    "darmstadtium",
    "roentgenium",
    "copernicium",
    "nihonium",
    "flerovium",
    "moscovium",
    "livermorium",
    "tennessine",
    "oganesson",
}


def make_goal(start):
    return (top, tuple((top, top) for _ in range(len(start[1]))))


def clamp(low, high, x):
    return max(min(x, high), low)


# Chip cannot coexist with generator of different type unless paired with own generator
# Must bring at least one item


def validate(
    target,
    index,
    component,
    floors,
    player_floor,
    target_generators,
    target_microchips,
    player_generators,
    player_microchips,
):
    if component == 0 and (not target_generators or index in target_microchips):
        return (target, floors[index][1])
    # If moving single generator:
    # Invalid if same microchip type on current floor and other generator types
    # Invalid if other microchip type on target without own microchip on target
    elif component == 1 and not (
        (player_generators - {index} and index in player_microchips)
        or (target_microchips and index not in target_microchips)
    ):
        return (floors[index][0], target)


def find_valid_moves(state):
    # breakpoint()
    player_floor, floors = state
    targets = TARGETS[player_floor]
    result = set()

    for target in targets:
        # Unpaired generator on floor above
        # player_microchips = set()
        player_generators = set()
        player_microchips = set()
        target_microchips = set()
        target_generators = set()
        movable = set()

        # i is arbitrary index of each item pair
        # If moving single microchip
        #   no danger on current floor
        #   Invalid if other generators on target floor without own generator type
        # For combinations: do single move, then validate second move

        for i, pair in enumerate(floors):
            # microchips
            if pair[0] == target:
                target_microchips.add(i)
            elif pair[0] == player_floor:
                movable.add((i, 0))
                # player_microchips.add(i)
            # generators
            if pair[1] == target:
                target_generators.add(i)
            elif pair[1] == player_floor:
                movable.add((i, 1))
                player_generators.add(i)

        pairs = set()
        # breakpoint()
        for option in movable:
            index, component = option
            # Chip
            replacement = validate(
                target,
                index,
                component,
                floors,
                player_floor,
                target_generators,
                target_microchips,
                player_generators,
                player_microchips,
            )
            if component == 0:
                updated_target_microchips = target_microchips | {index}
                updated_target_generators = target_generators
                updated_player_generators = player_generators
                updated_target_microchips = player_microchips - {index}
            else:
                updated_target_microchips = target_microchips
                updated_player_generators = player_generators - {index}
                updated_target_generators = target_generators | {index}
                updated_player_microchips = player_microchips
            if replacement:
                new = (target, floors[:index] + (replacement,) + floors[index + 1 :])
                result.add(new)
                # Check possible combinations
                for second in movable:
                    if second != option and (
                        pair := tuple(sorted((option, second))) not in pairs
                    ):
                        double_replacement = validate(
                            target,
                            *second,
                            new[1],
                            player_floor,
                            updated_target_generators,
                            updated_target_microchips,
                            updated_player_generators,
                            updated_target_generators,
                        )
                        pairs.add(pair)
                        if double_replacement:
                            result.add(
                                (
                                    target,
                                    floors[:index]
                                    + (double_replacement,)
                                    + floors[index + 1 :],
                                )
                            )
    print(result)
    print("\n")
    return result


def A_star(start, goal):
    f_score = defaultdict(lambda: inf)
    start_estimate = h(start)
    f_score[start] = start_estimate
    g_score = defaultdict(lambda: inf)
    g_score[start] = 0
    queue = PriorityQueue()
    queue.put((start_estimate, start), block=False)
    visited = set()

    while queue.qsize():
        h_score, current_state = queue.get(block=False)
        # print(current_state)
        # If h never overestimates, as it must for A* to
        # be correct, this will only trigger if the path is suboptimal
        if h_score + g_score[current_state] >= g_score[goal] or current_state == goal:
            continue

        neighbors = find_valid_moves(current_state)
        candidate_g_score = g_score[current_state] + 1
        for neighbor in neighbors:
            if candidate_g_score < g_score[neighbor]:
                estimate = h(neighbor)
                g_score[neighbor] = candidate_g_score
                f_score[neighbor] = candidate_g_score + estimate
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.put((estimate, neighbor), block=False)

    return g_score[goal]


# Bugged - overestimates even when heuristic ignored
def h(state):
    return 0
    # return sum(map(sum, state[1])) // 2


# (microchip, generator) pairs
def parse(lines):
    found = {}
    result = []
    for floor, line in enumerate(lines):
        words = line.split(" ")
        while words:
            current = words.pop().split("-")[0].replace(",", "")
            if current in ELEMENTS:
                component = words[0]
                # Paired component found?
                if current in found:
                    position = found[current]
                    chip, gen = result[position]
                    result[position] = (
                        (chip, floor) if component == "generator" else (floor, gen)
                    )
                else:
                    found[current] = len(result)
                    new = (floor, None) if component == "microchip" else (None, floor)
                    result.append(new)

    return tuple(sorted(result))


with open("inputs/day11.txt") as f:
    raw_input = f.read().splitlines()

bottom = 0
top = len(raw_input) - 1
TARGETS = {0: (1,), 1: (0, 2), 2: (1, 3), 3: (2,)}
parsed = parse(raw_input)
start = (bottom, parsed)
goal = make_goal(start)
part1 = A_star(start, goal)
print(part1)
