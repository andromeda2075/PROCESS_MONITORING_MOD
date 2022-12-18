import psutil
import threading
import configuration
import time
import math 
import re
from itertools import accumulate

""" @Programa con respecto a la salud del sistema. 
"""
"""
    !  Estado warning del sistema:
       Consumo de RAM > 60 %
       Alerta CPU TOTAL > 50%
       Alerta de CONSUMO DE DISCO   > 80%

    !  Temperatura de las particiones  

            Reposo 24C - 41C                              
            Normal 42C - 70C                              
            Max   71C - 75C                              
            Alerta > 75C

"""
"""
	! La clase SystemMonitor cuenta con los siguientes atributos:
		@ param m_repository: variable que almacena el objeto repositorio 
		@ param max_disk: variable que almacena el valor límite de consumo de disco dado por el usuario.
		@ param max_cpu: variable que almacena el valor límite de consumo de cpu dado por el usuario.
        @ param max_memory: variable que almacena el valor límite de consumo de memoria dado por el usuario.
        @ param pc_period_loging:variable que almacena el periodo de registro.
        @ param time_loging_pc: variable que almacena el tiempo de actualización del registro obligatorio.
        @ param pc_period_verification: tiempo de verificación 

"""

class SystemMonitor(threading.Thread):

    m_repository=0
    m_isRunning=False
    max_disk=0
    max_cpu= 0
    max_memory=0
    pc_period_loging=0
    time_loging_pc=0
    pc_period_verification=0
    
    def setConfiguration(self,repository,disk,cpu,memory,period_verification,loging_time):

        self.m_repository=repository
        self.pc_period_verification=period_verification
        self.max_cpu=cpu
        self.max_memory=memory
        self.max_disk=disk
        self.pc_period_loging=loging_time

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

    def disk(self):
        disk_partitions = psutil.disk_partitions()
        disk_free=[]
        disk_used=[]
        pattern = '/dev/sd'
        percent = 0

        for partition in disk_partitions:
            text = partition.device
            match = re.search(pattern, text)
            if match:
                disk_usage = psutil.disk_usage(partition.mountpoint)
                disk_free.append(disk_usage.free)
                disk_used.append(disk_usage.used)
                free=list(accumulate(disk_free))
                used=list(accumulate(disk_used))
                percent=math.ceil(round(used[-1]/(used[-1]+free[-1])*100,2))

        return(percent)

    def monitoring(self):

        cpu_usage=psutil.cpu_percent() 
        memory=psutil.virtual_memory()
        used_memory=memory.percent
        disk_usage=self.disk()
        t1,t2=self.pc_temperatura()    
        if cpu_usage>self.max_cpu or used_memory>self.max_memory or disk_usage>self.max_disk:
           
            self.m_repository.log_warning_pc_info(cpu_usage,used_memory,disk_usage,t1,t2,time.time())
             
        else:
            if time.time() > self.time_loging_pc: 
                self.time_loging_pc=time.time()+ self.pc_period_loging
                self.m_repository.log_normal_pc_info(cpu_usage,used_memory,disk_usage,t1,t2,time.time())

       
    def run(self):

        self.m_isRunning=True
        event = threading.Event()
        while (self.m_isRunning):
            self.monitoring()
            event.wait(self.pc_period_verification) 

        
    def set_repository(self,repository):
        self.m_repository=repository



