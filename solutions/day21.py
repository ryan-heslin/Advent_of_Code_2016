from collections import deque
from itertools import permutations


def swap_pos(x, y):
    password[x], password[y] = password[y], password[x]


def reverse_swap_pos(x, y):
    swap_pos(x, y)


def swap_letter(x, y):
    for i, letter in enumerate(password):
        if letter == x:
            password[i] = y
        elif letter == y:
            password[i] = x


def reverse_swap_letter(x, y):
    swap_letter(x, y)


def rotate(n):
    # n *= -1 * (direction == "left")
    password.rotate(n)


def reverse_rotate(n):
    rotate(-n)


def rotate_pos(target):
    index = password.index(target)
    n = index + 1 + (index > 3)
    rotate(n)


def reverse_rotate_pos(target):
    rotate(-1)
    rotate(target - password.index(target))


def reverse(x, y):
    end = y + 1
    indices = range(x, end)
    letters = [password[x] for x in indices]
    letters.reverse()
    for i, letter in zip(indices, letters):
        password[i] = letter


# I love involutory functions!
def reverse_reverse(x, y):
    reverse(x, y)


def move(x, y):
    # if y == 0:
    #     breakpoint()
    char = password[x]
    del password[x]
    password.insert(y, char)
    # Char in position y moves right if inserted ahead of y
    # del password[x + (y <= x)]


def reverse_move(x, y):
    move(y, x)


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


# I love how you can do 10 seconds of Vim copypasta instead of actually generalizing your defective code
reverse_parsers = {
    ("swap", "position"): lambda line: lambda: reverse_swap_pos(
        int(line[2]), int(line[5])
    ),
    ("swap", "letter"): lambda line: lambda: reverse_swap_letter(line[2], line[5]),
    ("rotate", "left"): lambda line: lambda: reverse_rotate(-int(line[2])),
    ("rotate", "right"): lambda line: lambda: reverse_rotate(int(line[2])),
    ("rotate", "based"): lambda line: lambda: reverse_rotate_pos(line[-1]),
    ("reverse", "positions"): lambda line: lambda: reverse_reverse(
        int(line[2]), int(line[4])
    ),
    ("move", "position"): lambda line: lambda: reverse_move(
        int(line[2]), int(line[-1])
    ),
}

instructions = [parse(line, parsers) for line in raw_input]
for line in instructions:
    line()

part1 = "".join(password)
print(part1)


part2 = None
target = "fbgdceah"
for perm in permutations(seed):
    if part2: 
        break
    password = deque(perm)
    for line in instructions:
        line()
    result = "".join(password)
    if result == target:
        part2 = "".join(perm)
        break
print(part2)
