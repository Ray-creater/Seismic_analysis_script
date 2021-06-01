"""
Energy dissipation calculation 

"""
from analysis_script.usrdefine import *
import pandas as pd 
import numpy as np 
import itertools

class Curve():
    def __init__(self,D,F):
        self.D=D
        self.F=F

    @classmethod
    def creat(cls,D,F):
        if len(D)==len(F):
            return cls(D,F)
        else:
            print('Same dimensions required for D and F')

    def __getitem__(self,item):
        cls=type(self)
        if isinstance(item,slice):
            return cls(self.D[item],self.F[item])
        if isinstance(item,int):
            return cls([self.D[item]],[self.F[item]])

    def split_to_loops(self):
        loops={}
        cut_index=[i for i in range(len(self.D)) if abs(self.D[i])<0.5]
        for j,i in enumerate(range(0,len(cut_index)-2,2)):
            loops[j]={"D":self.D[cut_index[i]:cut_index[i+2]],"F":self.F[cut_index[i]:cut_index[i+2]]}
        return loops

    def energy_loops(self):
        loops=self.split_to_loops()
        energy_real=[]
        energy_trangle=[]
        disp_list=[]
        for i in range(len(loops.keys())):
            energy,disp=area_loop(loops[i]["D"],loops[i]["F"])
            energy_real.append(energy)
            disp_list.append(disp)
            energy_trangle.append(area_trangle(loops[i]["D"],loops[i]["F"]))
        Eratio=[i/j for i,j in zip(energy_real,energy_trangle)]
        Esum=sum(energy_real)
        energy_accumulation=list(itertools.accumulate(energy_real))
        return disp_list,energy_real,energy_accumulation,Eratio,Esum

        


def energy_disspation(hysteresis_data:pd.DataFrame):
    curve=Curve(hysteresis_data.iloc[:,0].values,hysteresis_data.iloc[:,1].values)
    return curve.energy_loops()

    
