from __future__ import print_function
from math import sqrt,floor,gcd
# from fractions import gcd
import sys
import time

'''
static int Index5(int S,int i0,int i1,int i2,int i3) {
    static int Cn3[] = {0,1,5,15,35,70,126,210,330,495,715,1001,1365,1820} ;
    static int Cn2[] = {0,1,4,10,20,35,56,84,120,165,220,286,364,455} ;
    static int Cn1[] = {0,1,3,6,10,15,21,28,36,45,55,66,78,91} ;
    int ind = Cn3[S-i0]+Cn2[S-i0-i1]+Cn1[S-i0-i1-i2]+S-i0-i1-i2-i3 ;
    return ind ;
}
Cnp(int n,int p) {
    if(p==0) return 1 ;
    if(n<p) return 0 ;
    if(p==1) return n ;
    uint64_t cnp = n*(n-1)/2 ;
    if(p>2) {
        int i  ;
        for(i=2;i<p;i++) {
            cnp *= n-i ;
            cnp /= i+1 ;
        }
    }
    return cnp ;
}
'''

Cn3 = [0,1,5,15,35,70,126,210,330,495,715,1001,1365,1820]
Cn2 = [0,1,4,10,20,35,56,84,120,165,220,286,364,455]
Cn1 = [0,1,3,6,10,15,21,28,36,45,55,66,78,91]


def Index5(S,i0,i1,i2,i3):
    global Cn3,Cn2,Cn1
    ind = Cn3[S - i0] + Cn2[S - i0 - i1] + Cn1[S - i0 - i1 - i2] + S - i0 - i1 - i2 - i3
    return ind

def Cnp(n,p):
    if p == 0:
        return 1
    if n < p:
        return 0
    if p == 1:
        return n
    cnp = (n*(n-1))//2
    if p > 2:
        for i in range(2,p):
            cnp *= n - i
            cnp //= i+1
    return cnp


MaxNr=13

def main():
    global MaxNr
    t0=time.clock_gettime_ns(time.CLOCK_MONOTONIC)
    ant5 = [0]*5
    ant5[Index5(1, 0, 0, 0, 0)] = 1
    ant5[Index5(1, 1, 0, 0, 0)] = 0
    ant5[Index5(1, 0, 1, 0, 0)] = 0
    ant5[Index5(1, 0, 0, 1, 0)] = 0
    ant5[Index5(1, 0, 0, 0, 1)] = 0
    pow3 = [1, 3, 9, 27]
    for nr in range(2,MaxNr+1):
        cur5 =[0] * (Index5(nr, 0, 0, 0, 0)+1)
        for n0 in range(0,nr):
            for n1 in range(0, nr-n0):
                for n2 in range(0, nr - n0 - n1):
                    for n3 in range(0, nr - n0 - n1 - n2):
                        n4 = nr -1 - n0 - n1 - n2 - n3
                        nb0 = 4 * n0 + 3 * n1 + 2 * n2 + 2 * n3 + n4
                        ant = ant5[Index5(nr-1,n0,n1,n2,n3)]
                        if ant <= 0:
                            continue
                        # inser ****
                        cur5[Index5(nr, n0, n1, n2, n3)] += ant * nb0
                        if n1:
                            cur5[Index5(nr, n0+1, n1-1, n2, n3)] += ant * n1
                        if n2:
                            cur5[Index5(nr, n0, n1+1, n2-1, n3)] += ant * 2*n2
                        if n3:
                            cur5[Index5(nr,n0,n1+1,n2,n3-1)] += ant * 2*n3
                        if n4:
                            cur5[Index5(nr, n0, n1, n2 + 1, n3)] +=  ant * n4
                            cur5[Index5(nr, n0, n1, n2, n3+1)] +=  ant * 2*n4
                        for d in range(0,4):
                            d0 = d1 = d2 = d3 = 0
                            if d == 0: # * * * *
                                d0 = 1; nbp = 4
                            elif d == 1:  #  ** * *
                                d1 = 1;  nbp = 3
                            elif d == 2: # ** **
                                d2 = 1;  nbp = 2
                            else: #  *** *
                                d3 = 1;  nbp = 2
                            for i0 in range(0,nbp+1):
                                if i0 > nb0:
                                    break
                                delta0 = Cnp(nb0, i0)
                                if d1:
                                    delta0 *= 3
                                elif d3:
                                    delta0 *= 2
                                for i1 in range(0,n1+1):
                                    if i0+i1 > nbp:
                                        break
                                    delta1 = delta0 * Cnp(n1, i1)
                                    i2max = nbp-i0-i1
                                    if i2max == 0:
                                        cur5[Index5( nr, n0+i1+d0, n1-i1+d1, n2+d2, n3+d3)] += ant * delta1
                                        break
                                    for i22 in range(0,n2+1):
                                        if 2 * i22 > i2max:
                                            break
                                        for i21 in range(0,n2-i22+1):
                                            if i21 + 2 * i22 > i2max:
                                                break
                                            delta2 = delta1 * Cnp(n2, i22) * Cnp(n2-i22, i21) * (1 << i21)
                                            i3max = i2max -2 * i22 - i21
                                            if i3max == 0:
                                                cur5[Index5( nr, n0+d0+i1+i22, n1+d1-i1+i21, n2+d2-i22-i21, n3+d3)] +=  ant * delta2
                                                break
                                            for i32 in range(0,n3+1):
                                                if 2 * i32 > i3max:
                                                    break
                                                for i31 in range(0,n3 - i32+1):
                                                    if i31 + 2 * i32 > i3max:
                                                        break
                                                    delta3 = delta2 * Cnp(n3, i32) * Cnp(n3-i32, i31) * (1 << i31)
                                                    i4max = i3max - 2 * i32 - i31
                                                    if i4max == 0:
                                                        cur5[Index5( nr, n0+d0+i1+i22+i32, n1+d1-i1+i21+i31, n2+d2-i22-i21, n3+d3-i32-i31)] += ant *  delta3
                                                        break
                                                    for i43 in range(0,n4+1):
                                                        if i43 * 3 > i4max:
                                                            break
                                                        for i42 in range(0,n4-i43+1):
                                                            if i42 * 2 + 3 * i43 > i4max:
                                                                break
                                                            i41 = i4max-3 * i43 -2 * i42
                                                            if i41+i42+i43 > n4:
                                                                continue
                                                            delta = delta3
                                                            if i43:
                                                                delta *= n4
                                                            if i42:
                                                                delta *= Cnp(n4-i43, i42) * pow3[i42]
                                                            for j3 in range(0,i41+1):
                                                                cur5[Index5(nr, n0 + d0 + i1 + i22 + i32 + i43 \
                                                                ,n1 + d1 - i1 + i21 + i31 + i42 \
                                                                ,n2 + d2 - i22 - i21 + i41 - j3 \
                                                                ,n3 + d3 - i32 - i31 + j3)] \
                                                                += ant * delta * Cnp(n4 - i43 - i42, i41) * (1 << j3) * Cnp(i41, j3)
        prob = [0]* (nr+1)
        den = 0
        g = cur5[0]
        for i in range(1,Index5(nr, 0, 0, 0, 0)+1):
            g = gcd(g,cur5[i])
            if g ==1:
                break
        for i in range(0,Index5(nr, 0, 0, 0, 0)+1):
            cur5[i] //= g
            den += cur5[i]
        for n0 in range(0, nr+1):
            for n1 in range(0, nr+1 - n0):
                for n2 in range(0, nr+1 - n0 - n1):
                    for n3 in range(0, nr+1 - n0 - n1 - n2):
                        n4 = nr - n0 - n1 -n2 -n3
                        prob[n0] += cur5[Index5(nr, n0, n1, n2, n3)]
#                       print("nr=",nr,"(",n0,n1,n2,n3,n4,")=",cur5[Index5(nr,n0,n1,n2,n3)])
        print("4 color, rank ", nr,end='');
        for i in range(0,nr+1):
            print(" ", prob[i] / (1.0*den),end='')
        print(" ")
        if nr==13:
            num = prob[2]+prob[3]+prob[5]+prob[7]+prob[11]+prob[13]
            g = gcd(num,den)
            print("P(prime)=",num//g,"/",den//g," = ",num/(1.0*den))
        ant5 = cur5
        cur5 = []

    clk = (time.clock_gettime_ns(time.CLOCK_MONOTONIC) - t0) / 1000000
    print("{:.3f}ms ".format(clk), end='')

main()
