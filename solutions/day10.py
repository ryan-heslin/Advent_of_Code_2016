import re

from utils.utils import split_lines


class Bot:
    def __init__(self, number):
        self.low = self.high = None
        self.number = number

    def receive(self, value):
        if self.low is None and self.high is None:
            self.low = value
        elif self.low is not None:
            if value >= self.low:
                self.high = value
            else:
                self.high = self.low
                self.low = value
        elif self.high is not None:
            if value <= self.high:
                self.low = value
            else:
                self.low = self.high
                self.high = value
        else:
            raise ValueError("Cannot receive another chip")

    def give(self, low, high, low_mapping, high_mapping):
        # Only give if both chips available
        if self.low is None or self.high is None:
            return

        if isinstance(low_mapping[low], self.__class__):
            low_mapping[low].receive(self.low)
        else:
            low_mapping[low] = self.low
        if isinstance(high_mapping[high], self.__class__):
            high_mapping[high].receive(self.high)
        else:
            high_mapping[high] = self.high
        self.low = self.high = None

    def __repr__(self):
        return f"low {self.low}, high: {self.high}"


class Part1Bot(Bot):
    def give(self, low, high, low_mapping, high_mapping):
        if self.low == 17 and self.high == 61:
            answers[0] = self.number
        super().give(low, high, low_mapping, high_mapping)


# Mutable default because I live life on the edge
def parse(line, mapping={"bot": "bots", "output": "outputs"}):
    args = re.findall(r"\d+", line)
    if "value" in line:
        result = f"{mapping['bot']}[{args[1]}].receive({args[0]})"
    else:
        targets = re.findall(r"(?<=\s)[a-z]+(?=\s\d+)", line)
        targets = [mapping[target] for target in targets]
        result = f"{mapping['bot']}[{args[0]}].give({args[1]}, {args[2]}, {targets[0]}, {targets[1]})"
    return compile(result, "", "eval")


def execute(instructions, outputs):
    i = 0
    n_instr = len(instructions)
    while None in outputs.values():
        eval(parsed[i])
        i = (i + 1) % n_instr


raw_input = split_lines("inputs/day10.txt")

answers = [None]
output = {}
bot_numbers = set()
bots = {}

for line in raw_input:
    bot_numbers.update((int(x) for x in re.findall(r"bot (\d+)", line)))
bots = dict(zip(bot_numbers, (Part1Bot(num) for num in bot_numbers)))

output_numbers = set()
for line in raw_input:
    output_numbers.update((int(x) for x in re.findall(r"output (\d+)", line)))
outputs = dict(zip(output_numbers, (None,) * len(output_numbers)))

parsed = list(map(parse, raw_input))

execute(parsed, outputs)
part1 = answers[0]
print(part1)

part2 = outputs[0] * outputs[1] * outputs[2]
print(part2)
