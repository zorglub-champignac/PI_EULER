from __future__ import print_function
from time import clock
import sys

Pow10=13
if len(sys.argv) > 1:
    Pow10 = int(sys.argv[1])
Maxn=1
for i in range(0,Pow10):
    Maxn *= 10



#
# using S(n) = 1<<Fi + S(n-Fi) - S(F(i+1)-n -3)
# we call VL = n-Fi ; VR = F(i+1) - n - 3
# and if n=V[i] V[iL] = VL
def main():
    global  Maxn,Pow10
    clock()
    N=Maxn
    F = [1, 2]
    nbF = 1
    while 1:
        Fn = F[-1]+F[-2]
        F.append(Fn)
        nbF += 1
        if Fn > N:
            break
    V =  [0] * 3*Pow10 # different n values to compute
    iF = [0] * 3 * Pow10 # Fibonnaci index so F(i)<= n < F(i+1)
    iL = [0] * 3*Pow10  # index of left part
    nbV = 0  # number of S values to compute
    V[0]=N      # first value = N
    iF[0] = nbF-1 # index of corresponding Fibonnaci
    upL = nbV # backtracking for iL
    FL = N - F[-2]  # decomposition in FL and FR for N
    FR = F[-1] - N - 3
    upR = - 1 # backtracking for iR
    while FL > 1 or FR > 1:
        if FL == FR: # the two chains merge
            FR=0 # we stop FR
        if FL < FR: # so FL is the greater value (to store n values in order)
            (FL,FR)=(FR,FL)
            (upL,upR)=(upR,upL)
        nbV += 1 # new n value
        V[nbV] = FL # store the new n value
        if upL >=0: # if backtrack OK store the Left index
            iL[upL] = nbV
        upL = nbV # next backtrack for the new n value
        while nbF >=0 and F[nbF] > FL: # search Fibonnaci number
            nbF -= 1
        iF[nbV] = nbF # store index of Fibonnaci
        FL -= F[nbF] # new FL value
    nbV +=1 # add n value = 1
    if upL >=0:
        iL[upL] = nbV
    V[nbV] = 1
    iL[nbV] = 0

    vS = [0] * (nbV+1)
    vS[nbV]=1 # for n = 1 => S = 1
    # compute vS in reverse order
    for i in range(nbV-1,-1,-1):
        S = ( 1 << iF[i] )
        if iL[i] > 0:
            S += vS[iL[i]] # add VL part
        elif iL[i] == 0:
            S += 1
        VR = F[iF[i]+1]-V[i]-3
        if(VR > 0): # search VR value in already computed n values
            j = i + 1
            while V[j] != VR:
                j += 1
            S -= vS[j]
        elif VR == 0:
            S -= 1
        vS[i] = S
    clk = clock()
    print("{:.3f}s ".format(clk), end='')
    print("For N=10**",Pow10,"; NB Fibonnaci=",len(F)," ; number of Computed values=",nbV,"; S=",vS[0])

main()
