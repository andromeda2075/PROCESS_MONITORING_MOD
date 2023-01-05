
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
import time     
import mysql.connector
import sys
from datetime import datetime, timedelta
import string
from sqlalchemy import create_engine
from sqlalchemy.sql import text
# ver doc https://docs.sqlalchemy.org/en/14/glossary.html#term-2.0-style
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html
# https://medium.com/analytics-vidhya/analysis-of-time-series-data-dad4afa56358
# https://www.machinelearningplus.com/time-series/time-series-analysis-python/
# https://towardsdatascience.com/the-complete-guide-to-time-series-analysis-and-forecasting-70d476bfe775
# https://towardsdatascience.com/work-with-sql-in-python-using-sqlalchemy-and-pandas-cd7693def708
# para instalar pip install SQLAlchemy
# La version debe ser >=2.0+
# poner future necesariamente para usar la version 2.0
engine = create_engine("mysql+mysqlconnector://root:pruebas2022@localhost/pruebas2022", future=True)
# consultas

def generate_pd_query(sql_query,control=engine):
    with control.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(text(sql_query))  
        df = pd.DataFrame(query.fetchall())
    return df

banned_list="('mandb', 'xrandr', 'dpkg', 'fluxbox', 'ssh-agent','sleep', 'sh', 'aterm', 'guishow.sh', 'gzip', 'man-db', 'logrotate', 'apt', 'apt-get', 'run-parts', 'pulseaudio')"


# query_total_start_process_node=sql_template.format(event='fail',inicio=init,fin=intervalo[1])

#df=generate_pd_query(sql_monitored)
#print(df.head(9))

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


def query_pd(time_end,control_time,event,banned_list,control=engine):
    date=new_date(time_end)
    format_data= "%d/%m/%y %H:%M:%S"
    end_time = datetime.strptime(date, format_data)
    time= end_time - timedelta(seconds=control_time)
    
    sql_template = '''
        SELECT node_name, process_name, event,timestamp_occured FROM monitored 
        where event='{event}' and process_name not in {banned} and timestamp_occured BETWEEN '{inicio}' AND '{fin}' 
        GROUP BY node_name,process_name, event order by (node_name);
    '''
    query=sql_template.format(event=event,banned=banned_list,inicio=time,fin=time_end)
    print(query)
    df=generate_pd_query(query,control=engine)
    return df


def print_df(df,n):
    print(df.head(n))
#----------------------------------------

## parametros

time_end='2022-12-12 16:39:00'
control_time=600 # 10 minutes
event='fail'
df=query_pd(time_end,control_time,event,banned_list)

print_df(df,10)    

#def plotSeries(df,End,control_time,query):