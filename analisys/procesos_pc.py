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
import ast

# 28 nodes
nodes_name = ['fm57-01', 'fm57-02', 'fm57-03', 'fm57-04', 'fm57-05', 'fm57-06', 'fm57-07', 'fm57-08', 'fm57-09', 'fm57-10', 'fm57-11',
              'fm57-c01a', 'fm57-c01b', 'fm57-c02a', 'fm57-c02b', 'fm57-c03a', 'fm57-c03b', 'fm57-c04a', 'fm57-c04b', 'fm57-c06a', 'fm57-c06b',
              'fm57-c07a', 'fm57-c07b', 'fm57-c08a', 'fm57-c08b', 'fm57-c09a', 'fm57-c09b', 'fm57-t01']

# Principales procesos a analizar
main_name_process = ['GuiDisplay-run', 'GuiDisplaySec-run', 'EcRegMsg', 'networking', 'Rms-node-run',
                     'GuiRootPanel-run', 'GuiSoundWarnings-run', 'Radar-osiris-run', 'durability', 'ospl', 'spliced']

date = [['2022-12-12', '2022-12-13'], ['2022-12-13',
                                       '2022-12-14'], ['2022-12-14', '2022-12-15']]

sql_template_proc = '''
select concat(node_name,"_",process_name,"_",pid) as uniquename, node_name,cpu_percent,memory_Mb,timestamp_occured,pid,event from monitored where node_name='{node_name}' 
and process_name='{name_process}' and timestamp_occured BETWEEN '{inicio}' AND '{fin}' order by timestamp_occured;
'''
sql_template_pc = '''
select  node_name,cpu_used,memory_used,disk_used,status_pc,core_temperature,core_status_temperature,timestamp_occured from pc where node_name='{node_name}' 
and timestamp_occured BETWEEN '{inicio}' AND '{fin}' order by timestamp_occured;   
'''


def generate_pd_query(sql_query):
    mysql_db = mysql.connector.connect(
        # host='localhost',
        user='prueba2022',
        # user='pruebas2022',
        password='SoporteVarayoc..2022',
        # password='pruebas2022',
        database='testdata'
        # database='pruebas2022'
    )
    df = pd.read_sql(sql_query, mysql_db)
    return df


def query_general_proc(sql_consult, node_name, name_process, inicio, fin):
    query = sql_consult.format(
        name_process=name_process, node_name=node_name, inicio=inicio, fin=fin)
    df = generate_pd_query(query)
    new_df = df.loc[:, ['uniquename', 'timestamp_occured',
                        'event', 'pid', 'memory_Mb', 'cpu_percent']]
    new_df.set_index('timestamp_occured', inplace=True)
    new_df['event'].replace(['start', 'running', 'warning', 'fail'], [
                            3, 2, 1, 0], inplace=True)
    return new_df


def query_general_pc(sql_consult, node_name, inicio, fin):
    query = sql_consult.format(node_name=node_name, inicio=inicio, fin=fin)
    df = generate_pd_query(query)
    df.set_index('timestamp_occured', inplace=True)
    '''
    def lista(string):
        return ast.literal_eval(string)
    serie = df.loc[:, 'core_temperature']
    serie.apply(lista)
    '''
    return df


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


def interpolate(df_proc, df_pc):

    start1 = datetime(2022, 12, 12, 13, 29, 0)
    end1 = datetime(2022, 12, 12, 23, 58, 59)

    index1 = pd.date_range(start1, end1, freq="s")
    columnas = ['uniquename', 'node_name', 'event', 'pid', 'memory_Mb',
                'cpu_percent', 'cpu_used', 'memory_used', 'core_temperature']

    df_empty = pd.DataFrame(columns=columnas, index=index1)
    df_empty.index.names = ['timestamp_occured']

    new_df = pd.merge(df_empty.set_index('timestamp_occured'), df_pc.set_index('timestamp_occured'), how='outer',
                      left_index=True, right_index=True, suffixes=['_proc', '_pc'], indicator=True)
    return new_df

    '''
    start2=datetime.datetime(2022,12,13,0,0,0)
    end2=datetime.datetime(2022,12,13,23,59,59)

    start3=datetime.datetime(2022,12,14,0,0,0)
    end3=datetime.datetime(2022,12,14,23,59,59)

    '''


df_pc = query_general_pc(
    sql_template_pc, nodes_name[11], date[2][0], date[2][1])
df_proc = query_general_proc(
    sql_template_proc, nodes_name[11], main_name_process[0], date[2][0], date[2][1])


'''
def lista(string):
    L=ast.literal_eval(string)
    return L
serie = df_pc.loc[:, 'core_temperature']
new=serie.apply(lista)
for j in new:
    h=[float(i) for i in j]
    tam=len(h)
    for m in range(tam):
        title='core_'+str(m+1)
        a=list()
        a.append(h[m])
    print(h)
'''
'''
#print(df_pc.loc[0,:])
m,_=df_proc.shape
n,_=df_pc.shape
print(n)
print(df_proc.iloc[0])
print(df_proc.iloc[m-1])
print('-------------------------------------')
print(df_pc.iloc[0])
print(df_pc.iloc[n-1])
#print(df_proc.loc[-1,:])

'''
print(interpolate())
