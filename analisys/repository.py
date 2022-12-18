import mysql.connector
from abc import abstractmethod

class Repository:
    @abstractmethod
    def insert_process_data(self,data):
        pass

    @abstractmethod
    def insert_system_data(self,data):
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

        self.sqlInsertProcesses ="insert into monitored(node_name,process_name,timestamp_occured,event,pid,cpu_percent,memory_Mb)  values (%s,%s,%s,%s,%s,%s,%s)"
        self.sqlInsertPc ="insert into pc(node_name, cpu_used, memory_used, disk_used, status_pc,core_temperature, core_status_temperature,timestamp_occured) values (%s,%s,%s,%s,%s,%s,%s, %s)"

    def insert_process_data(self,data):
        self.curMysql.execute(self.sqlInsertProcesses,data)

    def insert_system_data(self,data):
        self.curMysql.execute(self.sqlInsertPc,data)