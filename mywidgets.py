from multiprocessing import pool
from typing import Iterable
from PySide2 import QtCore
from PySide2.QtGui import QCursor, QTextCursor
from PySide2.QtWidgets import *
from PySide2.QtCore import *

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import subprocess
import multiprocessing as mp
import threading as th
import sys



class MyQGroupBox(QGroupBox):

    def __init__(self,name,layout):
        super(MyQGroupBox, self).__init__(name)
        if layout=="Horizontal":
            self.layout=QHBoxLayout(self)
        elif layout=="Grid":
            self.layout=QGridLayout(self)
        elif layout=="Form":
            self.layout=QFormLayout(self)
        else: 
            self.layout=QVBoxLayout(self)

        self.my_qgroupbox={}
       
    def add_my_qwidget(self,layout="Vertical"):
        my_qwidget=MyQWidget(layout)
        self.layout.addWidget(my_qwidget)
        return my_qwidget


    def add_textedits(self,*name:str):
        if len(name)==1:
            textedits=QTextEdit(name[0])
            self.layout.addWidget(textedits)
        else:
            textedits={}
            for i in name:
                textedits[i]=QTextEdit(i)
                self.layout.addWidget(textedits[i])
        return textedits

    def add_labels(self,*name:str):
        if len(name)==1:
            labels=QLabel(text=name[0])
            self.layout.addWidget(labels)
        else:
            labels={}
            for i in name:
                labels[i]=QLabel(i)
                self.layout.addWidget(labels[i])
        return labels

    def add_pushbuttons(self,*name:str):
        if len(name)==1:
            pushbuttons=QPushButton(name[0])
            self.layout.addWidget(pushbuttons)
        else:
            pushbuttons={}
            for i in name:
                pushbuttons[i]=QPushButton(i)
                self.layout.addWidget(pushbuttons[i])
        return pushbuttons

    def add_radiobuttons(self,*name:str):
        if len(name)==1:
            radiobuttons=QRadioButton(name[0])
            self.layout.addWidget(radiobuttons)
        else:
            radiobuttons={}
            for i in name:
                radiobuttons[i]=QRadioButton(i)
                self.layout.addWidget(radiobuttons[i])
        return radiobuttons

    ## todo    
    ## this shallow copy may cause error 
    ## line 72 and 73
    def add_my_qgroupbox(self,name,layout):
        """
        especially for qwidget
        return created my_qwidget
        """
        new_my_qgroupbox=MyQGroupBox(layout) 
        self.my_qgroupbox[name]=new_my_qgroupbox
        self.layout.addWidget(self.my_qgroupbox[name])
        return new_my_qgroupbox

    def setStretchFactor(self,*widget:QWidget,scale:list)->None:
        for i,j in zip(widget,scale):
            self.layout.setStretchFactor(i,j)

    def add_widgets_formlayout(self,pair_widget:Iterable[Iterable]):
        if not isinstance(self.layout,QFormLayout):
            raise TypeError("Layout should be QFormlayout to use this function")
        else:
            for i in pair_widget:
                if len(i)!=2:
                    raise TypeError('Two widgets make up a pair to add at the same row')
            for i in range(len(pair_widget)):
                self.layout.addRow(pair_widget[i][0],pair_widget[i][1])
                # for j in range(2):
                #     # self.layout.addWidget(pair_widget[i][j],i+1,j)
                #     self.layout.addWidget(pair_widget[i][j])




class MyQWidget(QWidget):

    def __init__(self,layout):
        super(MyQWidget,self).__init__()
        if layout=="Horizontal":
            self.layout=QHBoxLayout(self)
        elif layout=="Grid":
            self.layout=QGridLayout(self)
        elif layout=="Form":
            self.layout=QFormLayout(self)
        else: 
            self.layout=QVBoxLayout(self)
        self.my_qwidgets={}
        self.my_qgroupbox={}

    ## todo    
    ## this shallow copy may cause error 
    ## line 72 and 73
    def add_my_qwidget(self,name,layout):
        """
        especially for qwidget
        return created my_qwidget
        """
        new_my_qwidgets=MyQWidget(layout) 
        self.my_qwidgets[name]=new_my_qwidgets
        self.layout.addWidget(self.my_qwidgets[name])
        return new_my_qwidgets

    
    def add_my_qgroupbox(self,name,layout)->MyQGroupBox:
        self.my_qgroupbox[name]=MyQGroupBox(name,layout)
        self.layout.addWidget(self.my_qgroupbox[name])
        return self.my_qgroupbox[name]

    def add_labels(self,*name:str):
        if len(name)==1:
            labels=QLabel(text=name[0])
            self.layout.addWidget(labels)
        else:
            labels={}
            for i in name:
                labels[i]=QLabel(i)
                self.layout.addWidget(labels[i])
        return labels


    def add_pushbuttons(self,*name):
        if len(name)==1:
            pushbuttons=QPushButton(name[0])
            self.layout.addWidget(pushbuttons)
        else:
            pushbuttons={}
            for i in name:
                pushbuttons[i]=QPushButton(i)
                self.layout.addWidget(pushbuttons[i])
        return pushbuttons

    def add_textedits(self,*name:str):
        if len(name)==1:
            textedits=QTextEdit(name[0])
            self.layout.addWidget(textedits)
        else:
            textedits={}
            for i in name:
                textedits[i]=QTextEdit(i)
                self.layout.addWidget(textedits[i])
        return textedits

    def add_radiobuttons(self,*name:str):
        if len(name)==1:
            radiobuttons=QRadioButton(name[0])
            self.layout.addWidget(radiobuttons)
        else:
            radiobuttons={}
            for i in name:
                radiobuttons[i]=QRadioButton(i)
                self.layout.addWidget(radiobuttons[i])
        return radiobuttons

    def add_any_qwidget(self,widget:QWidget)->None:
        self.layout.addWidget(widget)

    def add_widgets_formlayout(self,pair_widget:Iterable[Iterable]):
        if not isinstance(self.layout,QFormLayout):
            raise TypeError("Layout should be QFormlayout to use this function")
        else:
            for i in pair_widget:
                if len(i)!=2:
                    raise TypeError('Two widgets make up a pair to add at the same row')
            for i in range(len(pair_widget)):
                self.layout.addRow(pair_widget[i][0],pair_widget[i][1])

    def setStretchFactor(self,*widget:QWidget,scale:list)->None:
        for i,j in zip(widget,scale):
            self.layout.setStretchFactor(i,j)





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
            self.axes.set_ylabel('Force(kN)')
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



class CMDTextEdit(QTextEdit):

    output_str=QtCore.Signal(str)

    def __init__(self, text: str,parent: QWidget=None) -> None:
        super().__init__(text, parent=parent)
        self.setReadOnly(True)

    def receive_para(self,para_dict:dict):
        self.para_dict=para_dict

    def start_thread(self):
        thread=th.Thread(target=self.ouput)
        thread.start()


    def ouput(self):

        command="python ./opensees_script"

        for text in self.runcmd('ls'):
            self.output_str.emit(text+'\n')
            pass

    def runcmd(self,command:str):
        self.process=subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
        while True:
            line=self.process.stdout.readline().rstrip()
            if not line:
                yield "Process compelete"
                break
            yield str(line,encoding='utf-8')


    @Slot(str)
    def update(self,text:str):
        self.insertPlainText(text)
        self.moveCursor(QTextCursor.End)

    def kill_process(self):
        if hasattr(self,'process'):
            self.process.kill()
            self.insertPlainText('Process killed')

        else:
            self.insertPlainText('No process is running \n')


class CMDTextEditSelf(QTextEdit):


    def __init__(self, text: str,parent: QWidget=None) -> None:
        super().__init__(text, parent=parent)
        self.setReadOnly(True)


    def update(self,text:str):
        self.insertPlainText(text)
        self.moveCursor(QTextCursor.End)

    def write(self,string:str):
        self.update(string)

    def flush(self):
        pass



class My_qthread(QThread):

    def __init__(self, parent=QObject) -> None:
        super().__init__(parent=parent)

    def run(self):
        pass
