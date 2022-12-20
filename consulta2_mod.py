import query_mod
import os 

#path = "/home/guiomar/Escritorio/monitoring/PROCESS_MONITORING_MOD"
path="/home/carlos/temp/monitoreo/python/PROCESS_MONITORING_MOD"
dates=list()
#event="'start'"
#event="'running'"
#event="'warning'"
event="'fail'"
os.chdir(path)


def datebyline(path_file):
        dates=list()
     
        with open(path_file) as f:
            lines=f.readlines()
            return lines	

# listado de todos los directorios
for file in os.listdir():
	
    if file.endswith(".txt"):
        file_path = f"{path}/{file}"
        file_name=f"{file}"
        print('***************************')
        date=datebyline(file_path)
        for line in date:  
            consulta=query_mod.queries(line[0:21],line[22:44],event,file_name)
            db=consulta.consult(line[0:21],line[22:44],event)
            consulta.export(line[0:21],line[22:44],event,file_name,db)
            print('done it')

            







    '''
d1="'2022-12-12 14:04:00'"
d2="'2022-12-12 16:39:00'" 
event="'start'"
consult (d1,d2,event)
    #return header,rows
'''