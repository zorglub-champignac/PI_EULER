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

MEEKSUCC = {}
def MeekSucc(numr,powr,level):
    if level > 200:
        print("Succ(%x/2^%d)=exit" % (numr, powr))
        exit(0)
    if numr < 0:

        return (0,0,level)
    else:
        while powr > 0 and (numr & 1) == 0:
            numr >>=1
            powr -= 1
        if (numr,powr) in MEEKSUCC:
            return (MEEKSUCC[(numr,powr)][0],MEEKSUCC[(numr,powr)][1],level)


    for i in range(0, level):
        print(".", end='', sep='')
    print("--ASK(%x/2^%d)" % (numr,powr))


    # x <- MEEKSUCC(r-1)
    (numx,powx,levelx) = MeekSucc(numr-(1<<powr),powr,level+1)

    # d=x-(r-1)
    if powr <= powx:
        numd = numx - ((numr - (1 << powr)) << (powx - powr))
        powd = powx
    else:
        numd = (numx << (powr - powx)) - (numr - (1 << powr))
        powd = powr

    #ceil(log2(d))
    if numd > (1<<powd):
        powd2 = 1
        while numd > (1 << (powd+powd2)):
            powd2 +=1
    else:
        powd2 = 0
        while (numd << (powd2+1)) <= (1 << powd):
            powd2 += 1
        powd2 = - powd2
    # d = 1/2^powd2
    while powd > 0 and (numd & 1) == 0:
        numd >>= 1
        powd -= 1

    # y = 2r-x-1
    (numy, powy) = r2x(numr, powr, numx, powx)
    if numx==0:
        powa = 1
        while numr << powa >= (1 <<(powa+powr)) - (1<<powr):
            powa += 1
        numa = (1<<powa) -1
        print("MEEKSUCC(%x/2^%d)=%x/2^%d " % (numr, powr,numa ,powa))
        return (numa,powa,level)
    else:
        # y = y - 1 / 2^powx
        # y = y - 1 / 2^powxr
        powxr =powx
        if powxr < powr:
            powxr=powr

        if powy >= powxr:
            numy -= 1 << (powy - powxr)
        else:
            numy = (numy << (powxr - powy)) - 1
            powy = powxr

    # y + 2 ^ powd2
    if powy+powd2 >= 0:
        # y  = y + 2^(powy+powd2) / 2^powy
        numy += 1 << (powy+powd2)
    else:
        numy = (numy << (- (powy+powd2))) + 1
        powy = -powd2
    while powy > 0 and (numy & 1) == 0:
        numy >>= 1
        powy -= 1
    (numy, powy, levely) = MeekSucc(numy, powy, level + 1)

    if powx >= powy:
        numa = numx + (numy << (powx-powy)) + (1 << powx)
        powa = powx
    else:
        numa = (numx<< (powy-powx)) + numy  + (1 << powy)
        powa = powy
    powa += 1
    while powa > 0 and (numa & 1) == 0:
        numa >>= 1
        powa -= 1
    if level < 100:
        for i in range(0, level):
            print(".", end='', sep='')
        if powr <= powa:
            numd=numa - (numr<< (powa-powr))
            powd = powa
        else:
            numd = (numa <<(powr - powa)) - numr
            powd = powr
        while powd > 0 and (numd & 1) == 0:
            numd >>= 1
            powd -= 1
        print("MEEKSUCC(%x/2^%d)=%x/2^%d DELTA=%x/2^%d" % (numr,powr,numa,powa,numd,powd))
    MEEKSUCC[(numr,powr)]=(numa,powa)
    return (numa,powa,level)

n=3
if len(sys.argv) > 1:
    n = int(sys.argv[1])


MeekSucc(3,2,0)
MeekSucc(0x7fefffffd,34,0)
MeekSucc(n,0,0)