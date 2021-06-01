import pandas as pd 
import numpy as np

# Read excel file
data=pd.read_excel('final.xlsx')

# Chose certainly columns 
## by colum name 
disp=data['d']
force=data['f']
## by row index
row_100=data.loc[100]

## by num index 
disp=data.iloc[:,0]
force=data.iloc[:,1]
## Chose certain paragraph 
disp_first_paragraph=data.iloc[0:2,0]
force_first_paragraph=data.iloc[0:2,1]
##Chose a certain point 
disp_frist=data.iat[0,0]
force_frist=data.iat[0,1]

#operation 
## man,min value 
disp.max()
disp.min()
## correspond index 
disp.idxmax()
disp.idxmin()
### Value -> np.ndarray 
disp.values

#loop 
##row loop   -> tuple[index,pd.DataFrame] 
for i in data.iterrows():
    print(i)
##columns loop  -> tuple[label,pd.DataFrame]
print('------------------------------------------------------')
for i in data.iteritems():
    print(i[1])

print('-------------------------------------------------------------------')

##save excel
data.to_excel('aaa.xlsx')