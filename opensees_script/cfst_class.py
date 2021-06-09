from typing import Iterable


import pandas as pd 
from opensees_script.opensees_running import *
import threading as th 
import multiprocess as mp

class CFST(object):
    
    def __init__(self,shape:str,geometry:Iterable[float],material_grade:Iterable[float],load:Iterable) -> None:
        super().__init__()

        #shape
        if shape not in ['Circle','Rect']:
            raise TypeError('Shape should be Circle or Rect')
        self.shape=shape
        self.length,self.height,self.width,self.thickness=tuple(geometry)
        self.concrete_grade,self.steel_grade=tuple(material_grade)
        self.disp_list=load[1]
        self.axial_load_ratio=load[0]


    def opensess_analysis_thread(self):
        # process=mp.Process(target=self.opensees_analysis)
        # process.start()
        thread=th.Thread(target=self.opensees_analysis)
        thread.start()

    def opensees_analysis(self):
        if self.shape=='Rect':
            RectCFSTSteel02(self.length,self.height,self.width,self.thickness,self.concrete_grade,self.shape,self.axial_load_ratio,self.disp_list)
        else:
            pass

    @staticmethod
    def data_extract():
        return extracdata()
        

    