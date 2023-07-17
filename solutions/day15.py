def parse(line):
    parts = line.split()
    return Disk(int(parts[3]), int(parts[-1].rstrip(".")))


def simulate(disks, start_time=0):
    pos = 0
    n_disks = len(disks)

    while True:
        # First instant
        for disk in disks:
            disk.advance(1)
        for pos in range(n_disks):
            if not disks[pos].open():
                for disk in disks:
                    disk.reset()
                    disk.advance(start_time + 1)
                break
            for disk in disks:
                disk.advance(1)
        else:
            return start_time
        start_time += 1


class Disk:
    def __init__(self, n_positions, position) -> None:
        self.n_positions = n_positions
        self.position = self.init_position = position

    def advance(self, steps=1):
        self.position = (self.position + steps) % self.n_positions

    def open(self):
        return self.position == 0

    def reset(self):
        self.position = self.init_position

    def __repr__(self) -> str:
        return str(self.position)


with open("inputs/day15.txt") as f:
    raw_input = f.read().splitlines()

disks = list(map(parse, raw_input))

part1 = simulate(disks)
print(part1)

disks.append(Disk(11, 0))
part2 = simulate(disks, part1)
print(part2)
