# More Wikipedia pseudocode!
# https://en.wikipedia.org/wiki/Josephus_problem
def josephus(n):
    highest_one = 2 ** ((n * 2).bit_length() - 1)
    return ~highest_one & ((n << 1) | 1)


n = 3004953

part1 = josephus(n)
print(part1)

elves = list(range(1, n + 1))
stolen = [False] * n

i = 0
n_elves = n
while n_elves > 1:
    target = (i + n_elves // 2) % n_elves
    elves.pop(target)
    n_elves -= 1
    i = 0 if i >= n_elves else i + (target > i)

part2 = elves.pop()
print(part2)
