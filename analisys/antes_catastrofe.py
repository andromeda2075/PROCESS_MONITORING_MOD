
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

# Datos de entrada
# Ejercicios
intervalos = [
    ['2022-12-12 14:04:00', '2022-12-12 16:39:00'],
    ['2022-12-12 17:05:00', '2022-12-12 19:06:00'],
    ['2022-12-12 20:48:00', '2022-12-12 22:52:00'],
    ['2022-12-12 23:34:00', '2022-12-13 04:35:00'],
    ['2022-12-13 05:02:00', '2022-12-13 07:12:00'],
    ['2022-12-13 08:21:00', '2022-12-13 10:48:00'],
    ['2022-12-13 13:59:00', '2022-12-13 16:35:00'],
    ['2022-12-13 17:53:00', '2022-12-13 19:25:00'],
    ['2022-12-13 20:40:00', '2022-12-14 00:23:00'],
    ['2022-12-14 01:13:00', '2022-12-14 03:31:00'],
    ['2022-12-14 04:27:00', '2022-12-14 07:55:00'],
    ['2022-12-14 08:20:00', '2022-12-14 08:43:00'],
    ['2022-12-14 09:10:00', '2022-12-14 13:02:00'],
    ['2022-12-14 13:49:00', '2022-12-14 16:14:00'],
    ['2022-12-14 16:16:00', '2022-12-14 17:53:00'],
    ['2022-12-14 19:53:00', '2022-12-14 21:55:00'],
    ['2022-12-14 22:44:00', '2022-12-15 04:15:00']
]

banned_list = "('mandb', 'xrandr', 'dpkg', 'fluxbox', 'ssh-agent','sleep', 'sh', 'aterm', 'guishow.sh', 'gzip', 'man-db', 'logrotate', 'apt', 'apt-get', 'run-parts', 'pulseaudio')"

servidores = ['fm57-01', 'fm57-02', 'fm57-03', 'fm57-04', 'fm57-05',
              'fm57-06', 'fm57-07', 'fm57-08', 'fm57-09', 'fm57-10', 'fm57-11']

consolas = ['fm57-c01a', 'fm57-c01b', 'fm57-c02a', 'fm57-c02b', 'fm57-c03a', 'fm57-c03b', 'fm57-c04a', 'fm57-c04b', 'fm57-c06a', 'fm57-c06b',
            'fm57-c07a', 'fm57-c07b', 'fm57-c08a', 'fm57-c08b', 'fm57-c09a', 'fm57-c09b', 'fm57-t01']
bus_comunication = ['spliced', 'networking', 'durability', 'ospl']

sql_template = '''
select concat(node_name,"_",process_name,"_",pid) as uniquename, cpu_percent,memory_Mb,timestamp_occured,pid,event from monitored where node_name='{node_name}' 
and process_name='{name_process}' and timestamp_occured BETWEEN '{inicio}' AND '{fin}' order by timestamp_occured;
'''


def generate_pd_query(sql_query):
    mysql_db = mysql.connector.connect(
        host='localhost',
        user='prueba2022',
        # user='pruebas2022',
        password='SoporteVarayoc..2022',
        # password='pruebas2022',
        # database='testdata'
        database='pruebas2022'
    )
    df = pd.read_sql(sql_query, mysql_db)
    return df


def query_general(sql_consult, node_name, name_process, inicio, fin):
    query = sql_consult.format(
        name_process=name_process, node_name=node_name, inicio=inicio, fin=fin)
    df = generate_pd_query(query)
    new_df = df.loc[:, ['uniquename', 'timestamp_occured',
                        'event', 'pid', 'memory_Mb', 'cpu_percent']]
    new_df.set_index('timestamp_occured', inplace=True)
    new_df['event'].replace(['start', 'running', 'warning', 'fail'], [
                            3, 2, 1, 0], inplace=True)
    return new_df


def create_dataframe(df, id):
    df = df.reset_index()
    names = df["uniquename"].unique()
    for name in names:
        consult = df[df['uniquename'] == name]
        pid = consult.iloc[0, 3]
        if pid == id:
            print(pid)
            break
    return consult


def plotMemory(df, process, node_name, pid):
    # df = df.reset_index()
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
    title = 'PID: '+str(pid)
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


intervalos1_consola = [['2022-12-13 05:02:00', '2022-12-13 07:12:00'],
                       ['2022-12-13 13:59:00', '2022-12-13 16:35:00'],
                       ['2022-12-13 17:53:00', '2022-12-13 19:25:00'],
                       ['2022-12-14 19:53:00', '2022-12-14 21:55:00']
                       ]

intervalos2_consola = [['2022-12-13 08:21:00', '2022-12-13 10:48:00']]


intervalos3_consola = [['2022-12-12 20:48:00', '2022-12-12 22:52:00'],
                       ['2022-12-12 23:34:00', '2022-12-13 04:35:00'],
                       ['2022-12-13 20:40:00', '2022-12-14 00:23:00']
                       ]


intervalos4_consola = [['2022-12-12 20:48:00', '2022-12-12 22:52:00'],
                       ['2022-12-14 19:53:00', '2022-12-14 21:55:00'],
                       ['2022-12-14 13:49:00', '2022-12-14 16:14:00'],
                       ['2022-12-14 22:44:00', '2022-12-15 04:15:00'],
                       ['2022-12-13 08:21:00', '2022-12-13 10:48:00'],
                       ['2022-12-13 20:40:00', '2022-12-14 00:23:00']
                       ]


intervalos5_consola = [['2022-12-12 20:48:00', '2022-12-12 22:52:00'],
                       ['2022-12-12 23:34:00', '2022-12-13 04:35:00'],
                       ['2022-12-13 13:59:00', '2022-12-13 16:35:00'],
                       ['2022-12-13 20:40:00', '2022-12-14 00:23:00'],
                       ['2022-12-14 22:44:00', '2022-12-15 04:15:00'],
                       ['2022-12-14 19:53:00', '2022-12-14 21:55:00']]


intervalos6_consola = [['2022-12-12 23:34:00', '2022-12-13 04:35:00'],
                       ['2022-12-13 17:53:00', '2022-12-13 19:25:00'],
                       ['2022-12-13 20:40:00', '2022-12-14 00:23:00'],
                       ['2022-12-14 09:10:00', '2022-12-14 13:02:00'],
                       ['2022-12-14 13:49:00', '2022-12-14 16:14:00'],
                       ['2022-12-14 19:53:00', '2022-12-14 21:55:00'],
                       ['2022-12-14 22:44:00', '2022-12-15 04:15:00']]

intervalos7_consola = [['2022-12-13 08:21:00', '2022-12-13 10:48:00']]

intervalos8_consola = [['2022-12-12 20:48:00', '2022-12-12 22:52:00'],
                       ['2022-12-12 23:34:00', '2022-12-13 04:35:00'],
                       ['2022-12-13 08:21:00', '2022-12-13 10:48:00'],
                       ['2022-12-13 13:59:00', '2022-12-13 16:35:00'],
                       ['2022-12-13 17:53:00', '2022-12-13 19:25:00'],
                       ['2022-12-13 20:40:00', '2022-12-14 00:23:00'],
                       ['2022-12-14 13:49:00', '2022-12-14 16:14:00'],
                       ['2022-12-14 19:53:00', '2022-12-14 21:55:00']
                       ]


intervalos9_consola = [['2022-12-12 20:48:00', '2022-12-12 22:52:00'],
                       ['2022-12-12 23:34:00', '2022-12-13 04:35:00'],
                       ['2022-12-13 05:02:00', '2022-12-13 07:12:00'],
                       ['2022-12-13 17:53:00', '2022-12-13 19:25:00'],
                       ['2022-12-13 20:40:00', '2022-12-14 00:23:00'],
                       ['2022-12-14 13:49:00', '2022-12-14 16:14:00'],
                       ['2022-12-14 19:53:00', '2022-12-14 21:55:00'],
                       ['2022-12-14 22:44:00', '2022-12-15 04:15:00']
                       ]


consola = 'fm57-c01b'

for process in bus_comunication:
    print('.....................', process)
    for date in intervalos1_consola:
        print('CATASTROFE EN: ', date[1])
        df = query_general(sql_template, consola, process, date[0], date[1])
        print('Registros= ', df.shape)
        pids = df["pid"].unique()
        print('****** PIDs: ', pids)
        for id in pids:
            df2 = create_dataframe(df, id)
            plotMemory(df2, process, consola, id)

