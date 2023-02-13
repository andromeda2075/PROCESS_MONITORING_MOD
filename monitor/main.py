""" @brief Programa principal. 
"""
## 
# @mainpage Doxigen Módulo del Proceso de Monitoreo
#     
# @section description_main Descripción
# Módulo creado para el monitoreo de procesos 
# y para la salud del sistema.

##
# @file main.py
# @section author_doxygen_example Autor
# - Creado por Guiomar A. León


import repository 
import configuration
import system_monitor
import process_monitor 

import uselogging

# inicio del logeo de errores
logg=uselogging.logging_monitored("log_monitor.log")
logg.main_config()

"""! Creación del objeto configuración """
config = configuration.Configuration()

""" ! Creación del objeto repositorio """
new_repository=repository.SqliteRepository(config.getDbFile(),config.isRingBase(),config.getMaxRegisters())
new_repository.setLogger(logg)

""" ! Creación del objeto monitor de procesos """
process_monitor_obj=process_monitor.ProcessMonitor()

process_monitor_obj.setConfiguration(new_repository,config.getProcessesPeriodVerification(),config.getMaxProcessRam(),config.getMaxProcessCPU())
process_monitor_obj.setLogger(logg)

""" ! Se pasa la lista de los procesos dados para el monitoreo """
for process in config.getProcesses():
    process_monitor_obj.add_monitored(process['name'],process['processes_period_loging'],process['monitoring_children'])
    
""" ! Inicio correspondiente al monitoreo """
process_monitor_obj.start()

""" ! Inicio correspondiente a la salud del sistema (PC) """
system_monitor_obj=system_monitor.SystemMonitor()

system_monitor_obj.setConfiguration(new_repository,config.getMaxDisk(),config.getMaxCPU(),config.getMaxRam(),config.getPcPeriodVerification(),config.getPcPeriodLoging())

""" ! El método start invoca implícitamente al método run.
    El método run es parte de la libreria threading
"""
system_monitor_obj.start() 
