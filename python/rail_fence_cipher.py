
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
    indexes = get_indexes(n)

    rail_counts = [0] * n
    pos = 0

    for _ in string:
        rail_counts[indexes[pos]] += 1
        pos = (pos + 1) % len(indexes)

    rails = []
    index = 0
    for count in rail_counts:
        rails.append(list(string[index:index + count]))
        index += count

    pos = 0
    decoded = ""
    for _ in string:
        decoded += rails[indexes[pos]][0]
        del rails[indexes[pos]][0]
        pos = (pos + 1) % len(indexes)

    return decoded


print(decode_rail_fence_cipher("WECRLTEERDSOEEFEAOCAIVDEN", 3), "WEAREDISCOVEREDFLEEATONCE", sep="\n")
