def group_groceries(g):
    t='fruit','meat','other','vegetable'
    m={i:[] for i in t}
    for c, i in [s.split('_') for s in g.split(',')]:m[c if c in t else t[2]]+=[i]
    return ''.join(c+':'+','.join(sorted(m[c]))+'\n'for c in t)[:-1]