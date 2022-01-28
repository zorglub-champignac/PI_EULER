from __future__ import print_function
from math import sqrt , trunc
from time import clock
from decimal import *
import sys
import time

small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,101]
def freeSqare(maxSF):
    global small_primes
    fs = [1]
    for i in range(1,maxSF+1):
        fs.append(i)
    for p in small_primes:
        p2=p*p ; pt2=p2
        while pt2<= maxSF:
            fs[pt2]=0 ; pt2 += p2
    for i in range(1,maxSF+1):
        if fs[i]:
            yield i

def divisorFreeSq(sf):
    lstd2 = []
    d=1
    while d*d<=sf:
        if sf % d ==0:
            d2 = sf / d
            lstd2.append(d2)
            yield (d2,d2*d*d)
        d += 1
    if sf > 1:
        lstd2.reverse()
        for d in lstd2:
            d2 = sf /d
            yield (d2, d2 * d * d)

def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def TestSol(sqa,n,a,b ):
    m = int(sqa)+1
    if n == m*m and pgcd(a,b) ==1:
        clk = clock();
        print("{:.3f}s ".format(clk), end='')
        print(n,a,b)
        return True
    else:
        return False

def AddSol(n,a,b,k):
        clk = clock();
        print("{:.3f}s ".format(clk),a,"/",b,"x",k,sep='',end='')
        print("\t",n)




expMaxn=12
if len(sys.argv) > 1:
    expMaxn = int(sys.argv[1])

def is_square(n):
    m = int(sqrt(n))
    if m * m == n:
        return m
    else:
        return 0


def main():
    paramMaxN = int(10 ** expMaxn)
    sfl = freeSqare(int (10 ** (expMaxn /6.0)) + 1)
    SFL=[]
    COEF=[]
    id=0
    Sum = 0
    for sf in sfl:
        lstCoef = divisorFreeSq(sf)
        i0=id
        for (sfx,dx) in lstCoef:
            COEF.append((sfx,dx))
            id += 1
        iend=id
        SFL.append((sf,i0,iend))
    sqMax = sqrt(paramMaxN)

    for (sf,i0,iend) in SFL:
        for ib in range(i0, iend):
            (bf, b0) = COEF[ib]
            for ik in range(i0,iend):
                (kf, k0) = COEF[ik]
                if (kf*bf) % sf == 0:
                    k02 = k0 * k0
                    a = b0+1
                    a3 = a * a * a
                    a3Max = paramMaxN // (b0 * k02)
                    while a3 <= a3Max:
                        if (a|sf) & 1 :
                            sq_bfa = a*sqrt(a*bf)
                            ks = 1
                            ks2 = ks * ks
                            ks4 = ks2 * ks2
                            while a3*ks4 < a3Max:
                                b12 = int(ks*sq_bfa+1)
                                delta = b12*b12 - bf * ks2 * a3
                                if delta < 0:
                                    delta += 2 * b12 + 1
                                if b0 * delta < a * kf and (delta % kf) == 0:
                                    delta //= kf
                                    bs = is_square(delta)
                                    if bs:
                                        k = ks2*k0
                                        b = delta*b0
                                        n = k*b*(k*a3+b)
                                        if n < paramMaxN and pgcd(bs*b0,a) ==1:
                                            AddSol(n,a,b,k)
                                            Sum += n
                                ks += 1
                                ks2=ks*ks
                                ks4=ks2*ks2
                        a += 1
                        a3=a*a*a
    print("Sum=",Sum,"for n<2**",expMaxn)

main()
