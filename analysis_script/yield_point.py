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
from pandas.core.base import DataError
import scipy.integrate
from scipy.misc import derivative
from analysis_script.usrdefine import findclosest

# denoise section
def area(skeleton_data:pd.DataFrame):
    positive_disp_data=skeleton_data[skeleton_data.iloc[:,0]>0]
    D=positive_disp_data.iloc[:,0].reset_index(drop=True)
    F=positive_disp_data.iloc[:,1].reset_index(drop=True)
    index_max_point=F.idxmax()
    poly=np.polyfit(D.values[0:index_max_point],F.values[0:index_max_point],5)
    
    p = np.poly1d(poly)
    res,d = scipy.integrate.quad(p,0,D.iat[index_max_point])

    # yield selection
    yieldinte = []
    yieldd=[]
    for i in np.linspace(0,F.max(),5000):
        inte = (D.iat[index_max_point]-i)*F.max()+i*F.max()/2
        yieldinte.append(inte)
        yieldd.append(i)
    chazhi = [abs(m-res) for m in yieldinte]
    dindex = chazhi.index(min(chazhi))
    return yieldd[dindex],p(yieldd[dindex])


def equavalent_elasto_plastic(skeleton_data:pd.DataFrame):
    positive_disp_data=skeleton_data[skeleton_data.iloc[:,0]>0]
    D=positive_disp_data.iloc[:,0].reset_index(drop=True)
    F=positive_disp_data.iloc[:,1].reset_index(drop=True)
    index_max_point=F.idxmax()
    poly=np.polyfit(D.values[0:index_max_point],F.values[0:index_max_point],5)
    
    p = np.poly1d(poly)   #use 5 poly to moniter gujiaxian 
    
    p0 = derivative(p,0)  #get the derivative on 0 point 
    
    g_d = np.linspace(0,D.iat[index_max_point],100)
    g_f = g_d*p0     
    yi_d = g_d[findclosest(g_f,F.max())]
    yi_f = F[findclosest(D.values,yi_d)]
    return yi_d,yi_f



def r_park(skeleton_data:pd.DataFrame):
    positive_disp_data=skeleton_data[skeleton_data.iloc[:,0]>0]
    D=positive_disp_data.iloc[:,0].reset_index(drop=True)
    F=positive_disp_data.iloc[:,1].reset_index(drop=True)
    index_max_point=F.idxmax()
    poly=np.polyfit(D.values[0:index_max_point],F.values[0:index_max_point],5)
    p = np.poly1d(poly)   #use 5 poly to moniter skeleton
    k = 0.75*F.max()/D.iat[findclosest(F.values,0.75*F.max())] #get the k of gexian
    g_d = np.linspace(0,D.iat[index_max_point],100)
    g_f = g_d*k #get the plot of gexian
    
    yi_d = g_d[findclosest(g_f,F.max())]
    yi_f = p(yi_d)
    
    return yi_d,yi_f

def geometry(skeleton_data:pd.DataFrame):
    positive_disp_data=skeleton_data[skeleton_data.iloc[:,0]>0]
    D=positive_disp_data.iloc[:,0].reset_index(drop=True)
    F=positive_disp_data.iloc[:,1].reset_index(drop=True)
    index_max_point=F.idxmax()
    poly=np.polyfit(D.values[0:index_max_point],F.values[0:index_max_point],5)
    
    p = np.poly1d(poly)   #use 5 poly to moniter skeleton
    
    p0 = derivative(p,0)  #get the derivative at original point 
    
    g_d = np.linspace(0,D.iat[index_max_point],100)
    g_f = g_d*p0     
    mid_d = g_d[findclosest(g_f,F.max())]
    mid_f = F[findclosest(D.values,mid_d)]
    k = mid_f/mid_d
    la_d = np.linspace(0,D.iat[index_max_point],100)
    la_f = la_d*k
    yi_d = la_d[findclosest(la_f,F.max())]
    yi_f = p(yi_d)
    return yi_d,yi_f