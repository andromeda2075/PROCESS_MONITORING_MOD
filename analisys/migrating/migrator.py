import sqlite3
import datetime

class Migrator:
    hostname=""
    dbName=""
    con = 0
    cur = 0

    def setup(self,table, dbfilename,hostname,formatFunction,insertFunction):
        self.formatFunction = formatFunction
        self.insertFunction = insertFunction
        self.tablename = table
        self.hostname = hostname
        self.dbName = dbfilename
        self.con = sqlite3.connect(self.dbName, check_same_thread=False)
        self.cur = self.con.cursor()
            
    def migrate(self):
        # print("SELECT name FROM sqlite_master WHERE name='{table}'".format(table=self.tablename))
        res = self.cur.execute("SELECT name FROM sqlite_master WHERE name='{table}'".format(table=self.tablename))
        if res.fetchone() is None:
            print("{table}: tabla NO existe".format(table=self.tablename))
        else:
            res = self.cur.execute("SELECT * FROM {table}".format(table=self.tablename))
            for row in res:
                datos=self.formatFunction(self.hostname,row)
                self.insertFunction(datos)



def formatProcessesData(hostname, row):
    timestamp = datetime.datetime.fromtimestamp(row[1]).strftime('%Y-%m-%d %H:%M:%S.%f')
    datos=(hostname,timestamp,row[0],row[2],row[3],row[4],row[5])
    return datos

def formatSystemData(hostname, row):
    timestamp = datetime.datetime.fromtimestamp(row[6]).strftime('%Y-%m-%d %H:%M:%S')
    datos=(hostname,timestamp,row[0],row[1],row[2],row[3],row[4],row[5])
    return datos