
import psutil
import threading
import configuration

## max_freq,min_freq,total_cpu,total_cores,total_memory,available_memory,
## used_memory,memory_percent,bytes_sent,bytes_recived
config = configuration.Configuration()
class SystemInfo(threading.Thread):
    m_repository=0
    m_isRunning=False
    pc_list=[0,0,0,0,0,0,0,0,0,0,0]
    period=config.getPeriodoPC()

    #FUNCION bytes_to_
    def get_size(self, bytes ):
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
            #total_cores=psutil.cpu_count(logical=True)
            #FRECUENCIAS CPU
            #print("TOTAL CORES",total_cores)
            svmem = psutil.virtual_memory()
            net_io = psutil.net_io_counters()
            total_memory=self.get_size(svmem.total)
            available_memory=self.get_size(svmem.available)
            used_memory=self.get_size(svmem.used)
            memory_percent=svmem.percent
            bytes_sent=self.get_size(net_io.bytes_sent)
            bytes_recived=self.get_size(net_io.bytes_recv)
            temp=psutil.sensors_temperatures()
            self.pc_list[0]=cpufreq.max
            self.pc_list[1]=cpufreq.min
            self.pc_list[2]=round(cpufreq.current,2)
            self.pc_list[3]=round(total_cpu,2)
            self.pc_list[4]=round(total_memory,2)
            self.pc_list[5]=round(available_memory,2)
            self.pc_list[6]=round(used_memory,2)
            self.pc_list[7]=round(memory_percent,2)
            self.pc_list[8]=round(bytes_sent,2)
            self.pc_list[9]=round(bytes_recived,2)
            self.pc_list[10]=temp['acpitz'][0].current
              # REGISTRAR EN TABLA
            self.m_repository.log_start_pc_info(self.pc_list)					
          
            event.wait(self.period)

    
    def set_repository(self,repository):
        self.m_repository=repository

    

    # AGREGAR temps['acpitz'][0].current
    # CONFIGURAR EL PERIODO (LEERLO DESDE EL CONFIG JSON)
    # https://www.pragmaticlinux.com/2020/12/monitor-cpu-and-ram-usage-in-python-with-psutil/
    #https://github.com/giampaolo/psutil/blob/master/scripts/sensors.py
    # https://github.com/giampaolo/psutil/blob/master/scripts/temperatures.py