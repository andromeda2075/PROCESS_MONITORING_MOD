
import psutil
import threading


## max_freq,min_freq,total_cpu,total_cores,total_memory,available_memory,
## used_memory,memory_percent,bytes_sent,bytes_recived

class SystemInfo(threading.Thread):
    m_repository=0
    m_isRunning=False
    pc_list=[]

    #FUNCION bytes_to_
    def get_size(self, bytes, ):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]: # por lo generalen megas
            if bytes < factor:
                return bytes
            bytes /= factor

    def run(self):
        self.m_isRunning=True
        event = threading.Event()
        while (self.m_isRunning):     
            cpufreq = psutil.cpu_freq()
            total_cpu=psutil.cpu_percent()
            total_cores=psutil.cpu_percent(percpu=True)
            svmem = psutil.virtual_memory()
            total_memory=self.get_size(svmem.total)
            available_memory=self.get_size(svmem.available)
            used_memory=self.get_size(svmem.used)
            memory_percent=svmem.percent
            bytes_sent=self.get_size(net_io.bytes_sent)
            bytes_recived=self.get_size(net_io.bytes_recv)
         
            self.pc_list.append(cpufreq.max)
            self.pc_list.append( cpufreq.min)
            self.pc_list.append( total_cores)
            self.pc_list.append( total_memory)
            self.pc_list.append( available_memory)
            self.pc_list.append( used_memory)
            self.pc_list.append(  memory_percent)
            self.pc_list.append( bytes_sent)
            self.pc_list.append( bytes_recived)
              # REGISTRAR EN TABLA
            self.m_repository.log_start_pc_info(self.pc_list)					
          
            event.wait(1)

    
    def set_repository(self,repository):
        self.m_repository=repository