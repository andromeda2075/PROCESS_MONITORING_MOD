import sqlite3
import time
import datetime
import os        
import mysql.connector
import sys

class Mysqliterepository():
    hostname=""
    dbName=""
    con = 0
    cur = 0
    conMysql=0
    curMysql = 0

#total arguments

 def __init__(self):
        self.conMysql = mysql.connector.connect(
            host="localhost",
            user="pruebas2022",
            password="pruebas2022",
            database="pruebas2022"
        )

        self.curMysql = self.conMysql.cursor()
        


def setup(self,dbfilename,hostname):
        self.hostname = hostname
        self.dbName = dbfilename
        # if not os.path.exists(self.url_prefix):
        #     os.mkdir(self.url_prefix)
        self.con = sqlite3.connect(self.dbName, check_same_thread=False)
        self.cur = self.con.cursor()
            
def migrate(self):
        res = self.cur.execute("SELECT name FROM sqlite_master WHERE name='PC'")
        if res.fetchone() is None:
            print("pc: tabla NO existe")
        else:
            res = self.cur.execute("SELECT * FROM pc")
            for row in res:
                # node_name, cpu_used, memory_used, disk_used, status_pc,core_temperature, core_status_temperature,timestamp
                timestamp = datetime.datetime.fromtimestamp(row[6]).strftime('%Y-%m-%d %H:%M:%S')
                datos=(self.hostname,row[0],row[1],row[2],row[3],row[4],row[5],timestamp)
                #print(datos)
                self.curMysql.execute(self.sqlInsertPc,datos)
              
            self.conMysql.commit()  


n = len(sys.argv)
if n <= 1 :
    print("Debe ingresar el directorio a procesar")
    exit(0)
