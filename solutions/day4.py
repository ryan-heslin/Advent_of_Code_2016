import re
from collections import Counter
from collections import defaultdict

ASCII_A = ord("a")


def tabulate_letters(string):
    count = sorted(Counter(string).items(), key=lambda kv: -kv[1])
    count = Counter(string)
    # Map counts to letters with count
    inverted = defaultdict(list)
    for k, v in count.items():
        inverted[v].append(k)
    return inverted


def top_five(counts):
    n_found = 0
    result = []

    for tot in sorted(counts.keys(), key=lambda x: -x):
        if n_found == 5:
            break
        letters = sorted(counts[tot])
        remaining = 5 - n_found
        this_found = min(remaining, len(letters))
        result += letters[:this_found]
        n_found += this_found
    return result


def verify_room(code):
    counts = tabulate_letters((code["name"][0].replace("-", "")))
    five_most = "".join(top_five(counts))
    return int(code["id"][0]) if code["checksum"][0] == five_most else 0


def decrypt(code, id):
    code = code.replace("-", " ")
    return "".join(
        (
            char if char == " " else chr(((ord(char) - ASCII_A + id) % 26) + ASCII_A)
            for char in code
        )
    ).rstrip(" ")


def decrypt_room(rooms):
    for room in rooms:
        code = verify_room(room)
        if code != 0:
            decrypted = decrypt(room["name"][0], code)
            if "object storage" in decrypted:
                yield code


with open("inputs/day4.txt") as f:
    raw_input = f.read().splitlines()

pattern = r"^(?P<name>(?:[a-z]+-)+)(?P<id>\d+)\[(?P<checksum>[a-z]+)\]"

decomposed = [
    dict(
        zip(
            ("name", "id", "checksum"),
            ([x] for x in re.match(pattern, string).groups()),
        )
    )
    for string in raw_input
]

part1 = sum(map(verify_room, decomposed))
print(part1)
gen = decrypt_room(decomposed)
part2 = next(gen)

print(part2)
