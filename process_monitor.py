import time
import threading
import psutil

# @file process_monitor_mod.py

"""
	! Se realiza el monitoreo de los procesos. Se consideran los siguientes parámetros:
	@ param Consumo de RAM por proceso: 100 Mb 
	@ param Consumo de CPU por proceso: 5%

"""

"""
	! Estructura de la data relacionada con el proceso a manitorear. Se tienen los siguientes atributos:
		@ param m_pid: identificador de procesos (ID)
		@ param m_time_loging: tiempo en el que debe realizar un registro obligatorio (m_time_loging = time.time() + m_period_loging)
		@ param m_processed: variable booleana que indica si en el último chequeo se encontró al proceso con el PID
		@ param m_name: variable que almacenará el nombre del proceso
"""
	
class ProcessData:
	m_pid = -1   
	m_time_loging = 0  
	m_processed = False   
	m_name=""

"""
	! Estructura de metadata con los siguientes campos:
	@ param m_period_loging: corresponde al periodo de registro obligatorio
	@ param m_hasChildren: variable booleana que establece si se monitoreará o no los subprocesos

"""
	

class ProcessMetaData:
	m_period_loging=0  
	m_hasChildren = False


""" ! Clase principal para el monitoreo de procesos """

class ProcessMonitor(threading.Thread):

	m_monitoredMetadataList = {}
	m_monitoredList = {}
	m_repository=0
	m_isRunning=False
	const=0.05								
	m_period_verification=0
	m_process_ram=0
	m_process_cpu=0

	
	def setConfiguration(self,repository,period_verification,max_process_consume_ram,max_process_consume_cpu):
		""" !Función de configuración donde se pasan los parámetros establecidos por el usuario así como también el objeto repository """
			
		
		self.m_repository=repository
		self.m_period_verification = period_verification
		if  self.m_period_verification<self.const: 
			raise Exception("El periodo de verificación debe ser mayor de 0.05 segundos ")
		self.m_process_ram = max_process_consume_ram
		self.m_process_cpu= max_process_consume_cpu


	def monitoring(self,proc):
		"""
			!Esta función verifica si un proceso ha sido monitoreado o no.
			Se verifica si el proceso está en la lista de metadata para obtener su consumo de cpu y memoria.
			Luego se verifica si el ID del proceso está en la lista de  procesos monitoreados, de ser así se monitorea los 
			subprocesos (procesos hijos) y se establece como proceso monitoreado.
			Luego se verifica que el proceso monitoreado no sobrepase el consumo de CPU o RAM establecido
			por el usuario, si es así escribimos en la tabla de registros el evento "warning".
			Caso contrario, si la marca de tiempo actual supera el tiempo de registro obligatorio entonces 
			se recalcula el tiempo de registro obligatorio estableciendo el evento "running".
			Pero si el ID del proceso no está en la lista de procesos monitoreados entonces se agrega a la lista de procesos 
			monitoreados además de monitorear a los subprocesos, en la tabla de registros se establece el evento "start".

		"""
			
		name =  proc.name()
		pid = proc.pid
		if name  in self.m_monitoredMetadataList:
			
			metadata = self.m_monitoredMetadataList[name]
	
			consume_cpu=proc.cpu_percent(interval=None)  
			consume_memory=proc.info['memory_info'].rss
			memory_megabyte=consume_memory/1024**2  
	
			if pid in self.m_monitoredList:
				monitored=self.m_monitoredList[pid]
				self.addChildren(proc,metadata.m_period_loging,metadata.m_hasChildren)	
				monitored.m_processed = True 

				'''
					!Dado que m_process_ram es un parámetro dado en megabytes se pasa a bytes
					para realizar la comparación con respecto al consumo de memoria dado en
					bytes tambien.
				'''
				if consume_cpu>self.m_process_cpu or consume_memory>self.m_process_ram*1024*1024:
						
						self.m_repository.log_warning_process(name,pid,consume_cpu,memory_megabyte) 
				else:
					if time.time()>= monitored.m_time_loging:		
						monitored.m_time_loging = time.time() +  metadata.m_period_loging 
						self.m_repository.log_running_process(name,pid,consume_cpu,memory_megabyte)
			else:
				monitored = ProcessData()
				monitored.m_pid = pid
				monitored.m_name = name
				monitored.m_time_loging = proc.create_time() + metadata.m_period_loging
				monitored.m_processed = True   
				self.m_monitoredList [pid] = monitored 
				self.addChildren(proc,metadata.m_period_loging,metadata.m_hasChildren)
				self.m_repository.log_start_process(name,pid,consume_cpu,memory_megabyte) 
		
	def run(self):
		self.m_isRunning=True
		event = threading.Event()
		while (self.m_isRunning):
			for index in self.m_monitoredList:
				monitored = self.m_monitoredList[index]
				monitored.m_processed = False

			for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
				self.monitoring(proc)
			
			for index in list(self.m_monitoredList.keys()):
				monitored = self.m_monitoredList[index]
				
				if not monitored.m_processed:
					self.m_repository.log_fail_process(monitored.m_name,monitored.m_pid,time.time())					
					del self.m_monitoredList[index]

			event.wait(self.m_period_verification ) 
		
	def add_monitored(self,name,period,monitoring_children=False):
		if not name in self.m_monitoredMetadataList:
			monitored = ProcessMetaData()
			monitored.m_period_loging = period
			monitored.m_hasChildren = monitoring_children 
			self.m_monitoredMetadataList [name] = monitored
			

	def addChildren(self,proc,period,m_hasChildren):
		if m_hasChildren:
			for subproc in proc.children():
				self.add_monitored(subproc.name(),period,m_hasChildren)