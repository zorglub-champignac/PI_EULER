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

TAMESUCC = {}
def FusT(numr,powr,level):
    if numr < 0:

        return (0, 0, level)
    else:
        while powr > 0 and (numr & 1) == 0:
            numr >>= 1
            powr -= 1
        if (numr, powr) in TAMESUCC:
            return (TAMESUCC[(numr, powr)][0], TAMESUCC[(numr, powr)][1], level)
    if level < 10:
        for i in range(0, level):
            print(".", end='', sep='')
        print("--ASK(%x/2^%d)" % (numr, powr))

    # x <- MEEKSUCC(r-1)
    (numx, powx, levelx) = FusT(numr - (1 << powr), powr, level + 1)

    # y = 2r-x-1
    (numy, powy) = r2x(numr, powr, numx, powx)
    (numy,powy,levely) = FusT(numy, powy, level + 1)
    if powx >= powy:
        numa = numx + (numy << (powx - powy)) + (1 << powx)
        powa = powx
    else:
        numa = (numx << (powy - powx)) + numy + (1 << powy)
        powa = powy
    powa += 1
    while powa > 0 and (numa & 1) == 0:
        numa >>= 1
        powa -= 1
    if level < 10:
        for i in range(0, level):
            print(".", end='', sep='')
        if powr <= powa:
            numd = numa - (numr << (powa - powr))
            powd = powa
        else:
            numd = (numa << (powr - powa)) - numr
            powd = powr
        while powd > 0 and (numd & 1) == 0:
            numd >>= 1
            powd -= 1
        print("MEEKTAME(%x/2^%d)=%x/2^%d DELTA=%x/2^%d" % (numr, powr, numa, powa, numd, powd))
    TAMESUCC[(numr, powr)] = (numa, powa)
    return (numa, powa, level)


FusT(0x7fefffffd,34,0)
FusT(3,0,0)