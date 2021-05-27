"""
lots of general functin used in indexAnalysis
area_loop: calculate the area of hysteresis loops
area_trangle: calculate the area of imaginal trangle 
polyfit: fit loops with multinominals 
puple_sort_combine: sort two list with buble sort for the former
"""
import scipy.integrate
import numpy as np 
import pandas as pd 



def area_loop(D,F):
    sy=[F.index(max(F)),F.index(min(F))]
    sy.sort()
    line1=(D[sy[0]:sy[1]],F[sy[0]:sy[1]])
    D[sy[0]:sy[1]]=[]
    F[sy[0]:sy[1]]=[]
    D,F=puple_sort_combine(D,F)
    line2=(D,F)
    p1,p2=polyfit(*line1),polyfit(*line2)
    p=p1-p2
    return abs(scipy.integrate.quad(p,D[F.index(min(F))],D[F.index(max(F))])[0])    

def area_trangle(D,F):
    dr,fup,dl,flow=max(D),max(F),min(D),min(F)
    return (dr*fup+dl*flow)/2


def polyfit(displacment,force):
    coeffcient=np.polyfit(displacment,force,5)
    return np.poly1d(coeffcient)

def puple_sort_combine(a:list,b:list):
    if len(a)==len(b):
        for i in range(len(a)-1):
            for j in range(len(a)-1-i):
                if a[j]>a[j+1]:
                    a[j],a[j+1]=a[j+1],a[j]
                    b[j],b[j+1]=b[j+1],b[j]
        return a,b
    else:
        print('Same dimensions required')


def findclosest(array,goal):
    try:
        gap_abs=[abs(goal-i) for i in array]
        index=gap_abs.index(min(gap_abs))
        value=array[index]
        return index
    except:
        raise TypeError("Wrong type for Inputs")


