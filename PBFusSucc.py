from __future__ import print_function
import sys
if sys.version_info >= (3,0):
    from time import process_time
    sysnew = 1
else:
    from time import clock
    sysnew = 0

# 2r-x-1
def r2x(numr,powr,numx,powx):
    if powr >= powx:
        num = 2*numr - (numx<<(powr-powx))  - (1<<powr)
        pow = powr
    else:
        num = (numr<< (powx - powr+1)) - numx  - (1 << powx)
        pow = powx
    while pow > 0 and (num & 1) == 0:
        num >>= 1
        pow -= 1
    return (num,pow)

SUCC = {}
def Succ(numr,powr,level):
#    if level > 200:
    if level > 10:
        print("Succ(%x/2^%d)=exit" % (numr, powr))
        exit(0)
    if numr < 0:

        return (0,0,level)
    else:
        if (numr,powr) in SUCC:
            return (SUCC[(numr,powr)][0],SUCC[(numr,powr)][1],level)


    numm = numr+ (1<<powr)
    powm = powr

    numy = numr
    powy = powr

    # calcul r - 1/2 = numr/(1<<powr) - 1/2
    if powr > 0:
        powr2 = powr
        numr2 = numr - (1 << (powr-1))
    else:
        powr2 = 1
        numr2 = 2*numr - 1

    # y > r-1/2
    while (numy << powr2) > (numr2 << powy):
        # x <- SUCC(2r-y-1)
        (numx,powx) = r2x(numr,powr,numy,powy)
        (numx,powx,levelx) = Succ(numx,powx,level+1)
        # y <- SUCC(2r-x-1)
        (numy, powy) = r2x(numr, powr, numx, powx)
        (numy,powy,levely) = Succ(numy,powy,level+1)
        # x ~ y = (x+y+1)/2
        if powx >= powy:
            numxy = numx + (numy << (powx-powy))+(1<<powx)
            powxy = powx+1
        else:
            numxy =  (numx << (powy-powx))+numy +(1<<powy)
            powxy = powy+1
        while powxy > 0 and (numxy & 1)==0:
            numxy >>= 1
            powxy -=1
        if (numxy << powm) < (numm << powxy):
            numm = numxy
            powm = powxy
        numy = numy - 1
        while powy > 0 and (numy & 1) == 0:
            numy >>= 1
            powy -= 1

#    if level < 100:
    if level < 5:
        for i in range(0, level):
            print(".", end='', sep='')
        if powr <= powm:
            numd=numm - (numr<< (powm-powr))
            powd = powm
        else:
            numd = (numm <<(powr - powm)) - numr
            powd = powr
        while powd > 0 and (numd & 1) == 0:
            numd >>= 1
            powd -= 1
        print("SUCC(%x/2^%d)=%x/2^%d DELTA=%x/2^%d" % (numr,powr,numm,powm,numd,powd))
    SUCC[(numr,powr)]=(numm,powm)
    return (numm,powm,level)

n=2
if len(sys.argv) > 1:
    n = int(sys.argv[1])


Succ(n,0,0)