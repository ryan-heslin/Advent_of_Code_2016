import utils.assembunny as ab
from utils.utils import split_lines

# Topaz showed mercy and made the highest input 12,
# knowing the naive method is O(n!)
raw_input = split_lines("inputs/day23.txt")
params = [ab.parse_line(line) for line in raw_input]

program = ab.Program(params, a=7)
program.exec()
part1 = program.registers["a"]
print(part1)

params = [ab.parse_line(line) for line in raw_input]
program = ab.Program(params, a=12)
program.exec()
part2 = program.registers["a"]
print(part2)

# >59780
