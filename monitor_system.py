import psutil
import threading
import configuration
import time


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
        #print(cpu_usage,disk_usage,used_memory,self.max_cpu,self.max_memory,self.max_disk)
        timestamp=time.time()      
        if cpu_usage>self.max_cpu or used_memory>self.max_memory or disk_usage>self.max_disk:
           
            self.m_repository.log_warning_pc_info(cpu_usage,used_memory,disk_usage,t1,t2,timestamp)
            
         
        else:
            if timestamp > self.time_loging_pc: 
                self.time_loging_pc =  timestamp + self.pc_period_loging
                self.m_repository.log_normal_pc_info(cpu_usage,used_memory,disk_usage,t1,t2,timestamp)

       
            
    def run(self):
        self.m_isRunning=True
        event = threading.Event()
        while (self.m_isRunning):
            self.pc_monitor()
            event.wait(self.pc_period_verification) 

        
    def set_repository(self,repository):
        self.m_repository=repository

    



