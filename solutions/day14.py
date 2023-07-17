import re
from hashlib import md5


# Get distinct repeating characters
def repeat_chars(string, n):
    repeats = re.findall(r"([0-9a-f])\1{" + str(n - 1) + "}", string)
    if repeats:
        repeats = [x[0] for x in repeats]
    return repeats


def process_hash(string, times=1):
    old = string
    hash = None
    for _ in range(0, times):
        hash = str(md5(old.encode("utf-8")).hexdigest())
        old = hash

    quintuplets = set(repeat_chars(hash, 5))
    return hash, quintuplets


def generate_keys(salt, n=64, times=1):
    i = found = 0
    hash_keys = [None] * n
    hashes = {}
    keys = ("hash", "quintuplets")

    hashes = {
        i: dict(zip(keys, process_hash(f"{salt}{i}", times))) for i in range(1000)
    }

    i = 0
    while found < n:
        candidate = hashes[i]
        last = 1000 + i  # Starts on index 1000
        new_data = dict(zip(keys, process_hash(f"{salt}{last}", times)))
        hashes[last] = new_data.copy()
        triplets = repeat_chars(candidate["hash"], 3)
        if triplets:
            triplets = set(triplets[0])
            # Check next 1000 indices for matching quintuplet
            for j in range(i + 1, last + 1):
                if len(triplets.intersection(hashes[j]["quintuplets"])):
                    hash_keys[found] = hashes[j]["hash"]
                    found += 1
        hashes.pop(i)  # Current hash now unneeded
        i += 1
    return i - 1


salt = "zpqevtbw"
part1 = generate_keys(salt, 64)
print(part1)

part2 = generate_keys(salt, 64, 2017)
print(part2)
