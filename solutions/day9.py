with open("inputs/day9.txt") as f:
    raw_input = f.read().rstrip("\n")

# raw_input = "X(8x2)(3x3)ABCY"


def traverse(string):
    # breakpoint()
    while string:
        # Parse up to next open paren
        next_open = string.find("(")
        chunk, string = chomp_string(string, next_open)
        yield chunk

        # Parse through next close paren
        next_close = string.find(")")
        instruction, string = chomp_string(string, next_close + 1)
        yield instruction

        # Caller computes and supplies number of needed characters
        # Common pattern: halt, wait for caller to supply data, continue
        length, reps = parse_compression(instruction)
        chunk, string = chomp_string(string, length)
        yield chunk * reps
    yield None


def chomp_string(string, nchar):
    return string[:nchar], string[nchar:]


def parse(string, recurse=False):
    result = ""
    if string.find("(") == -1:
        return string
    gen = traverse(string)
    # breakpoint()
    while gen:
        # next_compression = string.find(")")
        # instructions = gen.send(next_compression)
        # gen.send(None)
        text = next(gen)
        if text is None:
            break
        result += text

        instructions = next(gen)
        if instructions == "":
            break
        # length, reps = parse_compression(instructions)
        # next(gen)
        # gen.send(length)
        # chunk, reps = next(gen)
        result += next(gen)  # * reps
        # print(result)
    return result


def parse_compression(instructions):
    length, reps = [
        int(x) for x in instructions[1 : (len(instructions) - 1)].split("x")
    ]
    return length, reps


parsed = parse(raw_input)
part1 = len(parsed)
print(part1)
