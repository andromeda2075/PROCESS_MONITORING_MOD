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

banned_list="('mandb', 'xrandr', 'dpkg', 'fluxbox', 'ssh-agent','sleep', 'sh', 'aterm', 'guishow.sh', 'gzip', 'man-db', 'logrotate', 'apt', 'apt-get', 'run-parts', 'pulseaudio')"

servidores=['fm57-01','fm57-02','fm57-03','fm57-04','fm57-05','fm57-06','fm57-07','fm57-08','fm57-09','fm57-10','fm57-11']

consolas=['fm57-c01a','fm57-c01b','fm57-c02a','fm57-c02b','fm57-c03a','fm57-c03b','fm57-c04a','fm57-c04b', 'fm57-c06a','fm57-c06b',
            'fm57-c07a','fm57-c07b','fm57-c08a','fm57-c08b','fm57-c09a','fm57-c09b','fm57-t01']
bus_comunication=['spliced','networking','durability','ospl']


query_total_event_process_node_template='''
select node_name, process_name, count(*) as total, max(timestamp_occured) as lasttime from monitored where
event='{event}' and node_name='{node}' and timestamp_occured between '{inicio}' and '{fin}' group by node_name, process_name
'''
# PROCESOS QUE CAYERON
query_total_start_fail_process_node_template1='''
select temp1.node_name, temp1.process_name, 
temp1.total as total_start, temp1.lasttime as laststart,
temp2.total as total_fail, temp2.lasttime as lastfail
from  ({total_start_query}) as temp1, ({total_fail_query}) as temp2 
where temp1.process_name=temp2.process_name and temp1.lasttime<temp2.lasttime
and temp1.process_name not in {banned}  order by lastfail;
'''
# PROCESOS QUE INICIARON 
query_total_start_fail_process_node_template2='''
select temp1.node_name, temp1.process_name, 
temp1.total as total_start, temp1.lasttime as laststart,
temp2.total as total_fail, temp2.lasttime as lastfail
from  ({total_start_query}) as temp1, ({total_fail_query}) as temp2 
where temp1.process_name=temp2.process_name and temp1.lasttime>temp2.lasttime
and temp1.process_name not in {banned}  order by lastfail;
'''

sql_template='''
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
            #database='testdata'
            database='pruebas2022'
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

def back_time_fail(date,control_time=120):
    new=new_date(date)
    format_data= "%d/%m/%y %H:%M:%S.%f"
    end_time = datetime.strptime(new, format_data)
    new_time= end_time - timedelta(seconds=control_time)
    return new_time

def plotConsumtionResources(sql_consult,node_name,process,time_last_fail,fin):
    inicio=back_time_fail(time_last_fail)
    df=query_general(sql_consult,node_name,process,inicio,fin)
    df = df.reset_index()
    print('*****Última falla***',time_last_fail)
    print('******* catástrofe*******',fin)
    print(df)
    x = df['timestamp_occured'].to_numpy()
    ymemory = df['memory_Mb'].to_numpy()
    ycpu = df['cpu_percent'].to_numpy()
    title = node_name+': '+process
    fig, ax = plt.subplots(2)
    fig.suptitle(str(process), fontsize=15, fontweight='bold')
    ax[0].plot(x, ymemory, color='blue')
    ax[1].plot(x, ycpu, color='black')
    fig.set_size_inches(9.5, 10.5, forward=True)
    fmt = mdates.DateFormatter('%d-%H:%M:%S')
    ax[0].xaxis.set_major_formatter(fmt)
    ax[0].set(xlabel='time', ylabel='Memory(mb)')
    ax[0].legend(title=title, shadow=True, fontsize='x-large')
    ax[0].set_title('Memoria', fontweight='bold')
    ax[0].axhline(y=100, color='#d62728', linewidth=2.0)
    plt.setp(ax[0].get_xticklabels(), rotation=45, ha='right')
    ax[0].grid()
    ax[1].xaxis.set_major_formatter(fmt)
    ax[1].set(xlabel='time', ylabel='CPU %')
    ax[1].legend(title=title, shadow=True, fontsize='x-large')
    ax[1].set_title('CPU', fontweight='bold')
    ax[1].axhline(y=50, color='#d62728', linewidth=2.0)
    ax[1].grid()
    # fig.savefig("test.png")
    plt.setp(ax[1].get_xticklabels(), rotation=45, ha='right')
    plt.show()


  
plotConsumtionResources(sql_template,'fm57-01','spliced','2022-12-13 10:32:30.829134','2022-12-13 10:48:00')   

'''
# Consulta 

dff=query_general(sql_template,'fm57-01','durability','2022-12-13 08:21:00','2022-12-13 10:48:00')
dff = dff.reset_index()
print(dff)
dff2 = dff [dff['timestamp_occured'] == '2022-12-13 10:32:27.796956']
if dff2.empty != True:
        print('*******************')
        print(dff2)
else:
    print('NO FOUND')
#2022-12-13 10:32:27.796956
#df = df.reset_index()

'''











