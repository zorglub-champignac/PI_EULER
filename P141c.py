from __future__ import print_function
from math import sqrt
import sys


# simple sieve
# no need many primes
def listprimes(n):
    """ Returns  a list of primes < n """
    sieve = [True] * (n//2)
    for i in range(3,int(n**0.5)+1,2):
        if sieve[i//2]:
            sieve[i*i//2::i] = [False] * ((n-i*i-1)//(2*i)+1)
    return [2] + [2*i+1 for i in range(1,n//2) if sieve[i]]


curListPrimes = [ 2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59, 61, 67, 71, 73, 79, 83, 89, 97,101]
def getnextPrime():
    global curListPrimes
    for p in curListPrimes:
        yield p
    p1 = p + 2
    while 1:
        sqp1 = int(sqrt(p1))
        for p in curListPrimes:
            if p > sqp1:
                break
            if p1 % p == 0:
                break
        if p > sqp1:
            curListPrimes.append(p1)
            yield p1
        p1 += 2





SF = []  # array for squarefree part of numbers t from n=s**2 * t
sfPivot = 1  # size of precomputed sqfree part
sfMaxval = 1    # maValue accepted (=> for number of primes)
sfMaxPrime = 1  #  number of primes
sfPrimes=[] # array of primes to search square part
# Initialise search of squerefree part
def initSF(pivot,maxVal):
    global SF,sfPivot,sfMaxval,sfMaxPrime,sfPrimes
    sfPivot=pivot
    sfMaxval=maxVal
    SF.append(0)
    SF.append(1)
    isq= 2
    isq2= 4
    for i in range(2,sfPivot):
        SQ=1
        if i == isq2:
            isq += 1
            isq2 = isq*isq
        for j in range(isq-1,1,-1):
            j2 = j * j
            if (i % j2) == 0:
                SQ = j2
                break
        SF.append(i // SQ)
    SFMaxPrime= int(sqrt(sfMaxval))
    sfPrimes = listprimes(SFMaxPrime)

def getSF(val):
    global SF,sfPivot,sfMaxval,sfMaxPrime,sfPrimes
    if val >= sfMaxval:
        return 0
    elif val < sfPivot:
        return SF[val]
    sqf = 1
    for p in sfPrimes:
        p2 = p*p
        if p2 > val:
            break
        q = val // p
        powp = 0
        while val == p*q:
            powp += 1
            val = q
            q = val // p
        if powp & 1:
            sqf *= p
        if val < sfPivot:
            break
    if val >= sfPivot:
        sqf *= val
    else:
        sqf *= SF[val]
    return sqf


def GetSquareFree(nbMax):
    squareFree = []
    primes=getnextPrime()
    sieveSQ = [1] * (nbMax+1)
    for p in primes:
        p2=p*p
        if p2 > nbMax:
            break
        for np2 in range(p2,nbMax,p2):
            sieveSQ[np2]=0
    for i in range(1,nbMax+1):
        if sieveSQ[i]:
            squareFree.append(i)
    sieveSQ = []
    return squareFree

def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def CFSQ(N):
    FC_N0=0 ;  FC_D0=1
    FC_N1=1 ;  FC_D1=0
    k0 = int(sqrt(N))
    a = n = k0
#    nb = 1
    d = 1
    tmp = FC_N0 ; FC_N0 = FC_N1 ; FC_N1 = a * FC_N0 + tmp
    tmp = FC_D0 ; FC_D0 = FC_D1 ; FC_D1 = a * FC_D0 + tmp
    if N == k0 * k0:
        d = 0
    if d == 0:
        yield (k0,0)
    else:
        while 1:
            d = (N - n * n) // d
            n = k0 - ( ( k0 + n) % d)
            a = (k0 + n) // d
            tmp = FC_N0 ; FC_N0 = FC_N1 ; FC_N1 = a * FC_N0 + tmp
            tmp = FC_D0 ; FC_D0 = FC_D1 ; FC_D1 = a * FC_D0 + tmp
#           nb += 1
            yield (FC_N1,FC_D1)




def computePgcd(bsq):
    primeforPgcd = getnextPrime()
    tbPgcd = [1] * bsq
    tbPgcd[0] = bsq
    b1=bsq
    for p in primeforPgcd:
        if b1 == 1:
            break
        if p*p > bsq:
            p = b1
        elif b1 % p: # p dont divide b1
            continue
        for pt in range(p,bsq,p):
            tbPgcd[pt] *= p
        b1 //= p
    if p ==0:
        print("FATAL ERROR not enough primes for gcd pre-compute")
        exit(0)
    return tbPgcd



expMaxn=12
if len(sys.argv) > 1:
    expMaxn = int(sys.argv[1])

Sum = 0
def main():
    global Sum,expMaxn
    paramSFpivot=2000
    paramMaxN = int(10 ** expMaxn)
    maxB0 = int(pow(paramMaxN, 1 / 6.0))
#    paramMAXSF = 64000000
    initSF(paramSFpivot,maxB0*maxB0)
    squareFree=GetSquareFree(maxB0)
    Sol = []
    Sum = 0
    def AddSol141(n, a, b, k):
        global Sum
        Sol.append((n,a,b,k))
        print("\r",a,"/",b,"x",k,"  ",n,"             ",sep='',end='') ; sys.stdout.flush()
#        print(a,"/",b,"x",k,"  ",n,"             ",sep='')
        Sum += n

    for b0 in squareFree:
        maxA3 = paramMaxN // (b0 * b0 * b0)
        pgcdB0 = computePgcd(b0)
        a = b0+1
        a3 = a * a * a
        aModb0 = 0
        while a3 <= maxA3:
            aModb0 += 1
            if aModb0 == b0:
                aModb0 = 0
            if pgcdB0[aModb0] == 1:
                maxD  = paramMaxN // (a3 * b0 * b0 * b0)
                cfsq = CFSQ(a3*b0)
                (N1,D1) = next(cfsq)
                if D1 != 0:
                    while 1:
                        k0 = D1*D1
                        if k0 * k0 > maxD:
                            break
                        delta = N1 * N1 - a3 * b0 * k0
                        bbs = pgcdB0[delta % b0]
                        if b0 * delta < a * bbs:
                            bf = getSF(delta)
                            if bf == 0:
                                print("FATAL ERROR get square free of",delta)
                                bf = getSF(delta)
                                exit(0)
                            b1 = b0 // bbs
                            b = b1 * (delta // bbs) * bf
                            if b < a:
                                k = k0 * b1 * b1 * bf
                                if k * b * ( k * a3+b) > paramMaxN:
                                    break
                                n = k * b * (k * a3 + b)
                                if pgcd(a, b) == 1:
                                    AddSol141(n, a, b, k)
                                    ksMax = paramMaxN // n
                                    ks = 2; ks2 = ks*ks
                                    while b * ks2 < a and ks2 * ks2 * ks2 <= ksMax:
                                        if pgcd(ks, a) == 1:
                                            AddSol141( ks2 * ks2 * ks2 * n, a, ks2 * b, ks2 * k)
                                        ks += 1
                                        ks2 = ks * ks
                        (N1, D1) = next(cfsq)
                        k0 = D1 * D1
                        if k0 * k0 > maxD:
                            break
                        (N1, D1) = next(cfsq)
            a += 1
            a3=a*a*a
    Sol.sort(key=lambda sol: (sol[0],sol[1]))
    print("\n")
    for (n,a,b,k) in Sol:
        print(a,"/",b,"x",k,"\t",n,sep='')

    print("For n<10**",expMaxn," Sum =",Sum)
main()