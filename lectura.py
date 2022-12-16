import os 

path_files    = 'home/carlos/temp/monitoreo/python/PROCESS_MONITORING_MOD' 
name_fies= os.listdir(path_files) 

with open("/home/carlos/temp/monitoreo/python/PROCESS_MONITORING_MOD/pruebatext.txt","r") as archivo:
    for linea in archivo:
        print(linea)

def buscar_archivos(ruta): 
	archivos_texto = [] 
	archivos       = os.listdir(ruta) 
	for archivo in archivos: 
		if archivo[-4:] == '.txt': 
			archivos_texto.append(archivo) 
	return archivos_texto 


for carpeta in nombres_carpetas: 
	ruta = ruta_carpetas + carpeta 
	archivos_texto = buscar_archivos(ruta) 
	for texto in archivos_texto: 
		with open(ruta + '/' + texto, 'r') as f: 
			# Hacer algo con los archivos de texto!

 
