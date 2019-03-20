from __future__ import print_function
from math import sqrt
from fractions import gcd
from time import clock
import sys
import time


#PB141_MAX = 10000000000000000000

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




expMaxn=12
if len(sys.argv) > 1:
    expMaxn = int(sys.argv[1])


def main():
    paramMaxN = int(10 ** expMaxn)
    sfl = freeSqare(5000)
    SFL=[]
    COEF=[]
    id=0
    a = 2
    a3 = a * a * a
    Sum = 0
    for sf in sfl:
        lstCoef = divisorFreeSq(sf)
        i0=id
        for (sfx,dx) in lstCoef:
            COEF.append((sfx,dx))
            id += 1
        iend=id
        SFL.append((sf,i0,iend))
    while a3 <= paramMaxN:
        for (sf,i0,iend) in SFL:
            if sf < a and (a3+1) * sf * sf *sf <= paramMaxN:
                if pgcd(a, sf) != 1:
                    continue
                for (sfk, k0) in COEF[i0:iend]:
                    b0 = sfk
                    if b0 >= a:
                        break
                    n = k0 * b0 * ( k0 * a3 + b0 )
                    if n > paramMaxN:
                        break
                    for (sfb,b0) in COEF[i0:iend]:
                        n = k0 * b0 * ( k0 * a3 +  b0 )
                        if b0 >= a or n > paramMaxN:
                            break
                        if ((sfk * sfb) % sf) != 0:
                            continue
                        sq_k0a = k0 * a * sqrt(a*b0)
                        bs=1
                        b= b0
                        while b < a :
                            n = k0 * b * (k0 * a3 + b )
                            if n > paramMaxN:
                                break
                            sq_k0b = bs * sq_k0a
                            if TestSol(sq_k0b, n, a, b):
                                Sum += n
                            ks = 2
                            ks2 = ks * ks
                            k = ks2 * k0
                            n = k * b * (k * a3 + b)
                            while n <= paramMaxN:
                                if TestSol(ks2*sq_k0b, n, a, b):
                                    Sum += n
                                ks += 1
                                ks2 = ks * ks
                                k = ks2 * k0
                                n = k * b * (k * a3 + b)
                            bs += 1
                            b = bs * bs * b0
            else:
                break
        a += 1
        a3 = a * a * a
    print("Sum=",Sum,"for n<2**",expMaxn)

main()