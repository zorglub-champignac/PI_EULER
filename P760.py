from __future__ import print_function
import sys
if sys.version_info >= (3,0):
    from time import process_time
    sysnew = 1
else:
    from time import clock
    sysnew = 0

POW10 = 18
is_full = 0
if len(sys.argv) > 1:
    if sys.argv[1] == '-f':
        is_full = 1
        if len(sys.argv) > 2:
            POW10 = int(sys.argv[2])
    else:
        POW10 = int(sys.argv[1])

N = 10**POW10
MOD = 1000000007


def fo760x2(fo_n, fo_nm1, n):
    # compute fo(2*n) from fo(n) and fo(n-1)
    return 2*fo_nm1+2*fo_n+n

def fo760x2_MOD(fo_n, fo_nm1, n):
    # compute fo(2*n) from fo(n) and fo(n-1)
    return (2*fo_nm1+2*fo_n+n) % MOD

def fo760x2p1(fo_n, n):
    # fo(2*n+1) from fo(n)
    return 4*fo_n+2*(n+1)


def fo760x2p1_MOD(fo_n, n):
    # fo(2*n+1) from fo(n)
    return (4*fo_n+2*(n+1)) % MOD

def go760n(go_n, fo_n, n, bn):
    # compute go(2*n+bn) from go(n) and fo(n)
    if bn:
        return 8 * go_n - 2 * fo_n + (3 * n + 4) * (n + 1) //2
    else:
        return 8 * go_n - 6 *  fo_n + 3 * n * (n + 1) //2


def go760n_MOD(go_n, fo_n, n, bn):
    # compute go(2*n+bn) from go(n) and fo(n)
    nm = n % MOD
    if bn:
        return (8 * go_n + 2 * (MOD - fo_n) + (((3 * nm + 4) * (nm + 1)) % MOD) * (MOD // 2 + 1)) % MOD
    else:
        return (8 * go_n + 6 * (MOD - fo_n) + ((3 * nm * (nm + 1)) % MOD) * (MOD // 2 + 1)) % MOD


def main():
    if sysnew:
        t0 = process_time()
    else:
        t0 = clock()
    pow2 = 1
    while pow2 <= N:
        pow2 <<= 1
    if pow2 > N:
        pow2 >>= 1
    fo_n = 0 ; fo_nm1 = 0 ; go_n = 0  # fo(n) fo(n-1)
    n = 0
    while pow2:
        if is_full:
            if N & pow2:
                # new bit = 1 (n,n-1) => (2*n+1,2*n)
                go_n = go760n(go_n, fo_n, n, 1)
                fo_nm1 = fo760x2(fo_n, fo_nm1, n)
                fo_n = fo760x2p1(fo_n, n)
                n = (n << 1) + 1
            else:
                go_n = go760n(go_n, fo_n, n, 0)
                fo_n = fo760x2(fo_n, fo_nm1, n)
                fo_nm1 = fo760x2p1(fo_nm1, n - 1)
                n <<= 1
        else:
            if N & pow2:
                # new bit = 1 (n,n-1) => (2*n+1,2*n)
                go_n = go760n_MOD(go_n, fo_n, n, 1)
                fo_nm1 = fo760x2_MOD(fo_n, fo_nm1, n)
                fo_n = fo760x2p1_MOD(fo_n, n)
                n = (n << 1) + 1
            else:
                go_n = go760n_MOD(go_n, fo_n, n, 0)
                fo_n = fo760x2_MOD(fo_n, fo_nm1, n)
                fo_nm1 = fo760x2p1_MOD(fo_nm1, n - 1)
                n <<= 1
        pow2 >>= 1
    S = 2 * go_n
    if not is_full:
        S =S % MOD
    if sysnew:
        t1 = process_time()
    else:
        t1=clock()
    print("%.3fms: S  = %d" % ((t1 - t0)*1000, S))


main()
