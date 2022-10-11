import threading
import repository 
import json
import psutil

class ProcessData1(threading.Thread):
	m_pid = -1
	m_timeControl = 0
	m_repository=0
	m_period=0
	m_name=""
	m_exist=False
	m_isRunning=False

	def config(self,name,period,repository):
		print('Objeto monitoring_one creado')
		self.repository = repository
		self.m_period = period
		self.m_name = name

	def run(self):
		self.m_isRunning=True
		event = threading.Event()
		while (self.m_isRunning):
			exist = False
			for proc in psutil.process_iter():#(['pid', 'name', 'username']):
				if proc.name() == self.m_name:
					self.m_exist = True
					exist = True
					print(proc.name(), ':  pid=', proc.pid)

					if self.m_pid == -1:
						self.m_pid = proc.pid
						self.m_timeControl = proc.create_time() + self.m_period

						#registrar inicio
						#self.m_repository.log_sart_proccess(proc)
						print ('PRIMER REGISTRO')
					else:
						if self.m_pid == proc.pid:
							if time.time()>= self.m_timeControl:
								print("registrar uso")
								self.m_timeControl = time.time() + self.m_period

						else:
							self.m_pid = proc.pid
							self.m_timeControl = proc.create_time() + self.m_period

							#self.m_repository.log_restart_process(proc)
							#regirar en el repositorio el cambio
							print('cambio')
					break
			if (not exist) and self.m_exist:
				self.m_pid = -1
				self.m_exist = False
				#registrar caida
				print ("se cayo")
			event.wait(1)

	def set_repository(self,repository):
		self.m_repository=repository
		pass


## LECTURA DE LA CONFIGUARACION DESDE UN ARCHIVO JSON
file='config.json'

f = open(file, "r")
data = json.load(f)
db_file=data['db_file']

##SE CREA UN REPOSITORIO QUE GUARDA DATA EN UNA BD SQLITE
new_repository=repository.SqliteRepository(db_file,data['ring_base'],data['max_register'])

## ejemplo de uso de la implementacion con hilo por proceso
#proceso1=module1.ProcessData1()
#proceso1.config('mousepad',10,new_repository)
#proceso1.start()
#proceso2=module1.ProcessData1()
#proceso2.config('xfce4-terminal',5,new_repository)
#proceso2.start()
