# generate knight move offsets
offs = (-2, -1, 1, 2)
knight_offs = set((x, y) for x in offs for y in offs if abs(x) != abs(y))


# generates all possible knight moves from position p
def add_moves_from(p, s):
    for off in knight_offs:
        m0 = p[0] + off[0]
        m1 = p[1] + off[1]
        if 0 <= m0 <= 7 and 0 <= m1 <= 7:  # bounds check
            s.add((m0, m1))


def to_ordinal(p):
    return ord(p[0]) - ord('a'), int(p[1]) - 1


def knight(start, target):
    # search moves from the start and target
    # the shortest sequence of moves is found when the two trees of moves intersect
    start_squares = {to_ordinal(start)}
    target_squares = {to_ordinal(target)}
    moves = 0

    while len(start_squares & target_squares) == 0:
        # alternate between expanding the start and target paths
        if moves % 2 == 0:
            expanding_set = start_squares
        else:
            expanding_set = target_squares

        # explore all possible knight moves from all squares where the knight could be on this move
        squares_reached = set()
        for p in expanding_set:
            add_moves_from(p, squares_reached)
        expanding_set |= squares_reached
        moves += 1

    return moves
