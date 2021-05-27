# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import pandas as pd

from PySide2.QtWidgets import *
from analysis_script.yield_point import *
from analysis_script.skeleton import skeleton

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as mplot
from mywidgets import MyQGroupBox,MyQWidget


class MyFigureCanvas(FigureCanvas): 
    def __init__(self,x,y,title):
        fig = Figure()  
        FigureCanvas.__init__(self, fig)
        self.axes = fig.add_subplot(111) 
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
            self.axes.set_ylabel('Force(kN/mm)')
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
        bottom_widget=central_widget_of_mainwindow.add_my_qwidget("Bottom","Vertical")
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
        self.plot_arg=[[1,2,3,4,5],[1,2,3,4,5],""]
        self.display_window=MyFigureCanvas(*self.plot_arg)
        right_mainview_widge.add_any_qwidget(self.display_window)
        plot_button=right_mainview_widge.add_pushbuttons('Replot')
        plot_button.setFixedWidth(100)

        #bottom
        bottom_widget.add_textedits('Messagebox').setReadOnly(True)

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
        analysis_buttons['Energy dissipation accumulation'].clicked.connect(self.test_button)
        # analysis_buttons['Energy dissipation accumulation'].clicked.connect(self.energy_dissipation_accumulation_analysis)

        ##
        plot_button.clicked.connect(self.replot)

        

    def replot(self):
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
        else:
            QMessageBox.warning(self,"Error",'Please select xslx path')
        

    def hysteresis_curve(self):
        self.plot_arg=[self.hysteresis_data.iloc[:,0],self.hysteresis_data[:,1],"Hysteresis"]
        self.display_window.redraw(*self.plot_arg)
        pass

    def skeleton_curve(self):
        self.skeleton_data=skeleton(self.hysteresis_data)
        self.plot_arg=[self.skeleton_data.iloc[:,0],self.skeleton_data[:,1],"Skeleton"]
        self.display_window.redraw(*self.plot_arg)
        pass

    def yield_point_analysis(self):
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
        self.plot_arg=[self.skeleton_data.iloc[:,0],self.skeleton_data[:,1],"Skeleton"]
        self.display_window.redraw_vline(*self.plot_arg,vline=yield_point)
        
    def ductility_factor_analysis(self):
        pass

    def stiffness_analysis(self):
        pass

    def energy_dissipation_per_round_analysis(self):
        pass

    def energy_dissipation_accumulation_analysis(self):
        pass

    def test_button(self):
        self.display_window.redraw(*self.plot_arg,vline=(2,2))


        

if __name__ == "__main__":
    app = QApplication([])
    widget = Seismic()
    widget.show()
    sys.exit(app.exec_())
