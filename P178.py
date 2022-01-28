from __future__ import print_function
from time import process_time
import sys

N_DIGITS = 40
if len(sys.argv) > 1:
    N_DIGITS = int(sys.argv[1])

def main():
    t0 = process_time()

    D1 = 0; D2 = 0; D3 = 0; D4 = 0
    FD0 = 0; FD1 = 0; FD2 = 0; FD3 = 0; FD4 = 0; FD5 = 0; FD6 = 0; FD7 = 0; FD8 = 0
    FFD0 = 0; FFD1 = 0; FFD2 = 0; FFD3 = 0; FFD4 = 0
    for id in range(0,N_DIGITS-1):
        tmp1 = D4; D4 += 1 + D3        # D4 = 2 +D3 +D4; d 4, 5
        tmp2 = D3; D3 = 1 + tmp1 + D2  # D3 = 2 +D2 + D4; d 3, 6
        tmp1 = D2; D2 = 1 + tmp2 + D1  # D2 = 2 +D1 + D3; d 2, 7
        tmp2 = D1; D1 = 1 + tmp1       # D1 = 2 + D2; d 1, 8
        #
        tmp1 = FD0; FD0 = 1 + tmp2 + FD1 # FD0 = 2 + D1 + FD1; 0, 9
        tmp2 = FD1; FD1 = tmp1 + FD2     # FD1 =  FD0 + FD2; 0-1, 9-8
        tmp1 = FD2; FD2 = tmp2 + FD3     # FD2 =  FD1 + FD3; 0-2, 9-7
        tmp2 = FD3; FD3 = tmp1 + FD4     # FD3 =  FD2 + FD3; 0-3, 9-6
        tmp1 = FD4; FD4 = tmp2 + FD5     # FD4 =  FD3 + FD5; 0-2, 9-5
        tmp2 = FD5; FD5 = tmp1 + FD6     # FD5 =  FD4 + FD6; 0-5, 9-4
        tmp1 = FD6; FD6 = tmp2 + FD7     # FD6 =  FD5 + FD7; 0-6, 9-3
        tmp2 = FD7; FD7 = tmp1 + FD8     # FD7 =  FD6 + FD8; 0-7, 9-2
        tmp1 = FD8; FD8 = tmp2           # FD8 =  FD7; 0-8, 9-1
        #
        tmp2 = FFD0; FFD0 = tmp1 + FFD1  # FFD0 = FD8  + FFD1; 0, 9
        tmp1 = FFD1; FFD1 = tmp2 + FFD2  # FFD1 = FFD0 + FFD2; 1, 8
        tmp2 = FFD2; FFD2 = tmp1 + FFD3  # FFD2 = FFD1 + FFD3; 2, 7
        tmp1 = FFD3; FFD3 = tmp2 + FFD4  # FFD3 = FFD2 + FFD4; 3, 6
        FFD4 += tmp1                     # FFD4 = FFD3 + FFD4; 4, 5
    # adding the last digit as Most Significant Digit(not 0)
    # so Half FD8(8 + 9)
    S = (FD8 + FFD1) + ((FFD0 + FFD1) << 1) + ((FFD2 + FFD3 + FFD4) << 2)
    t1 = process_time()
    print("%.3fms: Nb digits = %d ; S  = %d" % ((t1 - t0) * 1000, N_DIGITS, S))


main()
