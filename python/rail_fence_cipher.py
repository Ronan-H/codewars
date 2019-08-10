
def encode_rail_fence_cipher(string, n):
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


def decode_rail_fence_cipher(string, n):
    pass

