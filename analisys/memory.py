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

sql_template='''
select concat(node_name,"_",process_name,"_",pid) as uniquename, cpu_percent,memory_Mb,timestamp_occured,pid,event from monitored where node_name='{node_name}' 
and process_name='{name_process}' and timestamp_occured BETWEEN '{inicio}' AND '{fin}' order by timestamp_occured;
'''

'''
Analizar:
    -networking
    -durability
    -ospl
    -spliced 
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
    new_df=df.loc[:, ['uniquename', 'timestamp_occured','memory_Mb','event','cpu_percent','pid']]
    new_df.set_index('timestamp_occured', inplace = True)
    #new_df['event'].replace(['start', 'running','warning','fail'],[3, 2,1,0], inplace=True)
    return new_df

def ploty(df,process,node_name,pid):
     ax = plt.axes()
     fmt = mdates.DateFormatter('%d-%H:%M:%S')
     ax.xaxis.set_major_formatter(fmt)
     yticks = np.arange(0, 5, 1)
     yrange = (yticks[0], yticks[-1])
     ax.set_xlabel('timestamp_occured',fontsize = 12, fontweight ='bold')
     ax.set_ylabel('Event',fontsize = 13, fontweight ='bold')
     ax.set_yticks(yticks)
     ax.set_ylim(yrange)
     font_dict = {'fontsize': 9, 'fontweight': 'bold','verticalalignment':'top'}
     ax.set_yticklabels(['fail','warning','running','start'],fontdict=font_dict)
     ax.grid(True)
     plt.xticks(rotation=45)
     plt.plot(df['event'],label=pid,color='red',linestyle='--',linewidth=2)
     plt.legend(title='PIDs')
     title=node_name+': '+process
     plt.title(title,fontsize=12,fontweight ='bold')
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
        dataframe=create_dataframe(df,id)
        df2=transformDf(dataframe)
        print(df2)
        print('--------------------------','\n')
        ploty(df2,name_process,nodo_name,id)
     
 # PARAMETROS DE ENTRADA
                                                                                                                                           
df=query_general(sql_template,nodes_name[11],main_name_process[9],00000000000000000,date[0][1])
gkk1 = df.groupby(['timestamp_occured', 'memory_Mb'])
print(gkk1)
gkk = df.groupby(['timestamp_occured','uniquename'])['memory_Mb'].mean()
print(gkk)


