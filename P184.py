
from __future__ import print_function
from math import sqrt,floor
import sys
import time

MAXR=105

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

if len(sys.argv) > 1:
    MAXR = int(sys.argv[1])

# Stern-Brocot walk

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
    global nh,nl,nbPrimeL,nbPrimeH,nbPointsH,MAXR
    global FR_1n,FR_1d,FR_0n,FR_0d
    N= [0] * MAXR
    R2 = MAXR*MAXR
    t0=time.clock_gettime_ns(time.CLOCK_MONOTONIC)
    S1 = 0 ; S2 = 0 ;   S3 = 0
    FR_init(MAXR-1, 0, 1, 1, 1)
    # stern-brocot
    while 1:
        norm = FR_1n * FR_1n + FR_1d * FR_1d
        if norm < R2:
            ic = isqrt((R2-1)// norm)
            N[ic] += 2
        if FR_getNext() == 0:
            break
    N[MAXR-1] = 1
    N[int(MAXR/sqrt(2))] += 1
    for i in range(1, MAXR):
        S1 += i * N[i];  S2 += i * N[i] * i;  S3 += i * N[i] * i * i
    # print("R2=",R2,"nl=",nl,"nh=",nh)
    # quarter disk to half disk
    S1 *= 2 ; S2 = 2 * S2 ; S3 = 2 * S3
    S = S1*S1*S1 - 3 * S2 * S1 + 2 * S3
    S //= 3
    clk = (time.clock_gettime_ns(time.CLOCK_MONOTONIC) - t0) / 1000000
    print("{:.3f}ms ".format(clk), end='')
    print("r=",MAXR,"S=",S,"S1=",S1,"S2=",S2,"S3=",S3)

main()
