
def valid_parentheses(string):
    lefts = 0

    for c in string:
        if c == ")":
            if lefts == 0:
                return False
            else:
                lefts -= 1
        elif c == "(":
            lefts += 1

    return lefts == 0

