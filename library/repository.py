import mysql.connector
from abc import abstractmethod

class Repository:
    @abstractmethod
    def insert_process_data(self,data):
        pass

    @abstractmethod
    def insert_system_data(self,data):
        pass

    @abstractmethod
    def commit(self,data):
        pass

    @abstractmethod
    def query(self,data):
        pass


class MysqlRepository(Repository):
    def __init__(self,hostname,databasename,username,passvalue):
        self.conMysql = mysql.connector.connect(
            host=hostname,
            user=username,
            password=passvalue,
            database=databasename
        )

        self.curMysql = self.conMysql.cursor()

        self.sqlInsertProcesses ="insert into monitored(node_name,timestamp_occured,process_name,event,pid,cpu_percent,memory_Mb)  values (%s,%s,%s,%s,%s,%s,%s)"
        self.sqlInsertPc ="insert into pc(node_name, timestamp_occured, cpu_used, memory_used, disk_used, status_pc,core_temperature, core_status_temperature) values (%s,%s,%s,%s,%s,%s,%s, %s)"

    def insert_process_data(self,data):
        self.curMysql.execute(self.sqlInsertProcesses,data)

    def insert_system_data(self,data):
        self.curMysql.execute(self.sqlInsertPc,data)
    
    def commit(self):
        self.conMysql.commit()

    def getCursor(self):
        return self.curMysql

    def getConnection(self):
        return self.conMysql