from __future__ import print_function
import sys
import time

'''
'''
F702_cache = {}
def F702(x, m):
    if x <= 1:
        return 0
    if x == m-1:
        return (m-1)*(m-2)//2

    if 2*x < m :
        if (x, m) in F702_cache:
            return F702_cache[x, m]
        t, y = divmod(m, x)
        res = t * (x-1) * (m + y -x + 2)//4 + t * F702(x-y, x) + F702(x % y, y)
        F702_cache[x,m] = res
        return res
    else:
        x = m - x
        if (x, m) in F702_cache:
            return (m-1)*(m-2)//2 - F702_cache[x, m]
        t, y = divmod(m, x)
        res = t * (x-1) * (m + y -x + 2)//4 + t * F702(x-y, x) + F702(x % y, y)
        F702_cache[x,m] =  res
        return (m-1)*(m-2)//2 - res


nl=123456789
if len(sys.argv) > 1:
    nl = int(sys.argv[1])

def main():
    global nl
    t0=time.clock_gettime_ns(time.CLOCK_PROCESS_CPUTIME_ID)
    exp2Max = 0
    while (1 << exp2Max) < nl:
        exp2Max += 1

    sum2B1W = 0
    for exp2 in range(2,exp2Max+1):
        pow2 = 1 << exp2
        nbInv = F702(nl % pow2, pow2)
        # NbB = (pow2-1) *(pow2-2)//2 - nbInv
        # NbW = nbInv
        sum2B1W += (pow2-1) * (pow2-2)  - nbInv

    pow2 = (1 << exp2Max) - nl
    nbInv = F702(nl % pow2, pow2)
    sum2B1W -=2 * ( (pow2-1) * (pow2-2)  - nbInv )

    clk = (time.clock_gettime_ns(time.CLOCK_PROCESS_CPUTIME_ID) - t0) / 1000000
    print("{:.3f}ms ".format(clk), end='')
    print("SUM=",nl*(3*nl+1)/2*(exp2Max+1) - sum2B1W )

main()
