# adapted from my solution to the harder kata "Assorted Rectangular Pieces Puzzle", hehehe...

import array
import bisect

# battleship field dimensions
num_cells = 100
side_len = 10


def gen_place_map(field, ship_cells):
    """
    Generates a mapping of the biggest ship lengths that can fit into each ship cell remaining on the field.
    """
    place_map = dict()
    for i in ship_cells:
        j = i
        max_x = 0
        max_y = 0
        row_end = i + (side_len - (i % side_len))

        # find the longest horizontal ship size that can fit here
        while j < row_end and field[j]:
            max_x += 1
            j += 1

        # find the longest vertical ship size that can fit here
        j = i
        while j < num_cells and field[j]:
            max_y += 1
            j += side_len

        place_map[i] = [max_y, max_x]

    return place_map


def apply_ship_mask(field, ship_cells, ship_dim, i, placing):
    """
    Apply or undo the move of placing a ship at index i on the field.
    """
    for r in range(ship_dim[0]):
        row = r * side_len
        for c in range(ship_dim[1]):
            index = row + i + c
            field[index] = placing

            # keep track of which empty ship_cells remain on the field after this move
            if ship_cells:
                if placing:
                    # keep the ship_cells in sorted order for efficiency
                    bisect.insort(ship_cells, index)
                else:
                    ship_cells.remove(index)


def gen_placement_candidates(field, ship_cells, ship_len):
    """
    Generates all possible ship placements for a given field state, for a single ship.
    """
    # pre-process a map of the biggest ships that can fill each ship_cell
    place_map = gen_place_map(field, ship_cells)

    # test the ship and the flipped version, unless it's a submarine (which is the same when flipped)
    for flipped in [False, True] if ship_len != 1 else [False]:
        ship_dim = (1, ship_len) if flipped else (ship_len, 1)

        for i in ship_cells:
            # check if this ship can fit at this index
            ship_cell_place_map = place_map[i]
            if ship_dim[0] <= ship_cell_place_map[0] and ship_dim[1] <= ship_cell_place_map[1]:
                # yield this possible ship placement
                yield ship_dim, flipped, i


def is_setup_valid(field, ship_cells, ships):
    """
    Checks if a given field setup is valid by recursively exhausting
    all possible ship placements.
    """
    if len(ships) == 0:
        # all ships placed, field is valid
        return True

    # generate all placement permutations for the next ship
    ship_len = ships[-1]
    del ships[-1]
    candidates = gen_placement_candidates(field, ship_cells, ship_len)

    # exhaust all candidate moves using the above generator
    for ship, flipped, i in candidates:
        # apply ship placement
        apply_ship_mask(field, ship_cells, ship, i, False)

        # recursive call; try all possible ship placements from this field state
        if is_setup_valid(field, ship_cells, ships):
            return True

        # undo placement
        apply_ship_mask(field, ship_cells, ship, i, True)

    # re-add ship to the list
    ships.append(ship_len)

    # no remaining legal placements and a valid configuration hasn't been found; this is an invalid field state
    return False


def validate_battlefield(battle_field):
    # ship lengths, sorted so that bigger ships are placed first
    ship_lens = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]

    # first check that the correct number of cells are occupied by ships
    actual_num_occupied = sum(sum(row) for row in battle_field)
    expected_num_occupied = sum(ship_lens)
    if actual_num_occupied != expected_num_occupied:
        return False

    # represent the field in a more efficient format
    field = array.array('b', [sq == 1 for row in battle_field for sq in row])
    # maintain an array of cells containing a ship
    ship_cells = [i for i, _ in enumerate(field) if field[i]]

    return is_setup_valid(field, ship_cells, ship_lens)
