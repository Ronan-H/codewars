adj_list = [
    ["0", "8"],
    ["1", "2", "4"],
    ["2", "1", "3", "5"],
    ["3", "2", "6"],
    ["4", "1", "5", "7"],
    ["5", "2", "4", "6", "8"],
    ["6", "3", "5", "9"],
    ["7", "4", "8"],
    ["8", "5", "7", "9", "0"],
    ["9", "6", "8"],
]

def get_pins(observed):
    # adjacency list for the first pin digit
    adj_first = adj_list[int(observed[0])]
    
    # base case (pin is a single digit)
    if len(observed) == 1:
        return adj_first
    
    # remaining digits, ignoring the first digit
    remaining = "".join(observed[1:])
    
    # create a list of all possible pin permutations
    perms = []
    # for every possile starting digit...
    for adj in adj_first:
        # append a list of permutations starting with that digit
        # (recursive call)
        perms += [adj + sub_perm for sub_perm in get_pins(remaining)]
    
    return perms
    