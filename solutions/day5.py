from hashlib import md5


def find_password(stem, part1, length=8):
    index = found = 0
    password: list[None | str] = [None] * length

    while found < length:
        this = str(md5(f"{stem}{index}".encode("utf-8")).hexdigest())
        if this[:5] == "00000":
            if part1:
                password[found] = this[5]
                found += 1
            else:
                try:
                    target = int(this[5])
                    if 0 <= target < length and password[target] is None:
                        password[target] = this[6]
                        found += 1
                except ValueError:
                    pass
        index += 1
    return "".join(password)


door_id = "abbhdwsy"
part1 = find_password(door_id, True)
print(part1)

part2 = find_password(door_id, False)
print(part2)
