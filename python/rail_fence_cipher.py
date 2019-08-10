
def get_indexes(n):
    down = [n for n in range(n)]
    up = down[-2:0:-1]
    return down + up


def encode_rail_fence_cipher(string, n):
    indexes = get_indexes(n)

    # distribute characters into rails
    rails = [""] * n
    pos = 0
    for c in string:
        rails[indexes[pos]] += c
        pos = (pos + 1) % len(indexes)

    # join rails together into one encoded message
    return "".join(rails)


def decode_rail_fence_cipher(string, n):
    indexes = get_indexes(n)

    # count number of characters in each rail when string
    # was encoded
    rail_counts = [0] * n
    pos = 0

    for _ in string:
        index = indexes[pos]
        rail_counts[index] += 1
        pos = (pos + 1) % len(indexes)

    # reconstruct rails
    rails = []
    index = 0
    for count in rail_counts:
        rails.append(list(string[index:index + count]))
        index += count

    # alternate through rails to decode message
    pos = 0
    decoded = ""
    for _ in string:
        index = indexes[pos]
        decoded += rails[index][0]
        del rails[index][0]
        pos = (pos + 1) % len(indexes)

    return decoded


print(decode_rail_fence_cipher("WECRLTEERDSOEEFEAOCAIVDEN", 3), "WEAREDISCOVEREDFLEEATONCE", sep="\n")
