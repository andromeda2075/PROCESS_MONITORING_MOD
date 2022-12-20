import os
import string
# Path general donde se encuentran todos los archivos de texto

path = "/home/guiomar/Escritorio/monitoring/PROCESS_MONITORING_MOD"
dates=list()
os.chdir(path)

def datebyline(path):
	with open(path) as f:
		lines=f.readlines()
		print(lines)
	for line in lines:	
		
		if line!='\n':
			dates.append(line.split())
	return dates	

# Lista todos los archivos del path

for file in os.listdir():
	
	if file.endswith(".txt"):
		file_path = f"{path}/{file}"
		d=datebyline(file_path)
		print('d===',d)
		for i in d:
			print(i[0],i[1])
	

