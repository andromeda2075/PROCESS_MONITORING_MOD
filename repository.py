import sqlite3
import time
import threading
import os


class Repository:
    def __init__(self):
        print('se ha creado el repositorio')
        
    def log_start_process(self,proc):
        #tiempo_inicial=datetime.fromtimestamp(proc.create_time()).strftime('%H:%M:%S')
        print(proc.name(),"se registra inicio del proceso")

    def log_running_process(self,proc):
        #tiempo_inicial=datetime.fromtimestamp(proc.create_time()).strftime('%H:%M:%S')
        print(proc.name(),"se registra consumo del proceso")

    def log_fail_process(self,name,pid):
        print(name, "se registra caida del proceso. Ultimo PID=",pid)

    def log_warning_process(self,name,pid,consume_cpu,consume_memory):
        print("Se registra un warning")
#################################################
#################### DE LA PC ##################
    def log_normal_pc_info(self,cpu,memory,used_memory):
        print('Normal PC')

    def log_warning_pc_info(self,cpu,memory,used_memory):
        print('Alerta PC')
 
class SqliteRepository(Repository):
    dbName=""
    con = 0
    cur = 0
    lock = 0
    is_ring = False
    max_register = -1
    url_prefix = "/var/local/monitor/" # Ruta de donde se extraerà la base de datos
    
    def __init__(self,name,ring=False,max_register=-1):
        super().__init__()
        self.dbName = name
        if not os.path.exists(self.url_prefix):
            os.mkdir(self.url_prefix)
        self.con = sqlite3.connect(self.url_prefix + self.dbName, check_same_thread=False)
        self.cur = self.con.cursor()
        self.lock = threading.Semaphore()
        self.is_ring=ring
        self.max_register = max_register
        print(ring,max_register)
        # TABLA 1: MONITOREO DE PROCESOS
        res = self.cur.execute("SELECT name FROM sqlite_master WHERE name='monitored'")
        if res.fetchone() is None:
            print("monitored: tabla no existe")
            self.cur.execute("CREATE TABLE monitored(name,timestamp,event, pid, cpu, memory)")
        else:
            print("monitored: tabla existe")

        # TABLA 2: SALUD DE LA PC : CPU, MEMORIA, DISCO, CORES
        res1 = self.cur.execute("SELECT name FROM sqlite_master WHERE name='PC'")  # TABLA PARA LA PC
        if res1.fetchone() is None:
            print("PC: tabla no existe")
            self.cur.execute("CREATE TABLE PC(cpu_used,disk_used,memory_used,status,cores_temperatures,cores_status)")
        else:
            print("PC: tabla existe")

        # TODO crear el trigger cuando ring es igual a TRUE ( PREGUNTAR)
        if self.is_ring and self.max_register>0 :
            self.cur.execute("select * from sqlite_master where type = 'trigger' and name='delete_tail_monitored'")
            if res.fetchone() is None :
                print("Trigger delete_tail no existe")
                sentence1 = "CREATE TRIGGER delete_tail_monitored AFTER INSERT ON monitored BEGIN DELETE FROM monitored where rowid < NEW.rowid-"
                sentence2= str(self.max_register)
                sentence3="; END"
                sentence=sentence1+sentence2+sentence3
                print(sentence)
                self.cur.execute(sentence)
            else:
                print("Trigger delete_tail  existe")

            self.cur.execute("select * from sqlite_master where type = 'trigger' and name='delete_tail_pc'")
            if res1.fetchone() is None: 
                print("Trigger delete_tail no existe")
                sentence1 = "CREATE TRIGGER delete_tail_pc AFTER INSERT ON PC BEGIN DELETE FROM PC where rowid < NEW.rowid-"
                sentence2= str(self.max_register)
                sentence3="; END"
                sentence=sentence1+sentence2+sentence3
                print(sentence)
                self.cur.execute(sentence)
            else:
                  print("Trigger delete_tail_pc  existe")
            

    def log_start_process(self,proc):
        """Método que inicia el proceso"""
        self.lock.acquire()
        data = [
            (proc.name(), proc.create_time(),"start", proc.pid,proc.cpu_percent(interval=None),round(proc.memory_percent())),
        ]
        self.cur.executemany("INSERT INTO monitored VALUES(?, ?, ?, ?, ?, ?)", data)
        self.con.commit()
        self.lock.release()
        print()
        print('Se registra inicio del proceso {} con {}% y memoria {}%'.format(proc.name(),proc.cpu_percent(),round(proc.memory_percent(),2)))        
 
 # AQUÌ GUARDARRR

    def log_warning_process(self,name,pid,consume_cpu,consume_memory):
        
        self.lock.acquire()
        data = [
            (name, time.time(),"warning",pid,consume_cpu ,round(consume_memory,2)),
        ]
        self.cur.executemany("INSERT INTO monitored VALUES(?, ?, ?, ?, ?, ?)", data)
        self.con.commit()
        self.lock.release()
        print('WARNIG PROCESS WITH PID:  {}, cpu {}%,memoria{}%'.format(pid,consume_cpu,round(consume_memory,2)))

    def log_running_process(self,proc):
        """Método que registra el proceso"""
        self.lock.acquire()
        data = [
            (proc.name(), time.time(),"runnig",proc.pid, proc.cpu_percent(interval=None),round(proc.memory_percent())),
        ]
        self.cur.executemany("INSERT INTO monitored VALUES(?, ?, ?, ?, ?, ?)", data)
        self.con.commit()
        self.lock.release()
        print('se registra el proceso, PID: {}, cpu {}%,memoria{}%'.format(proc.pid,proc.cpu_percent(),round(proc.memory_percent(),2)))
# VERIFICARRRRRRR
    def log_fail_process(self,name,pid,time_fail):
        """Método que reporta la caida"""
        self.lock.acquire()
        data = [
            (name, time_fail,"fail",pid,0,0),
        ]
        self.cur.executemany("INSERT INTO monitored VALUES(?,?,?,?,?,?)", data)
        self.con.commit()
        self.lock.release()

## ---------------------------------PC HEALTH---------------------------
##----------------------------------------------------------------
   
    def log_normal_pc_info(self,cpu_usage,used_memory,disk_usage,t1,t2):                               
        self.lock.acquire()
        data = [
            (cpu_usage,used_memory,disk_usage,'normal',t1,t2)
        ]
        self.cur.executemany("INSERT INTO PC VALUES(?, ?, ?, ?,?,?)", data)
        self.con.commit()
        self.lock.release()
    
    def log_warning_pc_info(self,cpu_usage,used_memory,disk_usage,t1,t2):
        self.lock.acquire()
        data = [
            (cpu_usage,used_memory,disk_usage,'warning',t1,t2)
        ]
        self.cur.executemany("INSERT INTO PC VALUES(?, ?, ?, ?,?,?)", data)
        self.con.commit()
        self.lock.release()
#---------------------------------------------------------------------------------------
    
   

    
  

