import psutil
import threading
import configuration
import time

################# MODIFICARRRRRR ###############
#https://micro.recursospython.com/recursos/como-obtener-el-espacio-del-disco.html
#https://leetcode.com/problems/unique-paths/
#https://www.coursera.org/search?query=system%20process
#https://www.coursera.org/projects/practical-introduction-to-the-command-line
#https://www.coursera.org/learn/python-operating-system?utm_medium=email&utm_source=marketing&utm_campaign=JYG_ALI9EempyReieZALEQ#syllabus
#https://www.coursera.org/professional-certificates/google-it-automation?recoOrder=1&utm_medium=email&utm_source=marketing&utm_campaign=JYG_ALI9EempyReieZALEQ
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
## TEMPERATURA EN PARTICIONES 
# REPOSO 24-35 
# NORMAL 42-52
# MAX   72

## TEMPERATURA
##  NORMAL 20-70 Cº
## Alerta MAXIMO > 81Cª

class SystemInfo(threading.Thread):
    m_repository=0
    m_isRunning=False
    max_disk=0
    max_cpu= 0
    max_memory=0
    pc_period_loging=0
    pc_period_verification=0
    time_loging_pc=0
   
    def PCsetConfiguration(self,repository,disk,cpu,memory,period_verification,loging_time):
        self.m_repository=repository
        self.pc_period_verification=period_verification
        self.max_cpu=cpu
        self.max_memory=memory
        self.max_disk=disk
        self.pc_period_loging=loging_time

    #FUNCION bytes_to_megabytes
    def get_size(self, bytes ):
        return bytes/1024**2

    def toPercent(self,total,part):
        return round(part*100/total,1)

    def pc_temperatura(self):
        temperatures_values_partitions=list()
        temperatures_states=list()
        cores_info=psutil.sensors_temperatures()[ 'coretemp' ]
        for core in cores_info:
            temp=core.current
            if 24<=temp and temp <=41:
                temperatures_states.append('Reposo')
            elif 42<=temp and temp <=70:
                temperatures_states.append('Normal')
            elif 71<=temp and temp<=75:
                temperatures_states.append('Maximo')
            elif temp>75:
                temperatures_states.append('Alerta')
            temperatures_values_partitions.append(core.current)
        t1=str(temperatures_values_partitions)
        t2=str(temperatures_states)
        return t1,t2

    def pc_monitor(self):

        cpu_usage=psutil.cpu_percent() 

        disk= psutil.disk_usage("/") # en bytes
        disk_usage=round(disk.percent,1)

        memory=psutil.virtual_memory()
        used_memory=memory.percent

        t1,t2=self.pc_temperatura()
        print(cpu_usage,disk_usage,used_memory,self.max_cpu,self.max_memory,self.max_disk)      
        if cpu_usage>self.max_cpu or used_memory>self.max_memory or disk_usage>self.max_disk:
            self.m_repository.log_warning_pc_info(cpu_usage,used_memory,disk_usage,t1,t2)
            
         
        else:
            if time.time()> self.time_loging_pc: 
                self.time_loging_pc = time.time() + self.pc_period_loging
                self.m_repository.log_normal_pc_info(cpu_usage,used_memory,disk_usage,t1,t2)

       
            
    def run(self):
        self.m_isRunning=True
        event = threading.Event()
        while (self.m_isRunning):
            self.pc_monitor()
            event.wait(self.pc_period_verification) 

        
    def set_repository(self,repository):
        self.m_repository=repository

    



