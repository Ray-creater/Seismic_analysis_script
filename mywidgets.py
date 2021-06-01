from PySide2.QtWidgets import *



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

    def setStretchFactor(self,*widget:QWidget,scale:list)->None:
        for i,j in zip(widget,scale):
            self.layout.setStretchFactor(i,j)

