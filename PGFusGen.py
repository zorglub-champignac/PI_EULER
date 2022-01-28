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

def Fus(numx,powx,numy,powy):
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
    return (numa,powa)

FUS = {}
maxPow = 0


def KeyFus(fus):
    global maxPow
    return fus[0] << (maxPow-fus[1])

sizeFus = 0
nmax=2
def GenFus(n):
    global sizeFus,maxPow,nmax
    FUS[(0,0)] = 0
    sizeFus += 1
    for ir in range(0,n):
        level=ir
        supSize=0
        for (numx,powx) in FUS.keys():
            if(FUS[(numx,powx)])>level:
                continue
            for (numy,powy) in FUS.keys():
                if (FUS[(numy, powy)]) > level:
                    continue
                diff = (numy << powx) - (numx << powy)
                if diff < 0:
                    diff = -diff
                if diff >= (1 << (powx+powy)):
                    continue
                (numa, powa) = Fus(numx,powx,numy,powy)
                if numa <= nmax*(1<<powa) and (numa,powa) not in FUS.keys():
                #if (numa, powa) not in FUS.keys():
                    FUS[(numa,powa)]=level+1
                    print("(%x/2^%d)=(%x/2^%d)~(%x/2^%d)" % (numa,powa,numx,powx,numy,powy))
                    if powa > maxPow:
                        maxPow= powa
                    supSize+=1
        sizeFus += supSize
    listFus =[]
    for (numx, powx) in FUS.keys():
        listFus.append((numx, powx))
    listFus.sort(key=KeyFus)

    for j in range(0,len(listFus)):
        #print(j, listFus[j])
        print("(%x/2^%d)=%d" % (listFus[j][0], listFus[j][1],FUS[listFus[j]]))




n=3
if len(sys.argv) > 1:
    n = int(sys.argv[1])
GenFus(n)

