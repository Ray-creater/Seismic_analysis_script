import os, sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import numpy as np
from partial import *
 
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as mplot
 
class MyFigureCanvas(FigureCanvas): 
    def __init__(self,x,y):
        fig = Figure()  
        FigureCanvas.__init__(self, fig)
        self.axes = fig.add_subplot(111) 
        self.axes.plot(x,y)
        self.axes.set_title('Example matplotlib in PyQt5' )
        self.axes.set_xlabel('X(m)')
        self.axes.set_ylabel('Y(m)')
        self.axes.grid()
        self.draw()

    def redraw(self,x,y):
        self.axes.clear()
        self.axes.plot(x,y)
        self.axes.set_title('Example matplotlib in PyQt5' )
        self.axes.set_xlabel('X(m)')
        self.axes.set_ylabel('Y(m)')
        self.axes.grid()
        self.draw()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        self.plot=MyFigureCanvas([1,2,3,4],[1,23,4,2])
        self.buttonClose = QPushButton('Press to close this window')
        self.buttonClose.clicked.connect(self.close)
        self.plotbutton=QPushButton('Plot')
        x,y=([1,2,3,4],[1,23,4,2])
        self.plotbutton.clicked.connect(self.plot,x,y)
        layout = QVBoxLayout()
        layout.addWidget(self.plot)
        layout.addWidget(self.buttonClose)
        self.setLayout(layout)
        self.show()

    def plot(self,x,y):
        self.plot.redraw(x, y)



    
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    sys.exit(app.exec_())

