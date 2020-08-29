def add_padding(s1, s2):
    if s1 > s2:
        s1, s2 = s2, s1
    s1, s2 = str(s1), str(s2)
    return '0' * (len(s2) - len(s1)) + s1, s2


def add(n1, n2):
    pair = add_padding(n1, n2)
    result = ''
    for i in range(len(pair[0])):
        result += str(int(pair[0][i]) + int(pair[1][i]))

    return int(result)


print('1103')
print(add(122, 81))
