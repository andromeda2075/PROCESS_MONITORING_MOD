import sqlite3
import time
import datetime
import os        
import mysql.connector
import sys
 
'''
CREATE TABLE pc(id int NOT NULL AUTO_INCREMENT, node_name varchar(30),cpu_used float , memory_used float , disk_used int , status_pc varchar(30),core_temperature text, core_status_temperature text ,timestamp_occured TIMESTAMP, PRIMARY KEY (id));
'''
class SqliteRepository:
    hostname=""
    dbName=""
    con = 0
    cur = 0
    conMysql=0
    curMysql = 0

    sqlInsertPc ="insert into pc(node_name, cpu_used, memory_used, disk_used, status_pc,core_temperature, core_status_temperature,timestamp_occured) values (%s,%s,%s,%s,%s,%s,%s, %s)"

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



