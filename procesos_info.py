
import psutil    
import os
from datetime import datetime
import pandas as pd
from os import getpid
 
from psutil import Process
from os import getpid
import string



'''
Nombre de un proceso: name_process
Identificador de un proceso: pid 
Hora de inicio de un proceso: time_start_process 
Consumo de memoria RAM:RAM_used OK (cpu % )
'''


def InfoProcess(nameOne,nameTwo):

	listOfProcess=list()
	
	list_name=list()
	list_pid=list()
	list_cpu_percent=list()
	list_status=list()
	list_vms=list()	
	list_time_start=list()
	
	
	list_RAM=list()
	list_num_subprocess=list()
	
	for proc in psutil.process_iter():
			pInfoDict=proc.as_dict(attrs=['name','pid','cpu_percent','status'])
			pInfoDict['vms'] = proc.memory_info().vms / (1024 * 1024*1024)
			pInfoDict['Start Time']=datetime.fromtimestamp(proc.create_time()).strftime('%H:%M:%S')
			listOfProcess.append(pInfoDict)
	for i in range(len(listOfProcess)):
		if(listOfProcess[i]['name']==nameOne or listOfProcess[i]['name']==nameTwo):
			list_name.append(listOfProcess[i]['name'])
			list_pid.append(listOfProcess[i]['pid'])
			list_cpu_percent.append(listOfProcess[i]['cpu_percent'])
			list_status.append(listOfProcess[i]['status'])
			list_vms.append(listOfProcess[i]['vms'])
			list_time_start.append(listOfProcess[i]['Start Time'] )
	data={'Process Name':list_name, 'PID': list_pid, 		'StartTime':list_time_start ,'CPU%':list_cpu_percent,'Status':list_status,'VMS':list_vms}		
	df=pd.DataFrame(data=data)
			
		
	return df


## Prueba ##


	
	

	

'''
nameOne='gnome-screenshot'

nameTwo='bash'

print(InfoProcess(nameOne,nameTwo))

'''






	
