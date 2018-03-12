from fractions import Fraction


def torpids(dist):
    if len(dist) == 0:
        return [1], [[]]
    elif len(dist) == 1:
        return [1], [[0]]
    elif len(dist) == 2:
        p = [0, 0]
        p[0] = Fraction(dist[0], sum(dist))
        p[1] = Fraction(dist[1], sum(dist))
        return p, [[0,1], [1,0]]

    p = []
    l = []

    for i in xrange(len(dist)):
        q = Fraction(dist[i], sum(dist))
        p_before, l_before = torpids([dist[j] - dist[i] for j in xrange(i)])
        p_after, l_after = torpids(dist[i+1:])
        for j in xrange(len(p_before)):
            for k in xrange(len(p_after)):
                l.append([i] + l_before[j] + [i+1+l_after[k][x] for x in xrange(len(l_after[k]))])
                p.append(q * p_before[j] * p_after[k])

    return p, l


def check_parity(perm):
    parity = 0
    visited = [False] * len(perm)
    for ptr in xrange(len(perm)):
        if not visited[ptr]:
            visited[ptr] = True
            i = perm[ptr]
            k = 1
            while i != ptr:
                visited[i] = True
                i = perm[i]
                k += 1
            parity = (parity + k + 1) % 2
    return parity


p, l = torpids(range(45,32,-1))
total = 0
for i in xrange(len(p)):
    if check_parity(l[i]) == 0:
        total += p[i]
print '%.10f' % total
print total
