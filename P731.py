from __future__ import print_function
import sys
from time import clock


def modPow(a, exp, mod):
    aPow2 = a % mod
    if exp & 1:
        aPowExp = aPow2
    else:
        aPowExp = 1
    i=1
    while exp >= (1 << i):
        aPow2 = (aPow2 * aPow2) % mod
        if (1 << i) & exp:
            aPowExp = (aPowExp * aPow2) % mod
        i += 1
    return aPowExp


def F731(N):
    nbGuard=5
    ig=0
    Guard=1
    while ig< nbGuard:
        Guard= Guard * 10
        ig +=1
    PB731_Mod = 10000000000 * Guard
    pow3=1
    nbPow3=0
    while 3*pow3 < N:
        pow3 = 3 * pow3
        nbPow3 += 1
    period = pow3 // 9
    R = modPow(10, (N % period)-2,pow3)
    S= (R*PB731_Mod*10) // pow3
    print("Check",nbGuard,"guard bits sufficient ",Guard - (S % Guard)," > ",nbPow3)
    S= (PB731_Mod*10-S)//2
    S=(S % PB731_Mod)// Guard
    return S


expN=16
if len(sys.argv) > 1:
    expN = int(sys.argv[1])


def main():
    global expN
    clock()
    N = 1
    exp = 0
    while exp < expN:
        N = N * 10
        exp += 1
    Digits = F731(N)
    clk = clock();
    print("{:.3f}s ".format(clk), end='')
    print("Digits(",expN,")",Digits)

main()
