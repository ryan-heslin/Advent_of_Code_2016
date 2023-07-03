def part2_execute_line(line, start):
    position = start
    for char in line:
        new_position = position + directions[char]
        if new_position in part2_mapping.keys():
            position = new_position

    return position


def clamp(x, lower=-1, upper=1):
    return max(lower, min(x, upper))


def clamp_complex(x):
    return complex(clamp(x.real), clamp(x.imag))


def execute_line(line, start):
    position = start
    for char in line:
        position += directions[char]
        position = clamp_complex(position)
    return position


with open("inputs/day2.txt") as f:
    raw_input = f.read().splitlines()

last_position = 0

directions = {
    "R": 1,
    "U": 1j,
    "L": -1,
    "D": -1j,
}
mapping = {
    -1 + 1j: 1,
    0 + 1j: 2,
    1 + 1j: 3,
    -1 + 0j: 4,
    last_position: 5,
    1: 6,
    -1 - 1j: 7,
    -1j: 8,
    1 - 1j: 9,
}
result = 0
multiplier = 10**4


for line in raw_input:
    last_position = execute_line(line, last_position)
    result += multiplier * mapping[last_position]
    multiplier //= 10

part1 = result
print(part1)

part2_mapping = {
    0 + 2j: 1,
    -1 + 1j: 2,
    0 + 1j: 3,
    1 + 1j: 4,
    -2: 5,
    -1: 6,
    0: 7,
    1: 8,
    2: 9,
    -1 - 1j: "A",
    -1j: "B",
    1 - 1j: "C",
    -2j: "D",
}


last_position = complex(-2, 0)
result = []
for line in raw_input:
    last_position = part2_execute_line(line, last_position)
    result.append(str(part2_mapping[last_position]))

part2 = "".join(result)
print(part2)
