import time
import array

def piece_copy(piece, flipped):
    p = [d for d in piece]
    if flipped:
        p[0], p[1] = p[1], p[0]
    return p


def can_place(board, piece, x, y):
    # bounds check
    if x + piece[1] > len(board) or y + piece[0] > len(board):
        return False

    for i in range(y, y + piece[0]):
        for j in range(x, x + piece[1]):
            if not board[i][j]:
                return False
    return True


def apply_piece_mask(board, holes_used, piece, x, y, placing):
    for i in range(y, y + piece[0]):
        for j in range(x, x + piece[1]):
            board[i][j] = placing

            if holes_used is not None:
                if placing:
                    holes_used.remove((i, j))
                else:
                    holes_used.add((i, j))


def count_perimeter(board):
    perim = 0

    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x]:
                if y == 0 or not board[y - 1][x]:
                    perim += 1
                if y == len(board) - 1 or not board[y + 1][x]:
                    perim += 1
                if x == 0 or not board[y][x - 1]:
                    perim += 1
                if x == len(board) - 1 or not board[y][x + 1]:
                    perim += 1

    return perim


def exhaust_piece_perms(board, hole_locs, holes_used, pieces, used: list, index=0):
    if index == len(pieces):
        # all pieces placed, time to bail out
        return True

    piece = pieces[index]
    pf = piece_copy(piece, True)
    candidates = []

    # make a list of candidate moves, taking note of the resulting perimeter
    for i, j in hole_locs.difference(set(u for u in holes_used)):
        for flipped in [False, True] if piece[0] != piece[1] else [False]:
            p = pf if flipped else piece
            if can_place(board, p, j, i):
                apply_piece_mask(board, None, p, j, i, False)
                candidates.append((i, j, flipped, count_perimeter(board)))
                apply_piece_mask(board, None, p, j, i, True)

    # sort candidate moves by perimeter, smallest to largest
    candidates.sort(key=lambda c: c[3], reverse=False)

    # exhaust all piece positions using the above list
    for i, j, flipped, _ in candidates:
        p = pf if flipped else piece
        apply_piece_mask(board, holes_used, p, j, i, False)
        used.append([i, j, 1 if flipped else 0, piece[2]])
        params = board, hole_locs, holes_used, pieces, used, index + 1
        if exhaust_piece_perms(*params):
            return True
        # undo move
        used.pop()
        apply_piece_mask(board, holes_used, p, j, i, True)
    return False


def solve_puzzle(board, pieces):
    start = time.time()

    # give each piece an ID so they can be sorted back to their original order later
    pieces = [p + [i] for i, p in enumerate(pieces)]
    pieces.sort(key=lambda p: p[0] * p[1], reverse=True)
    board = tuple(array.array('b', [1 if c == '0' else 0 for c in l]) for l in board)
    hole_locs = set([(i, j) for (i, j) in [(i, j) for i in range(len(board)) for j in range(len(board))] if board[i][j]])

    used = []
    exhaust_piece_perms(board, hole_locs, set(), pieces, used)
    # restore original piece ordering
    used.sort(key=lambda p: p[3])
    # remove piece IDs
    used = [p[:3] for p in used]

    ms_taken = (time.time() - start) * 1000
    print(f'Took {ms_taken:.2f} ms.')

    return used


pre_test1 =\
[
    [
			'            ',
			' 00000      ',
			' 00000      ',
			' 00000   00 ',
			'       000  ',
			'   00  000  ',
			' 0000 00    ',
			' 0000 00    ',
			' 00   000 0 ',
			'   0  000 0 ',
			' 000      0 ',
			'            '
    ],
	[[1,1],[1,1],[1,2],[1,2],[1,2],[1,3],[1,3],[1,4],[1,4],[2,2],[2,2],[2,3],[2,3],[2,5]]]

print('Solution:', solve_puzzle(*pre_test1))