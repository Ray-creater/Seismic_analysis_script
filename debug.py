import pandas as pd 

data=pd.read_excel('final.xlsx')
disp=data.iloc[:,0].reset_index(drop=True)
print(disp)
print(disp.values)
print(type(disp.idxmax()))

a=[1,2,3,4,5]
print(a)
a.pop(1)
print(a)
