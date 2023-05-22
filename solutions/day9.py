def traverse(string):
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
    result = 0
    if string.find("(") == -1:
        return len(string)
    gen = traverse(string)
    while gen:
        text = next(gen)
        if text is None:
            break
        result += len(text)

        instructions = next(gen)
        if instructions == "":
            break
        new_text = next(gen)

        if recurse:
            new_length = parse(new_text, recurse)
        else:
            new_length = len(new_text)
        result += new_length
    return result


def parse_compression(instructions):
    length, reps = [
        int(x) for x in instructions[1 : (len(instructions) - 1)].split("x")
    ]
    return length, reps


with open("inputs/day9.txt") as f:
    raw_input = f.read().rstrip("\n")

part1 = parse(raw_input)
print(part1)

part2 = parse(raw_input, recurse=True)
print(part2)
