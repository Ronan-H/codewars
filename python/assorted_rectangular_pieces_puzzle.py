import time
import array
from PIL import Image
from PIL import ImageDraw
import random
import colorsys

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
    for i, flipped, id_num in used:
        p = piece_copy([p for p in pieces if p[2] == id_num][0], flipped)
        y = i // side_len
        x = i % side_len
        random_fill = tuple(round(c * 255) for c in colorsys.hsv_to_rgb(random.random(), 1, 1))

        for y_off in range(p[0]):
            for x_off in range(p[1]):
                new_x = (x + x_off) * square_size
                new_y = (y + y_off) * square_size
                draw.rectangle((new_x, new_y, new_x + square_size, new_y + square_size), random_fill, (100, 100, 100))
    img.save(file_name)


def exhaust_piece_perms(board, side_len, hole_locs, holes_used, pieces, orig_pieces, used: list, max_candidates):
    if len(pieces) == 0:
        # all pieces placed, time to bail out
        return True

    if time.time() - s > 10:
        print("Took too long, terminating...")
        exit(0)

    candidates = []
    piece_candidate_counts = [0] * (max(p[2] for p in pieces) + 1)
    orig_perim = count_perimeter(board, side_len)
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
                    candidates.append((p, flipped, i, count_perimeter(board, side_len), 0))
                    piece_candidate_counts[p[2]] += 1
                    apply_piece_mask(board, side_len, None, p, i, True)
                    can_place_somewhere = True
        # make sure you can place every piece somewhere
        if not can_place_somewhere:
            draw_board(board, side_len, used, orig_pieces, 25, 'board.png')
            return False

    # sort candidate moves by perimeter, smallest to largest
    candidates.sort(key=lambda c: (piece_candidate_counts[c[0][2]], 0 if c[3] < orig_perim else 1))
    candidates = candidates[:max_candidates]
    #print(candidates)

    # each piece remaining needs at least one candidate move
    #if len(set(c[0][2] for c in candidates)) < len(set(p[2] for p in pieces)):
    #    return False

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
    max_candidates = 1
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
    ['00     000     ', ' 000           ', ' 000  0  0000  ', ' 000  00 00000 ', ' 000  00  0000 ', '  00  00     0 ', '  00  00  00000', '  00000000000  ', '   00    0     ', '   00  000 00  ', '       000  00 ', '       000  00 ', '        0    0 ', '            00 ', '            0  '],
    [[1, 1], [1, 1], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 3], [1, 3], [1, 3], [1, 3], [1, 3], [1, 4], [1, 4], [1, 5], [1, 8], [2, 2], [2, 2], [2, 4], [3, 3], [3, 4]]]

print('Solution:', solve_puzzle(*test_args))
