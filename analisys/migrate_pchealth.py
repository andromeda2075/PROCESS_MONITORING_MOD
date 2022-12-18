# import sqlite3
# import datetime
import os        
import sys
import repository
import migrator 

# total arguments
n = len(sys.argv)
if n <= 1 :
    print("Debe ingresar el directorio a procesar")
    exit(0)

basepath=sys.argv[1]

repositoryObj = repository.MysqlRepository("localhost","pruebas2022","pruebas2022","pruebas2022")    
migratorObj =  migrator.Migrator()

directory_list1 = os.listdir(basepath)
directory_list1.sort()
for e in directory_list1:
    if os.path.isdir(os.path.join(basepath,e)):
        for f in os.listdir(os.path.join(basepath,e)):
            if os.path.isdir(os.path.join(basepath,e,f)):
                for g in os.listdir(os.path.join(basepath,e,f)):
                    if os.path.isfile(os.path.join(basepath,e,f,g)):
                        print(os.path.join(basepath,e,f,g))
                        # print(f)
                        unidad=f.split('.')[0]
                        # transaction.setup(os.path.join(basepath,e,f,g), unidad)
                        migratorObj.setup("PC",os.path.join(basepath,e,f,g), unidad, migrator.formatSystemData,repositoryObj.insert_system_data)
                        migratorObj.migrate()
                        repositoryObj.commit()

exit(0)



