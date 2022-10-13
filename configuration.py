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
    # METODO AGREGADO
    def getPeriodoPC(self):
        return self.data['pc_period']

    def getProcesses(self):
        return self.data['process_list']

    