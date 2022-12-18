import sqlite3
import datetime
import os        
import sys
import repository
 

class SqliteRepository:
    hostname=""
    dbName=""
    con = 0
    cur = 0

    def __init__(self):
        self.repository = repository.MysqlRepository("localhost","pruebas2022","pruebas2022","pruebas2022")

    def setup(self,dbfilename,hostname):
        self.hostname = hostname
        self.dbName = dbfilename
        self.con = sqlite3.connect(self.dbName, check_same_thread=False)
        self.cur = self.con.cursor()
            
    def migrate(self):
        res = self.cur.execute("SELECT name FROM sqlite_master WHERE name='PC'")
        if res.fetchone() is None:
            print("pc: tabla NO existe")
        else:
            res = self.cur.execute("SELECT * FROM pc")
            for row in res:
                timestamp = datetime.datetime.fromtimestamp(row[6]).strftime('%Y-%m-%d %H:%M:%S')
                datos=(self.hostname,row[0],row[1],row[2],row[3],row[4],row[5],timestamp)
                self.repository.insert_system_data(datos)
              
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



