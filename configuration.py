import json

class Configuration:
    file_name='config.json'
    file=0
    data=0

    def __init__(self):
        ## LECTURA DE LA CONFIGURACION DESDE UN ARCHIVO JSON
        self.file = open(self.file_name, "r")
        self.data = json.load(self.file)

    def getDbFile(self):
        return self.data['db_file']

    def isRingBase(self):
        return self.data['ring_base']
        
    def getMaxRegisters(self):
        return self.data['max_register']

    # Métodos agregados 
    def getPcPeriodVerification(self):
        return self.data['healthpc_period_verification']

    def getPcPeriodLoging(self):
        return self.data['healthpc_period_loging']

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