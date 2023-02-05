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
    
main_name_process=['GuiDisplay-run','GuiDisplaySec-run','EcRegMsg','networking','Rms-node-run',
        'GuiRootPanel-run','GuiSoundWarnings-run','Radar-osiris-run','durability','ospl','spliced']

def generate_pd_query(sql_query):
    mysql_db=mysql.connector.connect(
            host='localhost',
            #user='prueba2022',
            user='root',
            #password='SoporteVarayoc..2022',
            #database='testdata'
            password='pruebas2022',
            database='pruebas2022'
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

banned_list="('mandb', 'xrandr', 'dpkg', 'fluxbox', 'ssh-agent','sleep', 'sh', 'aterm', 'guishow.sh', 'gzip', 'man-db', 'logrotate', 'apt', 'apt-get', 'run-parts', 'pulseaudio')"

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
and process_name='{name_process}' order by timestamp_occured;
'''
sql_template5='''
select * from pc
'''


def query_pd_back(sql_consult,fila,control_time,name_process,banned_list,event,node_name,column=1):

    time_end=intervalos[fila][column]
    date=new_date(time_end)
    format_data= "%d/%m/%y %H:%M:%S"
    end_time = datetime.strptime(date, format_data)
    time= end_time - timedelta(seconds=control_time)
    query=sql_consult.format(event=event,name_process=name_process,inicio=time,fin=time_end,node_name=node_name)
    df=generate_pd_query(query)
    # Convirtiendo a la columna event de datos categóricos a numericos
    event_dummie=pd.get_dummies(df, columns = ['event'])

    return event_dummie

def query_pd_forward(sql_consult,fila,control_time,name_process,banned_list,event,node_name,column=0):

    time_first=intervalos[fila][column]
    date=new_date(time_first)
    format_data= "%d/%m/%y %H:%M:%S"
    firts_time = datetime.strptime(date, format_data)
    time= firts_time  + timedelta(seconds=control_time)
    query=sql_consult.format(event=event,name_process=name_process,inicio=time_first,fin=time,node_name=node_name)
    df=generate_pd_query(query)
    # Convirtiendo a la columna event de datos categóricos a numericos
    event_dummie=pd.get_dummies(df, columns = ['event'])

    return event_dummie


def query_general(sql_consult,node_name,name_process):
    query=sql_consult.format(name_process=name_process,node_name=node_name)
    df=generate_pd_query(query)
    # Convirtiendo a la columna event de datos categóricos a numericos
    event_dummie=pd.get_dummies(df, columns = ['event'])
    return event_dummie


def Show_df(df,n):
    print(df.head(n))

 # Gráficas Preliminares

def plotSeries(df,column_name,name_process,opt):

    ax = plt.axes()
    ax.plot(df['timestamp_occured'], df[column_name],'o',color='red')
    if opt == 1:
        title=name_process+' '+'End to back'
        ax.set_title(title)
    else:
        title=name_process+' '+'Init to Forward'
        ax.set_title(title)

    ax.set_xticks(df['timestamp_occured'])
    ax.set_xticklabels(df['timestamp_occured'], rotation=30, ha='right')

    ax.set_ylabel(column_name)
    ax.set_xlabel('Time')
    fmt = mdates.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(fmt)
    plt.subplots_adjust(bottom=0.15)
    plt.show()


def plotSeries2(df,column_name,name_process):
    ax = plt.axes()
    ax.plot(df['timestamp_occured'], df[column_name],'-',color='red')
    ax.set_xticks(df['timestamp_occured'])
    ax.set_xticklabels(df['timestamp_occured'], rotation=30, ha='right')
    ax.set_ylabel(column_name)
    ax.set_xlabel('Time')
    #2022-12-14 01:13:00
    #2022-12-14 21:55:00
    ax.set_xlim([datetime(2022,12,14,1,13,0), datetime(2022,12,14,21,55,00)])
    ax.set_ylim([0, 250])
    fmt = mdates.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(fmt)
    plt.xlim([datetime(2022,12,14,1,13,0), datetime(2022,12,14,21,55,00)])
    plt.subplots_adjust(bottom=0.15)
    plt.show()

def ploty(df,column_name,name_process):
    #plt.rcParams["figure.figsize"] = [7.00, 3.50]
    #plt.rcParams["figure.autolayout"] = True
    x=df['timestamp_occured']
    y =df['memory_Mb']
    fig, ax = plt.subplots()
    ax.plot(df['timestamp_occured'], df[column_name],'-',color='red')
    #ax.plot_date(x, y, markerfacecolor='green', markeredgecolor='red', ms=7)
    fig.autofmt_xdate()
    ax.set_xlim([datetime(2022,12,14,1,13,0), datetime(2022,12,14,3,31,00)])
    ax.set_ylim([0, 250])
    fmt = mdates.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(fmt)
    plt.show()

 # PARAMETROS

row=0
control_time1=3600  # Dado en minutos ( 1h)
control_time2=3630
# opcional
fail_event='fail'
start_event='start'
warning_event='warning'
running_event='running'

memory_column='memory_Mb'
cpu_column='cpu_percent'

#------------------------------ DataFrame-----------------

df=query_general(sql_template4,nodes_name[11],main_name_process[0])
print(df)
df['day'] = pd.DatetimeIndex(df['timestamp_occured']).day
df.set_index('timestamp_occured', inplace = True)
ax = plt.axes()
fmt = mdates.DateFormatter('%d-%H:%M:%S')
ax.xaxis.set_major_formatter(fmt)
df['memory_Mb'].plot()
plt.title('fm57-c01a GuiDisplay-run')
plt.ylabel('memoria(Mb)')
plt.show()

# -------------------------Consultas específicas al dataframe -----------------

consult=df.where((df['event_start']==1)|(df['event_fail']==1))
consult_only_start=df[df['event_start']==1]
ax = plt.axes()
fmt = mdates.DateFormatter('%d-%H:%M:%S')
ax.xaxis.set_major_formatter(fmt)
consult_only_start['memory_Mb'].plot(marker='.', alpha=0.5, linestyle='None', figsize=(15, 5),color='red')
plt.title('fm57-c01a GuiDisplay-run event start')
plt.ylabel('Memory (Mb)')
plt.show()

# ----------------------- Colsultas del descriptivo-------------------------------
desc_start = consult_only_start["memory_Mb"].describe()
print(desc_start)

#---------------------------------
print(df)
prueba=df.resample("T").median()
print(prueba)
