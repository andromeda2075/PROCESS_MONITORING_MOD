import time
import threading
import psutil



class ProcessData:
	m_pid = -1
	m_time_loging = 0
	m_processed = False
	m_period_loging=0
    m_name=''

class ProcessMonitor(threading.Thread):
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
			#raise Exception(f"El periodo de verificación debe ser mayor a {self.const} segundos")
		self.m_process_ram = max_process_consume_ram
		self.m_process_cpu= max_process_consume_cpu
    def monitoring(self,proc):
        if proc.pid in self.m_monitoredList:
            monitored=self.m_monitoredList[proc.pid]
            if monitored.m_pid==-1:
                monitored.m_pid=proc.pid
                monitored.m_time_loging = proc.create_time() + monitored.m_period_loging
                self.m_repository.log_start_process(proc)
                self.AddChildren(proc,monitored.m_period_loging)
            else:
                if monitored.m_pid==proc.pid:
                    self.AddChildren(proc,monitored.m_period_loging)
                    name=proc.name()
                    pid=proc.pid
                    consume_cpu=proc.cpu_percent(interval=None)
                    consume_memory=proc.memory_percent()
                    print("CPU actual= {} , Memoria actual= {}".format(consume_cpu,round(consume_memory,2)))

                    if consume_cpu>self.m_process_cpu or consume_memory>self.m_process_ram:
                        self.m_repository.log_warning_process(name,pid,consume_cpu,consume_memory)
                    else:
                        if time.time()>=monitored.m_time_loging:
                            monitored.m_time_loging = time.time() +  monitored.m_period_loging
                            self.m_repository.log_running_process(proc)
			
                else:
                    monitored.m_time_loging = proc.create_time() + monitored.m_period_loging
                    self.m_repository.log_fail_process(proc.name(),monitored.m_pid,proc.create_time()- self.const)	
                    self.m_repository.log_start_process(proc)
					monitored.m_pid=proc.pid
					print('CAMBIO')

            monitored.m_processed = True
			
	def run(self):
		self.m_isRunning=True
		event = threading.Event()
		while (self.m_isRunning):
			for proc in psutil.process_iter():
				self.monitoring(proc)

			for pid,name in self.m_monitoredList:
				monitored = self.m_monitoredList[pid]
				if monitored.m_pid != -1 and monitored.m_processed == False:	# proceso que se cae y nunca se recupera ( primer caso )
					#registrar caida
					self.m_repository.log_fail_process(name,monitored.m_pid,time.time())					
					monitored.m_pid = -1
				monitored.m_processed = False
			event.wait(self.m_period_verification ) 
		
	def add_monitored(self,pid,period,monitoring_children=False):
		if not pid in self.m_monitoredList:
			monitored = ProcessData()
			monitored.m_pid = -1
			monitored.m_period_loging = period
			self.m_monitoredList [pid] = monitored
			print(m_name, 'se agrega a la lista de monitoreo')

	def AddChildren(self,proc,period):
		for subproc in proc.children():
			self.add_monitored(subproc.pid,period)
			
		