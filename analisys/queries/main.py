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

# query_total_fail="SELECT process_name, COUNT(*) as Total FROM monitored where event='fail' and process_name not in "+banned_list+" and ("
# for intervalo  in intervalos:
#     aditional_query_part="timestamp_occured BETWEEN '{inicio}' AND '{fin}' or ".format(inicio=intervalo[0],fin=intervalo[1])
#     query_total_fail += aditional_query_part
# query_total_fail+=" 1=0) GROUP BY process_name order by (Total)  desc;"
# result_dataFrame = pd.read_sql(query_total_fail,mysql_connection)
# result_dataFrame.to_csv("results/total_fails.csv",index=False)


# for intervalo  in intervalos:
#     query_fail="SELECT process_name, COUNT(*) as Total FROM monitored where event='fail' and process_name not in "+banned_list+" and timestamp_occured BETWEEN '{inicio}' AND '{fin}'  GROUP BY process_name order by (Total) desc;".format(inicio=intervalo[0],fin=intervalo[1])
#     result_dataFrame = pd.read_sql(query_fail,mysql_connection)
#     result_dataFrame.to_csv("results/"+intervalo[0]+"_"+intervalo[1]+"_fails.csv",index=False)

query_total_event_process_node_template='''
select node_name, process_name, count(*) as total, max(timestamp_occured) as lasttime, min(timestamp_occured) as firsttime from monitored where
event='{event}' and timestamp_occured between '{inicio}' and '{fin}' group by node_name, process_name
'''

query_total_start_fail_process_node_template='''
select temp1.node_name, temp1.process_name, 
temp1.total as total_start, temp1.firsttime as firststart, temp1.lasttime as laststart,
temp2.total as total_fail, temp2.firsttime as firstfail, temp2.lasttime as lastfail
from  ({total_start_query}) as temp1, ({total_fail_query}) as temp2 
where temp1.process_name=temp2.process_name and temp1.node_name=temp2.node_name 
and temp1.process_name not in {banned} 
order by lastfail;
'''



for intervalo  in intervalos:
    query_total_start_process_node=query_total_event_process_node_template.format(event='start',inicio=intervalo[0],fin=intervalo[1])
    # print(query_total_start_process_node)
    query_total_fail_process_node=query_total_event_process_node_template.format(event='fail',inicio=intervalo[0],fin=intervalo[1])
    # print(query_total_fail_process_node)
    query_total_start_fail_process_node=query_total_start_fail_process_node_template.format(total_start_query=query_total_start_process_node,total_fail_query=query_total_fail_process_node,banned=banned_list)

    result_dataFrame = pd.read_sql(query_total_start_fail_process_node,mysql_connection)
    result_dataFrame.to_csv("results/near_"+intervalo[1]+"_fails.csv",index=False)
