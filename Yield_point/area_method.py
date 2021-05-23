# -*- coding: utf-8 -*-
"""
Using equal area method to find the yield point
Input: xlsx with two columns: displacement and force
return: yield displacement and yield force
Using 5-th polynominals to fit the skeleton
Created on Tue Mar 10 19:27:13 2020

@author: Ray
"""
import pandas as pd
import numpy as np
import scipy.integrate

# denoise section
def equal_area(pathofxlsx:str):
    pathofxlsx=r'C:\Users\Ray\Desktop\实验\数据\780mm-强轴-轴压比0.1(ok)\baoluo.xlsx'
    d = pd.read_excel(rpath)
    array = d.iloc[:,1:3]
    positive_disp_array=array[array[0]>0]
    D=positive_disp_array.iloc[:,0]
    F=positive_disp_array.iloc[:,1]
    index_max_point=F.idxmax()
    poly=np.polyfit(*[positive_disp_array.iloc[0:index_max_point,i] for i in range(2)],5)
    
    poly = np.polyfit(D[0:index_max_point],F[0:index_max_point],5)
    p = np.poly1d(poly)
    res,d = scipy.integrate.quad(p,0,D[index_max_point])

    # yield selection
    yieldinte = []
    yieldd=[]
    for i in np.linspace(0,F.max(),5000):
        inte = (D[index_max_point]-i)*max(F)+i*max(F)/2
        yieldinte.append(inte)
        yieldd.append(i)
    chazhi = [abs(m-res) for m in yieldinte]
    dindex = chazhi.index(min(chazhi))
    return yieldd[dindex],p(yieldd[dindex])

