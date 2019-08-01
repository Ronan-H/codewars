
def get_neighbourhood(n_type, mat, coordinates):
    m, n = coordinates
    w, h = len(mat[0]), len(mat)
    offsets = (-1, 0, 1)
    neighbours = []

    for om in offsets:
        for on in offsets:
            nm, nn = m + om, n + on
            if (abs(om) + abs(on) == 1 or n_type == "moore") \
                and not (om == on == 0) \
                and 0 <= nm < h and 0 <= nn < w:
                neighbours.append(mat[nm][nn])

    return neighbours
