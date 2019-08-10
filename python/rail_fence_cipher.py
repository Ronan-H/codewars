import itertools


# generator used to cycle through indexes (eg. 0, 1, 2, 1, 0, 1 ..)
def cycle_indexes(n):
    nums = [n for n in range(n)]
    index_cycle = itertools.cycle(nums + nums[-2:0:-1])
    while True:
        yield next(itertools.cycle(index_cycle))


def encode_rail_fence_cipher(string, n):
    cycle = cycle_indexes(n)

    # distribute characters into rails
    rails = [""] * n
    for c in string:
        rails[next(cycle)] += c

    # join rails together into one encoded message
    return "".join(rails)


def decode_rail_fence_cipher(string, n):
    cycle = cycle_indexes(n)

    # count number of characters in each rail when string
    # was encoded
    rail_counts = [0] * n

    for _ in string:
        rail_counts[next(cycle)] += 1

    # reconstruct rail characters
    rails = []
    index = 0
    for count in rail_counts:
        rails.append(list(string[index:index + count]))
        index += count

    # alternate through rails to decode message
    cycle = cycle_indexes(n)
    decoded = ""
    for _ in string:
        decoded += rails[next(cycle)].pop(0)

    return decoded

