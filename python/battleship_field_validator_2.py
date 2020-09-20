import array
import bisect
import time

s = time.time()

num_cells = 100
side_len = 10


def gen_place_map(board, holes):
    """
    Generates a mapping of the biggest pieces that can fit into each hole remaining in the board.
    """
    place_map = dict()
    for i in holes:
        j = i
        max_width = 0
        max_height = 0
        row_end = i + (side_len - (i % side_len))

        while j < row_end and board[j]:
            max_width += 1
            j += 1

        j = i
        while j < num_cells and board[j]:
            max_height += 1
            j += side_len

        place_map[i] = [max_height, max_width]

    return place_map


def apply_piece_mask(board, holes, piece, i, placing):
    """
    Apply or undo the move of placing a piece at index i on the board.
    """
    for r in range(piece[0]):
        row = r * side_len
        for c in range(piece[1]):
            index = row + i + c
            board[index] = placing

            # keep track of which holes remain on the board after this move
            if holes:
                if placing:
                    # keeping the holes in sorted order seems to improve efficiency massively
                    bisect.insort(holes, index)
                else:
                    holes.remove(index)


def add_to_candidate_locations(locs, candidate, i):
    """
    Updates a map of the candidate moves which fill each remaining hole on the board.
    """
    piece = candidate[0]
    for r in range(piece[0]):
        row = r * side_len
        for c in range(piece[1]):
            index = row + i + c
            # record candidate id at this board index
            locs[index].add(candidate[3])


def gen_move_candidates(board, holes, piece):
    """
    Generates a list of all possible moves from a given board state.
    This list may be pruned, E.g. one candidate move may be returned if
    that move can logically be made first with no risk of reaching
    an illegal board state down the line. An empty list may be returned
    if the given board state is found to have no solutions by various
    tests.
    """

    candidates = []
    # number of candidate moves found per piece
    piece_candidate_counts = dict()
    # mapping of the candidate moves which could fill each hole on the board
    candidate_locations = {h: set() for h in holes}
    candidate_id = 0
    # pre-process a map of the biggest pieces that can fill each hole
    place_map = gen_place_map(board, holes)
    # make a list of all possible candidate moves

    can_place_somewhere = False

    # test the piece and the flipped version, unless it's a submarine (which is the same when flipped)
    for flipped in [False, True] if piece != 1 else [False]:
        p = (1, piece) if flipped else (piece, 1)

        for i in holes:
            # check if this piece can fit at this index
            hole_place_map = place_map[i]
            if p[0] <= hole_place_map[0] and p[1] <= hole_place_map[1]:
                # record candidate piece move
                candidate = (p, flipped, i, candidate_id)
                add_to_candidate_locations(candidate_locations, candidate, i)
                candidates.append(candidate)
                candidate_id += 1
                can_place_somewhere = True

    # make sure you can place this piece somewhere
    if not can_place_somewhere:
        return []

    # a complicated heuristic idea, but a summary is: how unique is each candidate move?
    # if a candidate move fills squares that could be filled by many other candidate moves, that's probably
    # a bad move (and vice versa)
    # candidate_squares = [0] * len(candidates)
    # for cl in candidate_locations.values():
    #     for cid in cl:
    #         # using exponentiation so that higher numbers are considered much worse
    #         candidate_squares[cid] += len(cl) ** len(cl)

    # sort candidate moves based on some heuristics
    # candidates.sort(key=lambda x: (piece_candidate_counts[x[0]], candidate_squares[x[3]]))

    # no special case, all candidates will be exhausted at this level
    # using the above heuristic until the puzzle is solved
    return candidates


def exhaust_piece_perms(board, holes, pieces):
    """
    Recursively exhausts all possible piece moves from a given board state, with the help of gen_move_candidates.
    """

    if len(pieces) == 0:
        # all pieces placed, puzzle solved
        return True

    # if time.time() - s > 10:
    #     print("Took too long, terminating...")
    #     exit(0)

    piece = pieces[-1]
    del pieces[-1]
    candidates = gen_move_candidates(board, holes, piece)

    # exhaust all candidate moves using the above list
    for p, flipped, i, _ in candidates:
        # apply move
        apply_piece_mask(board, holes, p, i, False)

        # recursive call
        if exhaust_piece_perms(board, holes, pieces):
            return True

        # undo move
        apply_piece_mask(board, holes, p, i, True)

    pieces.append(piece)

    # no candidates lead to a solved puzzle; this is an invalid board state
    return False


def solve_puzzle(board, pieces):
    pieces.sort()
    board = array.array('b', [sq == 1 for row in board for sq in row])
    holes = [i for i, _ in enumerate(board) if board[i]]

    return exhaust_piece_perms(board, holes, pieces)


def validate_battlefield(battle_field):
    ship_lens = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

    print('BattleField:')
    for row in battle_field:
        print(row, ',', sep='')
    # for row in battle_field:
    #     for cell in row:
    #         print('X' if cell == 1 else ' ', ' ', end='')
    #     print()

    # first check that the correct number of cells are occupied by ships
    actual_num_occupied = sum(sum(row) for row in battle_field)
    expected_num_occupied = sum(ship_lens)
    if actual_num_occupied != expected_num_occupied:
        return False

    result = solve_puzzle(battle_field, ship_lens)
    time_taken = time.time() - s
    print('Time taken: ', time_taken)
    return result


print('Actual:', validate_battlefield(
		[[1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
		 [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
		 [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
		 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
		 [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
		 [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]))
print('Expected: True\n')

print('Actual:', validate_battlefield(
		[[1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
		 [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
		 [1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
		 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
		 [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
		 [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
		 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]))
print('Expected: False\n')

print('Actual:', validate_battlefield(
		[[0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
[0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
[0, 1, 1, 1, 0, 1, 1, 0, 0, 0],
[0, 1, 0, 0, 0, 0, 1, 1, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]))
print('Expected: ~~\n')
