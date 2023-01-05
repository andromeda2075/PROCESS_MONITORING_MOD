import sqlite3
import time
import threading
import os

'''
    !La clase padre repository cuyos métodos
    establecen los cuatro estados de los procesos como son:
    start,running,fail y warning, además de los métodos 
    correspondientes a la salud del sistema encargadas de establecer 
    los estados normal y warning.
'''
class Repository:

    ''' !Constructor del objeto repositorio'''
    def __init__(self):
        print('se ha creado el repositorio')

    ''' !Métodos correspondientes al monitoreo de los procesos''' 

    def log_start_process(self,proc):
        print(proc.name(),"se registra inicio del proceso")

    def log_running_process(self,proc):
        print(proc.name(),"se registra consumo del proceso")

    def log_fail_process(self,name,pid):
        print(name, "se registra caida del proceso. Ultimo PID=",pid)

    def log_warning_process(self,name,pid,consume_cpu,consume_memory):
        print("Se registra un warning")
    
    def log_zombie_process(self,name,pid):
        print("Proceso ZOMBIE")

    '''
        !Métodos correspondientes a la salud del sistema
    '''
    def log_normal_pc_info(self,cpu,memory,used_memory):
        print('Normal PC')

    def log_warning_pc_info(self,cpu,memory,used_memory):
        print('Alerta PC')
'''
    !Clase hija encargada de crear las tablas y escribir en ellas
    los registros obtenidos de los procesos y salud del sistema.
'''
class SqliteRepository(Repository):

    '''
        !Los atributos de la clase hija son:

            @ param dbName: variable que almacena el nombre de la base de datos cuya extensión es .db
            @ param con: variable que representa al objeto Connection que representa la base de datos.
            @ param cur:variable que almacena la instancia Cursor
            @ param lock:  gestiona un contador interno que se reduce con cada llamada de acquire()
            y se incrementa con cada llamada de release() de la libreria threading.
            @ param max_register:numero de registros máximos
            @ param url_prefix: variable que almacena la ruta donde se almacenará la base de datos

    '''

    dbName=""
    con = 0
    cur = 0
    lock = 0
    is_ring = False
    max_register = -1
    url_prefix = "/var/local/monitor/" 
    
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
       

        # Creación de la Tabla 1 de monitoreo de procesos

        res = self.cur.execute("SELECT name FROM sqlite_master WHERE name='monitored'")
        if res.fetchone() is None:
            print("monitored: tabla no existe")
            self.cur.execute("CREATE TABLE monitored(name,timestamp,event, pid, cpu_percent, memory_Mb)")
        else:
            print("Monitored: tabla existe")

        # Creación de la Tabla 2 de la salud del sistema: cpu %, memoria %, disco %, Temperaturas por cada nucleo

        res1 = self.cur.execute("SELECT name FROM sqlite_master WHERE name='PC'")  
        if res1.fetchone() is None:
            print("PC: tabla no existe")
            self.cur.execute("CREATE TABLE PC(cpu_used,memory_used,disk_used,Status_PC_cpu_disk_memory,Cores_temperatures,Cores_status_temperature,Timestamp)")
        else:
            print("PC: tabla existe")

        # Creación del trigger cuando ring es igual a TRUE 

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
            
    #   Desarrollo de cada método definido en la clase repository

    def log_start_process(self,name,pid,consume_cpu,consume_memory):

        """ !Método que inicia el proceso """

        self.lock.acquire()
        data = [
            (name, time.time(),"start",pid,consume_cpu ,round(consume_memory,2)),
        ]
        self.cur.executemany("INSERT INTO monitored VALUES(?, ?, ?, ?, ?, ?)", data)
        self.con.commit()
        self.lock.release()
        

    def log_warning_process(self,name,pid,consume_cpu,consume_memory):
        
        self.lock.acquire()
        data = [
            (name, time.time(),"warning",pid,consume_cpu ,round(consume_memory,2)),
        ]
        self.cur.executemany("INSERT INTO monitored VALUES(?, ?, ?, ?, ?, ?)", data)
        self.con.commit()
        self.lock.release()

        

    def log_running_process(self,name,pid,consume_cpu,consume_memory):

        """ !Método que registra el proceso """


        self.lock.acquire()
        data = [
            (name, time.time(),"running",pid,consume_cpu ,round(consume_memory,2)),
        ]
        self.cur.executemany("INSERT INTO monitored VALUES(?, ?, ?, ?, ?, ?)", data)
        self.con.commit()
        self.lock.release()
       
        

    def log_fail_process(self,name,pid,time_fail):

        """ ! Método que reporta la caida"""

        self.lock.acquire()
        data = [
            (name, time_fail,"fail",pid,0,0),
        ]
        self.cur.executemany("INSERT INTO monitored VALUES(?,?,?,?,?,?)", data)
        self.con.commit()
        self.lock.release()

    def log_zombie_process(self,name,pid,time_fail):

        """ ! Método que reporta un proceso Zombie """

        self.lock.acquire()
        data = [
            (name, time_fail,"zombie",pid,0,0),
        ]
        self.cur.executemany("INSERT INTO monitored VALUES(?,?,?,?,?,?)", data)
        self.con.commit()
        self.lock.release()
       

    """ ! Desarrollo de los métodos relacionados a la salud del sistema  """

    def log_normal_pc_info(self,cpu_usage,used_memory,disk_usage,t1,t2,timestamp):                               
        self.lock.acquire()
        data = [
            (cpu_usage,used_memory,disk_usage,'normal',t1,t2,timestamp)
        ]
        self.cur.executemany("INSERT INTO PC VALUES(?, ?, ?, ?,?,?,?)", data)
        self.con.commit()
        self.lock.release()
    
    def log_warning_pc_info(self,cpu_usage,used_memory,disk_usage,t1,t2,timestamp):
        self.lock.acquire()
        data = [
            (cpu_usage,used_memory,disk_usage,'warning',t1,t2,timestamp)
        ]
        self.cur.executemany("INSERT INTO PC VALUES(?,?,?,?,?,?,?)", data)
        self.con.commit()
        self.lock.release()

    
   

    
  

