
from __future__ import print_function
from math import sqrt,floor
import sys
from time import clock

MAXR=105
nbPrimeL=[]
nbPrimeH=[]
nbPointsH=[]
nl=0
nh=0
R2=0



def isqrt(n):
    y = int(sqrt(n))
    if y < 50000000:
        return y
    x = y + 1
    dx = x*x-n
    while dx <=0:
        dx += (x << 1) + 1
        x += 1

    while True:
        y = (x + n // x) >> 1
        if y >= x:
            return x
        x = y



#quarter disk
'''
compute Sigma 1 for x^2+y^2 <= N x>0, y>0
3 zones
 . ...
 |  Z3   .
 |---------.
 |       . |  .
 |    Z1 . |   .
 |  .      | Z2 .
 |_________|____.
'''
def Nbx184PointsInCirle(N):
    sqrN2 = isqrt(N // 2)
    sqrN = isqrt(N)
    S = sqrN2 * sqrN2
    S1 = 0
    Ni = N - S
    for i in range(sqrN2+1,sqrN+1):
        sqrY = isqrt(N-i * i)
        S1 += sqrY

    return S + 2 * S1


def CounC2_nbPoints(ih,il):
    global nh,nl,nbPointsH
    if nbPointsH[ih] == 0:
        nbPointsH[ih] =Nbx184PointsInCirle(il)
    return nbPointsH[ih]



def CounC2_CalcNbPrimeI(ih):
    global R2,nl,nh,nbPrimeH,nbPrimeL
    ih2 = ih*ih
    if ih2*2 > R2:
        return 0
    il = R2 // ih2
    if ih >= nh:
        return nbPrimeL[il]
    if nbPrimeH[ih]:
        return nbPrimeH[ih]
    S = CounC2_nbPoints(ih,il) - CounC2_nbPoints(ih*2,il//4)
    jh = 3*ih
    while jh < nh:
        S -=  CounC2_CalcNbPrimeI(jh)
        jh += 2*ih
    jh2=jh*jh
    while 2*jh2 <=R2:
        jl = R2 // jh2
        S -= nbPrimeL[jl]
        jh2 += 4  * (jh + ih) * ih
        jh += 2 * ih
    nbPrimeH[ih] = S
    return S




if len(sys.argv) > 1:
    MAXR = int(sys.argv[1])


FR_0n=0; FR_0d=1
FR_1n=0; FR_1d=1
FR_end_n=0 ; FR_end_d=1
FR_maxDen=1
def FR_init(maxDen,frStart_n,frStart_d,frEnd_n,frEnd_d):
    global FR_maxDen, FR_0n, FR_0d, FR_1n, FR_1d, FR_end_n, FR_end_d
    FR_end_n = frEnd_n; FR_end_d = frEnd_d
    FR_maxDen = maxDen
    if frStart_n:
        FR_1n = frStart_n; FR_1d = frStart_d
        FR_0n = frEnd_n;   FR_0d = frEnd_d
    else:
        FR_0n = frStart_n;  FR_0d = frStart_d
        FR_1n = 1;    FR_1d = maxDen
    return

def FR_getNext():
    global FR_maxDen, FR_0n, FR_0d, FR_1n, FR_1d, FR_end_n, FR_end_d
    a = (FR_maxDen + FR_0d) // FR_1d
    tmp = FR_1d
    FR_1d = a * FR_1d - FR_0d
    FR_0d = tmp
    tmp = FR_1n
    FR_1n = a * FR_1n - FR_0n
    FR_0n = tmp
    if FR_1d == FR_end_d and FR_1n == FR_end_n:
        return 0
    return 1




def main():
    global R2,nh,nl,nbPrimeL,nbPrimeH,nbPointsH,MAXR
    global FR_1n,FR_1d,FR_0n,FR_0d
    R2 = MAXR*MAXR - 1
    clock()
    np = int(pow(R2,1/3.0))
    nh = np
    nl = R2 // (np*np)
    nl += 1
    nbPrimeL =[0]*nl
    nbPrimeH = [0] * nh
    nbPointsH =[0]*(2*nh)
    S1 = 0 ; S2 = 0 ;   S3 = 0
    FR_init(int(sqrt(nl)), 0, 1, 1, 1)
    while 1:
        norm = FR_1n * FR_1n + FR_1d * FR_1d
        if norm < nl:
            nbPrimeL[norm] += 2
        if FR_getNext() == 0:
            break
    nbPrimeL[2] = 1


    for i in range(1, nl):
        Ni = nbPrimeL[i]
        if i == 1:
            Ni += 1
        if Ni:
            j  = isqrt(R2//i)
            if j >= nh:
                S1 += j * Ni;  S2 += j * Ni * j;  S3 += j * Ni * j * j
        nbPrimeL[i] += nbPrimeL[i-1]
    antNbPrime = CounC2_CalcNbPrimeI(1)
    for i in range(1, nh):
        newNbPrime = CounC2_CalcNbPrimeI(i + 1)
        Ni = antNbPrime - newNbPrime
        if Ni:
            S1 += i * Ni;  S2 += i * Ni * i;  S3 += i * Ni * i * i
            antNbPrime = newNbPrime
    # print("R2=",R2,"nl=",nl,"nh=",nh)
    # quarter disk to half disk
    S1 *= 2 ; S2 = 2 * S2 ; S3 = 2 * S3
    S = S1*S1*S1 - 3 * S2 * S1 + 2 * S3
    S //= 3
    clk = clock();
    print("{:.3f}s ".format(clk), end='')
    print("r=",MAXR,"S=",S,"S1=",S1,"S2=",S2,"S3=",S3)



main()
