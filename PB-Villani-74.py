from itertools import *
from math import gcd
# from fractions import gcd

import sys
import time


def main(len):
    permuts=permutations(range(len))
    # p est la permutation des elements classes vers l'ordre initial choisi
    # chaque individu prend pour couleur :
    # sa couleur initiale ^ signature(permutation des autres individus (qu'il voit))
    for p in permuts:
        for u in range(len):
            signature = 0
            # calcul signature  NB(p[i]>p[j] ; 0<=i<j<len, i,j != u )
            for i in range(len-1):
                if i==u:
                    continue
                for j in range(i+1,len):
                    if j==u:
                        continue
                    if(p[i] > p[j]):
                        signature= 1-signature
            if u==0:
                # couleur initiale ^ signature
                ant_color = (p[u] & 1) ^ signature
            else:
                cur_color = (p[u] & 1) ^ signature
                # Test alternance 0, 1
                if cur_color + ant_color != 1:
                    print("ERROR")
                ant_color=cur_color



t0 = time.clock_gettime_ns(time.CLOCK_PROCESS_CPUTIME_ID)
main(7)
clk =(time.clock_gettime_ns(time.CLOCK_PROCESS_CPUTIME_ID) - t0) / 1000000
print("{:.3f}ms ".format(clk), end='')