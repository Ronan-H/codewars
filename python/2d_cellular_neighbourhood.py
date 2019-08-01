
def in_bounds(m, n, w, h):
    return 0 <= m < h and 0 <= n < w


def get_neighbourhood(n_type, mat, coordinates):
    m, n = coordinates
    w, h = len(mat[0]), len(mat)

    if not in_bounds(m, n, w, h):
        return []

    offsets = (-1, 0, 1)
    neighbours = []

    for offset_m in offsets:
        for offset_n in offsets:
            new_m, new_n = m + offset_m, n + offset_n
            if (abs(offset_m) + abs(offset_n) == 1 or n_type == "moore") \
                and not (offset_m == offset_n == 0) and in_bounds(new_m, new_n, w, h):
                neighbours.append(mat[new_m][new_n])

    return neighbours
