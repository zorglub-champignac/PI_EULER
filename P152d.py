from __future__ import print_function

import sys
from math import log
from time import clock

small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
                103, 107,109,113,119,127,131,137,139,149,151,157,161]

#list of powp (p, powp, ppcmPowp)
LP_powpList = []
LP_den_ppcm = 1


LS_numLevel=0
LS_Elem=[]
LS_Constraint=1
LS_ppcm=2
LS_PP=(1,2,2)
LS_fact=1
LS_usedVal=[2]
LS_cumPpcm=1

LV_nbSum=0
LV_index=[]
LV_maxSum=0




def ListPowp(maxN):
    global small_primes
    global LP_powpList
    global LP_den_ppcm
    maxExp = lambda p: int(log(maxn // 2, p))
    candpowp = [(p, p ** maxExp(p)) for p in reversed(small_primes) if p < maxn // 4 and maxExp(p) > 0]
    for (p, powp) in candpowp:
        isFound = 0
        while powp > 1:
            sqp = p * p
            np = maxn // powp
            if p != 2 and np >= powp-1:
                np = powp - 1
            if p == 2 and np > 2*powp-1:
                np = powp - 1
            listInv= []
            for i in [i for i in range(1, np+1) if i % p != 0]:
                i2 = (i * i) % sqp
                invi2 = 1
                while (i2 * invi2) % sqp != 1:
                    invi2 = (invi2 * i2) % sqp
                listInv.append(invi2)
            sumInv = [ 0 ]
            for inv in listInv:
                sumSup = []
                for sum in sumInv:
                    s = (sum+inv) % sqp
                    if s == 0:
                        isFound = 1
                        break
                    sumSup.append(s)
                if isFound:
                    break
                sumInv.extend(sumSup)
#               print(sumInv, "_")
            if isFound:
                break
            powp = powp // p
        if isFound:
            LP_den_ppcm *= powp
            ppcmPowp = p
            while powp >1:
                LP_powpList.append((p, powp,ppcmPowp))
                ppcmPowp *= p
                powp = powp // p


def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def nextLevelState():
    global LS_numLevel, LS_usedVal , LS_Elem, LS_Constraint, LS_fact, LS_ppcm,LS_PP,LS_cumPpcm
    global LP_powpList , LP_den_ppcm
    LS_Elem = []
    oldLevel = LS_numLevel
    while len(LS_Elem) == 0 and len(LP_powpList) > 0 :
        (p,powp,ppcmPowp) = LP_powpList.pop(0)
        ppcm = LS_cumPpcm
        for k in range(powp, maxn + 1, powp):
            if k in LS_usedVal:
                continue
            if LP_den_ppcm % k == 0:
#                pgcd64=pgcd(ppcm,k)
                ppcm = ppcm * k // pgcd(ppcm,k)
                LS_Elem.append((k,0))
        if len(LS_Elem) > 0:
            (LS_PP_p, LS_PP_powp , LS_PP_ppcmPowp)=LS_PP
            LS_Constraint= p*p
            LS_fact = ppcm * LS_PP_p // LS_ppcm
            LS_cumPpcm = ppcm // pgcd(ppcmPowp,ppcm)
            LS_ppcm = ppcm
            LS_PP=(p,powp,ppcmPowp)
            for i in range(0,len(LS_Elem)):
                (k,w)=LS_Elem[i]
                w = (ppcm // k)* (ppcm //k)
                LS_Elem[i] = (k,w)
                LS_usedVal.append(k)
            LS_numLevel += 1
    return LS_numLevel - oldLevel


def nextLevelStateLPLPS(LP_powpList , LP_den_ppcm,LS_numLevel, LS_usedVal ,LS_PP,LS_ppcm,LS_cumPpcm):
    LS_Elem = []
    LS_Constraint = 1
    LS_fact = 1
    oldLevel = LS_numLevel
    while len(LS_Elem) == 0 and len(LP_powpList) > 0 :
        (p,powp,ppcmPowp) = LP_powpList.pop(0)
        ppcm = LS_cumPpcm
        for k in range(powp, maxn + 1, powp):
            if k in LS_usedVal:
                continue
            if LP_den_ppcm % k == 0:
#                pgcd64=pgcd(ppcm,k)
                ppcm = ppcm * k // pgcd(ppcm,k)
                LS_Elem.append((k,0))
        if len(LS_Elem) > 0:
            (LS_PP_p, LS_PP_powp , LS_PP_ppcmPowp)=LS_PP
            LS_Constraint= p*p
            LS_fact = ppcm * LS_PP_p // LS_ppcm
            LS_cumPpcm = ppcm // pgcd(ppcmPowp,ppcm)
            LS_ppcm = ppcm
            LS_PP=(p,powp,ppcmPowp)
            for i in range(0,len(LS_Elem)):
                (k,w)=LS_Elem[i]
                w = (ppcm // k)* (ppcm //k)
                LS_Elem[i] = (k,w)
                LS_usedVal.append(k)
            LS_numLevel += 1
#    return LS_numLevel - oldLevel
    return (LS_numLevel,LS_Elem,LS_Constraint,LS_fact,LS_ppcm,LS_PP,LS_cumPpcm)


def compute_level(Elem , constraint):
    global LV_index, LV_maxSum
    LV_index = []
    LV_maxSum=0
    for i in range(0,constraint):
        LV_index.append([])
    nbSum = 1 << len(Elem)
    sumL=[]
    sumL.append((0, 0))
    LV_index[0].append(0)
    for (k,w) in Elem:
        intSum = w // constraint
        modSum = w - constraint * intSum
        sumL1 = []
        for (intL,modL) in sumL:
            intL += intSum
            modL += modSum
            if modL >= constraint:
                modL -= constraint
                intL += 1
            sumL1.append((intL,modL))
            LV_index[modL].append(intL)
            if intL > LV_maxSum:
                LV_maxSum = intL
        sumL.extend(sumL1)
    for i in range(0, constraint):
        LV_index[i].sort()





# start global variables

# maximum number
# maxn = 80


maxn = int(sys.argv[1])


# end global variables

def Print_LV():
    for modL in range(0, len(LV_index)):
        listSum = LV_index[modL]
        if len(listSum) > 0:
            print("mod=", modL, " Val", listSum)
# Pp=(p,powp,ppcpPopm)
def getPowp(Pp):
    return Pp[1]


def ComputeHisto(LP_powpList):
    LS_numLevel = 0
    LS_Elem = []
    LS_Constraint = 1
    LS_ppcm = 2
    LS_ppcm = 1
    LS_PP = (1, 2, 2)
    LS_fact = 1
    LS_usedVal = [2]
    LS_cumPpcm = 1

    histo0 = {}
    histo0[1] = 1
    histo1 = {}
    explain1 = {}
    minSum0 = 1
    maxSum0 = 1
    mode = 0
    count0 = []
    offsetS0 = 0

    constraint = 1
    #    while nextLevelState():
    while True:
        oldLevel = LS_numLevel
        (LS_numLevel, LS_Elem, LS_Constraint, LS_fact, LS_ppcm, LS_PP, LS_cumPpcm) = \
            nextLevelStateLPLPS(LP_powpList, LP_den_ppcm, LS_numLevel, LS_usedVal, LS_PP, LS_ppcm, LS_cumPpcm)
        print("LSnumLevel",LS_numLevel,"Oldlevel",oldLevel)
        constraint *= LS_Constraint
        if LS_numLevel == oldLevel:
            print("BREAK")
            break
#        print(LS_numLevel, LS_Elem)
        clk = clock();
        print("{:.3f}s ".format(clk), end='')
        compute_level(LS_Elem, LS_Constraint)
        print(LV_index)
        clk = clock();
        print("Compute_level {:.3f}s ".format(clk))
        factS = LS_fact * LS_fact
        offsetS0 = minSum0
        sumMax = maxSum0
        sumMax = (sumMax * factS) // LS_Constraint
#        nbCountS1 = sumMax - offsetS0 * factS // LS_Constraint + LV_maxSum + 1
        nbCountS1 = sumMax - offsetS0 * factS // LS_Constraint + maxSum0 + 1
        if nbCountS1 - 1 > sumMax:
            nbCountS1 = sumMax + 1
        offsetS1 = sumMax - (nbCountS1 - 1)
        clk = clock();
        print("{:.3f}s ".format(clk), end='')
        print("Level=", LS_numLevel, "Min=", minSum0, "Max=", maxSum0, " Elem=[", LS_Elem[0], "...", LS_Elem[-1],
              end='')
        print("] ppcm=", LS_ppcm, " fact=", LS_fact, "ExpOut", nbCountS1, "Hin=", len(histo0), end='')
        minSum0 = LS_ppcm * LS_ppcm
        maxSum0 = 0
        nout = 0
        print("h=")
        for sum in histo0:
            count = histo0[sum]
            sum *= factS
            sum += 4
            intSum = sum // LS_Constraint
            modSum = sum - intSum * LS_Constraint
            print((modSum, intSum), end='')
            for intLV in LV_index[modSum]:
#                if intSum < intLV:
#                    break
                nout += 1
                newSum = intSum - intLV
                if newSum > maxSum0:
                    maxSum0 = newSum
                elif newSum < minSum0:
                    minSum0 = newSum
                if newSum in histo1:
                    histo1[newSum] += count
                else:
                    histo1[newSum] = count
        if mode == 0:
            #            print("h="); print(histo1)
            histo0.clear()
            print("=>LenH=", nout, "/", len(histo1))
            (histo0, histo1) = (histo1, histo0)
    vals = histo0.keys()
    print(constraint,maxSum0,vals)
    nLV_index = []

    for i in range(0, constraint):
            nLV_index.append([])
    for v in vals:
        v = sumMax - v
        intL =  v // constraint
        modL =  v - intL * constraint
        nLV_index[modL].append(intL)
    for i in range(0, constraint):
        nLV_index[i].sort()
    histo0.clear()
    print(nLV_index)
    return nLV_index

def main():
    global LP_den_ppcm,LP_powpList
    global LS_numLevel, LS_usedVal , LS_Elem, LS_Constraint, LS_fact, LS_ppcm,LS_cumPpcm,LS_PP
    global LV_index
    clock() ;
    clk = 0 ;
    ListPowp(maxn)
    if 0:
        (p0, powp0, ppcmPowp0) = LP_powpList.pop(0)
        (p1, powp1, ppcmPowp1) = LP_powpList.pop(0)
        (q01,q02,q03)=(p0*p1,powp0*powp1,ppcmPowp0*ppcmPowp1)
        (p0, powp0, ppcmPowp0) = LP_powpList.pop(0)
        (p1, powp1, ppcmPowp1) = LP_powpList.pop(0)
        (q11, q12, q13) = (p0 * p1, powp0 * powp1, ppcmPowp0 * ppcmPowp1)
        (p0, powp0, ppcmPowp0) = LP_powpList.pop(0)
        (p1, powp1, ppcmPowp1) = LP_powpList.pop(0)
        (q21, q22, q23) = (p0 * p1, powp0 * powp1, ppcmPowp0 * ppcmPowp1)
        LP_powpList.insert(0,(q21, q22, q23))
        LP_powpList.insert(0,(q11, q12, q13))
        LP_powpList.insert(0, (q01, q02, q03))

    print("Denppcm=", LP_den_ppcm, " Powp: ", LP_powpList)
    if 1:
#   print("Denppcm=",LP_den_ppcm," Powp: ",[getPowp(Pp) for Pp in LP_powpList])
#       while nextLevelState():
        (p0, powp0, ppcmPowp0) = LP_powpList.pop(0)
        (p1, powp1, ppcmPowp1) = LP_powpList.pop(0)
        LP2_powpList = []
        LP2_powpList.append((p0, powp0, ppcmPowp0))
#        LP2_powpList.append((p1, powp1, ppcmPowp1))
        print("Before Compute")
        hist2 = ComputeHisto(LP2_powpList)
#        print(hist2)
        print("After Compute")
        exit(0)

    histo0={}
    histo0[1]=1
    histo1={}
    explain1 = {}
    minSum0 = 1
    maxSum0 = 1
    mode=0
    count0=[]
    offsetS0=0
    while nextLevelState():
        clk = clock() ; print("{:.3f}s ".format(clk),end='')
        compute_level(LS_Elem,LS_Constraint)
        clk = clock() ; print("Compute_level {:.3f}s ".format(clk))
        factS = LS_fact * LS_fact
        offsetS0 = minSum0
        sumMax = maxSum0
        sumMax = (sumMax * factS ) // LS_Constraint
        nbCountS1 = sumMax - offsetS0*factS // LS_Constraint + LV_maxSum + 1
        if nbCountS1-1 > sumMax:
            nbCountS1 =  sumMax + 1
        offsetS1 = sumMax - (nbCountS1-1)
        clk = clock() ;
        print("{:.3f}s ".format(clk),end='')
        print("Level=", LS_numLevel, "Min=",minSum0, "Max=",maxSum0," Elem=[", LS_Elem[0],"...",LS_Elem[-1],end='')
        print("] ppcm=", LS_ppcm, " fact=", LS_fact,"ExpOut",nbCountS1,"Hin=",len(histo0),end='')
        if nbCountS1 < 2 * len(histo0) -10:
            print("Swap to mode OUT_COUNT",end='')
            mode=1
            break
        minSum0 = LS_ppcm * LS_ppcm
        maxSum0 = 0
        nout=0
        print("h=")
        for sum in histo0:
            count = histo0[sum]
            sum *= factS
            intSum = sum // LS_Constraint
            modSum = sum - intSum * LS_Constraint
            print((modSum,intSum),end='')
            for intLV in LV_index[modSum]:
                if intSum < intLV:
                    break
                nout +=1 ;
                newSum = intSum - intLV
                if newSum > maxSum0:
                   maxSum0 = newSum
                elif newSum < minSum0:
                    minSum0 = newSum
                if newSum in histo1:
                    histo1[newSum] += count
                else:
                    histo1[newSum] = count
            if nout > nbCountS1:
                mode=1
                break
        if mode == 0:
#            print("h="); print(histo1)
            histo0.clear()
            print("=>LenH=",nout,"/",len(histo1))
            (histo0,histo1)=(histo1,histo0)
        else:
            print("*** => OUNT_COUNT ***",end='')
            break
    if mode == 1:
        count1 = [0]*nbCountS1
        nout =0
        for sum in histo0:
            count = histo0[sum]
            sum *= factS
            intSum = sum // LS_Constraint
            modSum = sum - intSum * LS_Constraint
            for intLV in LV_index[modSum]:
                if intSum < intLV:
                    break
                nout += 1
                newSum = intSum - intLV
                count1[newSum-offsetS1] += count
        histo0.clear()
        (count0,count1)=(count1,count0)
        offsetS0=offsetS1
        print("=>LenH=", nout, "/", len(count0))
    LP_powpList.sort(reverse=True,key=getPowp)
    while nextLevelState():
        compute_level(LS_Elem, LS_Constraint)
        #        Print_LV()
        factS = LS_fact * LS_fact
        sumMax = (sumMax * factS ) // LS_Constraint
        nbCountS1 = sumMax - offsetS0*factS // LS_Constraint + LV_maxSum + 1
        if nbCountS1-1 > sumMax:
            nbCountS1 =  sumMax + 1
        offsetS1 = sumMax - (nbCountS1-1)
        clk = clock() ;
        print("{:.3f}s ".format(clk),end='')
        print("Level=", LS_numLevel, " Elem=[", LS_Elem[0],"...",LS_Elem[-1],end='')
        print("] ppcm=", LS_ppcm, " fact=", LS_fact,"ExpOut",nbCountS1,"Hin=",len(count0),end='')
        count1 = [0]*nbCountS1
        nout = 0
        for ih in range(0,len(count0)):
            sum = ih + offsetS0
            count = count0[ih]
            if count==0:
                continue
            sum *= factS
            intSum = sum // LS_Constraint
            modSum = sum - intSum * LS_Constraint
            for intLV in LV_index[modSum]:
                if intSum < intLV:
                    break
                nout += 1
                newSum = intSum - intLV
                count1[newSum-offsetS1] += count
        count0=[]
        (count0,count1)=(count1,count0)
        offsetS0=offsetS1
        print("=>LenH=",nout,"/",len(count0))


    if mode==0:
        print("histo0",histo0[minSum0])
    else:
        print("Count0",count0[0])
main()
