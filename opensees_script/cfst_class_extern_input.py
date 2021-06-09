from typing import Iterable

import pandas as pd 
from opensees_script.opensees_running import *

class CFST_extern(object):
    
    def __init__(self,Shape:str,Geometry:Iterable[float],material_grade:Iterable[float],load:Iterable[Iterable[float],float]) -> None:
        super().__init__()

        #Shape
        if Shape not in ['Circle','Rect']:
            raise TypeError('Shape should be Circle or Rect')
        self.shape=Shape
        self.length,self.height,self.width,self.thickness=tuple(Geometry)
        self.concrete_grade,self.steel_grade=tuple(material_grade)
        self.disp_list=load[0]
        self.axial_load_ratio=load[1]

    def opensees_analysis(self):
        if self.shape=='Rect':
            RectCFSTSteel02(self.length,self.height,self.width,self.thickness,self.concrete_grade,self.Shape,self.axial_load_ratio,self.disp_list)
            self.numerical_disp,self.numerical_force=extracdata()
        else:
            pass
        return self.numerical_disp,self.numerical_force
        

    