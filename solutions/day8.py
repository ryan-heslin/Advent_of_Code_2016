import re

import matplotlib.pyplot as plt
import numpy as np
from utils.utils import split_lines

raw_input = split_lines("inputs/day8.txt")

grid = np.zeros([6, 50])
word_pattern = re.compile(r"[a-z]{3,}")


def rect(x, y):
    grid[:y, :x] = np.ones([y, x])


def rotate_row(row, n):
    grid[row, :] = np.roll(
        grid[row, :],
        n,
    )


def rotate_column(col, n):
    grid[:, col] = np.roll(grid[:, col], n)


mapping = {"rotate_row": rotate_row, "rotate_column": rotate_column, "rect": rect}


def process_line(line):
    func = "_".join(re.findall(word_pattern, line))
    args = [int(x) for x in re.findall(r"\d+", line)]
    return {"func": func, "args": args}


processed = [process_line(line) for line in raw_input]

for line in processed:
    mapping[line["func"]](*line["args"])

part1 = np.sum(grid)
print(part1)

plt.imshow(grid)
plt.colorbar()
plt.show()
