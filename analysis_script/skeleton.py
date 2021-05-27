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
    skeleton_disp=np.linspace(hystere_curve.iloc[:,0].min,hystere_curve.iloc[:,0].max,300)

    #obtain the force value for the every pre-difined disp reached first
    select_index=[]
    for i in skeleton_disp:
        for j,k in enumerate(hystere_curve.iloc[:,0]):
            if abs(i-k)<0.1:
                select_index.append(j)
                break
    skeleton_force=np.array([hystere_curve.iloc[i,1] for i in select_index])
    
    #combine the obtained disp and force into skeleton:numpy.darray
    skeleton=np.array([skeleton_disp,skeleton_force])
    skeleton=pd.DataFrame(skeleton)
    return skeleton


