import array
import bisect


def gen_place_map(board, side_len, holes):
    """
    Generates a mapping of the biggest pieces that can fit into each hole remaining in the board.
    """
    place_map = dict()
    size = len(board)
    for i in holes:
        j = i
        max_width = -1
        height = 1
        hole_place_map = []
        row_end = i + (side_len - (i % side_len))

        # loop with ascending rectangle height
        while j < size:
            width = 0
            # find the maximum width rectangle that can fit here
            while j < row_end and board[j] and (max_width == -1 or width < max_width):
                j += 1
                width += 1
            if width == 0:
                break
            hole_place_map.append(width)
            max_width = width if max_width == -1 else min(width, max_width)
            j = i + (height * side_len)
            height += 1
            row_end += side_len

        place_map[i] = [len(hole_place_map)] + hole_place_map

    return place_map


def apply_piece_mask(board, side_len, holes, piece, i, placing):
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


def add_to_candidate_locations(locs, side_len, candidate, i):
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


def removes_island(board, side_len, piece, i):
    """
    Returns True if placing piece removes an island, false otherwise.
    Assumes the move has been validated already.
    """

    size = len(board)
    # TOP SIDE
    if i >= side_len:
        for j in range(piece[1]):
            if board[(i + j) - side_len]:
                return False
    # BOTTOM SIDE
    if i + (piece[0] * side_len) < size:
        for j in range(piece[1]):
            if board[i + j + (piece[0] * side_len)]:
                return False
    # LEFT SIDE
    if i % side_len != 0:
        for j in range(piece[0]):
            if board[i + (j * side_len) - 1]:
                return False
    # RIGHT SIDE
    if i % side_len != side_len - 1:
        for j in range(piece[0]):
            if board[i + (j * side_len) + 1]:
                return False

    return True


def gen_move_candidates(board, side_len, holes, pieces, max_candidates):
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
    piece_candidate_counts = [0] * (max(p[2] for p in pieces) + 1)
    # mapping of the candidate moves which could fill each hole on the board
    candidate_locations = {h: set() for h in holes}
    candidate_id = 0
    # pre-process a map of the biggest pieces that can fill each hole
    place_map = gen_place_map(board, side_len, holes)
    tried = set()
    # make a list of all possible candidate moves
    for piece in pieces:
        can_place_somewhere = False
        # only try each piece dimension once (I.e. if there are 2 of the same shape,
        # there's no point in exhausting all moves for both)
        pt = (piece[0], piece[1])
        if pt in tried:
            continue
        # add both flipped and unflipped variations, since they'll both be tested
        tried.add(pt)
        tried.add((pt[1], pt[0]))

        # test the piece and the flipped version, unless it's a square (which is the same when flipped)
        for flipped in [False, True] if piece[0] != piece[1] else [False]:
            p = [piece[1], piece[0], piece[2]] if flipped else piece

            for i in holes:
                # check if this piece can fit at this index
                hole_place_map = place_map[i]
                if p[0] <= hole_place_map[0] and p[1] <= hole_place_map[p[0]]:
                    # record candidate piece move
                    candidate = (p, flipped, i, candidate_id)
                    add_to_candidate_locations(candidate_locations, side_len, candidate, i)
                    island_removed = removes_island(board, side_len, p, i)
                    if island_removed:  # placing this piece removes an island
                        # best move
                        return [candidate]
                    candidates.append(candidate)
                    candidate_id += 1
                    piece_candidate_counts[p[2]] += 1
                    can_place_somewhere = True

        # make sure you can place this piece somewhere
        if not can_place_somewhere:
            return []

    # if any piece can only go in one place, don't consider any other candidate move
    for c in candidates:
        if piece_candidate_counts[c[0][2]] == 1:
            return [c]

    for i, c in candidate_locations.items():
        # if any hole can only be filled by one candidate move, don't consider any other candidate move
        if len(c) == 1:
            return [candidates[list(c)[0]]]

        # make sure all holes can be filled by a piece that hasn't been used yet
        if len(c) == 0:
            # invalid board state
            return []

    # a complicated heuristic idea, but a summary is: how unique is each candidate move?
    # if a candidate move fills squares that could be filled by many other candidate moves, that's probably
    # a bad move (and vice versa)
    candidate_squares = [0] * len(candidates)
    for cl in candidate_locations.values():
        for cid in cl:
            # using exponentiation so that higher numbers are considered much worse
            candidate_squares[cid] += len(cl) ** len(cl)

    # sort candidate moves based on some heuristics
    candidates.sort(key=lambda x: (piece_candidate_counts[x[0][2]], candidate_squares[x[3]]))
    candidates = candidates[:max_candidates]

    # no special case, all candidates will be exhausted at this level
    # using the above heuristic until the puzzle is solved
    return candidates


def exhaust_piece_perms(board, side_len, holes, pieces, orig_pieces, used: list, max_candidates):
    """
    Recursively exhausts all possible piece moves from a given board state, with the help of gen_move_candidates.
    """

    if len(pieces) == 0:
        # all pieces placed, puzzle solved
        return True

    candidates = gen_move_candidates(board, side_len, holes, pieces, max_candidates)

    # exhaust all candidate moves using the above list
    for p, flipped, i, _ in candidates:
        # apply move
        apply_piece_mask(board, side_len, holes, p, i, False)
        used.append([i, 1 if flipped else 0, p[2]])
        pieces_less_used = [x for x in pieces if x[2] != p[2]]

        # recursive call
        if exhaust_piece_perms(board, side_len, holes, pieces_less_used, orig_pieces, used, max_candidates):
            return True

        # undo move
        used.pop()
        apply_piece_mask(board, side_len, holes, p, i, True)

    # no candidates lead to a solved puzzle; this is an invalid board state
    return False


def solve_puzzle(board, pieces):
    side_len = len(board)

    # give each piece an ID so they can be sorted back to their original order later
    pieces = [p + [i] for i, p in enumerate(pieces)]
    # sort pieces from biggest to smallest (this doesn't make too much of a difference anymore, but it helps)
    pieces.sort(key=lambda p: p[0] * p[1], reverse=True)
    board = array.array('b', [sq == '0' for row in board for sq in row])
    holes = [i for i, _ in enumerate(board) if board[i]]

    # this idea is similar to an "iterative deepening depth-first search",
    # it prevents the first few moves from being "locked in" and reduces
    # the resulting combinatorial explosion of the rest of the search
    used = []
    max_candidates = 2
    while not exhaust_piece_perms(board, side_len, holes, pieces, pieces, used, max_candidates):
        max_candidates += 1
        used = []

    # at this point the puzzle has been solved, and the used pieces just need to be reformatted

    # convert single index back into 2D indexes
    used = [[u[0] // side_len, u[0] % side_len, u[1], u[2]] for u in used]
    # restore original piece ordering
    used.sort(key=lambda p: p[3])
    # remove piece IDs
    used = [p[:3] for p in used]

    return used
