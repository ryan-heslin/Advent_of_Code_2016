import re


def has_abba(code):
    return bool(re.match(pattern, code)) and not bool(re.match(exclude_pattern, code))


def has_bab(code):
    abas = set(re.finditer(aba_pattern, re.sub(r"\[[^\]]*\]", "", code)))

    for aba in abas:
        aba = aba.group(1)
        bab = f"{aba[1]}{aba[0]}{aba[1]}"
        if re.match(r".*\[[^\]]*" + bab + r"[^\]]*\].*", code):
            return True
    return False


with open("inputs/day7.txt") as f:
    raw_input = f.read().splitlines()
abba = r"(([a-z])(?!\2)([a-z])\3\2)"
pattern = re.compile(".*" + abba + ".*")
exclude_pattern = re.compile(r".*\[[^\]]*" + abba + r"[^\]]*\].*")
aba_pattern = re.compile(r"(?=(([a-z])(?!\2)[a-z]\2))")

part1 = sum(map(has_abba, raw_input))
print(part1)

part2 = sum(map(has_bab, raw_input))
print(part2)
