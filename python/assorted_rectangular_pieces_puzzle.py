import time
import array
from PIL import Image
from PIL import ImageDraw
import random
import colorsys
import copy

s = time.time()


def piece_copy(piece, flipped):
    p = [d for d in piece]
    if flipped:
        p[0], p[1] = p[1], p[0]
    return p


def can_place(board, side_len, piece, i):
    # bounds check
    if (i % side_len) + piece[1] > side_len or (i // side_len) + piece[0] > side_len:
        return False

    for r in range(piece[0]):
        row = r * side_len
        for j in range(piece[1]):
            if not board[row + i + j]:
                return False
    return True


def apply_piece_mask(board, side_len, holes_used, piece, i, placing):
    for r in range(piece[0]):
        row = r * side_len
        for c in range(piece[1]):
            index = row + i + c
            board[index] = placing

            if holes_used is not None:
                if placing:
                    holes_used.remove(index)
                else:
                    holes_used.add(index)


def count_perimeter(board, side_len):
    perim = 0
    size = len(board)

    for i in range(size):
        if board[i]:
            # ABOVE
            if i < side_len or not board[i - side_len]:
                perim += 1
            # BELOW
            if i >= (size - side_len) or not board[i + side_len]:
                perim += 1
            # LEFT
            if i % side_len == 0 or not board[i - 1]:
                perim += 1
            # RIGHT
            if i % side_len == side_len - 1 or not board[i + 1]:
                perim += 1

    return perim


def count_islands(board, side_len):
    size = len(board)
    visited = set()
    visited = set()
    stack = []
    count = 0

    for i in range(size):
        if board[i] and i not in visited:
            count += 1
            # begin flooding
            stack.append(i)

            while len(stack) > 0:
                index = stack.pop()
                visited.add(index)
                # ABOVE
                if index >= side_len and board[index - side_len] and (index - side_len) not in visited:
                    stack.append(index - side_len)
                # BELOW
                if index < (size - side_len) and board[index + side_len] and (index + side_len) not in visited:
                    stack.append(index + side_len)
                # LEFT
                if index % side_len > 0 and board[index - 1] and (index - 1) not in visited:
                    stack.append(index - 1)
                # RIGHT
                if index % side_len < side_len - 1 and board[index + 1] and (index + 1) not in visited:
                    stack.append(index + 1)

    return count


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
        p = piece_copy([p for p in pieces if p[2] == id_num][0], flipped)
        y = i // side_len
        x = i % side_len
        fill = tuple(round(c * 255) for c in colorsys.hsv_to_rgb(
            num / len(pieces), 1, 1)
        )
        num += 1

        for y_off in range(p[0]):
            for x_off in range(p[1]):
                new_x = (x + x_off) * square_size
                new_y = (y + y_off) * square_size
                draw.rectangle((new_x, new_y, new_x + square_size, new_y + square_size), fill, (100, 100, 100))
    img.save(file_name)


def exhaust_piece_perms(board, side_len, hole_locs, holes_used, pieces, orig_pieces, used: list, max_candidates):
    if len(pieces) == 0:
        # all pieces placed, time to bail out
        draw_board(board, side_len, used, orig_pieces, 25, 'board.png')
        return True

    if time.time() - s > 10:
        print("Took too long, terminating...")
        exit(0)

    candidates = []
    piece_candidate_counts = [0] * (max(p[2] for p in pieces) + 1)
    orig_perim = count_perimeter(board, side_len)
    orig_islands = count_islands(board, side_len)
    tried = set()
    # make a list of candidate moves, taking note of the resulting perimeter
    for piece in pieces:
        pf = piece_copy(piece, True)

        can_place_somewhere = False

        pt = (piece[0], piece[1])
        if pt in tried:
            continue
        tried.add(pt)
        tried.add((pt[1], pt[0]))

        for flipped in [False, True] if piece[0] != piece[1] else [False]:
            p = pf if flipped else piece

            for i in hole_locs.difference(set(u for u in holes_used)):
                if can_place(board, side_len, p, i):
                    apply_piece_mask(board, side_len, None, p, i, False)
                    candidates.append((p, flipped, i, count_perimeter(board, side_len), count_islands(board, side_len)))
                    piece_candidate_counts[p[2]] += 1
                    apply_piece_mask(board, side_len, None, p, i, True)
                    can_place_somewhere = True

        # make sure you can place every piece somewhere
        if not can_place_somewhere:
            #draw_board(board, side_len, used, orig_pieces, 25, 'board.png')
            #exit(0)
            return False

    # make sure all holes can be filled by a piece that hasn't been used yet
    board_copy = copy.copy(board)
    for c in candidates:
        p = piece_copy(c[0], True) if c[1] else c[0]
        apply_piece_mask(board_copy, side_len, None, p, c[2], False)
    if any(board_copy):
        # 1 or more holes couldn't be filled by any of the candidate piece moves
        #draw_board(board, side_len, used, orig_pieces, 25, 'board.png')
        #exit(0)
        return False

    # if any piece has only 1 legal move, place it and don't consider anything else
    one_moves = [c for c in candidates if piece_candidate_counts[c[0][2]] == 1]
    if len(one_moves) > 0:
        candidates = [one_moves[0]]
    else:
        # if any candidate move removes an island, make that move and don't consider anything else
        removes_island = [c for c in candidates if c[4] < orig_islands]
        if len(removes_island) > 0:
            candidates = [removes_island[0]]
        else:
            # sort candidates based on a heuristic
            candidates.sort(key=lambda c: (piece_candidate_counts[c[0][2]], (c[3]) / (2 * c[0][0] + 2 * c[0][1])))
            candidates = candidates[:max_candidates]

    # exhaust all piece positions using the above list
    for p, flipped, i, _, _ in candidates:
        #print('Placing piece', p)
        apply_piece_mask(board, side_len, holes_used, p, i, False)
        used.append([i, 1 if flipped else 0, p[2]])
        pieces_less_used = [x for x in pieces if x[2] != p[2]]
        params = board, side_len, hole_locs, holes_used, pieces_less_used, orig_pieces, used, max_candidates
        if exhaust_piece_perms(*params):
            return True
        # undo move
        #print('Backtracking...')
        used.pop()
        apply_piece_mask(board, side_len, holes_used, p, i, True)
    return False


def solve_puzzle(board, pieces):
    start = time.time()

    side_len = len(board)
    print('board:', board)
    print('pieces:', pieces)

    # give each piece an ID so they can be sorted back to their original order later
    pieces = [p + [i] for i, p in enumerate(pieces)]
    pieces.sort(key=lambda p: p[0] * p[1], reverse=True)
    board = array.array('b', [c == '0' for l in board for c in l])
    hole_locs = set(i for i, v in enumerate(board) if board[i])

    used = []
    max_candidates = 2
    while not exhaust_piece_perms(board, side_len, hole_locs, set(), pieces, pieces, used, max_candidates):
        max_candidates += 1
        used = []
    print('Max candidates:', max_candidates)

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
    ['00       00         ', '00       00         ', '00       00    0000 ', '0000     000000000  ', '0000000000 00  000  ', '00         00  000  ', '00         00  000  ', ' 000000000000     0 ', '  0000  0   0000  0 ', '    000000000000  0 ', '    000000000000 000', '  0000 000000000 0  ', '  000000 0000000 0  ', '      0000       0  ', '                 0  ', '               000  ', '  0            00   ', ' 000      000000    ', ' 00       00        ', '   00   00000       '],
    [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 3], [1, 3], [1, 3], [1, 4], [1, 4], [1, 4], [1, 4], [1, 6], [1, 12], [2, 2], [2, 2], [2, 2], [2, 2], [2, 3], [2, 3], [2, 4], [2, 4], [2, 5], [2, 7], [3, 5], [4, 7]]]

print('Solution:', solve_puzzle(*test_args))
