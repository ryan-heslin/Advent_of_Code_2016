import re

with open("inputs/day7.txt") as f:
    raw_input = f.read().splitlines()
abba = r"(([a-z])(?!\2)([a-z])\3\2)"
pattern = re.compile(".*" + abba + ".*")
exclude_pattern = re.compile(r".*\[[^\]]*" + abba + r"[^\]]*\].*")
aba_pattern = re.compile(r"(?=(([a-z])(?!\2)[a-z]\2))")


def has_abba(code):
    return bool(re.match(pattern, code)) and not bool(re.match(exclude_pattern, code))


def has_bab(code):
    print(code)
    abas = set(re.finditer(aba_pattern, re.sub(r"\[[^\]]*\]", "", code)))
    if len(abas):
        # breakpoint()
        for aba in abas:
            aba = aba.group(1)
            # aba = code[aba.start() : aba.end()]
            print(aba)
            bab = f"{aba[1]}{aba[0]}{aba[1]}"
            if re.match(r".*\[[^\]]*" + bab + r"[^\]]*\].*", code):
                print(True)
                return True
    return False


matches = [has_abba(code) for code in raw_input]
part1 = sum(matches)
print(part1)

part2 = sum(has_bab(code) for code in raw_input)
print(part2)
