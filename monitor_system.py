import psutil
import threading
import configuration
import time

################# MODIFICARRRRRR ###############
# https://git-scm.com/book/es/v2/Inicio---Sobre-el-Control-de-Versiones-Acerca-del-Control-de-Versiones
# https://pypi.org/project/psutil/3.4.2/
# https://pypi.org/project/psutil/3.4.2/
#  https://pypi.org/project/psutil/
#https://pypi.org/search/?c=Programming+Language+%3A%3A+Python+%3A%3A+Implementation+%3A%3A+CPython
#https://ellibrodepython.com/herencia-en-python
#https://lyz-code.github.io/blue-book/architecture/repository_pattern/
#https://www.geeksforgeeks.org/python-get-list-of-running-processes/
#https://geekytheory.com/obtener-datos-de-la-cpu-en-linux-de-8-formas-diferentes/
#https://geekflare.com/es/process-cpu-memory-monitoring/
#https://www.youtube.com/watch?v=YSDS1ICiHI0
#https://www.folkstalk.com/tech/how-to-get-current-cpu-and-ram-usage-in-python-with-code-examples/
#https://schedule.readthedocs.io/en/stable/
#https://programmerclick.com/article/66681141470/
#https://github.com/giampaolo/psutil/blob/master/scripts/disk_usage.py
#https://micro.recursospython.com/recursos/como-obtener-el-espacio-del-disco.html
#https://hetpro-store.com/TUTORIALES/compilar-cpp-g-linux-en-terminal-leccion-1/
# https://github.com/giampaolo/psutil/blob/master/scripts/temperatures.py
## Alerta RAM >60%
## Alerta CPU TOTAL  >50%
## Alerta de CONSUMO > 80%
## TEMPERATURA
##  NORMAL 20-70 Cº
## Alerta MAXIMO > 81Cª
## TEMPERATURA EN PARTICIONES 
  # REPOSO 24-35 
  # NORMAL 42-52
  # MAX   72


class SystemInfo(threading.Thread):
    m_repository=0
    m_isRunning=False
    pc_list=[0,0,0,0,0]
    max_disk=0
    max_cpu= 0
    max_memory=0
    max_temperature=0
    pc_period_loging=0
    pc_period_verification=0
    time_loging_pc=0
   

    def PCsetConfiguration(self,repository,disk,cpu,memory,period_verification,loging_time):
        self.m_repository=repository
        self.pc_period_verification=period_verification
        self.max_cpu=cpu
        self.max_memory=memory
        self.max_disk=disk
        #self.max_temperature=pc_temperature
        self.pc_period_loging=loging_time

    #FUNCION bytes_to_megabytes
    def get_size(self, bytes ):
        return bytes/1024**2

    def pc_monitor(self):
        total_cpu=psutil.cpu_percent() # intervalo de actualizacion uso de procesadores CORREGIR
        memory=psutil.virtual_memory()
        used_memory=self.get_size(memory.used) 
        total_memory=memory.percent  # corregir
        #temps=psutil.sensors_temperatures()
        
        if total_cpu>self.max_cpu or used_memory>self.consume_memory:
            self.m_repository.log_warning_pc_info(total_cpu,total_memory,used_memory)
        else:
            if time.time()> self.time_loging_pc: 
                self.time_loging_pc = time.time() + self.pc_period_loging
                self.m_repository.log_normal_pc_info(total_cpu,total_memory,used_memory)
            

    def run(self):
        self.m_isRunning=True
        event = threading.Event()
        while (self.m_isRunning):
            self.pc_monitor()
            event.wait(self.pc_period_verification) 

        
    def set_repository(self,repository):
        self.m_repository=repository



