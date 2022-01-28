from __future__ import print_function

import sys
from math import log,sqrt
from time import clock

def SumN(N):
    return N*(N+1)//2

def SigmaInvInt(nb):
    Inb0=nb
    S=0
    i=1
    while i<Inb0:
        Inb1 = nb // (i+1)
        S += Inb0 * i + i * (Inb1+1+Inb0)*(Inb0-Inb1) // 2
        Inb0=Inb1
        i += 1
    if i == Inb0:
        S += i * Inb0
    return S

def NbxPointsInCirle(N):
    sqrN2=int(sqrt(N//2))
    sqrN=int(sqrt(N))
    S = SumN(sqrN2)*sqrN2
    for i in range(sqrN2+1, sqrN+1):
        sqrY=int(sqrt(N-i*i))
        S += i*sqrY + SumN(sqrY)
    return S


CircleLow = []
CircleHigh = []
PrimeLow= []
PrimeHigh= []

def CompCircle(N,n1):
    global CircleLow ,CircleHigh , PrimeLow , PrimeHigh
    CircleLow.append(0)
    CircleHigh.append(0)
    PrimeLow.append(0)
    PrimeHigh = [0] * (n1+2)

    for i in range(1,n1+1):
        CircleLow.append(NbxPointsInCirle(i))
        CircleHigh.append(NbxPointsInCirle(N // i))
    for i in range(1, n1 + 1):
        S = CircleLow[i]
        j=2
        while j*j<=i:
            S -= j * PrimeLow[i // (j*j)]
            j += 1
        PrimeLow.append(S)
    for i in range(n1,0,-1):
        i1 = N // i
        S = CircleHigh[i]
        j=2
        while j*j<=i1:
            j1 = i1 // (j*j)
            if j1 > n1:
                S -= j * PrimeHigh[i*j*j]
            else:
                S -= j * PrimeLow[j1]
            j += 1
        PrimeHigh[i] = S


maxn=100000000
if len(sys.argv) > 1:
    maxn = int(sys.argv[1])

def main():
    global CircleLow ,CircleHigh , PrimeLow , PrimeHigh , maxn
    clock()
    clk = 0
    N=maxn
    n1=int(sqrt(N))
    CompCircle(N,n1)
    S = SigmaInvInt (N)
    for i in range(1,n1):
        S += 2 * (PrimeHigh[i]-PrimeHigh[i+1]) * SigmaInvInt(i)
    S += 2 * (PrimeHigh[n1] - PrimeLow[N // (n1+1) ]) * SigmaInvInt(n1)
    for i in range(1,N // n1 ):
        S += 2 * (PrimeLow[i] - PrimeLow[i - 1]) * SigmaInvInt(N // i)

    clk = clock();
    print("{:.3f}s ".format(clk), end='')
    print(" S=",S)

main()


