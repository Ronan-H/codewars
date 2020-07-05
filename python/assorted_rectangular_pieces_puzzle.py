import time
import array
import bisect
from PIL import Image
from PIL import ImageDraw
import colorsys
import cProfile

s = time.time()


def draw_board(board, side_len, used, pieces, square_size, file_name):
    img_len = side_len * square_size
    img = Image.new('RGB', (img_len, img_len), color='black')
    draw = ImageDraw.Draw(img)

    # draw holes
    for i in range(len(board)):
        if board[i]:
            y = (i // side_len) * square_size
            x = (i % side_len) * square_size
            draw.rectangle((x, y, x + square_size, y + square_size), fill=(255, 255, 255))

    # draw each piece placed on the board in random colours
    print('used', used)
    print('pieces', pieces)
    num = 0
    for i, flipped, id_num in used:
        piece = None
        for p in pieces:
            if p[2] == id_num:
                piece = [p[1], p[0], p[2]] if flipped else p
                break

        y = i // side_len
        x = i % side_len
        fill = tuple(round(c * 255) for c in colorsys.hsv_to_rgb(
            num / len(pieces), 1, 1)
        )
        num += 1

        for y_off in range(piece[0]):
            for x_off in range(piece[1]):
                new_x = (x + x_off) * square_size
                new_y = (y + y_off) * square_size
                draw.rectangle((new_x, new_y, new_x + square_size, new_y + square_size), fill, (100, 100, 100))
    img.save(file_name)


def apply_piece_mask(board, side_len, holes, piece, i, placing):
    for r in range(piece[0]):
        row = r * side_len
        for c in range(piece[1]):
            index = row + i + c
            board[index] = placing

            if holes:
                if placing:
                    bisect.insort(holes, index)
                else:
                    holes.remove(index)


def add_to_candidate_locations(locs, side_len, candidate, i):
    piece = candidate[0]
    for r in range(piece[0]):
        row = r * side_len
        for c in range(piece[1]):
            index = i + row + c
            # record candidate id at this board index
            locs[index].add(candidate[3])


def removes_island(board, side_len, piece, i):
    """
    Returns True if placing piece removes an island, false otherwise.
    Assumes can_place(board, side_len, piece, i) is True
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
    candidates = []
    piece_candidate_counts = [0] * (max(p[2] for p in pieces) + 1)
    tried = set()
    candidate_locations = {h: set() for h in holes}
    candidate_id = 0
    # make a list of all possible candidate moves
    for piece in pieces:
        can_place_somewhere = False
        # only try each piece dimension once (I.e. if there are 2 of the same shape, there's no point in exhausting
        # all moves for both)
        pt = (piece[0], piece[1])
        if pt in tried:
            continue
        tried.add(pt)
        tried.add((pt[1], pt[0]))

        for flipped in [False, True] if piece[0] != piece[1] else [False]:
            p = [piece[1], piece[0], piece[2]] if flipped else piece

            for i in holes:
                # make sure you can place this piece at this index
                if (i % side_len) + p[1] > side_len or (i // side_len) + p[0] > side_len \
                        or not all(board[i + (r * side_len) + j] for r in range(p[0]) for j in range(p[1])):
                    continue

                # piece can be placed at this index
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

        # make sure you can place every piece somewhere
        if not can_place_somewhere:
            return []

    # if any piece can only go in one place, don't consider any other candidate move
    for c in candidates:
        if piece_candidate_counts[c[0][2]] == 1:
            return [c]

    for i, c in candidate_locations.items():
        if board[i]:
            # make sure all holes can be filled by a piece that hasn't been used yet
            if len(c) == 0:
                # 1 or more holes couldn't be filled by any of the candidate piece moves; invalid board state
                return []

            # if any hole can only be filled by one piece, don't consider any other candidate move
            elif len(c) == 1:
                return [candidates[list(c)[0]]]

    candidate_squares = [0] * len(candidates)

    for cl in candidate_locations.values():
        for cid in cl:
            candidate_squares[cid] += len(cl)

    #print(sorted([(piece_candidate_counts[x[0][2]], candidate_squares[x[3]], max(x[0][0], x[0][1])) for x in candidates]))
    # sort candidates based on a heuristic
    candidates.sort(key=lambda x: (piece_candidate_counts[x[0][2]], candidate_squares[x[3]]))
    candidates = candidates[:max_candidates]

    # no special case, all candidates will be exhausted using the above heuristic
    return candidates


def exhaust_piece_perms(board, side_len, holes, pieces, orig_pieces, used: list, max_candidates):
    if len(pieces) == 0:
        # all pieces placed, time to bail out
        # draw_board(board, side_len, used, orig_pieces, 25, 'board.png')
        return True

    #if time.time() - s > 10:
    #    print("Took too long, terminating...")
    #    exit(0)

    candidates = gen_move_candidates(board, side_len, holes, pieces, max_candidates)

    # exhaust all piece positions using the above list
    for p, flipped, i, _ in candidates:
        apply_piece_mask(board, side_len, holes, p, i, False)
        used.append([i, 1 if flipped else 0, p[2]])
        pieces_less_used = [x for x in pieces if x[2] != p[2]]
        params = board, side_len, holes, pieces_less_used, orig_pieces, used, max_candidates
        if exhaust_piece_perms(*params):
            return True
        # undo move
        used.pop()
        apply_piece_mask(board, side_len, holes, p, i, True)

    # no candidates worked; this is an invalid board state
    #draw_board(board, side_len, used, orig_pieces, 25, 'board.png')
    #exit()
    return False


def solve_puzzle(board, pieces):
    start = time.time()

    print(str(board) + ',')
    print(pieces)

    side_len = len(board)
    # give each piece an ID so they can be sorted back to their original order later
    pieces = [p + [i] for i, p in enumerate(pieces)]
    pieces.sort(key=lambda p: p[0] * p[1], reverse=True)
    board = array.array('b', [c == '0' for l in board for c in l])
    holes = [i for i, _ in enumerate(board) if board[i]]

    used = []
    max_candidates = 2
    while not exhaust_piece_perms(board, side_len, holes, pieces, pieces, used, max_candidates):
        max_candidates += 1
        print("Retrying with max_candidates = ", max_candidates)
        used = []

    # convert single index back into 2D indexes
    used = [[u[0] // side_len, u[0] % side_len, u[1], u[2]] for u in used]
    # restore original piece ordering
    used.sort(key=lambda p: p[3])
    # remove piece IDs
    used = [p[:3] for p in used]

    ms_taken = (time.time() - start) * 1000
    print(f'Took {ms_taken:.2f} ms.')

    return used


test_args =\
[
    ['   00  0       0   0  0 ', '   00  0      0000000000', '    000000    0000000000', '  00000       0000000000', '   0000000    0000000000', '       0      0000000000', '000000000     0000000000', '000000000     0000000000', '0000000 000   0000000000', '       0000   0000000000', '      00000   0000000000', '00000000000 000    0000 ', '00000000000 00   00 0   ', '00000000000 00000 00    ', ' 000 000    00000 0 0   ', '   00000  000000000  000', '   00     000  000000000', '   0000   0000000000000 ', '   0000   000000     00 ', '     00000000000     000', '        00000000 00  000', '        0000000 000  000', '        00000000000  00 ', '              00000  00 '],
    [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 3], [1, 3], [1, 3], [1, 4], [1, 4], [1, 4], [1, 4], [1, 5], [1, 5], [1, 6], [2, 2], [2, 2], [2, 2], [2, 2], [2, 3], [2, 3], [2, 3], [2, 4], [2, 4], [2, 4], [2, 4], [2, 4], [2, 5], [2, 9], [3, 6], [3, 7], [4, 5], [4, 6], [10, 10]]
]

#cProfile.run('solve_puzzle(*test_args)')
print('Solution:', solve_puzzle(*test_args))
