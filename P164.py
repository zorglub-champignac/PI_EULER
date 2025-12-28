from __future__ import print_function

import sys
import time

ndigits=20
if len(sys.argv) > 1:
    ndigits = int(sys.argv[1])

def main():
    t0=time.clock_gettime_ns(time.CLOCK_PROCESS_CPUTIME_ID)
    clk = 0

    n00 = 0; n01 = 0; n02 = 0; n03 = 0; n04 = 0; n05 = 0; n06 = 0; n07 = 0; n08 = 0; n09 = 0
    n10 = 1; n11 = 1; n12 = 1; n13 = 1; n14 = 1; n15 = 1; n16 = 1; n17 = 1; n18 = 1
    n20 = 1; n21 = 1; n22 = 1; n23 = 1; n24 = 1; n25 = 1; n26 = 1; n27 = 1
    n30 = 1; n31 = 1; n32 = 1; n33 = 1; n34 = 1; n35 = 1; n36 = 1
    n40 = 1; n41 = 1; n42 = 1; n43 = 1; n44 = 1; n45 = 1
    n50 = 1; n51 = 1; n52 = 1; n53 = 1; n54 = 1
    n60 = 1; n61 = 1; n62 = 1; n63 = 1
    n70 = 1; n71 = 1; n72 = 1
    n80 = 1; n81 = 1
    n90 = 1

    for i in range(2,ndigits):
        m00 = n00 + n10 + n20 + n30 + n40 + n50 + n60 + n70 + n80 + n90
        m01 = n00 + n10 + n20 + n30 + n40 + n50 + n60 + n70 + n80
        m02 = n00 + n10 + n20 + n30 + n40 + n50 + n60 + n70
        m03 = n00 + n10 + n20 + n30 + n40 + n50 + n60
        m04 = n00 + n10 + n20 + n30 + n40 + n50
        m05 = n00 + n10 + n20 + n30 + n40
        m06 = n00 + n10 + n20 + n30
        m07 = n00 + n10 + n20
        m08 = n00 + n10
        m09 = n00

        m10 = n01 + n11 + n21 + n31 + n41 + n51 + n61 + n71 + n81
        m11 = n01 + n11 + n21 + n31 + n41 + n51 + n61 + n71
        m12 = n01 + n11 + n21 + n31 + n41 + n51 + n61
        m13 = n01 + n11 + n21 + n31 + n41 + n51
        m14 = n01 + n11 + n21 + n31 + n41
        m15 = n01 + n11 + n21 + n31
        m16 = n01 + n11 + n21
        m17 = n01 + n11
        m18 = n01

        m20 = n02 + n12 + n22 + n32 + n42 + n52 + n62 + n72
        m21 = n02 + n12 + n22 + n32 + n42 + n52 + n62
        m22 = n02 + n12 + n22 + n32 + n42 + n52
        m23 = n02 + n12 + n22 + n32 + n42
        m24 = n02 + n12 + n22 + n32
        m25 = n02 + n12 + n22
        m26 = n02 + n12
        m27 = n02

        m30 = n03 + n13 + n23 + n33 + n43 + n53 + n63
        m31 = n03 + n13 + n23 + n33 + n43 + n53
        m32 = n03 + n13 + n23 + n33 + n43
        m33 = n03 + n13 + n23 + n33
        m34 = n03 + n13 + n23
        m35 = n03 + n13
        m36 = n03

        m40 = n04 + n14 + n24 + n34 + n44 + n54
        m41 = n04 + n14 + n24 + n34 + n44
        m42 = n04 + n14 + n24 + n34
        m43 = n04 + n14 + n24
        m44 = n04 + n14
        m45 = n04

        m50 = n05 + n15 + n25 + n35 + n45
        m51 = n05 + n15 + n25 + n35
        m52 = n05 + n15 + n25
        m53 = n05 + n15
        m54 = n05

        m60 = n06 + n16 + n26 + n36
        m61 = n06 + n16 + n26
        m62 = n06 + n16
        m63 = n06

        m70 = n07 + n17 + n27
        m71 = n07 + n17
        m72 = n07

        m80 = n08 + n18
        m81 = n08

        m90 = n09

        n00 = m00; n01 = m01; n02 = m02; n03 = m03;  n04 = m04;  n05 = m05; n06 = m06; n07 = m07; n08 = m08;  n09 = m09
        n10 = m10; n11 = m11; n12 = m12; n13 = m13;  n14 = m14;  n15 = m15; n16 = m16; n17 = m17; n18 = m18
        n20 = m20; n21 = m21; n22 = m22; n23 = m23;  n24 = m24;  n25 = m25; n26 = m26; n27 = m27
        n30 = m30; n31 = m31; n32 = m32; n33 = m33;  n34 = m34;  n35 = m35; n36 = m36
        n40 = m40; n41 = m41; n42 = m42; n43 = m43;  n44 = m44;  n45 = m45
        n50 = m50; n51 = m51; n52 = m52; n53 = m53;  n54 = m54
        n60 = m60; n61 = m61; n62 = m62; n63 = m63
        n70 = m70; n71 = m71; n72 = m72
        n80 = m80; n81 = m81
        n90 = m90

    S = n00 + n01 + n02 + n03 + n04 + n05 + n06 + n07 + n08 + n09 \
    + n10 + n11 + n12 + n13 + n14 + n15 + n16 + n17 + n18 \
    + n20 + n21 + n22 + n23 + n24 + n25 + n26 + n27 \
    + n30 + n31 + n32 + n33 + n34 + n35 + n36 \
    + n40 + n41 + n42 + n43 + n44 + n45 \
    + n50 + n51 + n52 + n53 + n54 \
    + n60 + n61 + n62 + n63 \
    + n70 + n71 + n72 \
    + n80 + n81 \
    + n90
    clk = (time.clock_gettime_ns(time.CLOCK_PROCESS_CPUTIME_ID)-t0)/1000000000;
    print("{:.6f}s ".format(clk), end='')
    print(" S=", S)


main()
