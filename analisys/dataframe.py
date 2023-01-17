import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time     
import mysql.connector
import sys
from datetime import datetime, timedelta
import string
import matplotlib.dates as mdates
import seaborn as sns
from datetime import datetime

df = pd.DataFrame([['20221212202504',  'fm57-c01a_GuiDisplay-run_1178' ,     3,  1178], ['20221212202508',  'fm57-c01a_GuiDisplay-run_1178',      0,  1178],['20221212202512',  'fm57-c01a_GuiDisplay-run_1178',      2,  1178]], columns=['timestamp_occured', 'uniquename','event','pid'])
 
#print(df)

#new_row=['2022-12-12 20:25:05','fm57-c01a_GuiDisplay-run_1178',3,1178]
'''
newDataframe = df.copy()

event= df.iloc[0,2]

for index,aa in df.iterrows():
	print('index',index)	
	if event != aa[2]:
		new_row=[df.iloc[index,0],aa[1],df.iloc[index-1,2] ,aa[3]]
		print(new_row)
		pos=index
		newDataframe = pd.DataFrame(np.insert(newDataframe.values, pos, new_row, axis=0))
		event=aa[2]
		print('evento actual',event)
'''
df['timestamp_occured'] = pd.to_datetime(df['timestamp_occured'], format='%Y%m%d%H%M%S')
print(df)
print('\n')




newDataframe = df.copy()

event= df.iloc[0,2]
print(event)
print('----------------------------------------')

index=0
for indextemp, aa in df.iterrows():
	print(index,indextemp)
	if event != aa[2]:
		newDataframe = pd.DataFrame(np.insert(newDataframe.values, index, [aa[0], aa[1], event, aa[3]], axis=0))
		event=aa[2]
		print('insert')
		print(newDataframe)
		index+=1
	index+=1
   
df1 = newDataframe.set_index('timestamp_occured')


	
print(df1)


'''
for index,aa in df.iterrows():
	print(index,type(index))
'''
#newDataframe.loc[1.5]=new_row
#newDataframe.sort_index().reset_index(drop=True)

#newDataframe = pd.DataFrame(np.insert(newDataframe.values, 1, new_row, axis=0))
#print(newDataframe.values)		
'''
print(df.iloc[0,1])
print('******************************')
print(df.iloc[1,:])
print('******************************')
print(df.iloc[2,:])
'''