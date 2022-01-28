from __future__ import print_function
from math import sqrt
# from primesieve import *
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


Maxn=100000000000000
if len(sys.argv) > 1:
    Maxn = int(sys.argv[1])



def main():
    global  Maxn
    N=Maxn
    N2 = int(sqrt(Maxn+1))
    tbPrime = listprimes(N2)
#    tbPrime = primes(N2)
    nbPrime = len(tbPrime)
    Lv_ip=[0]*30
    Lv_p2=[0]*30
    Lv_N_xp2=[0]*30
    Lv_W=[0]*30

    Lv_ip[0]=0
    Lv_p2[0]=1
    Lv_N_xp2[0] = N
    Lv_W[0]=1
    il=0
    S=0
    while 1:
        N_xp2 = Lv_N_xp2[il]
        isUp=0
        if N_xp2 >= 1:
            S = (S + Lv_W[il] * N_xp2)
            if Lv_ip[il] < nbPrime:
                isUp = 1
                Lv_ip[il +1] = Lv_ip[il]
                il += 1
        if isUp or (Lv_ip[il] < nbPrime ):
            # Up level or  Not last prime
            p2 = tbPrime[Lv_ip[il]] * tbPrime[Lv_ip[il]]
            Lv_ip[il] += 1
            Lv_p2[il] = p2
            if p2 <= Lv_N_xp2[il-1]: # prime product don't exeed N
                # use next prime p => p*p
                Lv_N_xp2[il]= Lv_N_xp2[il-1] // p2
                Lv_W[il] = Lv_W[il-1]* (p2 - 1)
                continue
        # level is finished : last valid prime, and max exponant
        il -= 1
        if il==0:
            break  # down level
        if Lv_N_xp2[il] >= Lv_p2[il]:
            Lv_N_xp2 [il] //= Lv_p2[il]
            Lv_W[il]  *=  Lv_p2[il]
        else:
            Lv_N_xp2[il] = 0
    print("For N=", Maxn, " Sum =", S)


main()


