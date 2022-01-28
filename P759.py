from __future__ import print_function
from time import process_time
import sys

N_POW10 = 16
is_full = 0
if len(sys.argv) > 1:
    if sys.argv[1] == '-f':
        is_full = 1
        if len(sys.argv) > 2:
            N_POW10 = int(sys.argv[2])
    else:
        N_POW10 = int(sys.argv[1])
    
N = 10 ** N_POW10

MOD = 1000000007
INV_2 = (MOD + 1) // 2
INV_6 = (MOD + 1) // 6
class State(object):
    def __init__(self, n=0):
        self.n = self.p = self.n1i0 = self.n2i0 = self.n1i1 = self.n2i1 = self.n1i2 = self.n2i2 = n

    def copy_into(self, other):
        other.n = self.n
        other.p = self.p
        other.n1i0 = self.n1i0
        other.n2i0 = self.n2i0
        other.n1i1 = self.n1i1
        other.n2i1 = self.n2i1
        other.n1i2 = self.n1i2
        other.n2i2 = self.n2i2

    def copy(self):
        other = State()
        self.copy_into(other)
        return other


def sumnp(n, p):
    return (n + p) * (n - p + 1) // 2


def sumsq(n):
    return n * (n + 1) * (2 * n + 1) // 6


def sumnp_MOD(n, p):
    return ((n + p) * (n - p + 1) * INV_2) % MOD


def sumsq_MOD(n):
    return (n * (n + 1) * (2 * n + 1) * INV_6) % MOD


def next759(b_cur, p2_ant, p):
    b_ant = b_cur.copy()

    b_cur.p = p
    n = b_cur.n = b_ant.n + p
    if is_full:
        b_cur.n1i0 = b_ant.n1i0 + p2_ant.n1i0 + b_ant.n + 1
        b_cur.n2i0 = b_ant.n2i0 + p2_ant.n2i0 + b_ant.n + 1 + 2 * b_ant.n1i0
        b_cur.n1i1 = b_ant.n1i1 + p2_ant.n1i1 + sumnp(n, p) + p * b_ant.n1i0
        b_cur.n1i2 = b_ant.n1i2 + p2_ant.n1i2 + sumsq(n) - sumsq(p - 1) + p * p * b_ant.n1i0 + 2 * p * b_ant.n1i1
        b_cur.n2i1 = b_ant.n2i1 + p2_ant.n2i1 + 2 * p * b_ant.n1i0 + p * b_ant.n2i0 + sumnp(n, p) + 2 * b_ant.n1i1
        b_cur.n2i2 = b_ant.n2i2 + p2_ant.n2i2 + 2 * p * p * b_ant.n1i0 + 2 * b_ant.n1i2 + 4 * p * b_ant.n1i1 + \
            sumsq(n) - sumsq(p-1) + p * p * b_ant.n2i0 + 2 * p * b_ant.n2i1
    else:
        pm = p % MOD
        nm = n % MOD
        ant_nm = b_ant.n % MOD
        b_cur.n1i0 = (b_ant.n1i0 + p2_ant.n1i0 + ant_nm + 1) % MOD
        b_cur.n2i0 = (b_ant.n2i0 + p2_ant.n2i0 + ant_nm + 1 + 2 * b_ant.n1i0) % MOD
        b_cur.n1i1 = (b_ant.n1i1 + p2_ant.n1i1 + sumnp_MOD(nm, pm) + pm * b_ant.n1i0) % MOD
        b_cur.n1i2 = (b_ant.n1i2 + p2_ant.n1i2 + sumsq_MOD(nm) - sumsq_MOD(
            pm - 1) + pm * pm * b_ant.n1i0 + 2 * pm * b_ant.n1i1) % MOD
        b_cur.n2i1 = (b_ant.n2i1 + p2_ant.n2i1 + 2 * pm * b_ant.n1i0 + p * b_ant.n2i0 + sumnp_MOD(nm,
                                                                                                  pm) + 2 * b_ant.n1i1) % MOD
        b_cur.n2i2 = (b_ant.n2i2 + p2_ant.n2i2 + 2 * pm * pm * b_ant.n1i0 + 2 * b_ant.n1i2 + 4 * pm * b_ant.n1i1 + \
                      sumsq_MOD(nm) - sumsq_MOD(pm - 1) + pm * pm * b_ant.n2i0 + 2 * pm * b_ant.n2i1) % MOD



def main():
    t0 = process_time()

    b_cur = State(0)
    p2_ant = State(0)
    p2_cur = State(1)

    # iterations for power of 2
    while p2_cur.n < N:
        p2_cur.copy_into(p2_ant)
        next759(p2_cur, p2_ant, 2 * p2_cur.p)
        # is current bit in N ?
        if N & p2_cur.p:
            next759(b_cur, p2_ant, p2_cur.p)

    s = b_cur.n2i2

    t1 = process_time()
    print("%.3fms: N = 10**%d ; S %% 1000000007 = %d" % ((t1 - t0) * 1000, N_POW10, s % 1000000007))
    if is_full:
       print("S = %d" % s)

main()
