from collections import deque
from itertools import permutations


def swap_pos(x, y):
    password[x], password[y] = password[y], password[x]


def swap_letter(x, y):
    for i, letter in enumerate(password):
        if letter == x:
            password[i] = y
        elif letter == y:
            password[i] = x

def rotate(n):
    password.rotate(n)

def rotate_pos(target):
    index = password.index(target)
    n = index + 1 + (index > 3)
    rotate(n)


def reverse(x, y):
    end = y + 1
    indices = range(x, end)
    letters = [password[x] for x in indices]
    letters.reverse()
    for i, letter in zip(indices, letters):
        password[i] = letter

def move(x, y):
    char = password[x]
    del password[x]
    password.insert(y, char)


def parse(line, map):
    words = line.split(" ")
    return map[tuple(words[:2])](words)


with open("inputs/day21.txt") as f:
    raw_input = f.read().splitlines()


seed = "abcdefgh"
password = deque(seed)
n_letters = len(password)

parsers = {
    ("swap", "position"): lambda line: lambda: swap_pos(int(line[2]), int(line[5])),
    ("swap", "letter"): lambda line: lambda: swap_letter(line[2], line[5]),
    ("rotate", "left"): lambda line: lambda: rotate(-int(line[2])),
    ("rotate", "right"): lambda line: lambda: rotate(int(line[2])),
    ("rotate", "based"): lambda line: lambda: rotate_pos(line[-1]),
    ("reverse", "positions"): lambda line: lambda: reverse(int(line[2]), int(line[4])),
    ("move", "position"): lambda line: lambda: move(int(line[2]), int(line[-1])),
}
instructions = [parse(line, parsers) for line in raw_input]
for line in instructions:
    line()

part1 = "".join(password)
print(part1)

part2 = None
target = "fbgdceah"
for perm in permutations(seed):
    password = deque(perm)
    for line in instructions:
        line()
    result = "".join(password)
    if result == target:
        part2 = "".join(perm)
        break
print(part2)
