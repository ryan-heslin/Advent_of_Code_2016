from collections import defaultdict
from itertools import chain
from itertools import combinations
from math import inf
from queue import PriorityQueue
from string import punctuation

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


def floor_valid(microchips, generators):
    return not (generators and microchips - generators)


def validate(
    player_microchips,
    player_generators,
    target_microchips,
    target_generators,
    taken_microchips,
    taken_generators,
):
    new_player_microchips = player_microchips - taken_microchips
    new_player_generators = player_generators - taken_generators
    if not floor_valid(new_player_microchips, new_player_generators):
        return False

    new_target_microchips = target_microchips | taken_microchips
    new_target_generators = target_generators | taken_generators
    return floor_valid(new_target_microchips, new_target_generators)


def find_valid_moves(state):
    player_floor, floors = state
    targets = TARGETS[player_floor]
    result = set()

    for target_floor in targets:
        # Unpaired generator on floor above
        player_generators = set()
        player_microchips = set()
        target_microchips = set()
        target_generators = set()
        movable = set()

        for i, pair in enumerate(floors):
            # microchips
            if pair[0] == target_floor:
                target_microchips.add(i)
            elif pair[0] == player_floor:
                movable.add((i, 0))
                player_microchips.add(i)
            # generators
            if pair[1] == target_floor:
                target_generators.add(i)
            elif pair[1] == player_floor:
                movable.add((i, 1))
                player_generators.add(i)

        choices = chain(movable, combinations(movable, r=2))
        common_args = {
            "player_microchips": player_microchips,
            "player_generators": player_generators,
            "target_microchips": target_microchips,
            "target_generators": target_generators,
        }
        for choice in choices:
            match choice:
                # Single microchip
                case (i, 0):
                    var_args = {"taken_microchips": {i}, "taken_generators": set()}
                    replacements = {i: (target_floor, floors[i][1])}
                case (i, 1):
                    var_args = {"taken_microchips": set(), "taken_generators": {i}}
                    replacements = {i: (floors[i][0], target_floor)}

                    # Two microchips
                case ((i1, 0), (i2, 0)):
                    var_args = {"taken_microchips": {i1, i2}, "taken_generators": set()}
                    replacements = {
                        i1: (target_floor, floors[i1][1]),
                        i2: (target_floor, floors[i2][1]),
                    }

                # Two generators
                case ((i1, 1), (i2, 1)):
                    var_args = {"taken_microchips": set(), "taken_generators": {i1, i2}}
                    replacements = {
                        i1: (floors[i1][0], target_floor),
                        i2: (floors[i2][0], target_floor),
                    }
                # microchip-generator
                case ((i1, 0), (i2, 1)):
                    var_args = {"taken_microchips": {i1}, "taken_generators": {i2}}
                    if i1 == i2:
                        replacements = {i1: (target_floor, target_floor)}
                    else:
                        replacements = {
                            i1: (target_floor, floors[i1][1]),
                            i2: (floors[i2][0], target_floor),
                        }
                # Generator-microchip
                case ((i1, 1), (i2, 0)):
                    var_args = {"taken_microchips": {i2}, "taken_generators": {i1}}
                    if i1 == i2:
                        replacements = {i1: (target_floor, target_floor)}
                    else:
                        replacements = {
                            i1: (floors[i1][0], target_floor),
                            i2: (
                                target_floor,
                                floors[i2][1],
                            ),
                        }
                case _:
                    raise ValueError

            if validate(**common_args, **var_args):
                copy = list(floors)
                for position, replacement in replacements.items():
                    copy[position] = replacement
                result.add((target_floor, tuple(sorted(copy))))

    return result


def A_star(start, goal):
    dist = defaultdict(lambda: inf)
    dist[start] = 0
    g_score = defaultdict(lambda: inf)
    g_score[start] = 0
    f_score = defaultdict(lambda: inf)
    estimate = h(start)
    f_score[start] = estimate
    queue = PriorityQueue()
    queue.put((estimate, start), block=False)

    while queue.qsize():
        estimate, current_state = queue.get()
        this_g_score = g_score[current_state]
        if this_g_score >= g_score[goal] or current_state == goal:
            continue

        neighbors = find_valid_moves(current_state)
        new_g_score = this_g_score + 1
        for neighbor in neighbors:
            if new_g_score < g_score[neighbor]:
                g_score[neighbor] = new_g_score
                new_f_score = new_g_score + h(neighbor)
                f_score[neighbor] = new_f_score
                queue.put((new_f_score, neighbor))

    return g_score[goal]


def h(state):
    return sum(map(sum, state[1])) // 2


# (microchip, generator) pairs
def parse(lines):
    found = {}
    result = []
    remover = str.maketrans("", "", punctuation)
    for floor, line in enumerate(lines):
        words = line.split(" ")
        while words:
            current = words.pop(0).split("-")[0].replace(",", "")
            if not current:
                continue
            if current in ELEMENTS:
                component = words[0].translate(remover)
                # Paired component found?
                if current in found:
                    position = found[current]
                    chip, gen = result[position]
                    result[position] = (chip, floor) if gen is None else (floor, gen)
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

new_elements = """
    An elerium generator.
    An elerium-compatible microchip.
    A dilithium generator.
    A dilithium-compatible microchip.
"""
raw_input[0] += " ".join(new_elements.splitlines())
ELEMENTS.update(("elerium", "dilithium"))
parsed = parse(raw_input)
start = (bottom, parsed)
goal = make_goal(start)
part2 = A_star(start, goal)
print(part2)
