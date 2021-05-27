# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 12:58:47 2020

@author: Ray
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import derivative
from analysis_script.usrdefine import findclosest

def equavalent_elasto_plastic(skeleton_data:pd.DataFrame):
    array=skeleton_data
    positive_disp_array=array[array[0]>0]
    D=positive_disp_array.iloc[:,0]
    F=positive_disp_array.iloc[:,1]
    index_max_point=F.idxmax()
    poly=np.polyfit(*[positive_disp_array.iloc[0:index_max_point,i] for i in range(2)],5)
    poly = np.polyfit(D[0:index_max_point],F[0:index_max_point],5)
    
    p = np.poly1d(poly)   #use 5 poly to moniter gujiaxian 
    
    p0 = derivative(p,0)  #get the derivative on 0 point 
    
    g_d = np.linspace(0,D[index_max_point],100)
    g_f = g_d*p0     
    yi_d = g_d[findclosest(g_f,max(F))]
    yi_f = F[findclosest(D,yi_d)]
    return yi_d,yi_f
