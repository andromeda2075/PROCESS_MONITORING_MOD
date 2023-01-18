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

# Tiempos de los ejercicios 
intervalos = [
        ['2022-12-12 14:04:00' ,'2022-12-12 16:39:00'],
        ['2022-12-12 17:05:00' ,'2022-12-12 19:06:00'],
        ['2022-12-12 20:48:00' ,'2022-12-12 22:52:00'],
        ['2022-12-12 23:34:00' ,'2022-12-13 04:35:00'],
        ['2022-12-13 05:02:00' ,'2022-12-13 07:12:00'],
        ['2022-12-13 08:21:00' ,'2022-12-13 10:48:00'],
        ['2022-12-13 13:59:00' ,'2022-12-13 16:35:00'],
        ['2022-12-13 17:53:00' ,'2022-12-13 19:25:00'],
        ['2022-12-13 20:40:00' ,'2022-12-14 00:23:00'],
        ['2022-12-14 01:13:00' ,'2022-12-14 03:31:00'],
        ['2022-12-14 04:27:00' ,'2022-12-14 07:55:00'],
        ['2022-12-14 08:20:00' ,'2022-12-14 08:43:00'],
        ['2022-12-14 09:10:00' ,'2022-12-14 13:02:00'],
        ['2022-12-14 13:49:00' ,'2022-12-14 16:14:00'],
        ['2022-12-14 16:16:00' ,'2022-12-14 17:53:00'],
        ['2022-12-14 19:53:00' ,'2022-12-14 21:55:00'],
        ['2022-12-14 22:44:00' ,'2022-12-15 04:15:00']
    ]
# 28 nodes
nodes_name=['fm57-01','fm57-02','fm57-03','fm57-04','fm57-05','fm57-06','fm57-07','fm57-08','fm57-09','fm57-10','fm57-11',
            'fm57-c01a','fm57-c01b','fm57-c02a','fm57-c02b','fm57-c03a','fm57-c03b','fm57-c04a','fm57-c04b', 'fm57-c06a','fm57-c06b',
            'fm57-c07a','fm57-c07b','fm57-c08a','fm57-c08b','fm57-c09a','fm57-c09b','fm57-t01']

# Principales procesos a analizar    
main_name_process=['GuiDisplay-run','GuiDisplaySec-run','EcRegMsg','networking','Rms-node-run',
        'GuiRootPanel-run','GuiSoundWarnings-run','Radar-osiris-run','durability','ospl','spliced']

banned_list="('mandb', 'xrandr', 'dpkg', 'fluxbox', 'ssh-agent','sleep', 'sh', 'aterm', 'guishow.sh', 'gzip', 'man-db', 'logrotate', 'apt', 'apt-get', 'run-parts', 'pulseaudio')"

date=[['2022-12-12','2022-12-13'],['2022-12-13','2022-12-14'],['2022-12-14','2022-12-15']]

# Consultas
sql_template1 = '''
        SELECT node_name, process_name, event,timestamp_occured FROM monitored 
        where event='{event}' and process_name not in {banned} and timestamp_occured BETWEEN '{inicio}' AND '{fin}' 
        GROUP BY node_name,process_name, event,timestamp_occured order by (node_name);
    '''
    
sql_template2 = '''
    SELECT node_name, process_name, event,timestamp_occured,memory_Mb,cpu_percent FROM monitored 
    where process_name='{name_process}' and process_name not in {banned} and timestamp_occured BETWEEN '{inicio}' AND '{fin}' 
    GROUP BY node_name,process_name, event,timestamp_occured,memory_Mb,cpu_percent order by (node_name);
'''

    
sql_template3 = '''
    SELECT node_name, pid,process_name, event,timestamp_occured,memory_Mb,cpu_percent FROM monitored 
    where process_name='{name_process}'  and timestamp_occured BETWEEN '{inicio}' AND '{fin}' and node_name='{node_name}'
    ;
'''

sql_template4='''
select concat(node_name,"_",process_name,"_",pid) as uniquename, cpu_percent,memory_Mb,timestamp_occured,pid,event from monitored where node_name='{node_name}' 
and process_name='{name_process}' and timestamp_occured BETWEEN '{inicio}' AND '{fin}' order by timestamp_occured;
'''
sql_template5='''
select * from pc
'''

# Métodos

def generate_pd_query(sql_query):
    mysql_db=mysql.connector.connect(
            host='localhost',
            user='prueba2022',
            password='SoporteVarayoc..2022',
            database='testdata'
        )
    df=pd.read_sql(sql_query,mysql_db)
    return df

def new_date(time_end):
    c=time_end
    new_c=c.split(" ")
    new_c1=new_c[0].replace('-','/')
    new_c2=new_c1.split("/")
    year=new_c2[0][2:4]
    new_c2[0]=year
    reverse_new_c2=list(reversed(new_c2))
    new_date= "/".join(reverse_new_c2)
    date= new_date+" "+new_c[1]
    return date


def query_general(sql_consult,node_name,name_process,inicio,fin):
    query=sql_consult.format(name_process=name_process,node_name=node_name,inicio=inicio,fin=fin)
    df=generate_pd_query(query)
    new_df=df.loc[:, ['uniquename', 'timestamp_occured','event', 'pid']]
    new_df['event'].replace(['start', 'running','warning','fail'],[3, 2,1,0], inplace=True)
    return new_df

def ploty(df,process,node_name,pid):
    x=df['timestamp_occured'].to_numpy()
    y=df['event'].to_numpy()

    fig, ax = plt.subplots()

    ax.step(x, y,where='post',label=pid,color='green',linewidth=2.5)
    ax.grid(axis ='x', color ='0.5')
    ax.grid(axis ='y', color ='0.5')
    ax.legend(title ='PID')
    title=node_name+': '+process
    ax.set_title(title,fontsize=12,fontweight ='bold')

    plt.show()
    

def create_dataframe(df,id):
    names=df["uniquename"].unique()
    for name in names:
        consult=df[df['uniquename']==name]
        pid = consult.iloc[0,2]
        if pid==id:
            break
    return consult

def consultPlot(df,name_process,nodo_name):
    pids=df["pid"].unique()
    newpid=pids.tolist()
    for id in newpid:
        df2=create_dataframe(df,id)
        print(df2)
        print('--------------------------','\n')
        ploty(df2,name_process,nodo_name,id)
     
 # PARAMETROS DE ENTRADA

number_nodo=11
def main():
    for date in [['2022-12-12','2022-12-13'],['2022-12-13','2022-12-14'],['2022-12-14','2022-12-15']]:
        for process in  main_name_process:
            df=query_general(sql_template4,nodes_name[number_nodo],process,date[0],date[1])
            consultPlot(df,process,nodes_name[11])
            
# INVOCACION DE LAS FUNCIONES
'''
if __name__=="__main__":
    main()
'''
main()