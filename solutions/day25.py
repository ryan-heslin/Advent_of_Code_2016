from math import inf

import utils.assembunny as ab
from utils.utils import split_lines


class ClockProgram(ab.Program):
    def __init__(self, params, **settings) -> None:
        super().__init__(params, **settings)
        self.count = 0
        self.next = 0
        self.found = False

    def reset(self):
        self.registers = {k: 0 for k in self.names}
        self.next = 0
        self.states = set()

    def out(self, x, i):
        signal = self.registers.get(x, x)
        if signal != self.next:
            return inf
        self.next = (self.next + 1) % 2
        if self.count > 512:
            self.found = True
            return inf
        self.count += 1

        return i + 1


raw_input = split_lines("inputs/day25.txt")
params = list(map(ab.parse_line, raw_input))
i = 1

while True:
    program = ClockProgram(params, a=i)
    program.exec()
    if program.found:
        break
    i += 1

part1 = i
print(part1)
