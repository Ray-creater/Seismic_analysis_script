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
        central_widget_of_mainwindow=QWidget()
        self.setCentralWidget(central_widget_of_mainwindow)
        main_layout=QVBoxLayout(central_widget_of_mainwindow)

        # top location for buttons 
        top_button_widget=QWidget()
        top_button_layout=QHBoxLayout(top_button_widget)
        button_name_list=["Button"+str(i) for i in range(3)]
        button_list=[QToolButton(text=i) for i in button_name_list]
        [top_button_layout.addWidget(j) for i,j in enumerate(button_list)]

        # middle location for mianview
        middle_window_widget=QWidget()
        middle_window_layout=QHBoxLayout(middle_window_widget)
        middle_select_buttons_widget=QWidget()
        middle_select_buttons_layout=QVBoxLayout(middle_select_buttons_widget)
        middle_main_display_widget=QWidget()
        middle_main_display_layout=QVBoxLayout(middle_main_display_widget)
        middle_window_layout.addWidget(middle_select_buttons_widget)
        middle_window_layout.addWidget(middle_main_display_widget)
        middle_window_layout.setStretchFactor(middle_select_buttons_widget,1)
        middle_window_layout.setStretchFactor(middle_main_display_widget,9)
        ## middle select button widget
        ###path button
        path_box=QGroupBox("Path")
        path_box_layout=QVBoxLayout(path_box)
        middle_select_buttons_layout.addWidget(path_box)
        path_label=QLabel(".xlsx path:")
        path_label.setFixedHeight(30)
        self.path_edit=QTextEdit();self.path_edit.setReadOnly(True)
        self.path_edit.setFixedHeight(30)
        path_select=QPushButton("select path")
        path_box_layout.addWidget(path_label)
        path_box_layout.addWidget(self.path_edit)
        path_box_layout.addWidget(path_select)
        ###Curve button
        curve_box=QGroupBox("Curve")
        curve_box_layout=QVBoxLayout(curve_box)
        middle_select_buttons_layout.addWidget(curve_box)
        curve_button_name_list=["Hysteresis","Skeleton"]
        curve_button_list=[QToolButton(text=i) for i in curve_button_name_list]
        [curve_box_layout.addWidget(i) for i in curve_button_list]
        ###Analysis button
        analysis_box=QGroupBox("Analysis")
        analysis_box_layout=QVBoxLayout(analysis_box)
        middle_select_buttons_layout.addWidget(analysis_box)
        analysis_button_name_list=["Ductility factor",
            "Stiffness",
            "Energy dissipation for every round",
            'Energy dissipation cumunlation']
        analysis_button_list=[QToolButton(text=i) for i in analysis_button_name_list]
        [analysis_box_layout.addWidget(i) for i in analysis_button_list]
        ##middle maindisplay widget
        x=[1,2,3,4,5];y=[1,2,3,4,5]
        title='Energy'
        self.display_window=MyFigureCanvas(x, y, title)
        display_plot_button=QPushButton("data output")
        middle_main_display_layout.addWidget(self.display_window)
        middle_main_display_layout.addWidget(display_plot_button)

        # bottom location for message
        bottom_message_widget=QTextEdit()
        bottom_message_widget.setReadOnly(True)

        # assemble widgets for locations
        main_layout.addWidget(top_button_widget)
        main_layout.setStretchFactor(top_button_widget,1)
        main_layout.addWidget(middle_window_widget)
        main_layout.setStretchFactor(middle_window_widget,8)
        main_layout.addWidget(bottom_message_widget)
        main_layout.setStretchFactor(bottom_message_widget,1)

        #button function 
        display_plot_button.clicked.connect(self.replot)


    def replot(self):
        x=[1,2,3,4,5];y=[5,4,3,2,1]
        title="Stiffness"
        self.display_window.redraw(x, y, title)
        



        


if __name__ == "__main__":
    app = QApplication([])
    widget = Seismic()
    widget.show()
    sys.exit(app.exec_())
