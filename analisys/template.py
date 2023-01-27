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
            user='prueba2022',
            #user='pruebas2022',
            password='SoporteVarayoc..2022',
            #password='pruebas2022',
            database='testdata'
            #database='pruebas2022'
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

def plot_memory_event(df,process,date1,date2):
    df_start = df[df['event'] == 3]
    serie3_m=df_start.loc[:, ['memory_Mb']]
    serie3_c=df_start.loc[:, ['cpu_percent']]  
    df_running = df[df['event'] == 2]
    serie2_m= df_running.loc[:, ['memory_Mb']] 
    serie2_c=df_running.loc[:, ['cpu_percent']] 
    df_warning =df[df['event'] == 1]
    serie1_m=df_warning.loc[:, ['memory_Mb']]
    serie1_c=df_warning.loc[:, ['cpu_percent']] 

    fig, axs = plt.subplots(2)
    title=process+' ' +str(date1)+' / '+str(date2)
    fig.suptitle(title,color='m',fontweight ='bold')
    axs[0].plot(serie3_m,color='g', label='Start')
    axs[0].plot(serie2_m,color='r', label='Running')
    axs[0].plot(serie1_m,color='b', label='Warning')
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Megabytes')
    axs[0].set_title('Memoria',color='k',fontsize=12,fontweight ='bold')
    axs[0].legend()

    axs[1].plot(serie3_c,color='g', label='Start')
    axs[1].plot(serie2_c,color='r', label='Running')
    axs[1].plot(serie1_c,color='b', label='Warning')
    
    axs[1].set_xlabel('Time')
    axs[1].set_ylabel('%')
    axs[1].set_title('CPU',color='k',fontsize=12,fontweight ='bold')
    axs[1].legend()
    plt.show() 


df1=query_general(sql_template4,'fm57-c01b','Rms-node-run',date[2][0],date[2][1])
plot_memory_event(df1,'Rms-node-run',date[2][0],date[2][1])
df2=query_general(sql_template4,'fm57-c01b','Rms-node-run',date[1][0],date[1][1])
plot_memory_event(df2,'Rms-node-run',date[1][0],date[1][1])
df3=query_general(sql_template4,'fm57-c01b','Rms-node-run',date[0][0],date[0][1])
plot_memory_event(df3,'Rms-node-run',date[0][0],date[0][1])
#Sugerencia: ts.resample("M").mean()
