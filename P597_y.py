from fractions import Fraction

even = {}


def cross(pa, pb, parity):
    if parity == 0:
        return pa*pb+(1-pa)*(1-pb)
    else:
        return pa*(1-pb)+(1-pa)*pb


def evenp(n, l):
    if n < 2:
        return 1
    else:
        if (n, l) in even:
            return even[(n, l)]
        else:
            sum = Fraction(0, 1)
            for k in xrange(n):
                sum += (l-k)*cross(evenp(n-k-1, l-k-1), evenp(k, k), k & 1)
            even[(n, l)] = sum/((n * (2*l-n+1))/2)
            return even[(n, l)]


for nboat in (13, 20, 24):
    total = evenp(nboat, 45)
    print '%.10f' % total, total

