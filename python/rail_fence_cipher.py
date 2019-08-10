
def get_indexes(n):
    down = [n for n in range(n)]
    up = down[-2:0:-1]
    return down + up


def encode_rail_fence_cipher(string, n):
    indexes = get_indexes(n)

    rails = [""] * n
    pos = 0

    for c in string:
        rails[indexes[pos]] += c
        pos = (pos + 1) % len(indexes)

    return "".join(rails)


def decode_rail_fence_cipher(string, n):
    rails = [""] * n
    pos = 0
    direction = 1

    for c in string:
        rails[pos] += c

        pos += direction
        if pos < 0:
            pos = 1
            direction = 1
        elif pos > n - 1:
            pos = n - 2
            direction = -1

    return "".join(rails)
