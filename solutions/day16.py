from math import ceil
from math import floor
from math import log2

# num + 0 + reverse(num xor 1)


def binary(x):
    return int(x, 2)


def binary_digits(n):
    log = log2(max(abs(n), 1))
    return floor(log + 1)


def even_binary_length(n):
    return (binary_digits(n) % 2) == 0


# Remove dummy leading bit
def to_string(n):
    return bin(n)[3:]


def strip_leading_digits(n, digits):
    n_digits = binary_digits(n)
    if n_digits <= digits:
        return 0
    mask = sum(2**i for i in range(n_digits - digits, n_digits, 1))
    return n - (n & mask)


# To preserve leading zeroes
def add_dummy_bit(n, target_length=None):
    target_length = binary_digits(n) if target_length is None else target_length
    return n + 2 ** (target_length)


# Copied from https://stackoverflow.com/questions/12681945/reversing-bits-of-python-integer
# TODO handle leading zero bits
def reverse_bits(num):
    result = i = 0
    while num:
        result <<= 1
        # Clip rightmost
        result += num & 1
        num >>= 1
        i += 1
    return result, max(i, 1)


def dragon_curve(a):
    # Handle leading: get length, pad to
    # length with leading 1
    # breakpoint()
    b, n_digits = reverse_bits(a)
    b = add_dummy_bit(b, binary_digits(a))
    b ^= max(2 ** (n_digits) - 1, 1)
    # Restore dummy bit just xor'd away
    # b |= 2**n_digits
    # Just find position of dummy bit in concatenated number and XOR 2 **i
    result = (a << (n_digits + 1)) + b
    # print(bin(result)[2:])
    return result ^ (2 ** (n_digits))


assert dragon_curve(1) == 4
assert dragon_curve(0) == 1
assert dragon_curve(31) == 1984
assert dragon_curve(binary("111100001010")) == binary("1111000010100101011110000")


def fill_disk(n, disk_size):
    while True:
        n_digits = binary_digits(n)
        offset = n_digits - disk_size
        if offset >= 0:
            return n, offset
        # May have to add dummy bit here
        n = dragon_curve(n)


def checksum_stage(n):
    # Assume n has dummy leading 1 bit to retain leading zeroes
    n_digits = binary_digits(n)
    # cur_digit = n_digits // 2
    result = 1
    while n_digits > 1:
        # Filling result from right
        result <<= 1
        # Two leftmost, stripping dummy bit
        pair = (n >> (n_digits - 3)) - 4
        # print(bin(pair))
        # left = pair >>2
        next_digit = int(pair == 0 or pair == 3)
        result += next_digit  # * (2 ** cur_digit - 1)
        # Remove leading digits plus dummy bit, then restore dummy bit,
        # effectively padding with zeroes
        n = strip_leading_digits(n, 3)
        n_digits -= 2
        n = add_dummy_bit(n, target_length=n_digits - 1)
        # print(bin(n))
    # print(bin(result))
    return result  # , n_digits


def make_checksum(n, offset):
    n >>= offset
    n = add_dummy_bit(n)
    # print(bin(n))
    # print(binary_digits(n))
    while (binary_digits(n) - 1) % 2 == 0:
        n = checksum_stage(n)
    return n


def byte_xor(bytes):
    return (48 + (x - 47) % 2 for x in bytes)


def dragon_curve_bytes(seed):
    last = seed
    while True:
        new = tuple(last) + (48,) + tuple(byte_xor(reversed(last)))
        yield new
        last = new


def fill_disk_bytes(bytes, disk_size):
    gen = dragon_curve_bytes(bytes)
    while len(bytes) < disk_size:
        bytes = next(gen)
    return bytes[:disk_size]


def generate_checksum(bytes):
    # breakpoint()
    while len(bytes) % 2 == 0:
        new = []
        for i in range(0, len(bytes) - 1, 2):
            new.append(int(bytes[i] == bytes[i + 1]))
        bytes = new
    return bytes


num = binary("11101000110010100")
expanded, offset = fill_disk(num, 272)
part1 = make_checksum(expanded, offset)
print(to_string(part1))

bytes = tuple(ord(x) for x in "11101000110010100")
disk_size = 35651584

expanded = fill_disk_bytes(bytes, disk_size)
part2 = generate_checksum(expanded)
print("".join(str(x) for x in part2))
