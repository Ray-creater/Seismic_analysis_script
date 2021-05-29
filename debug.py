import pandas as pd 

data=pd.read_excel('final.xlsx')
disp=data.iloc[:,0].reset_index(drop=True)
print(disp)
print(disp.values)
print(disp.idxmax())
print(disp.max())
print(disp.iat[3])