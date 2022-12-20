import time
import datetime       
import mysql.connector
import sys
import string
import pandas as pd
import sys



n = len(sys.argv)
  
for i in range(1, n):
    add += float(sys.argv[i])
  
print ("the sum is :", add)



mysql_db=mysql.connector.connect(
            host='localhost',
            user='pruebas2022',
            #user='root',
            password='pruebas2022',
            database='pruebas2022'
        )
selection="SELECT node_name, process_name, event, COUNT(*)  FROM monitored  where event={} and process_name not in ('sleep', 'sh', 'aterm', 'guishow.sh') and timestamp_occured BETWEEN {} AND {} GROUP BY node_name,process_name, event order by (node_name);"
comand_process=selection.format(event,inicio,fin)
print(comand_process)
# Pasando a pandas
db = pd.read_sql(comand_process,mysql_db)
by_count = db.sort_values('COUNT(*)',ascending=False)

print(by_count.head(20))
print('DONE IT!')