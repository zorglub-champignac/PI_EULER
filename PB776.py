from __future__ import print_function
import sys
if sys.version_info >= (3,0):
    from time import process_time
    sysnew = 1
else:
    from time import clock
    sysnew = 0
from fractions import Fraction

nbDigit=19
if len(sys.argv) > 1:
    nbDigit = int(sys.argv[1])

def main():
    global nbDigit
    digits=[0]*nbDigit
    if sysnew:
        t0 = process_time()
    else:
        t0 = clock()
    digits[0] = d = 1
    nbSize = 9*nbDigit+1
    Sum =[0] *  nbSize
    Nb = [0] *  nbSize
    for id in range(0, digits[0]):
        Nb[id] += 1
        Sum[id] += id
    sumD = digits[0]
    exact = digits[0]

    for i in range(1,nbDigit):
        d += 1
        if d == 10:
            d = 0
        digits[i] = d
        for js in range(9*i-1,-1,-1):
            nb = Nb[js]
            if nb:
                sum10 = Sum[js]*10
                Sum[js] = sum10
                for id in range(1,10):
                    Nb[js+id] += nb
                    Sum[js+id] += sum10 + nb * id
        exact *= 10
        for id in range(0,digits[i]):
            Nb[sumD+id] += 1
            Sum[sumD+id] += exact + id
        sumD += digits[i]
        exact += digits[i]
    S = 0.0
    for js in range(1,nbSize):
        S += Sum[js] / js
    S += exact / sumD
    '''
    SR=Fraction(0,1)
    for js in range(1,nbSize):
        SR +=Fraction(Sum[js],js)
    SR=SR+Fraction(exact,sumD)
    '''
    if sysnew:
        t1 = process_time()
    else:
        t1=clock()
    print("%.3fs Sum=%.12e For:%d" % (t1-t0,S,exact))
    print(" S=",S)


main()
