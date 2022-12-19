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

    
    def __init__(self,inicio,termino,evento):
        self.first=inicio
        self.end=termino
        self.event=evento
        #self.path=ruta

    '''    

    def datebyline(self.path_file):
        dates=list()
        os.chdir(self.path_file)
        with open(self.path_file) as f:
            lines=f.readlines()
        for line in lines:		
            if line!='\n':
                dates.append(line.split())
        return dates	
    '''
        
    def consult (self,firts,end,event):
        mysql_db=mysql.connector.connect(
            host='localhost',
            #user='pruebas2022',
            user='root',
            password='pruebas2022',
            database='pruebas2022'
        )
        comand_one_process= "SELECT node_name, process_name, event, COUNT(*) FROM monitored  where event="
        comand_two_process= " and process_name not in ('sleep', 'sh', 'aterm', 'guishow.sh') and timestamp_occured BETWEEN "
        comand_three_process= " AND "
        comand_four_process=" GROUP BY node_name,process_name, event order by (node_name)"

        comand_process_start=comand_one_process+event+comand_two_process+firts+comand_three_process+end+comand_four_process

        mysql_db_cur=mysql_db.cursor()
        mysql_db_cur.execute(comand_process_start)

        header=[row[0] for row in mysql_db_cur.description]
        rows=mysql_db_cur.fetchall()
        mysql_db.close()

        return header, rows


    def export(self,firts,end,event):
        name_table= firts+'_'+end+'_'+event
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

