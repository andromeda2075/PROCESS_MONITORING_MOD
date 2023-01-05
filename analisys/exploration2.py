import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time     
import mysql.connector
import sys
from datetime import datetime, timedelta
import string

def generate_pd_query(sql_query):
    mysql_db=mysql.connector.connect(
            host='localhost',
            user='prueba2022',
            password='SoporteVarayoc..2022',
            database='testdata'
        )
    df=pd.read_sql(sql_query,mysql_db)
    return df

banned_list="('mandb', 'xrandr', 'dpkg', 'fluxbox', 'ssh-agent','sleep', 'sh', 'aterm', 'guishow.sh', 'gzip', 'man-db', 'logrotate', 'apt', 'apt-get', 'run-parts', 'pulseaudio')"


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


def query_pd(time_end,control_time,event,banned_list):
    date=new_date(time_end)
    format_data= "%d/%m/%y %H:%M:%S"
    end_time = datetime.strptime(date, format_data)
    time= end_time - timedelta(seconds=control_time)
    
    sql_template1 = '''
        SELECT node_name, process_name, event,timestamp_occured FROM monitored 
        where event='{event}' and process_name not in {banned} and timestamp_occured BETWEEN '{inicio}' AND '{fin}' 
        GROUP BY node_name,process_name, event,timestamp_occured order by (node_name);
    '''
    
    sql_template2 = '''
        SELECT node_name, process_name, event,timestamp_occured FROM monitored 
        where process_name='Rms-node-run' and process_name not in {banned} and timestamp_occured BETWEEN '{inicio}' AND '{fin}' 
        GROUP BY node_name,process_name, event,timestamp_occured order by (node_name);
    '''
    query=sql_template2.format(event=event,banned=banned_list,inicio=time,fin=time_end)
    df=generate_pd_query(query)
    return df
    
def print_df(df,n):
    print(df.head(n))
#----------------------------------------

## parametros

time_end='2022-12-12 16:39:00'
control_time=600  # 10 minutes
event='fail'
df=query_pd(time_end,control_time,event,banned_list)

print_df(df,10)

print('\n')    

# corregir
df_dummies = pd.get_dummies(df['event'])

print(df_dummies.head(90))
#Gráficas Preliminares


#def plotSeries(df,End,control_time,query):

