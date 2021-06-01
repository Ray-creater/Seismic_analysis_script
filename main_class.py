# phis Python file uses the following encoding: utf-8
from itertools import accumulate
import os
from pathlib import Path
import sys
import pandas as pd

from PySide2.QtWidgets import *
from analysis_script.yield_point import *
from analysis_script.skeleton import skeleton
from analysis_script.usrdefine import *
from analysis_script.energy import *

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as mplot
from mywidgets import MyQGroupBox,MyQWidget


class MyFigureCanvas(FigureCanvas): 
    def __init__(self,x,y,title):
        self.fig = Figure()  
        FigureCanvas.__init__(self, self.fig)
        self.axes = self.fig.add_subplot(111) 
        self.axes.plot(x,y)
        self.axes.set_title(title)
        if title=="Energy":
            self.axes.set_ylabel('Energy(J)')
        elif title=="Stiffness":
            self.axes.set_ylabel('Stiffness(kN/mm)')
        else:
            self.axes.set_ylabel('Force(kN/mm)')
        self.axes.set_xlabel('Disp(mm)')
        self.axes.grid()
        self.draw()

    def redraw(self,x,y,title,vline=()):
        self.axes.clear()
        self.axes.plot(x,y)
        if vline:
            self.axes.vlines(vline[0],0,vline[1],color='red')
        self.axes.set_title(title)
        if title=="Energy":
            self.axes.set_ylabel('Energy(J)')
        elif title=="Stiffness":
            self.axes.set_ylabel('Stiffness(kN/mm)')
        else:
            self.axes.set_ylabel('Force(kN/mm)')
        self.axes.set_xlabel('Disp(mm)')
        self.axes.grid()
        self.draw()

    def redraw_vline(self,x,y,title,vline:tuple):
        self.axes.clear()
        self.axes.plot(x,y)
        self.axes.vlines(vline[0],0,vline[1],color='red')
        self.axes.set_title(title)
        if title=="Energy":
            self.axes.set_ylabel('Energy(J)')
        elif title=="Stiffness":
            self.axes.set_ylabel('Stiffness(kN/mm)')
        else:
            self.axes.set_ylabel('Force(kN)')
        self.axes.set_xlabel('Disp(mm)')
        self.axes.grid()
        self.draw()

class Seismic(QMainWindow):
    def __init__(self):
        super(Seismic, self).__init__()
        central_widget_of_mainwindow=MyQWidget("Vertical")
        self.setCentralWidget(central_widget_of_mainwindow)

        #Three_main_mywidget
        top_widget=central_widget_of_mainwindow.add_my_qwidget("Top","Horizontal")
        middle_widget=central_widget_of_mainwindow.add_my_qwidget("Middle","Horizontal")
        bottom_widget=central_widget_of_mainwindow.add_my_qwidget("Bottom","Horizontal")

        central_widget_of_mainwindow.setStretchFactor(top_widget,middle_widget,bottom_widget,scale=(1,8,1))

        #top
        top_widget.add_pushbuttons('Button1',"Button2")

        #middle
        left_option_widget=middle_widget.add_my_qwidget("Option","Vertical")
        right_mainview_widge=middle_widget.add_my_qwidget("Mainview","Vertical")
        middle_widget.setStretchFactor(left_option_widget,right_mainview_widge,scale=(1,9))

        right_option_widget=middle_widget.add_my_qwidget("View","Vertical")
        ## left option widget
        path_groupbox=left_option_widget.add_my_qgroupbox("Path",'Vertical')
        curve_groupbox=left_option_widget.add_my_qgroupbox("Curve",'Vertical')
        analysis_groupbox=left_option_widget.add_my_qgroupbox("Analysis",'Vertical')
        left_option_widget.setStretchFactor(path_groupbox,curve_groupbox,analysis_groupbox,scale=(1,1,2))
        ### path groupbox setting
        path_groupbox.add_labels('Xlsx select').setFixedHeight(25)
        self.path_textedit=path_groupbox.add_textedits('Select path');self.path_textedit.setFixedHeight(30);self.path_textedit.setReadOnly(True)
        path_buttons=path_groupbox.add_pushbuttons("Select",'Comfirm')

        ### curve groupbox setting 
        curve_buttons=curve_groupbox.add_pushbuttons("Hysteresis","Skeleton")
        ### Analysis groupbox setting 
        radiobuttons_myqwidget=analysis_groupbox.add_my_qwidget("Horizontal")
        self.radiobuttons=radiobuttons_myqwidget.add_radiobuttons("R-park","Area","Geometry")
        self.radiobuttons["R-park"].setChecked(True)

        analysis_buttons=analysis_groupbox.add_pushbuttons("Yield point",
            "Ductility factor",
            "Stiffness",
            "Energy dissipation per round",
            "Energy dissipation accumulation") 
        analysis_widgets=[i for i in analysis_buttons.values()]
        analysis_widgets.append(radiobuttons_myqwidget)
        analysis_scale=[4 for _ in analysis_widgets]
        analysis_scale[-1]=1
        analysis_groupbox.setStretchFactor(*analysis_widgets,scale=analysis_scale)

        ## Main display window
        self.plot_arg=[[1,2,3,4,5],[1,2,3,4,5],""]
        self.display_window=MyFigureCanvas(*self.plot_arg)
        right_mainview_widge.add_any_qwidget(self.display_window)
        plot_button=right_mainview_widge.add_pushbuttons('Output pic')
        plot_button.setFixedWidth(100)

        

        #bottom
        yield_point_qgroupbox=bottom_widget.add_my_qgroupbox('Yield point','Verticle')
        ductility_qgroupbox=bottom_widget.add_my_qgroupbox('Ductility','Verticle')
        ##
        yield_disp_qwidget=yield_point_qgroupbox.add_my_qwidget('Horizontal')
        yield_force_qwidget=yield_point_qgroupbox.add_my_qwidget("Horizontal")
        yield_disp_qwidget.add_labels("Yield disp:")
        self.yield_disp_textedit=yield_disp_qwidget.add_textedits("Yield disp value")
        self.yield_disp_textedit.setFixedHeight(20)
        yield_force_qwidget.add_labels("Yield force:")
        self.yield_force_textedit=yield_force_qwidget.add_textedits('Yield force value')
        self.yield_force_textedit.setFixedHeight(20)
        ##
        ductility_qgroupbox.add_labels('Ductility factor:')
        self.ductility_textedit=ductility_qgroupbox.add_textedits("Ductility factor value")
        self.ductility_textedit.setFixedHeight(20)


        #button function
        ##path_button
        path_buttons['Select'].clicked.connect(self.select_xlsx_path)
        path_buttons['Comfirm'].clicked.connect(self.comfirm_path)
        ##cuve_buttons
        curve_buttons['Hysteresis'].clicked.connect(self.hysteresis_curve)
        curve_buttons['Skeleton'].clicked.connect(self.skeleton_curve)
        ##analysis_buttons
        analysis_buttons['Yield point'].clicked.connect(self.yield_point_analysis)
        analysis_buttons['Ductility factor'].clicked.connect(self.ductility_factor_analysis)
        analysis_buttons['Stiffness'].clicked.connect(self.stiffness_analysis)
        analysis_buttons['Energy dissipation per round'].clicked.connect(self.energy_dissipation_per_round_analysis)
        # analysis_buttons['Energy dissipation accumulation'].clicked.connect(self.test_button)
        analysis_buttons['Energy dissipation accumulation'].clicked.connect(self.energy_dissipation_accumulation_analysis)

        ##
        plot_button.clicked.connect(self.output_pic)

        

    def output_pic(self):
        save_path,_=QFileDialog.getSaveFileName(self)
        if _:
            self.display_window.fig.savefig(save_path)
        else:
            print("No path choose")
            
        self.display_window.redraw(*self.plot_arg)


    def select_xlsx_path(self):
        xlsx_path,_=QFileDialog.getOpenFileName(self)
        if _:
            self.path_textedit.setText(xlsx_path)
        else:
            print("No path choose")

    #readdata
    def comfirm_path(self):
        xlsx_path=self.path_textedit.toPlainText()
        if xlsx_path!="Select path":
            self.hysteresis_data=pd.read_excel(xlsx_path)
            print("Read success")
            print("Hysteresis data: ")
            print(self.hysteresis_data)
        else:
            QMessageBox.warning(self,"Error",'Please select xslx path')
        
    def hysteresis_curve(self):
        if hasattr(self,'hysteresis_data'):
            self.comfirm_path()
        self.plot_arg=[self.hysteresis_data.iloc[:,0],self.hysteresis_data.iloc[:,1],"Hysteresis"]
        self.display_window.redraw(*self.plot_arg)
       
    def skeleton_curve(self):
        if not hasattr(self,'hysteresis_data'):
            self.comfirm_path()
        self.skeleton_data=skeleton(self.hysteresis_data)
        self.plot_arg=[self.skeleton_data.iloc[:,0],self.skeleton_data.iloc[:,1],"Skeleton"]
        self.display_window.redraw(*self.plot_arg)

    def yield_point_analysis(self):
        if not hasattr(self,'hysteresis_data'):
            self.comfirm_path()
        self.skeleton_data=skeleton(self.hysteresis_data)
        for i,j in self.radiobuttons.items():
            if j.isChecked():
                method_chosen=i
        if method_chosen=="R-park":
            yield_point=r_park(self.skeleton_data)
        elif method_chosen=="Area":
            yield_point=area(self.skeleton_data)
        elif method_chosen=="Geometry":
            yield_point=geometry(self.skeleton_data)
        self.plot_arg=[self.skeleton_data.iloc[:,0],self.skeleton_data.iloc[:,1],"Skeleton"]
        self.display_window.redraw_vline(*self.plot_arg,vline=yield_point)
        
        self.yield_disp_textedit.setText(str(yield_point[0]))
        self.yield_force_textedit.setText(str(yield_point[1]))
        
            
        
    def ductility_factor_analysis(self):
        if not hasattr(self,'hysteresis_data'):
            self.comfirm_path()
        self.skeleton_data=skeleton(self.hysteresis_data)
        force_list=self.skeleton_data.iloc[:,1]
        peak_force=force_list.max()
        peak_index=findclosest(force_list.values,peak_force)
        peak_disp=self.skeleton_data.iat[peak_index,0]
        force_list=force_list.iloc[::-1]  ##to do  check the effect of reversed class
        failure_index=findclosest(force_list.values,peak_force*0.85)
        failure_disp_est=self.skeleton_data.iat[failure_index,0]
        if failure_disp_est>peak_disp:
            failure_disp=failure_disp_est
        else:
            print("No decrease to 0.85, max disp chosen")
            failure_disp=self.skeleton_data.iloc[:,0].max()

        for i,j in self.radiobuttons.items():
            if j.isChecked():
                method_chosen=i
        if method_chosen=="R-park":
            yield_point=r_park(self.skeleton_data)
        elif method_chosen=="Area":
            yield_point=area(self.skeleton_data)
        elif method_chosen=="Geometry":
            yield_point=geometry(self.skeleton_data)
        yield_disp=yield_point[0]
        ductility_factor=failure_disp/yield_disp
        self.ductility_textedit.setText(str(ductility_factor))
        return ductility_factor

    def stiffness_analysis(self):
        if not hasattr(self,'hysteresis_data'):
            self.comfirm_path()
        self.skeleton_data=skeleton(self.hysteresis_data)
        disp=self.skeleton_data.iloc[:,0]
        stiffness=[i[1].iat[1]/i[1].iat[0] for i in self.skeleton_data.iterrows() ]
        self.plot_arg=[disp,stiffness,"Stiffness"]
        self.display_window.redraw(*self.plot_arg)

    def energy_dissipation_per_round_analysis(self):
        if not hasattr(self,'hysteresis_data'):
            self.comfirm_path()
        self.energy=energy_disspation(self.hysteresis_data)
        self.plot_arg=[self.energy[0],self.energy[1],"Energy"]
        self.display_window.redraw(*self.plot_arg)
        
            
    def energy_dissipation_accumulation_analysis(self):
        if not hasattr(self,'energy'):
            self.energy=energy_disspation(self.hysteresis_data)
        self.plot_arg=[self.energy[0],self.energy[2],"Energy"]
        self.display_window.redraw(*self.plot_arg)
            




if __name__ == "__main__":
    app = QApplication([])
    widget = Seismic()
    widget.show()
    sys.exit(app.exec_())
