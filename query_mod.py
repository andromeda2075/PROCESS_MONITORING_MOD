
import time
import datetime       
import mysql.connector
import sys
import string
import pandas as pd


class queries():
    event=''
    first=''
    end=''
    path=''
    file_name=''

    
    def __init__(self,inicio,termino,evento,file_name):
        self.first=inicio
        self.end=termino
        self.event=evento
        self.file_name=file_name


        
    def consult(self,firts,end,event):
        mysql_db=mysql.connector.connect(
            host='localhost',
            user='pruebas2022',
            #user='root',
            password='pruebas2022',
            database='pruebas2022'
        )
        selection="SELECT node_name, process_name, event, COUNT(*) FROM monitored where event ={} and process_name not in ('sleep', 'sh', 'aterm', 'guishow.sh','fluxbox') and timestamp_occured BETWEEN {} AND {} GROUP BY node_name,process_name,event order by (node_name);"
        comand_process=selection.format(event,firts, end)
        # Pasando a pandas
        db = pd.read_sql(comand_process,mysql_db)
        mysql_db.close() #close the connection

        return db


    def export(self,firts,end,event,file_name,db):
        name=file_name.split('.txt')
        name_table=end+'_'+ event+'_'+name[0]
        by_count = db.sort_values('COUNT(*)',ascending=False)
        extension=name_table+'.xlsx'
        by_count.to_excel(extension)  
        




