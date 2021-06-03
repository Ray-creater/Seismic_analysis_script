# 抗震性能-拟静力试验参数分析
这个项目是根据拟静力试验所得到的 P - $\Delta$滞回曲线，进行一般性的参数分析。

# 使用方法
安装python及其该项目的依赖库
改项目使用的依赖库有：
xlrd
openpyxl
numpy 
pandas
scipy
PySide2
matplotlib

可以直接使用pip安装以上依赖库
安装完成后直接在改目录下使用相应的python解释器运行 main_class.py
python main_class.py

# 分析的参数及分析方法
## 滞回曲线
将位移荷载曲线使用excel进行保存，保存格式如final.xlsx，分二列，第一列为位移，第二列为对应的应变，其中第一行作为变量变量标志，分别为d和f，各表示位移和力
## 骨架曲线
目前仅仅是将滞回曲线的外包络线作为骨架曲线，有不严谨的地方
以后会添加不同的取骨架曲线的方式
## 屈服点
屈服点是根据骨架曲线来识别的，其确定方法多种多样，不同的材料采用不同的方法
目前实现了三种屈服点确定的方法：R-park法，等面积法，几何法
## 延性系数
延性系数为最终失效位移除以屈服位移
最终失效位移的确定：85%峰值应力点所对应的位移，或者最大位移（试验没有做到85%的峰值位移）
## 每一圈的耗能
每一个滞回圈的面积，横坐标为该滞回圈最大位移
## 累计耗能
之前所有滞回圈的面积之和，横坐标为该滞回圈最大位移