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

# 28 nodes
nodes_name=['fm57-01','fm57-02','fm57-03','fm57-04','fm57-05','fm57-06','fm57-07','fm57-08','fm57-09','fm57-10','fm57-11',
            'fm57-c01a','fm57-c01b','fm57-c02a','fm57-c02b','fm57-c03a','fm57-c03b','fm57-c04a','fm57-c04b', 'fm57-c06a','fm57-c06b',
            'fm57-c07a','fm57-c07b','fm57-c08a','fm57-c08b','fm57-c09a','fm57-c09b','fm57-t01']

# Principales procesos a analizar    
main_name_process=['GuiDisplay-run','GuiDisplaySec-run','EcRegMsg','networking','Rms-node-run',
        'GuiRootPanel-run','GuiSoundWarnings-run','Radar-osiris-run','durability','ospl','spliced']

date=[['2022-12-12','2022-12-13'],['2022-12-13','2022-12-14'],['2022-12-14','2022-12-15']]

sql_template4='''
select concat(node_name,"_",process_name,"_",pid) as uniquename, cpu_percent,memory_Mb,timestamp_occured,pid,event from monitored where node_name='{node_name}' 
and process_name='{name_process}' and timestamp_occured BETWEEN '{inicio}' AND '{fin}' order by timestamp_occured;
'''

def generate_pd_query(sql_query):
    mysql_db=mysql.connector.connect(
            host='localhost',
            #user='prueba2022',
            user='pruebas2022',
            #password='SoporteVarayoc..2022',
            password='pruebas2022',
            #database='testdata'
            database='pruebas2022'
        )
    df=pd.read_sql(sql_query,mysql_db)
    return df

def query_general(sql_consult,node_name,name_process,inicio,fin):
    query=sql_consult.format(name_process=name_process,node_name=node_name,inicio=inicio,fin=fin)
    df=generate_pd_query(query)
    new_df=df.loc[:, ['timestamp_occured','uniquename','event', 'pid','cpu_percent','memory_Mb']]
    new_df.set_index('timestamp_occured', inplace = True)
    new_df['event'].replace(['start', 'running','warning','fail'],[3, 2,1,0], inplace=True)
    return new_df

def create_dataframe(df,id):
    df = df.reset_index()
    names=df["uniquename"].unique()
    for name in names:
        consult=df[df['uniquename']==name]
        pid = consult.iloc[0,3]
        if pid==id:
            #print(pid)
            break
    return consult

def plot_box(df,process,opt):
    df=df.reset_index()
    sub_consult_3 = df[df['event']==3]
    sub_consult_2 = df[df['event']==2]
    sub_consult_1 = df[df['event']==1]
    #sub_consult_0 = consult[ consult['event']==0]
    if opt==1:
        opt='memory_Mb' 
        title=process + ': '+'Memoria' 
        plt.ylabel('megabytes')
    else:
        opt='cpu_percent'
        title=process + ': '+'CPU' 
        plt.ylabel('CPU %')
    datos = {'Start': sub_consult_3[opt],'Running': sub_consult_2[opt],'Warning':sub_consult_1[opt]}
    df_box = pd. DataFrame.from_dict(datos)
    plt.title(title,color='b',fontsize=12)
    plt.xlabel('Eventos')
    Sboxplot = df_box.boxplot(column=['Start','Running','Warning'],grid=True, rot=30, fontsize=11)
    #boxplot = df_box.boxplot(column=['Start','Running','Warning'],grid=True, rot=30, fontsize=11, bootstrap=1000)
    plt.show()

    #return df_box





df=query_general(sql_template4,'fm57-c01a','GuiDisplay-run',date[2][0],date[2][1])
plot_box(df,'GuiDisplay-run',2)
plot_box(df,'GuiDisplay-run',1)
'''
df2=plot_box(df,'cpu_percent')
print(plot_box(df,'cpu_percent'))
boxplot = df2.boxplot(column=['Start','Running','Warning'],grid=True, rot=45, fontsize=15)  
plt.show()

columnas = ['event','memory_Mb']
consult = df[columnas]
sub_consult_3 = consult[ consult['event']==3]
sub_consult_2 = consult[ consult['event']==2]
sub_consult_1 = consult[ consult['event']==1]
sub_consult_0 = consult[ consult['event']==0]
print(sub_consult_3)
print(sub_consult_2)
print(sub_consult_1)
print(sub_consult_0)
x3=sub_consult_3['memory_Mb'].to_numpy()
x2=sub_consult_2['memory_Mb'].to_numpy()
x1=sub_consult_1['memory_Mb'].to_numpy()

data= {"start":x3,
       "running": x2,
       "warning": x1}

# Figura
plt.figure(figsize=(6,4))
plt.boxplot(data.values())
plt.xticks(range(1,len(data)+1), data.keys())
plt.show()
'''






