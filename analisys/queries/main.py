#import ...library.repository as repository
import sys
import os
import pandas as pd

sys.path.append(os.getcwd() + '/../../')
import library.repository as repository
repositoryObj = repository.MysqlRepository("localhost","pruebas2022","pruebas2022","pruebas2022")    

mysql_cursor=repositoryObj.getCursor()
mysql_connection=repositoryObj.getConnection()
intervalos = [
        ['2022-12-12 14:04:00' ,'2022-12-12 16:39:00'],
        ['2022-12-12 17:05:00' ,'2022-12-12 19:06:00'],
        ['2022-12-12 20:48:00' ,'2022-12-12 22:52:00'],
        ['2022-12-12 23:34:00' ,'2022-12-13 04:35:00'],
        ['2022-12-13 05:02:00' ,'2022-12-13 07:12:00'],
        ['2022-12-13 08:21:00' ,'2022-12-13 10:48:00'],
        ['2022-12-13 13:59:00' ,'2022-12-13 16:35:00'],
        ['2022-12-13 17:53:00' ,'2022-12-13 19:25:00'],
        ['2022-12-13 20:40:00' ,'2022-12-14 00:23:00'],
        ['2022-12-14 01:13:00' ,'2022-12-14 03:31:00'],
        ['2022-12-14 04:27:00' ,'2022-12-14 07:55:00'],
        ['2022-12-14 08:20:00' ,'2022-12-14 08:43:00'],
        ['2022-12-14 09:10:00' ,'2022-12-14 13:02:00'],
        ['2022-12-14 13:49:00' ,'2022-12-14 16:14:00'],
        ['2022-12-14 16:16:00' ,'2022-12-14 17:53:00'],
        ['2022-12-14 19:53:00' ,'2022-12-14 21:55:00'],
        ['2022-12-14 22:44:00' ,'2022-12-15 04:15:00']
    ]
banned_list="('mandb', 'xrandr', 'dpkg', 'fluxbox', 'ssh-agent','sleep', 'sh', 'aterm', 'guishow.sh', 'gzip', 'man-db', 'logrotate', 'apt', 'apt-get', 'run-parts', 'pulseaudio')"

query_total_fail="SELECT process_name, COUNT(*) as Total FROM monitored where event='fail' and process_name not in "+banned_list+" and ("
for intervalo  in intervalos:
    aditional_query_part="timestamp_occured BETWEEN '{inicio}' AND '{fin}' or ".format(inicio=intervalo[0],fin=intervalo[1])
    query_total_fail += aditional_query_part
query_total_fail+=" 1=0) GROUP BY process_name order by (Total)  desc;"
result_dataFrame = pd.read_sql(query_total_fail,mysql_connection)
result_dataFrame.to_csv("results/total_fails.csv",index=False)


for intervalo  in intervalos:
    query_fail="SELECT process_name, COUNT(*) as Total FROM monitored where event='fail' and process_name not in "+banned_list+" and timestamp_occured BETWEEN '{inicio}' AND '{fin}'  GROUP BY process_name order by (Total) desc;".format(inicio=intervalo[0],fin=intervalo[1])
    result_dataFrame = pd.read_sql(query_fail,mysql_connection)
    result_dataFrame.to_csv("results/"+intervalo[0]+"_"+intervalo[1]+"_fails.csv",index=False)
    


for intervalo  in intervalos:
    query='''
    select t1.node_name, t1.process_name, min(t1.timestamp_occured) as firsttime, 
    max(t1.timestamp_occured) as lasttime, temp.total from monitored as t1, 
        (select node_name, process_name , COUNT(*) as total from monitored where event='fail' 
        and timestamp_occured between '{inicio}' and '{fin}' 
        group by node_name,process_name) as temp 
    where t1.event='fail' and t1.process_name not in '''
    query+=banned_list
    query+='''
    and t1.timestamp_occured between '{inicio}' and '{fin}'  
    and temp.node_name=t1.node_name 
    and temp.process_name=t1.process_name  
    group by t1.node_name, t1.process_name order by lasttime, t1.node_name 
    '''
    query = query.format(inicio=intervalo[0],fin=intervalo[1])

    result_dataFrame = pd.read_sql(query,mysql_connection)
    result_dataFrame.to_csv("results/near_"+intervalo[1]+"_fails.csv",index=False)

#     query_fail="SELECT process_name, COUNT(*) as Total FROM monitored where event='fail' and process_name not in "+banned_list+" and timestamp_occured BETWEEN '{inicio}' AND '{fin}'  GROUP BY process_name order by (Total) desc;".format(inicio=intervalo[0],fin=intervalo[1])
#     result_dataFrame = pd.read_sql(query_fail,mysql_connection)
#     result_dataFrame.to_csv("results/"+intervalo[0]+"_"+intervalo[1]+"_fails.csv",index=False)
    

    #pd.set_option('display.expand_frame_repr', False)
    
    # mysql_cursor.execute(query)
    # mysql_cursor.fetchall()
    # print(result_dataFrame.head())
