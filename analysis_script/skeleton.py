'''
Extract the skeleton from hysteresis curve 
'''
import pandas as pd 
import numpy as np 

def skeleton(hysteresis_data:pd.DataFrame):
    '''
    Extract the skeleton from hysteresis curve\n
    input para{pd.DataFrame}: hysteresis_data(0:disp, 1:force) \n
    ouput para{pd.DataFrame}: skeleton(0:disp, 1:force) 
    '''
    #read hysteresis curve
    hystere_curve=hysteresis_data
    #pre-define skeleton disp range and num
    skeleton_disp=np.linspace(min(hystere_curve.iloc[:,0]),max(hystere_curve.iloc[:,0]),300)
    skeleton_disp_select=[]
    skeleton_force_select=[]
    #obtain the force value for the every pre-difined disp reached first
    for i in skeleton_disp:
        for j,k in enumerate(hystere_curve.iloc[:,0]):
            if abs(i-k)<0.5:
                skeleton_disp_select.append(k)
                skeleton_force_select.append(hystere_curve.iloc[j,1])
                break
    
    #combine the obtained disp and force into skeleton:numpy.darray
    skeleton=pd.DataFrame({"d":skeleton_disp_select,'f':skeleton_force_select})
    return skeleton


