import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time     
import mysql.connector
import sys
from datetime import datetime, timedelta
import string
import matplotlib.dates as mdates

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

'''Parametros de entrada
'''

#time_end='2022-12-12 16:39:00'
#time_end='2022-12-13 07:12:00'
row=0
control_time1=3600  # Dado en minutos ( 1h)
control_time2=3630
# opcional
event='fail'

name_process='Rms-node-run'
node_name='fm57-01'

column_name1='memory_Mb'
column_name2='cpu_percent'

'''
Consultas
'''
df_end=query_pd_back(sql_template3,row,control_time1,name_process,banned_list,event,node_name)
df_first=query_pd_forward(sql_template3,row,control_time2,name_process,banned_list,event,node_name)
print(df_end)
print('\n')
print(df_first)

#Show_df(df,40)


plotSeries(df_first,column_name1,name_process,0)

plotSeries(df_end,column_name1,name_process,1)

    




