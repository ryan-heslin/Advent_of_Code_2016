def expand(start, n):
    last = {j: x for j, x in enumerate(start)}
    cols = len(start)
    total = sum(not x for x in last.values())
    for _ in range(n - 1):
        left, middle = [False, last[0]]
        new = {}
        for j in range(cols):
            right = last.get(j + 1, False)
            adjacent = sum((left, middle, right))
            this = (1 <= adjacent <= 2) and (
                (adjacent == 1 and not middle) or (adjacent == 2 and middle)
            )
            new[j] = this
            total += not this
            left, middle = middle, right
        last = new

    return total


with open("inputs/day18.txt") as f:
    raw_input = f.read().rstrip("\n")

trap = "^"
processed = [x == trap for x in list(raw_input)]
part1 = expand(processed, 40)
part2 = expand(processed, 400000)
print(part1)
print(part2)
