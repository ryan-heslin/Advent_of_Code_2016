from operator import attrgetter
from functools import cached_property

class Interval:
    def __init__(self, lower, upper) -> None:
        self.lower = lower
        self.upper = upper

    def __repr__(self) -> str:
        return f"[{self.lower}, {self.upper}]"

    @cached_property
    def size(self):
        return self.upper - self.lower + 1


def find_lowest_allowed(intervals):
    candidate = 0
    found = []

    for interval in intervals:
        if interval.lower > candidate:
            # Should handle point interval correctly
            found.append(Interval(candidate, interval.lower - 1))
        candidate = max(interval.upper + 1, candidate)
    return found


with open("inputs/day20.txt") as f:
    raw_input = f.read().splitlines()

intervals = sorted(
    [Interval(*map(int, line.split("-"))) for line in raw_input],
    key=attrgetter("lower"),
)
all_allowed = find_lowest_allowed(intervals)
part1 = all_allowed[0].lower
print(part1)

part2 = sum(map(attrgetter("size"), all_allowed))
print(part2)
