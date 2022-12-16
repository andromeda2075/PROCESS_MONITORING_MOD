import sqlite3
import time
import datetime
import os        
import mysql.connector
import sys

mysql_db=mysql.connector.connect(
    host='localhost',
    user='pruebas2022',
    password='pruebas2022',
    database='pruebas2022'
)

print(mysql_db)

mysql_db_cur=mysql_db.cursor()
mysql_db_cur.execute(
"SELECT node_name, process_name, event, COUNT(*) FROM monitored  where event='start' and process_name not in ('sleep', 'sh', 'aterm', 'guishow.sh') and timestamp_occured BETWEEN '2022-12-12:23:34' AND '2022-12-13:04:35'  GROUP BY node_name,process_name, event order by (node_name)")

#consulta=mysql_db_cur.fetchall()
#print(consulta)

result = mysql_db_cur.fetchall()

for all in result:
    print(all)
  
print(result)

'''
for consult in consulta:
    print('consult')
'''

'''
n = len(sys.argv)
if n <= 1 :
    print("Debe ingresar el directorio a procesar")
    exit(0)
'''

'''
# This SQL statement selects all data from the CUSTOMER table.
result = mycursor.fetchall()
  
# Printing all records or rows from the table.
# It returns a result set. 
for all in result:
  print(all)

'''



