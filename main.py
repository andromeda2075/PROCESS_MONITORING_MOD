''' Programa principal. Se llaman a los módulos creados 
    para el monitoreo de procesos y salud del sistema.
'''

import repository 
import configuration
import monitor_system
import process_monitor_mod 

''' Creación del objeto configuración '''
config = configuration.Configuration()

''' Creación del objeto repositorio '''
new_repository=repository.SqliteRepository(config.getDbFile(),config.isRingBase(),config.getMaxRegisters())

''' Creación del objeto monitor de procesos '''
process_monitor_mod=process_monitor_mod.ProcessMonitor()

process_monitor_mod.SetConfiguration(new_repository,config.getProcessesPeriodVerification(),config.getMaxProcessRam(),config.getMaxProcessCPU())

''' Se pasa la lista de los procesos dados para el monitoreo '''
for process in config.getProcesses():
    process_monitor_mod.add_monitored(process['name'],process['processes_period_loging'],process['monitoring_children'])
    
''' Inicio del monitoreo '''
process_monitor_mod.start()

''' Inicio de la salud del sistema (PC) '''
pc_info=monitor_system.SystemInfo()

pc_info.PCsetConfiguration(new_repository,config.getMaxDisk(),config.getMaxCPU(),config.getMaxRam(),config.getPcPeriodVerification(),config.getPcPeriodLoging())

''' El método start invoca inplícitamente al método run.
    El método run es parte de la libreria threading
'''
pc_info.start() 
