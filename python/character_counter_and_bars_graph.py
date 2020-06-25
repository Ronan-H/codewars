def count_and_print_graph(t, m):
    r=range(97,124)
    d=[[ord(x)for x in ''.join(c for c in t.lower() if c.isalpha())].count(i)for i in r]
    return '\n'.join([chr(l)+':'+'#'*int(c/max(d)*m)for l,c in sorted(zip(r,d),key=lambda x:(-x[1],x[0]))if c > 0])
