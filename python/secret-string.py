
def force_order(buffer, triplet):
    sorted_indexes = sorted(buffer.index(t) for t in triplet)

    for i in range(len(triplet)):
        buffer[sorted_indexes[i]] = triplet[i]


def recoverSecret(triplets):
    buffer = set()

    for arr in triplets:
        buffer.update(arr)

    buffer = list(buffer)

    last_buffer = None
    while tuple(buffer) != last_buffer:
        last_buffer = tuple(buffer)
        for triplet in triplets:
            force_order(buffer, triplet)

    return ''.join(buffer)
