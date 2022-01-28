from __future__ import print_function
import sys
if sys.version_info >= (3,0):
    from time import process_time
    sysnew = 1
else:
    from time import clock
    sysnew = 0
from math import cos, pi, tan


def main():
    if sysnew:
        t0 = process_time()
    else:
        t0 = clock()
    Cos = [0]*181
    Sin = [0]*181
    Csc = [0]*181
    degre = pi / 180

    for i in range(0,91):
        Cos[i] = cos(i * degre)
        Cos[180-i] = - Cos[i]
        Sin[90-i] = Sin[90+i] = Cos[i]
        if i != 90:
            Csc[90-i] =  Csc[90+i] = 1 / Sin[90-i]
    S = 0
    halfNbTg = int(2000 * tan(89 * degre)) + 1
    indTg = [0] * (2*halfNbTg + 1)
    valTg = [0] * 181
    for i in range(-89, 90):
        valTg[i + 90] = tan(i * degre)
        indTg[int(valTg[i+90] * 2000+halfNbTg+0.5)] = i+90
    for d1 in range(1, 90):
        sind1 = Sin[d1]
        d2=1
        while d2 <= 180 - 2 * d1 and d2 <= 90:
            # xb, yb intersection y * cos(d1)=(x+1) * sin(d1) and y * cos(d2)=-x * sin(d2)
            cscd2 = Csc[d2] ; cscd1d2 = Csc[d1 + d2]
            # xb = -sind1 * cosd2 * cscd1d2; yb = sind1 * sind2 * cscd1d2;
            xd_yd = Cos[d2] * cscd2  #  xd / yd
            xc_yd = sind1 * cscd1d2  # to calculate xc later
            d3=1
            while 2*d3 <= d2:
                if d2 == 90 and d3 > d1:
                    break
                # xd, yd intersection y * cos(d3) = -(x + 1) * sin(d3) and y * cos(d2) = -x * sin(d2)
                # xd = sind3 * cosd2 / sind2d3
                # yd = -sind3 * sind2 / sind2d3
                inv_yd = -Csc[d3] * cscd2 * Sin[d2 - d3]
                for d4 in range(d2-1, 0, -1):
                    if d2 + 2 * d1 == 180 and d3 < d2 - d4: # OB=OA=1
                        break
                    xc = xc_yd * Sin[d2 - d4] * Csc[d4]
                    if xc > 1.00000001:
                        break
                    tan_d5 = xc * inv_yd + xd_yd
                    d5 = indTg[int(2000 * tan_d5 + halfNbTg + 0.5)]
                    if d5 == 0:
                        d4 += 1; continue
                    if tan_d5 > valTg[d5]+0.00000001 or tan_d5 < valTg[d5] - 0.00000001:  # precise test
                        d4 += 1; continue
                    if d3 == d2 - d3 and d1 < 180 - d5 - d2:
                        d4 += 1; continue
                    S += 1
                    d4 += 1
                d3 += 1
            d2 += 1
    if sysnew:
        t1 = process_time()
    else:
        t1=clock()
    print("%.3fs: S  = %d" % ((t1 - t0), S))


main()
