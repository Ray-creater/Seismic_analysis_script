# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide2.QtWidgets import *

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

    def redraw(self,x,y,title):
        self.axes.clear()
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
        left_option_widget.setStretchFactor(path_groupbox,curve_groupbox,analysis_groupbox,scale=(1,1,1))
        ### path groupbox setting
        path_groupbox.add_labels('Xlsx select').setFixedHeight(25)
        self.path_textedit=path_groupbox.add_textedits('Select path');self.path_textedit.setFixedHeight(25);self.path_textedit.setReadOnly(True)
        path_buttons=path_groupbox.add_pushbuttons("Select",'Confirm')

        ### curve groupbox setting 
        curve_buttons=curve_groupbox.add_pushbuttons("Hysteresis","Skeleton")
        ### Analysis groupbox setting 
        analysis_buttons=analysis_groupbox.add_pushbuttons("Yield point",
            "Ductility factor",
            "Stiffness",
            "Energy dissipation per round",
            "Energy dissipation cumcumulation") 
        x=[1,2,3,4,5];y=[1,2,3,4,5]
        title="Energy"
        self.display_window=MyFigureCanvas(x,y,title)
        right_mainview_widge.add_any_qwidget(self.display_window)
        plot_button=right_mainview_widge.add_pushbuttons('Replot')
        plot_button.setFixedWidth(100)

        #bottom
        bottom_widget.add_textedits('Messagebox').setReadOnly(True)

        #button function
        plot_button.clicked.connect(self.replot)
        path_buttons['Select'].clicked.connect(self.select_xlsx_path)

        

    def replot(self):
        x=[1,2,3,4,5];y=[5,4,3,2,1]
        title="Stiffness"
        self.display_window.redraw(x, y, title)


    def select_xlsx_path(self):
        xlsx_path,_=QFileDialog.getOpenFileName(self)
        if _:
            self.path_textedit.setText(xlsx_path)
        else:
            print("No path choose")
        

if __name__ == "__main__":
    app = QApplication([])
    widget = Seismic()
    widget.show()
    sys.exit(app.exec_())
