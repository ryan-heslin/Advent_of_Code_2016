from math import inf


def parse_line(line):
    parts = line.split(" ")
    parts[1:] = [f"'{x}'" if x.isalpha() and not "-" in x else x for x in parts[1:]]
    args = ", ".join(parts[1:] + ["i"])
    return {"func": parts[0], "args": args}


def compile_parts(parts, args):
    return compile(f"{parts[0]}({args})", "", "eval")


def inc(reg, i):
    registers[reg] += 1
    return i + 1


def dec(reg, i):
    registers[reg] -= 1
    return i + 1


def cpy(x, y, i):
    registers[y] = registers.get(x, x)
    return i + 1


def jnz(x, y, i):
    return i + y if registers.get(x, x) != 0 else i + 1


class Program:
    replacements = {
        "inc": "dec",
        "dec": "inc",
        "tgl": "inc",
        "jnz": "cpy",
        "cpy": "jnz",
    }

    def __init__(self, params, **settings):
        self.length = len(params)
        self.params = params
        self.code = [__class__.compile_parts(**di) for di in self.params]
        registers = set()
        for di in self.params:
            registers.update(filter(str.isalpha, di["args"]))
        self.registers = {k: 0 for k in registers}
        settings = {**settings}
        self.registers.update(settings)
        self.registers.pop("i")
        self.names = set(self.registers.keys())

    @staticmethod
    def compile_parts(func, args):
        return compile(f"self.{func}({args})", "", "eval")

    def inc(self, reg, i):
        if reg in self.names:
            self.registers[reg] += 1
        return i + 1

    def dec(self, reg, i):
        if reg in self.names:
            self.registers[reg] -= 1
        return i + 1

    def cpy(self, x, y, i):
        # Skip if invalid
        if y in self.names:
            self.registers[y] = self.registers.get(x, x)
        return i + 1

    def jnz(self, x, y, i):
        return i + self.registers.get(y, y) if self.registers.get(x, x) != 0 else i + 1

    def tgl(self, reg, i):
        target = i + self.registers.get(reg, reg)
        if 0 <= target < self.length:
            # Update instruction
            self.params[target]["func"] = __class__.replacements[
                self.params[target]["func"]
            ]
            self.code[target] = __class__.compile_parts(**self.params[target])
        return i + 1

    def exec(self):
        i = 0
        while 0 <= i < self.length:
            i = eval(self.code[i])
