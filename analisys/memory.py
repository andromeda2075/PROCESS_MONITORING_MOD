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
            password='SoporteVarayoc..2022',
            database='testdata'
        )
    df=pd.read_sql(sql_query,mysql_db)
    return df

def query_general(sql_consult,node_name,name_process,inicio,fin):
    query=sql_consult.format(name_process=name_process,node_name=node_name,inicio=inicio,fin=fin)
    df=generate_pd_query(query)
    new_df=df.loc[:, ['timestamp_occured','event', 'pid','cpu_percent','memory_Mb']]
    new_df.set_index('timestamp_occured', inplace = True)
    new_df['event'].replace(['start', 'running','warning','fail'],[3, 2,1,0], inplace=True)
    return new_df

    
df=query_general(sql_template4,'fm57-c01a','GuiDisplay-run',date[0][0],date[0][1])

# Group by multiple columns
df2 =df.groupby(['pid', 'event','memory_Mb']).sum()
pids=df["pid"].unique()
print(pids)
print(df2.shape[0])
pids=df2["pid"].unique()
print(pids)

