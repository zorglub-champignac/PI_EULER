from __future__ import print_function

import sys
# from pyprimes import primes
from functools import reduce
from math import log
from operator import mul
from bisect import bisect

small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
                103, 107]


def primes(mini=None, maxi=None):
    global small_primes

    i, j = 0, len(small_primes)
    if mini is not None:
        i = bisect(small_primes, mini)-1
    if maxi is not None:
        j = bisect(small_primes, maxi)
    for n in xrange(i, j):
        yield small_primes[n]


# start global variables

# maximum number
# maxn = 80


maxn = int(sys.argv[1])

# list of used prime powers
# to be filled
pklist = []

# list of prime power exponents to generate ending values
p_end = [2, 1]
if len(sys.argv) > 2:
    p_end = eval(sys.argv[2])
elif maxn < 120:
    p_end = [2, 1]
elif maxn < 180:
    p_end = [2, 1, 1]
else:
    p_end = [2, 1, 1, 1]


# end global variables

# help functions for printing lists of prime powers
def pplist(pkl):
    res = []
    for (p, mk) in pkl:
        res += [p ** k for k in range(1, mk + 1)]
    return res


def pend_pp():
    pkl = [(pklist[np][0], mk) for (np, mk) in enumerate(p_end)]
    return pplist(pkl)


# initial list of prime powers
# 4*p<=maxn and 3*p^k<=maxn
def initial_primepow():
    global pklist
    maxp = maxn // 4
    maxk = lambda p: int(log(maxn // 3, p))
    pklist = [(p, maxk(p)) for p in primes(2, maxp + 1)]
    print("Initial primes and powers:", pplist(pklist))
    print()


# common multiple( l^2)
def lcm2():
    l = reduce(mul, (p ** k for (p, k) in pklist))
    return l ** 2


# subsets of ns
def subsets(ns):
    def grow(k, ss):
        yield ss
        for l in range(k, len(ns)):
            ssn = ss + [ns[l]]
            for ms in grow(l + 1, ssn):
                yield ms

    return grow(0, [])


# help functions to add elements to table
def append_by_key(key, it, d):
    if key in d:
        d[key].append(it)
    else:
        d[key] = [it]


# help function to increment value of table
def inc_by_key(key, c, d):
    if key in d:
        d[key] += c
    else:
        d[key] = c


# sums of inverse squares multiplied by l^2
def sums_subsets(mlist):
    l2 = lcm2()
    ss = subsets(mlist)
    suminvsq = lambda ns: sum(l2 // n ** 2 for n in ns)
    return (suminvsq(sub) for sub in ss)


# table of sums for new sequences of numbers, indexed modulo p2
def dict_subsets(mlist, np, k):
    p, mk = pklist[np]
    p2 = p ** 2
    p2mk = p ** (2 * mk)
    p2k = p ** (2 * k)
    res = {}
    matchables = list(sums_subsets(mlist))
    print(len(matchables), "matching values")
    for suminv in matchables:
        b = suminv // p2k
        bb = (suminv // p2mk) % p2
        append_by_key(bb % p2, b, res)
    return res


# prunes some primes and some prime powers
def prune_primepow():
    global pklist

    def test_pk(np, k):
        p, mk = pklist[np]
        pp = p ** (2 * mk + 2)
        maxit = maxn // p ** k
        mlist = [n for n in range(1, maxit + 1) if n % p != 0]
        return any(b % pp == 0 for b in sums_subsets(mlist) if b != 0)

    def max_pow(np):
        (p, klim) = pklist[np]
        k = 0
        while k < klim and test_pk(np, k + 1): k += 1
        return k

    pklist0 = [(p, max_pow(np)) for (np, (p, mk)) in enumerate(pklist)]
    pklist = [(p, mk) for (p, mk) in pklist0 if mk > 0]
    print("Pruned primes and powers:", pplist(pklist))
    print()


# match previous values with new sums
def match(mlist, previous, np, k):
    p, mk = pklist[np]
    p2 = p ** 2
    pk = p ** k
    print()
    print("prime power", pk)
    p2mkk = p ** (2 * (mk - k))
    ssubsets = dict_subsets(mlist, np, k)
    res = {}
    for c in previous:
        key = (-c // p2mkk) % p2
        if key in ssubsets:
            for b in ssubsets[key]:
                inc_by_key(b + c, previous[c], res)
    print(len(res), "resulting values")
    return res


# numbers to generate new sums
def gen_mlist(npk, npklist):
    (np, k) = npklist[npk]
    (p, mk) = pklist[np]
    maxm = maxn // p ** k
    l2 = lcm2()
    divbyprev = lambda n: any(n % (pklist[np][0] ** k) == 0
                              for (np, k) in npklist[npk + 1:])
    res = []
    for n in range(1, maxm + 1):
        if n % p != 0 and l2 % n ** 2 == 0 and not divbyprev(n):
            res.append(n)
    return res


# values generated for current prime power
def nextpk(npk, npklist):
    (np, k) = npklist[npk]
    mlist = gen_mlist(npk, npklist)
    if npk + 1 == len(npklist):
        previous = {0: 1}
    else:
        previous = nextpk(npk + 1, npklist)
    return match(mlist, previous, np, k)


# search, looking for sums divisible by p^2, from larger to smaller primes
def search():
    npklist = []
    for (np, (p, mk)) in enumerate(pklist):
        for k in range(1, mk + 1):
            if np >= len(p_end) or k > p_end[np]:
                npklist.append((np, k))
    if len(npklist) > 0:
        return nextpk(0, npklist)
    else:
        return {0: 1}


# generate ending numbers
def end_numbers():
    def grow(k, n):
        yield n
        for l in range(k, len(fac)):
            for m in range(len(fac[l])):
                nn = n * fac[l][m]
                if nn <= maxn:
                    for v in grow(l + 1, nn):
                        yield v

    pend2 = [(pklist[i][0], p_end[i]) for i in range(len(p_end))]
    print("pend2", pend2)
    fac = [[p ** k for k in range(1, mk + 1)] for (p, mk) in pend2]
    print("fac",fac)
    num = list(grow(0, 1))
    print("num",num)
    res = {}
    count = 0
    for s in sums_subsets(num):
        count += 1
        inc_by_key(s, 1, res)
    print("end prime powers", pend_pp())
    print(count, "end values")
    return res


# match generated values with ending numbers
def end():
    l2 = lcm2()
    endn = end_numbers()
    count = 0
    loose = search()
    for s2 in loose:
        dif = l2 // 2 - s2
        if dif in endn:
            count += endn[dif] * loose[s2]
    return count


def main():
    initial_primepow()
    prune_primepow()
    if len(pklist) == 0:
        res = 0
    else:
        res = end()
    print()
    print("Result: ", res, " sequences")


main()
