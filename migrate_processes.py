import sqlite3
import time
import datetime
import os        
import mysql.connector
import sys
 

'''
CREATE TABLE monitored(id int NOT NULL AUTO_INCREMENT, node_name varchar(30),process_name VARCHAR(30),timestamp_occured TIMESTAMP,event varchar(20), pid INT, cpu_percent FLOAT, memory_Mb FLOAT, PRIMARY KEY (id)) 
'''
class SqliteRepository:
    hostname=""
    dbName=""
    con = 0
    cur = 0
    conMysql=0
    curMysql = 0

    sqlInsertProcesses ="insert into monitored(node_name,process_name,timestamp_occured,event,pid,cpu_percent,memory_Mb)  values (%s,%s,%s,%s,%s,%s,%s)"

    url_prefix = "./backups" # Ruta de donde se extraerà la base de datos

    
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
        res = self.cur.execute("SELECT name FROM sqlite_master WHERE name='monitored'")
        if res.fetchone() is None:
            print("monitored: tabla NO existe")
        else:
            res = self.cur.execute("SELECT * FROM monitored")
            for row in res:
                #print(row[1])
                seconds = int(row[1])
                timestamp = datetime.datetime.fromtimestamp(row[1]).strftime('%Y-%m-%d %H:%M:%S')
                #print(timestamp)
                datos=(self.hostname,row[0],timestamp,row[2],row[3],row[4],row[5])
                self.curMysql.execute(self.sqlInsertProcesses,datos)
              
            self.conMysql.commit()  

# total arguments
n = len(sys.argv)
if n <= 1 :
    print("Debe ingresar el directorio a procesar")
    exit(0)

basepath=sys.argv[1]

transaction =  SqliteRepository()

directory_list1 = os.listdir(basepath)
directory_list1.sort()
for e in directory_list1:
    if os.path.isdir(os.path.join(basepath,e)):
        for f in os.listdir(os.path.join(basepath,e)):
            if os.path.isdir(os.path.join(basepath,e,f)):
                for g in os.listdir(os.path.join(basepath,e,f)):
                    if os.path.isfile(os.path.join(basepath,e,f,g)):
                        print(os.path.join(basepath,e,f,g))
                        # print(f)
                        unidad=f.split('.')[0]
                        #print(unidad)
                        transaction.setup(os.path.join(basepath,e,f,g), unidad)
                        transaction.migrate()

exit(0)