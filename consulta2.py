import query
import os 

path = "/home/guiomar/Escritorio/monitoring/PROCESS_MONITORING_MOD"
dates=list()
event="'start'"
os.chdir(path)


def datebyline(path_file):
        dates=list()
     
        with open(path_file) as f:
            lines=f.readlines()
        for line in lines:		
            if line!='\n':
                dates.append(line.split())
        return dates	

# listado de todos los directorios
for file in os.listdir():
	
    if file.endswith(".txt"):
        file_path = f"{path}/{file}"
        print('***************************',read_file(file_path ))
        date=datebyline(file_path)
        for d in date:   
            consulta=query.queries(d[0],d[1],event)
            header,rows=consulta.consult(d[0],d[1],event)
            consulta.export(d[0],d[1],event)

            







    '''
d1="'2022-12-12 14:04:00'"
d2="'2022-12-12 16:39:00'" 
event="'start'"
consult (d1,d2,event)
    #return header,rows
'''