import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time     
import mysql.connector
import sys
from datetime import datetime, timedelta
#import xlsxwriter
import string

'''
SELECT node_name, process_name, event, COUNT(*)  FROM monitored 
where event="running" and process_name not in ("sleep", "sh", "aterm", "guishow.sh","fluxbox") and timestamp_occured BETWEEN '2022-12-12:14:04' AND '2022-12-12:16:39' 
GROUP BY node_name,process_name, event order by (node_name);
'''
control_time=6000

time_data="13/12/22 10:48:00"

format_data= "%d/%m/%y %H:%M:%S"

end_time = datetime.strptime(time_data, format_data)

time= end_time - timedelta(seconds=control_time)

mydb = mysql.connector.connect(
        host="localhost", 
        database ='pruebas2022',
        user="pruebas2022",
        passwd="pruebas2022",  
        )

selection = "SELECT node_name, process_name, event, COUNT(*)  FROM monitored and process_name not in ('sleep', 'sh', 'aterm', 'guishow.sh','fluxbox') and timestamp_occured BETWEEN {} AND {} GROUP BY node_name, process_name, event order by (node_name);"
query=selection.format(str(time), str(end_time))

print(query)



'''
db = pd.read_sql(query,mydb)
mydb.close() #close the connection
print(db.head(10))
'''
