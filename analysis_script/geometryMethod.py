# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 11:10:03 2020

@author: Ray
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import derivative
from analysis_script.usrdefine import findclosest

def geometry(skeleton_data:pd.DataFrame):
    array=skeleton_data
    positive_disp_array=array[array[0]>0]
    D=positive_disp_array.iloc[:,0]
    F=positive_disp_array.iloc[:,1]
    index_max_point=F.idxmax()
    poly=np.polyfit(*[positive_disp_array.iloc[0:index_max_point,i] for i in range(2)],5)
    poly = np.polyfit(D[0:index_max_point],F[0:index_max_point],5)
    
    p = np.poly1d(poly)   #use 5 poly to moniter skeleton
    
    p0 = derivative(p,0)  #get the derivative at original point 
    
    g_d = np.linspace(0,D[index_max_point],100)
    g_f = g_d*p0     
    mid_d = g_d[findclosest(g_f,max(F))]
    mid_f = F[findclosest(D,mid_d)]
    k = mid_f/mid_d
    la_d = np.linspace(0,D[index_max_point],100)
    la_f = la_d*k
    yi_d = la_d[findclosest(la_f,max(F))]
    yi_f = p(yi_d)
    return yi_d,yi_f

