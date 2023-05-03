import utils.assembunny as ab
from utils.utils import split_lines

raw_input = split_lines("inputs/day12.txt")
params = list(map(ab.parse_line, raw_input))

program = ab.Program(params)
program.exec()

part1 = program.registers["a"]
print(part1)

program = ab.Program(params, c=1)
program.exec()

part2 = program.registers["a"]
print(part2)
