# phis Python file uses the following encoding: utf-8
from opensees_script.cfst_class import CFST
import sys
from typing import Text
from numpy import isin
import pandas as pd
from PySide2.QtWidgets import *
from analysis_script.yield_point import *
from analysis_script.skeleton import skeleton
from analysis_script.usrdefine import *
from analysis_script.energy import *
from mywidgets import CMDTextEdit, CMDTextEditSelf, MyQWidget,MyFigureCanvas 
import sys
import threading as th
from PySide2.QtCore import QThread

class Seismic(QMainWindow):
    def __init__(self):
        super(Seismic, self).__init__()
        
        self.central_widget_of_mainwindow=MyQWidget("Vertical")
        self.setCentralWidget(self.central_widget_of_mainwindow)
        select_widget=self.central_widget_of_mainwindow.add_my_qwidget("Select","Horizontal")
        select_buttons=select_widget.add_pushbuttons('Startup',"CFST opensees") 

        self.starup_page()


        #select button function
        select_buttons['Startup'].clicked.connect(self.starup_page)
        select_buttons['CFST opensees'].clicked.connect(self.cfst_opensees_analysis_page)
        

    def starup_page(self):
        if hasattr(self,"cfst_opensees_analysis_widget"):
            if not self.cfst_opensees_analysis_widget.isHidden():
                self.cfst_opensees_analysis_widget.hide()

        if not hasattr(self,"startup_widget"):
            self.startup_widget=self.central_widget_of_mainwindow.add_my_qwidget("Startup","Vertical")

            #Three_main_mywidget 
            middle_widget=self.startup_widget.add_my_qwidget("Middle","Horizontal")
            bottom_widget=self.startup_widget.add_my_qwidget("Bottom","Horizontal")

            # self.startup_widget.setStretchFactor(top_widget,middle_widget,bottom_widget,scale=(1,8,1))
            self.startup_widget.setStretchFactor(middle_widget,bottom_widget,scale=(8,2))

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
            plot_button=right_mainview_widge.add_pushbuttons('Output picture')
            save_button=right_mainview_widge.add_pushbuttons('Output data')
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
            save_button.clicked.connect(self.output_data)
        self.startup_widget.show()

    def cfst_opensees_analysis_page(self):
        if hasattr(self,"startup_widget"):
            if not self.startup_widget.isHidden():
                self.startup_widget.hide()
        if not hasattr(self,"cfst_opensees_analysis_widget"):
            self.cfst_opensees_analysis_widget=self.central_widget_of_mainwindow.add_my_qwidget('cfst opensees','Vertical')
            cfst_main=self.cfst_opensees_analysis_widget.add_my_qwidget('CFST Main','Horizontal')
            cfst_message=self.cfst_opensees_analysis_widget.add_my_qwidget('CFST Message','Horizontal')
            self.cfst_opensees_analysis_widget.setStretchFactor(cfst_main,cfst_message,scale=(8,2))

            cfst_main_parameter_mygroupbox=cfst_main.add_my_qgroupbox('CFST Main Parameter',"Form") 
            main_plot_opensees=cfst_main.add_my_qwidget('main plot opensees','Veritcal')
            cfst_main.setStretchFactor(cfst_main_parameter_mygroupbox,main_plot_opensees,scale=(2,8))



            # main qwidget
            ## main parameters groupbox
            para_label_str=['Section shape',"Length","SecHeight",'SecWidth','Thickness','Concrete grade','Steel grade','Axial load ratio','Disp control']
            self.para_dic={i:(QLabel(i),QTextEdit(i+" value")) for i in para_label_str}
            [i[1].setFixedHeight(40) for i in self.para_dic.values()]
            cfst_main_parameter_mygroupbox.add_widgets_formlayout([i for i in self.para_dic.values()])
            para_preset_value=['Rect','600','300','120','14','130','420','0.3','10,20,30,40']
            [self.para_dic[i][1].setText(j) for i,j in zip(para_label_str,para_preset_value)]
            opensees_plot_button=QPushButton("Plot")
            opensees_analysis_button=QPushButton('Opensees analysis')
            process_kill_button=QPushButton('Process kill')
            process_run_button=QPushButton("Process run")
            cfst_main_parameter_mygroupbox.add_widgets_formlayout([[opensees_analysis_button,opensees_plot_button],])
            cfst_main_parameter_mygroupbox.add_widgets_formlayout([[process_run_button,process_kill_button],])
            self.plot_arg_opensees=([1,2,3],[3,3,4],'d')
            self.cfst_figure=MyFigureCanvas(*self.plot_arg_opensees)
            main_plot_opensees.add_any_qwidget(self.cfst_figure)
            cfst_main_button_widget=main_plot_opensees.add_my_qwidget("Plot buttons",'Horizontal')
            cfst_main_buttons=cfst_main_button_widget.add_pushbuttons('Picture output','Data output')
            main_plot_opensees.setStretchFactor(self.cfst_figure,cfst_main_button_widget,scale=(9,1))


            cfst_main.setStretchFactor(*[cfst_main_parameter_mygroupbox,self.cfst_figure],scale=[1,9])

            ###self cmd
            cmd_textedit_self=CMDTextEditSelf('CMD TextEdit',cfst_message)
            cmd_textedit_self.insertPlainText('\n')
            cfst_message.add_any_qwidget(cmd_textedit_self)
            sys.stdout=cmd_textedit_self


            #### button function

            opensees_analysis_button.clicked.connect(self.opensees_analysis)
            opensees_plot_button.clicked.connect(self.opensees_plot)
            process_run_button.clicked.connect(self.test)
            cfst_main_buttons['Picture output'].clicked.connect(self.output_pic_opensees)
            cfst_main_buttons['Data output'].clicked.connect(self.output_data_opensees)


        self.cfst_opensees_analysis_widget.show()


    def test(self):
        print("aaaa\n")

    def output_pic(self):
        save_path,_=QFileDialog.getSaveFileName(self,filter='*.png')
        if _:
            self.display_window.fig.savefig(save_path+'png')
        else:
            print("No path choose")

    def output_data(self):
        save_path,_=QFileDialog.getSaveFileName(self,filter='*.xlsx')
        if _:
            self.savedata=pd.DataFrame(self.plot_arg[:2])
            self.savedata=self.savedata.T
            self.savedata.to_excel(save_path+'.xlsx')
        else:
            print("No path choose")      
            

    def output_pic_opensees(self):
        save_path,_=QFileDialog.getSaveFileName(self,filter='*.png')
        if _:
            self.cfst_figure.fig.savefig(save_path+'.png')
        else:
            print("No path choose")

    def output_data_opensees(self):
        save_path,_=QFileDialog.getSaveFileName(self,filter='*.xlsx')
        if _:
            self.savedata=pd.DataFrame(self.plot_arg_opensees[:2])
            self.savedata=self.savedata.T
            self.savedata.to_excel(save_path+'.xlsx')
        else:
            print("No path choose")           


    def select_xlsx_path(self):
        xlsx_path,_=QFileDialog.getOpenFileName(self,filter='*.xlsx')
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


    def comfirm_para_opensees(self):
        self.checked_para_dic={i:j[1].toPlainText() for i,j in self.para_dic.items()}
        for i,j in self.checked_para_dic.items():
            if i== "Section shape":
                if j not in ['Circle','Rect']:
                    print("Please select section from Circle and Rect")
                
            elif i=="Disp control":
                try:
                    j=float(j)
                except ValueError:
                    j=parse_str_array(j)
            else:
                j=float(j)
            self.checked_para_dic[i]=j

        print(self.checked_para_dic)


            
    def opensees_analysis(self):
        self.comfirm_para_opensees()
        self.reform_para={}
        self.reform_para['shape']=self.checked_para_dic['Section shape']
        self.reform_para['geometry']=(self.checked_para_dic[i] for i in ['Length','SecHeight',"SecWidth",'Thickness'])
        self.reform_para["material_grade"]=(self.checked_para_dic[i] for i in ['Concrete grade','Steel grade'])
        self.reform_para['load']=(self.checked_para_dic['Axial load ratio'],self.checked_para_dic['Disp control'])
        cfst=CFST(**self.reform_para)
        cfst.opensees_analysis()
        
    def opensees_plot(self):
        self.opensees_disp,self.opensees_force=CFST.data_extract()
        minner_length=min(len(self.opensees_disp),len(self.opensees_force))
        self.opensees_disp,self.opensees_force=self.opensees_disp[:minner_length],self.opensees_force[:minner_length]
        self.plot_arg_opensees=[self.opensees_disp,self.opensees_force,'dd']
        self.cfst_figure.redraw(*self.plot_arg_opensees)


if __name__ == "__main__":
    app = QApplication([])
    widget = Seismic()
    widget.show()
    sys.exit(app.exec_())
