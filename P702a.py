from __future__ import print_function
import sys
import time


def F702a(x, m):
    M=[]
    isSecond = 0
    if 2 * x > m:
        x = m-x
        isSecond = 1
    if x == 1:
        if isSecond:
            return (m-1) * (m-2) // 2
        else:
            return 0
    M.append(m)
    while True:
        y = m % x
        if 2 * y >= x:
            y = x - y
        M.append(x)
        m = x; x = y
        if x == 1 or x == m-1:
            break
    nbV=len(M)
#    print("M=",M)
    M.append(1)
    F1 = 0; F = 0
    for i  in range(nbV-1,0,-1):
        # y = m % x; ∁(y) = x - y; ŷ = inf(y,∁(y))
        F2= F1;  F1= F
        m = M[i-1]; x = M[i];  t, y = divmod(m, x)
        F = t * (x-1) * (m + y - x +2) // 4
        if 2 * y > x:
            yb = x -y
# F = x * (x - 1) * t * (t + 1) / 4 - t * (x - 1) * (ŷ - 1) / 2 + (t + 1) f(ŷ, x) - f(∁(x % ŷ), ŷ) - (y + 1) * (ŷ - 1) / 2
#   = t * (x - 1) * (m + y - x + 2) / 4 + (t + 1) f(ŷ, x) - f(∁(x % ŷ), ŷ) - (y + 1) * (ŷ - 1) / 2
            if yb <= 1 or (x+M[i+2]) % yb == 0:
                F -= F2  # - f (x % ŷ, ŷ)
            else:
                F -= (M[i+1] -1) * (M[i+1] -2) // 2 - F2  # - f(∁(x % ŷ),ŷ)
            F += (t+1) * F1  - (y+1) * (yb-1) / 2
        else:
#  F = t * (t-1) * x * (x-1) /4 + t (y+1)(x-1)/2  + t * f(∁(y),x)  + f(x % y ,y)
#    = t * (x-1) * (m + y - x +2)/4  + t * f(∁(y),x) + f(x % y ,y)
            if y <= 1 or (x-M[i+2]) % y == 0:
                F += F2 # + f (x % y, y)
            else:
                F += (M[i+1] -1) * (M[i+1] -2) // 2 - F2 #  +f(∁(x%y),y)
            F += t * ((M[i]-1) * (M[i]-2) // 2-F1) #  + t f(∁(y),x)
    if isSecond:
        F = (M[0] - 1) * (M[0] - 2) // 2 - F
    return F


nl=123456789
if len(sys.argv) > 1:
    nl = int(sys.argv[1])

def main():
    global nl
    t0=time.clock_gettime_ns(time.CLOCK_MONOTONIC)
    exp2Max = 0
    while (1 << exp2Max) < nl:
        exp2Max += 1

    sum2B1W = 0
    for exp2 in range(2,exp2Max+1):
        pow2 = 1 << exp2
        nbInv = F702a(nl % pow2, pow2)
        # NbB = (pow2-1) *(pow2-2)//2 - nbInv
        # NbW = nbInv
        sum2B1W += (pow2-1) * (pow2-2)  - nbInv


    pow2 = (1 << exp2Max) - nl
    nbInv = F702a(nl % pow2, pow2)
    sum2B1W -=2 * ( (pow2-1) * (pow2-2)  - nbInv )
    clk = (time.clock_gettime_ns(time.CLOCK_MONOTONIC) - t0) / 1000000
    print("{:.3f}ms ".format(clk), end='')
    print("SUM=",nl*(3*nl+1)/2*(exp2Max+1) - sum2B1W )

main()
