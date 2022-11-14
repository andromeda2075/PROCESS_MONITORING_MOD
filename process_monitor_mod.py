import time
import threading
import psutil
# Consumo de RAM = 100 Mb ( Falta trabajar en Megabytes)
# Consumo de CPU = 5 %

# Estructura de un objeto ( los respectivos campos)
class ProcessData:
	m_pid = -1   ##identificador del procesos
	m_time_loging = 0  ##tiempo en el que se debe hacer un registro obligatorio
	m_processed = False   ##indica si en el ultimo checkeo se encontro al proceso con el PID
	m_name=""

class ProcessMetaData:
	m_period_loging=0  ##El periodo de registro obligarotorio  (m_time_loging = time.time() + m_period_loging)
	m_hasChildren = False


class ProcessMonitor(threading.Thread):
	m_monitoredMetadataList = {}
	m_monitoredList = {}
	m_repository=0
	m_isRunning=False
	# Todo para procesos
	const=0.05								
	m_period_verification=0
	m_process_ram=0
	m_process_cpu=0

	
	def SetConfiguration(self,repository,period_verification,max_process_consume_ram,max_process_consume_cpu):
		self.m_repository=repository
		self.m_period_verification = period_verification
		if  self.m_period_verification<0.05: 
			print("El periodo de verificación debe ser mayor a {} segundos ".format(self.const)) 
		self.m_process_ram = max_process_consume_ram
		self.m_process_cpu= max_process_consume_cpu


	def monitoring(self,proc):
		name =  proc.name()
		pid = proc.pid
		if name  in self.m_monitoredMetadataList:
			metadata = self.m_monitoredMetadataList[name]

			consume_cpu=proc.cpu_percent(interval=None)
			
			#consume_memory=proc.memory_percent() # Modificar pasar a megabytes
			consume_memory=proc.info['memory_info'].rss
			
			memory_megabyte=consume_memory/1024**2  # De bytes a Megabytes
			if pid in self.m_monitoredList:
				monitored=self.m_monitoredList[pid]
				self.addChildren(proc,metadata.m_period_loging,metadata.m_hasChildren)	
				monitored.m_processed = True 

				print("CPU actual process= {} , Memoria actual process= {}".format(consume_cpu,round(memory_megabyte,2))) 
				if consume_cpu>self.m_process_cpu or consume_memory>self.m_process_ram*1024*1024:
						
						self.m_repository.log_warning_process(name,pid,consume_cpu,memory_megabyte) 
				else:
					if time.time()>= monitored.m_time_loging:	##Si la marca de tiempo supera el tiempo de registro obligatorio entonces se hace un registro			
						monitored.m_time_loging = time.time() +  metadata.m_period_loging  ## Se calcula el nuemvo tiempo de registro obligatorio
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
			print(name, 'se agrega a la lista de monitoreo')

	def addChildren(self,proc,period,m_hasChildren):
		if m_hasChildren:
			for subproc in proc.children():
				self.add_monitored(subproc.name(),period,m_hasChildren)