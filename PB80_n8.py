from __future__ import print_function
from math import sqrt,floor
import sys
import time

n=8
"""
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

"""
T3=[]
T2=[]

def main():
    global n,T3,T2
    t0 = time.clock_gettime(time.CLOCK_HIGHRES)
    for i1 in range(n):
        for i2 in range(n):
            if i2 != i1:
                T2.append(tuple[i1,i2])
    clk = (time.clock_gettime_ns(time.CLOCK_PROCESS_CPUTIME_ID) - t0) / 1000000
    print("{:.3f}ms ".format(clk), end='')
    print("T2=",T2)

main()
