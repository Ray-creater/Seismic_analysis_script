# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 11:10:03 2020

@author: Ray
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import derivative
from usrdefine import eqindex


rpath=r'C:\Users\Ray\Desktop\实验\数据\780mm-强轴-轴压比0.1(ok)\baoluo.xlsx'
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
mid_d = g_d[eqindex(g_f,max(F))]
mid_f = F[eqindex(D,mid_d)]
k = mid_f/mid_d
la_d = np.linspace(0,D[F.index(max(F))],100)
la_f = la_d*k
yi_d = la_d[eqindex(la_f,max(F))]
yi_f = p(yi_d)

print("yield d",yi_d)
print('yield f',yi_f)




plt.plot(la_d,la_f)
plt.plot(g_d,g_f)
plt.plot(D,F)
plt.show()