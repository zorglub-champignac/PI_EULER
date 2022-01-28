from math import sqrt
import sys
import numpy as np
from time import clock

# from time import process_time

#@nb.njit
def a(L, y):
    Ly = L // y
    if (y * 2 + 1) ** 2 >= Ly:
        jmax = Ly // (y * 2 + 1)
        ans = 0
        for j in range(1, jmax):
            ans += j * ((Ly // j + 1) // 2 - (Ly // (j + 1) + 1) // 2)
        ans += jmax * ((Ly // jmax + 1) // 2 - y)
        return ans
    M2 = int((sqrt(4 * y * y - 12 * y + 9 + 8 * L / y) - 2 * y - 1) / 4)
    M1 = Ly // (M2 + 1)
    ans = 0
    for x in range(y * 2 + 1, M1 + 1, 2):
        ans += Ly // x
    for j in range(1, M2 + 1):
        ans += j * ((Ly // j + 1) // 2 - (Ly // (j + 1) + 1) // 2)
    return ans

#@nb.njit
def b(L, y):
    Ly = L // y
    if (y + 1) ** 2 >= Ly:
        jmax = Ly // (y + 1)
        ans = 0
        for j in range(1, jmax):
            ans += j * (Ly // j - Ly // (j + 1))
        ans += jmax * (Ly // jmax - y)
        return ans
    M2 = int((sqrt(y * y - 2 * y + 1 + 4 * L / y) - y - 1) / 2)
    M1 = Ly // (M2 + 1)
    ans = 0
    for x in range(y + 1, M1 + 1):
        ans += Ly // x
    for j in range(1, M2 + 1):
        ans += j * (Ly // j - Ly // (j + 1))
    return ans

#@nb.njit
def A0(L):
    l = (int(sqrt(8 * L + 1)) - 1) // 4
    ans = 0
    for y in range(1, l + 1):
        ans += a(L, y)
    return ans

#@nb.njit
def B0(L):
    l = (int(sqrt(4 * L + 1)) - 1) // 2
    ans = 0
    for y in range(1, l + 1, 2):
        ans += b(L, y)
    return ans

#@nb.njit
def main(L):
    v2 = int(sqrt(L / 2))
    v3 = int(sqrt(L / 3))
    isprime = np.ones(v2 + 1, dtype=np.bool_)
    mu = np.ones(v2 + 1, dtype=np.int8)

    for p in range(2, v2 + 1):
        if not isprime[p]:
            continue
        q = p * p
        p2 = p + p
        isprime[p2::p] = 0
        mu[p::p2] = -mu[p::p2]
        mu[q::q] = 0
    print("Sieved")
    ansA = 0
    for d in range(1, v3 + 1, 2):
        if mu[d]:
            ansA += mu[d] * A0(L // d // d)
            if d< 20 or d > v3-20:
                print(d,"->",mu[d],"x",A0(L // d // d))
    ansB = 0
    for d in range(1, v2 + 1, 2):
        if mu[d]:
            ansB += mu[d] * B0(L // d // d)
    ans = ansA + ansB + L
    print("For N=",L," Sum=",ans," =",ansA," + ",ansB)
    return ans

L=1000000000000
if len(sys.argv) > 1:
    L = int(sys.argv[1])
main(L)