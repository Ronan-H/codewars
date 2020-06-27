
def piece_copy(piece, flipped):
    p = [d for d in piece]
    if flipped:
        p[0], p[1] = p[1], p[0]
    return p


def can_place(board, piece, flipped, x, y):
    p = piece_copy(piece, flipped)

    # bounds check
    if x + p[1] > len(board[0]) or y + p[0] > len(board):
        return False

    for i in range(y, y + p[0]):
        for j in range(x, x + p[1]):
            if not board[i][j]:
                return False
    return True


def apply_piece_mask(board, piece, x, y, flipped, placing=False):
    p = piece_copy(piece, flipped)

    for i in range(y, y + p[0]):
        for j in range(x, x + p[1]):
            board[i][j] = placing


def exhaust_piece_perms(board, pieces, used: list, index=0):
    if index == len(pieces):
        # all pieces placed, time to bail out
        return True

    piece = pieces[index]
    for flipped in [False, True]:
        for i in range(len(board)):
            for j in range(len(board[0])):
                #print('Trying to place piece', piece, 'at', j, i, 'flipped: ', flipped)
                if can_place(board, piece, flipped, j, i):
                    #print('Placing', piece, j, i)
                    apply_piece_mask(board, piece, j, i, flipped)
                    used.append([i, j, 1 if flipped else 0, piece[2]])
                    params = board, pieces, used, index + 1
                    if exhaust_piece_perms(*params):
                        return True
                    apply_piece_mask(board, piece, j, i, flipped, placing=True)
                    used.pop()
    return False


def solve_puzzle(board, pieces):
    # give each piece an ID so they can be sorted back to their original order later
    pieces = [p + [i] for i, p in enumerate(pieces)]
    pieces.sort(key=lambda p: p[0] * p[1], reverse=True)
    board = [[c == '0' for c in l] for l in board]
    #print('Board:', board)
    #print('Pieces:', pieces)

    used = []
    exhaust_piece_perms(board, pieces, used)
    # restore original piece ordering
    used.sort(key=lambda p: p[3])
    # remove piece IDs
    used = [p[:3] for p in used]
    return used


pre_test1 = [
	[
		'     0  ',
		' 00  0  ',
		' 00     ',
		' 00     ',
		'   0    ',
		'       0',
		'       0',
		'0000   0'],[[1,1],[1,2],[1,3],[1,4],[2,3]]]

print('Solution:', solve_puzzle(*pre_test1))