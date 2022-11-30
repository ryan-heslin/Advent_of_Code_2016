from utils import split_lines

raw_input = split_lines("inputs/day12.txt")
registers = {"a": 0, "b": 0, "c": 0, "d": 0}
stop = len(raw_input)
i = 0


def parse_line(line):
    parts = line.split(" ")
    parts[1:] = [f"'{x}'" if x.isalpha() and not "-" in x else x for x in parts[1:]]
    args = ", ".join(parts[1:] + ["i"])
    return compile(f"{parts[0]}({args})", "", "eval")


def inc(reg, i):
    registers[reg] += 1
    return i + 1


def dec(reg, i):
    registers[reg] -= 1
    return i + 1


def cpy(x, y, i):
    registers[y] = registers.get(x, x)
    return i + 1


def jnz(x, y, i):
    return i + y if registers.get(x, x) != 0 else i + 1


parsed = [parse_line(line) for line in raw_input]

while i < stop:
    i = eval(parsed[i])

part1 = registers["a"]
print(part1)

for k in registers.keys():
    registers[k] = 0
registers["c"] = 1

i = 0
while i < stop:
    i = eval(parsed[i])

part2 = registers["a"]
print(part2)
