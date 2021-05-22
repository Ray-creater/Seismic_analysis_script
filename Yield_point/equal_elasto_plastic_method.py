# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 12:58:47 2020

@author: Ray
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import derivative
from usrdefine import eqindex


rpath='/home/ray/Desktop/实验/数据/780mm-强轴-轴压比0.1(ok)1/baoluo.xlsx'
d = pd.read_excel(rpath)
array = np.array(d.iloc[:,1:3])
D=[]    
F=[]
for a in array:
    if a[0]>0:
        D.append(a[0])
        F.append(a[1])    #input D and F from excel

poly = np.polyfit(D[0:F.index(max(F))],F[0:F.index(max(F))],5)
p = np.poly1d(poly)   #use 5 poly to moniter gujiaxian 

p0 = derivative(p,0)  #get the derivative on 0 point 

g_d = np.linspace(0,D[F.index(max(F))],100)
g_f = g_d*p0     
yi_d = g_d[eqindex(g_f,max(F))]
yi_f = F[eqindex(D,yi_d)]

print("yield d",yi_d)
print('yield f',yi_f)
print('u f:',max(F))
print('u d:',D[F.index(max(F))])

plt.plot(D,F)
plt.plot(g_d,g_f)
plt.show()
