import psutil
import threading
import configuration
################# MODIFICARRRRRR ###############
## total_cpu,
# total_memory,
# available_memory,
## used_memory,
# memory_percent
config = configuration.Configuration()
class SystemInfo(threading.Thread):
    m_repository=0
    m_isRunning=False
    pc_list=[0,0,0,0,0]
    period=config.getPcPeriodVerification()

    #FUNCION bytes_to_megabytes
    def get_size(self, bytes ):
        factor = 1024
        megas=bytes/factor**2
        return megas

    def run(self):
        self.m_isRunning=True
        event = threading.Event()
        while (self.m_isRunning):     
            total_cpu=psutil.cpu_percent()
            svmem = psutil.virtual_memory()
            total_memory=self.get_size(svmem.total)
            available_memory=self.get_size(svmem.available)
            used_memory=self.get_size(svmem.used)
            memory_percent=svmem.percent
        
            self.pc_list[0]=round(total_cpu,2)
            self.pc_list[1]=round(total_memory,2)
            self.pc_list[2]=round(available_memory,2)
            self.pc_list[3]=round(used_memory,2)
            self.pc_list[4]=round(memory_percent,2)
    
              # REGISTRAR EN TABLA
            self.m_repository.log_start_pc_info(self.pc_list)					
          
            event.wait(self.period)

    
    def set_repository(self,repository):
        self.m_repository=repository