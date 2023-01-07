from math import inf

import utils.assembunny as ab


class ClockProgram(ab.Program):
    def __init__(self, params) -> None:
        super().__init__()
        self.states = set()
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
        new_state = tuple(self.registers.values())
        # Todo; can't check for repeat states, but must
        # ensure index never overshoots program end
        # Maybe all greater/less?
        if new_state in self.states:
            self.found = True
            return inf
        self.states.add(new_state)
        return i + 1
