from itertools import *
from math import sqrt,gcd
# from fractions import gcd

import sys
import time


def div_pow(n, d):
    e = 0
    while n % d == 0:
        e += 1
        n //= d
    return e, n


def is_square(n):
    m = int(sqrt(n))
    return m * m == n


def has_square(n):
    squares = takewhile(lambda s: s <= n, (k * k for k in count(2)))
    return any(n % s == 0 for s in squares)


def divide_square_and_not(n, p0=2):
    if n == 1:
        return 1, 1
    else:
        for p in takewhile(lambda p: p * p <= n, count(p0)):
            if n % p == 0:
                e, m = div_pow(n, p)
                s, t = divide_square_and_not(m, p + 1)
                return p ** (e // 2) * s, p ** (e % 2) * t
        else:
            return 1, n


def f(t, p, u):
    return p * t ** 3 * (u ** 3 + p)


# solutions of am^2 = bu^3 + c (m <= M, u >= U)
def g(a, b, c, U, M):
    def gcd2(a, c):
        d = gcd(a, c)
        s, t = divide_square_and_not(d)
        return s * t

    def g2(a, b, c, U, M):
        for u in takewhile(lambda u: b * u ** 3 + c <= a * M, count(U)):
            rhs = b * u ** 3 + c
            if rhs % a == 0 and is_square(rhs / a):
                yield int(sqrt(rhs / a)), u

    d1 = gcd(a, b)
    d = gcd(d1, c)
    if d > 1:
        return g(a // d, b // d, c // d, U, M)

    if d1 > 1:
        return ()

    d2 = gcd2(a, c)
    if d2 > 1:
        return ((m, u * d2) for m, u in
                g(a // d2, b * d2 * d2, c // d2, U // d2, M))

    d3 = gcd2(b, c)
    if d3 > 1:
        return ((m * d3, u) for m, u in g(a * d3, b // d3, c // d3, U, M // (d3 * d3)))

    return g2(a, b, c, U, M)


def gen_progressive_perfect_squares(N):
    for t in takewhile(lambda t: f(t, 1, t + 1) < N, count(1)):
        if has_square(t): continue
        for p in takewhile(lambda p: f(t, p, p * t + 1) < N, count(1)):
            for m, u in g(1, p * t ** 3, p * p * t ** 3, p * t + 1, N):
                if t * p < u:
                    print(t, p, m, u, m * m , "->" , p*p*t*t*t , p*u*t*t, u*u*t)
                    yield m * m

expMaxn=12
if len(sys.argv) > 1:
    expMaxn = int(sys.argv[1])

t0 = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
N = 10 ** expMaxn
print(sum(set(gen_progressive_perfect_squares(N))))
clk = (time.clock_gettime_ns(time.CLOCK_MONOTONIC) - t0) / 1000000
print("{:.3f}ms ".format(clk), end='')