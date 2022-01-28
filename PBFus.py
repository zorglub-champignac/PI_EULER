from __future__ import print_function
import sys
if sys.version_info >= (3,0):
    from time import process_time
    sysnew = 1
else:
    from time import clock
    sysnew = 0

'''
FusVal FusM(FusVal fv) {
    if(fv.num < 0) {
//        printf("M(%lld/(2**%lld))=%lld/2**%lld ",fv.num,fv.pow2D,-fv.num,fv.pow2D);
        return (FusVal) { -fv.num,fv.pow2D,fv.level};
    } else {
        FusVal fv1 = FusM((FusVal){fv.num-(1LL<<fv.pow2D),fv.pow2D,fv.level});
        FusVal fvAnsw ;
        if(fv1.pow2D > fv.pow2D) {
            fvAnsw.num = (fv.num << (fv1.pow2D-fv.pow2D)) - fv1.num;
            fvAnsw.pow2D = fv1.pow2D ;
        } else {
            fvAnsw.num = fv.num  - (fv1.num << (fv.pow2D-fv1.pow2D) );
            fvAnsw.pow2D = fv.pow2D ;
        }
        fvAnsw.level = fv.level+1 ;
        while(fvAnsw.pow2D && (fvAnsw.num & 1)==0) { fvAnsw.pow2D-- ; fvAnsw.num >>= 1 ; }
        fvAnsw = FusM(fvAnsw) ;
        fvAnsw.pow2D++ ;
        fvAnsw.level = fv.level+1;
        while(fvAnsw.pow2D && (fvAnsw.num & 1)==0) { fvAnsw.pow2D-- ; fvAnsw.num >>= 1 ; }
        for(int i=0;i<fvAnsw.level;i++)printf(".");
        printf("M(%lld/2^%lld)=%lld/2^%lld\n",fv.num,fv.pow2D,fvAnsw.num,fvAnsw.pow2D);
            return fvAnsw ;
    }
}
'''
FDict = {}
def FusM(num,powD,level):
    if level > 50:
        print("M(%x/2^%d)=exit" % (num, powD))
        exit(0)
    if num < 0:
        return (-num,powD,level)
    else:
        if (num,powD) in FDict:
            return (FDict[(num,powD)][0],FDict[(num,powD)][1],level)

        (num1,powD1,level1)=FusM(num- (1<<powD),powD,level)
        if powD1 > powD:
            numa = (num << (powD1-powD)) - num1
            powDa = powD1
        else:
            numa = num - (num1 << (powD-powD1))
            powDa = powD
        while powDa > 0 and (numa & 1)==0:
            powDa -= 1
            numa >>= 1
        (numa,powDa,levela) =FusM (numa,powDa,level+1)
        powDa += 1
        while powDa > 0 and (numa & 1)==0:
            powDa -= 1
            numa >>= 1
        for i in range(0, level):
            print(".", end='', sep='')
        print("M(%x/2^%d=%x/2^%d //M(%x/2^%d-1)=%x/2^%d" % (num,powD,numa,powDa,num, powD,num1,powD1))
        FDict[(num,powD)]=(numa,powDa)
        return (numa,powDa,levela)


FusM(3,0,0)