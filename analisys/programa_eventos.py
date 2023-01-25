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
    new_df=df.loc[:, ['uniquename', 'timestamp_occured','event', 'pid','memory_Mb','cpu_percent']]
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
            print(pid)
            break
    return consult
        
def plotStep(df,process,node_name,pid,d0,d1):
    x=df['timestamp_occured'].to_numpy()
    y=df['event'].to_numpy()
    fig,ax = plt.subplots()
    #ax = plt.axes()
    fig.set_size_inches(9.5, 10.5, forward=True)
    fmt = mdates.DateFormatter('%d-%H:%M:%S')
    ax.xaxis.set_major_formatter(fmt)
    yticks = np.arange(0, 5, 1)
    yrange = (yticks[0], yticks[-1])
    ax.set_yticks(yticks)
    ax.set_ylim(yrange)
    font_dict = {'fontsize': 10, 'fontweight': 'bold','verticalalignment':'top'}
    ax.set_yticklabels(['fail','warning','running','start'],fontdict=font_dict)
    plt.xticks(rotation=45)
    ax.step(x, y,where='post', color='red',label=pid,linewidth=2.0)
    legend = ax.legend(title='PID', shadow=True, fontsize='x-large')
    # Put a nicer background color on the legend.
    legend.get_frame().set_facecolor('#00FFCC')
    ax.grid(axis ='x', color ='0.5')
    ax.grid(axis ='y', color ='0.5')
    ax.set_xlabel('timestamp_occured',fontsize = 12, fontweight ='bold',color='blue')
    ax.set_ylabel('Event',fontsize = 13, fontweight ='bold',color='blue')
    title=node_name+': '+process
    subtitle=d0 + ' / ' + d1
    #ax.set_title(title,fontsize=12,fontweight ='bold',color='blue')
    ax.set_title("%s\n%s" % (title, subtitle),fontsize=11,fontweight ='bold',color='blue')
    
    plt.show() 

def plotMemory(df,process,node_name,pid):
    x=df['timestamp_occured'].to_numpy()
    ymemory=df['memory_Mb'].to_numpy()
    ycpu=df['cpu_percent'].to_numpy()
    title=node_name+': '+process
    fig, ax = plt.subplots(2)
    fig.suptitle(str(process),fontsize=15,fontweight ='bold')
    ax[0].plot(x, ymemory,color='blue')
    ax[1].plot(x, ycpu,color='black')
    fig.set_size_inches(9.5, 10.5, forward=True)
    fmt = mdates.DateFormatter('%d-%H:%M:%S')
    ax[0].xaxis.set_major_formatter(fmt)
    ax[0].set(xlabel='time', ylabel='Memory(mb)')
    title= 'PID: '+str(pid)
    ax[0].legend(title=title, shadow=True, fontsize='x-large')
    ax[0].set_title('Memoria',fontweight ='bold')
    ax[0].axhline(y=100,color='#d62728',linewidth=2.0)
    ax[0].grid()

    ax[1].xaxis.set_major_formatter(fmt)
    ax[1].set(xlabel='time', ylabel='CPU %')
    ax[1].legend(title=title, shadow=True, fontsize='x-large')
    ax[1].set_title('CPU',fontweight ='bold')
    ax[1].axhline(y=50,color='#d62728',linewidth=2.0)
    ax[1].grid()
    #fig.savefig("test.png")
  
    plt.show()
    

'''pids=[1136 1154 1172 1196 1164 1182 1201 1223 1210 1228 1246 1132 1150 1168
 1144 1162 1180 1484 1160 1178 1305 1186 1205 1517]'''

number_nodo=nodes_name[11]

'''
process=main_name_process[0] 
df=query_general(sql_template4,number_nodo,process,date[0][0],date[0][1])
pids=df["pid"].unique()
for id in pids:
    df2=create_dataframe(df,id)
    print(df2)
    plotStep(df2,process,number_nodo,id)
'''

def main():
    for date in [['2022-12-12','2022-12-13'],['2022-12-13','2022-12-14'],['2022-12-14','2022-12-15']]:
        for process in  main_name_process:
            df=query_general(sql_template4,number_nodo,process,date[0],date[1])
            pids=df["pid"].unique()
            for id in pids:
                df2=create_dataframe(df,id)
                print(df2)
                #plotStep(df2,process,number_nodo,id,date[0],date[1])
                plotMemory(df2,process,number_nodo,id)
def main2():
    for process in  main_name_process:
            df=query_general(sql_template4,number_nodo,process,'2022-12-12','2022-12-14')
            pids=df["pid"].unique()
            for id in pids:
                df2=create_dataframe(df,id)
                print(df2)
                plotStep(df2,process,number_nodo,id,'2022-12-12','2022-12-15')
                
                            
# INVOCACION DE LAS FUNCIONES

if __name__=="__main__":
    main()

