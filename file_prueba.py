import os
import string
# Path general donde se encuentran todos los archivos de texto

path = "/home/carlos/temp/monitoreo/python/PROCESS_MONITORING_MOD"
dates=list()
os.chdir(path)

def datebyline(path):
    with open(path) as f:
        lines=f.readlines()
    return lines


    for line in lines:	
        print(len(line))
        print(line[0:21],line[22:44])


for file in os.listdir():
    if file.endswith(".txt"):
        file_path = f"{path}/{file}"
        lines=datebyline(file_path)
        for line in lines:
            

       # print(d[0:21], d[22:44])
        #print(d[0],d[1],d[2],d[3],d[4])

'''
		d=datebyline(file_path)
		print('d===',d)
		for i in d:
			print(i[0],i[1])
'''
	