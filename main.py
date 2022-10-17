#!/usr/bin/python3

import process_monitor 
import repository 
import configuration
import system_monitor

## LECTURA DE LA CONFIGUARACION DESDE UN ARCHIVO JSON
config = configuration.Configuration()

##SE CREA UN REPOSITORIO QUE GUARDA DATA EN UNA BD SQLITE
new_repository=repository.SqliteRepository(config.getDbFile(),config.isRingBase(),config.getMaxRegisters())
#new_repository=repository.SqliteRepository(config.getDbFile(),config.isRingBase(),config.getMaxRegisters(),config.getPeriodoPC())
#config.getPeriodoPC()

##SE CREA EL MONITOR DE PROCESOS
process_monitor=process_monitor.ProcessMonitor()

#process_monitor.set_repository(new_repository)
#process_monitor.set_period_verification(config.getProcessesPeriodVerification())

process_monitor.SetConfiguration(new_repository,config.getProcessesPeriodVerification(),config.getMaxProcessRam(),config.getMaxProcessCPU())

##SE AGREGAN LOS PROCESOS A MONITOREAR
for process in config.getProcesses():
    process_monitor.add_monitored(process['name'],process['processes_period_loging'],process['monitoring_children'])

##SE INICIA EL MONITOREO
process_monitor.start()

############## INFORMACIÓN DE LA PC #####################

pc_info=system_monitor.SystemInfo()
pc_info.set_repository(new_repository)

## config modificar
'''
for process in config.getProcesses():
   system_monitor.add_monitored(process['name'],process['period'],process['monitoring_children'])
'''
## SE INICIA LA OBTENCIÒN DE LA INFORMACION DE LA PC
pc_info.start() # start invoca a run que es mètodo de threading

