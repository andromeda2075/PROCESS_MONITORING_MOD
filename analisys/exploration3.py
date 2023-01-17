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
# paginas de consulta
# https://julianroth.org/
# https://julianroth.org/documentation/neural_networks/classifier_demo.html
# https://www.kaggle.com/code/claytonmiller/bdg2-pandas-times-series-data-analysis-example
# https://www.dataquest.io/blog/tutorial-time-series-analysis-with-pandas/
# https://www.kaggle.com/code/hamelg/python-for-data-17-dealing-with-dates
# https://www.kaggle.com/code/thebrownviking20/everything-you-can-do-with-a-time-series
# https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subplot.html#sphx-glr-gallery-subplots-axes-and-figures-subplot-py
# https://towardsdatascience.com/resample-function-of-pandas-79b17ec82a78
# https://medium.com/codex/say-goodbye-to-loops-in-python-and-welcome-vectorization-e4df66615a52
# https://support.minitab.com/es-mx/minitab/20/help-and-how-to/statistics/basic-statistics/how-to/display-descriptive-statistics/interpret-the-results/all-statistics-and-graphs/
# https://platzi.com/clases/2913-matplotlib-seaborn/47950-categoricos/
# https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/psd_demo.html#sphx-glr-gallery-lines-bars-and-markers-psd-demo-py



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
    new_df.set_index('timestamp_occured', inplace = True)
    new_df['event'].replace(['start', 'running','warning','fail'],[3, 2,1,0], inplace=True)
    return new_df

#print(new_df)
# df_transposed = new_df.T
# print(df_transposed)
# ax = plt.axes()
# fmt = mdates.DateFormatter('%d-%H:%M:%S')
# ax.xaxis.set_major_formatter(fmt)
# new_df['event'].plot(marker='.', alpha=0.5, linestyle='None', figsize=(15, 5),color='red')
# plt.show()
# consult1=new_df[new_df['uniquename']=='fm57-c01a_GuiDisplay-run_1154']
# print(consult1)
# consult2=new_df[new_df['uniquename']=='fm57-c01a_GuiDisplay-run_1172']
# print(consult2)
# ax = plt.axes()
# fmt = mdates.DateFormatter('%d-%H:%M:%S')
# ax.xaxis.set_major_formatter(fmt)
# ax.set_xlim([datetime(2022,12,12,14,0,0), datetime(2022,12,15,4,30,00)])
# yticks = np.arange(0, 4, 1)
# yrange = (yticks[0], yticks[-1])
# ax.set_ylabel('Event')
# ax.set_yticks(yticks)
# ax.set_ylim(yrange)
# consult['event'].plot(color='red')
# plt.show()

'''
    def ploty():
    # Graficos
        ax = plt.axes()
        fmt = mdates.DateFormatter('%d-%H:%M:%S')
        ax.xaxis.set_major_formatter(fmt)
        yticks = np.arange(0, 4, 1)
        yrange = (yticks[0], yticks[-1])
        ax.set_xlabel('timestamp_occured',fontsize = 12, fontweight ='bold')
        ax.set_ylabel('Event',fontsize = 13, fontweight ='bold')
        ax.set_yticks(yticks)
        ax.set_ylim(yrange)
        font_dict = {'fontsize': 10, 'fontweight': 'bold','verticalalignment':'top'}
        ax.set_yticklabels(['fail','warning','running','start'],fontdict=font_dict)
        ax.grid(True)
        plt.xticks(rotation=45)
        plt.margins(x=0.1, y=0.1)
        plt.plot(consultFinal['event'],label=pid,color='red')
        plt.legend(title='PIDs')
        plt.title(procces,fontsize=14,fontweight ='bold')
      
        # plt.savefig(procces)
        plt.show()

'''


def newDf(df):
    df = df.reset_index()
    newDataframe = df
    event_list=df['event'].tolist()
    time_list=df['timestamp_occured'].tolist()
    cont=0
    for index, aa in df.iterrows():
        if event_list[cont]!=event_list[cont+1]:
            new_row=['timestamp_occured',time_list[cont+1], 'uniquename',aa[0] ,'event',event_list[cont] , 'pid',aa[2]]
            print(new_row)
            newDataframe.loc[str(cont+1), :] = new_row
        cont=cont+1
    return newDataframe
    

#nueva_fila = {'name':'Geo', 'physics':87, 'chemistry':92, 'algebra':97}
#Añadiendo una fila al dataframe
#df_marks = df_marks.append(nueva_fila, ignore_index=True)
    
    # pid = df.iloc[0,2]
    # event = 3
    # consultFinal = df
    # for index, aa in df.iterrows():
    #     if aa[1] !=0 and event ==0:
    #         index1= index - timedelta(seconds=1)
    #         consultFinal.loc[index1] = aa[0], 0, aa[2]
    #         consultFinal = consultFinal.sort_index()
    #     event = aa[1]
    # return consultFinal



def create_dataframe(df,id):
    names=df["uniquename"].unique()
    for name in names:
        consult=df[df['uniquename']==name]
        pid = consult.iloc[0,2]
        if pid==id:
            break
    return consult
        

    

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
'''  LEYENDA
3:start
2:running
1:warning
0:fail
'''

'''
plt.margins(0.2)

for date in [['2022-12-12','2022-12-13'],['2022-12-13','2022-12-14'],['2022-12-14','2022-12-15']]:
    for procces in  main_name_process:

        df=query_general(sql_template4,nodes_name[11],procces,date[0],date[1])
        new_df=df.loc[:, ['uniquename', 'timestamp_occured','event', 'pid']]
        new_df.set_index('timestamp_occured', inplace = True)
        new_df['event'].replace(['start', 'running','warning','fail'],[3, 2,1,0], inplace=True)
        
        create_dataframe(new_df,procces)

'''

df=query_general(sql_template4,nodes_name[11],main_name_process[0],date[0][0],date[0][1])
# pids=df["pid"].unique()
# print(df)
# print(pids)
dataframe=create_dataframe(df,1178)
# print(dataframe.iloc[0,0])
# print(dataframe.iloc[0,1])
# print(dataframe.iloc[0,2])
# print(dataframe.index)
#print(dataframe.index)
#newDf(dataframe)
#df.columns.get_loc('Fee'))
print(dataframe)
#dfi = dataframe.reset_index()
#print(dfi)
#print(newDf(dataframe))
# for index, aa in dataframe.iterrows():
#     #print(index)
#     print(aa.iloc[1])


