import sqlite3
import time
import datetime       
import mysql.connector
import sys
import xlsxwriter
import string


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
        #self.path=ruta

        
    def consult (self,firts,end,event):
        mysql_db=mysql.connector.connect(
            host='localhost',
            #user='pruebas2022',
            user='root',
            password='pruebas2022',
            database='pruebas2022'
        )

        selection = "SELECT node_name, process_name, event, COUNT(*)  FROM monitored and process_name not in ('sleep', 'sh', 'aterm', 'guishow.sh','fluxbox') and timestamp_occured BETWEEN {} AND {} GROUP BY node_name, process_name, event order by (node_name);"
        comand_process=selection.format(firts, end)
        mysql_db_cur=mysql_db.cursor()
        mysql_db_cur.execute(comand_process)

        header=[row[0] for row in mysql_db_cur.description]
        rows=mysql_db_cur.fetchall()
        mysql_db.close()

        return header, rows


    def export(self,firts,end,event,file_name):
        name_table= firts+'_'+end+'_'+event+'_'+file_name
        workbook = xlsxwriter.Workbook(name_table + '.xlsx')
        worksheet = workbook.add_worksheet('MENU')

        header_cell_format = workbook.add_format({'bold': True, 'border': True, 'bg_color': 'yellow'})
        body_cell_format = workbook.add_format({'border': True})

        header, rows = self.consult(firts,end,event)

        row_index = 0
        column_index = 0

        for column_name in header:
            worksheet.write(row_index, column_index, column_name, header_cell_format)
            column_index += 1

        row_index += 1
        for row in rows:
            column_index = 0
            for column in row:
                worksheet.write(row_index, column_index, column, body_cell_format)
                column_index += 1
            row_index += 1

        print(str(row_index) + ' rows written successfully to ' + workbook.filename)

        # Closing workbook
        workbook.close()

