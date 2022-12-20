import json
'''
    !La clase Configuration es la encargada 
    de la lectura del archivo JSON. 
    Sus métodos retornan los valores establecidos en el archivo
    de configuración. 

'''
class Configuration:
    file_name='config.json'
    file=0
    data=0

    def __init__(self):
        self.file = open(self.file_name, "r")
        self.data = json.load(self.file)

    '''
        !Conjunto de métodos que retornan valores 
        correspondientes a la base de datos.
    '''
    def getDbFile(self):
        return self.data['db_file']

    def isRingBase(self):
        return self.data['ring_base']
        
    def getMaxRegisters(self):
        return self.data['max_register']

    '''
        !Conjunto de métodos que retornan valores 
        correspondientes a la salud del sitema (PC).
    '''
 
    def getPcPeriodVerification(self):
        return self.data['healthpc_period_verification']

    def getPcPeriodLoging(self):
        return self.data['healthpc_period_loging']

    
    def getMaxCPU(self):
        return self.data['max_cpu_user']

    
    def getMaxRam(self):
        return self.data['max_ram_user']

    
    def getMaxDisk(self):
        return self.data['max_disk_user']
    
    '''
        !Conjunto de métodos que retornan valores 
        correspondientes a los procesos.
    '''

    def getProcessesPeriodLoging(self):
        return self.data['processes_period_loging']
    
    def getProcessesPeriodVerification(self):
        return self.data['processes_period_verification']

    def getMaxProcessRam(self):
        return self.data['max_process_consume_ram']

    def getMaxProcessCPU(self):
        return self.data['max_process_consume_cpu']

    def getProcesses(self):
        return self.data['process_list']

