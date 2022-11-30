with open("inputs/day2.txt") as f:
    raw_input = f.read().splitlines()

last_position = complex(0, 0)


def clamp(x, lower=-1, upper=1):
    return max(lower, min(x, upper))


def clamp_complex(x, lower=-2, upper=2):
    return complex(clamp(x.real), clamp(x.imag))


def execute_line(line, start):
    position = start
    # print("\n")
    for char in line:
        position += directions[char]
        position = clamp_complex(position)
        # print(position)
    return position


directions = {
    "R": complex(1, 0),
    "U": complex(0, 1),
    "L": complex(-1, 0),
    "D": complex(0, -1),
}
mapping = {
    complex(-1, 1): 1,
    complex(0, 1): 2,
    complex(1, 1): 3,
    complex(-1, 0): 4,
    last_position: 5,
    complex(1, 0): 6,
    complex(-1, -1): 7,
    complex(0, -1): 8,
    complex(1, -1): 9,
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
    complex(0, 2): 1,
    complex(-1, 1): 2,
    complex(0, 1): 3,
    complex(1, 1): 4,
    complex(-2, 0): 5,
    complex(-1, 0): 6,
    complex(0, 0): 7,
    complex(1, 0): 8,
    complex(2, 0): 9,
    complex(-1, -1): "A",
    complex(0, -1): "B",
    complex(1, -1): "C",
    complex(0, -2): "D",
}


def part2_execute_line(line, start):
    position = start
    # print("\n")
    for char in line:
        new_position = position + directions[char]
        if new_position in part2_mapping.keys():
            position = new_position

        # print(position)
    return position


last_position = complex(-2, 0)
result = []
for line in raw_input:
    last_position = part2_execute_line(line, last_position)
    result.append(str(part2_mapping[last_position]))

part2 = "".join(result)
print(part2)
