from __future__ import print_function
from math import sqrt
# from primesieve import *
import sys

Maxn=100000000000000
if len(sys.argv) > 1:
    Maxn = int(sys.argv[1])



def main():
    global  Maxn
    N=Maxn
    N2 = int(sqrt(Maxn+1))
    invN=[0]*(N2+1)
    F=[0]*(N2+1)
    for i in range(1,N2+1):
        invN[i] = N // (i*i)
    for i in range(N2,0,-1):
        Sf = invN[i]
        j = 2
        ij = i * j
        while ij <= N2:
            Sf += j*j * invN[ij] - F[ij]
            ij += i
            j += 1
        F[i] = Sf
    print("For N=", Maxn, " Sum =", F[1])


main()

