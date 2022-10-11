import time
import threading
import psutil


class ProcessData:
	m_pid = -1
	m_timeControl = 0
	m_processed = False
	m_period=0


class ProcessMonitor(threading.Thread):
	m_monitoredList = {}
	m_repository=0
	m_isRunning=False

	def monitoring(self,proc):
		if proc.name() in self.m_monitoredList:
			monitored = self.m_monitoredList[proc.name()] 
			
			if monitored.m_pid == -1:
				monitored.m_pid = proc.pid
				monitored.m_timeControl = proc.create_time() + monitored.m_period
				#registrar inicio
				self.m_repository.log_start_process(proc)
				self.AddChildren(proc,monitored.m_period)

			else:
				if monitored.m_pid == proc.pid:
					self.AddChildren(proc,monitored.m_period)
					if time.time()>= monitored.m_timeControl:
						monitored.m_timeControl = time.time() +  monitored.m_period
						#registrar uso
						self.m_repository.log_running_process(proc)
				'''
				else:
					monitored.m_pid = proc.pid
					monitored.m_timeControl = proc.create_time() + self.m_period

					#self.m_repository.log_restart_monitored(proc)
					#regirar en el repositorio el cambio
					print('cambio')
			
				'''
			monitored.m_processed = True
			
	def run(self):
		self.m_isRunning=True
		event = threading.Event()
		while (self.m_isRunning):
			for proc in psutil.process_iter():#(['pid', 'name', 'username']):
				self.monitoring(proc)

			for index in self.m_monitoredList:
				monitored = self.m_monitoredList[index]
				if monitored.m_pid != -1 and monitored.m_processed == False:
					#registrar caida
					self.m_repository.log_fail_process(index,monitored.m_pid)					
					monitored.m_pid = -1
				monitored.m_processed = False
			event.wait(1)

		
	def set_repository(self,repository):
		self.m_repository=repository
		
	def add_monitored(self,name,period,monitoring_children=False):
		if not name in self.m_monitoredList:
			monitored = ProcessData()
			monitored.m_pid = -1
			monitored.m_period = period
			self.m_monitoredList [name] = monitored
			print(name, 'se agrega a la lista de monitoreo')

	def AddChildren(self,proc,period):
		#print(proc.name(), ' procesos hijo: ', proc.children())
		for subproc in proc.children():
			self.add_monitored(subproc.name(),period)
			#print('Se aprega un subproceso: ', subproc.name())
		
