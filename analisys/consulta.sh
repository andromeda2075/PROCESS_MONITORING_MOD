#!/bin/bash


execute_queries()
{
    fecha_inicio=$1
    fecha_fin=$2

#                                            SELECT node_name, process_name, event, COUNT(*)  FROM monitored  where event="running" and process_name not in ("sleep", "sh", "aterm", "guishow.sh") and timestamp_occured BETWEEN '2022-12-12:14:04' AND '2022-12-12:16:39'  GROUP BY node_name,process_name, event order by (node_name);
mysql -u pruebas2022 -D pruebas2022 -p -e " SELECT node_name, process_name, event, COUNT(*)  FROM monitored  where event='start' and process_name not in ('sleep', 'sh', 'aterm', 'guishow.sh') and timestamp_occured BETWEEN '$fecha_inicio' AND '$fecha_fin'  GROUP BY node_name,process_name, event order by (node_name);"  > start${fecha_inicio}_${fecha_fin}.csv
sed -i  's/\t/,/g' start$fecha_inicio_$fecha_fin.csv
mysql -u pruebas2022 -D pruebas2022 -p -e " SELECT node_name, process_name, event, COUNT(*)  FROM monitored  where event='running' and process_name not in ('sleep', 'sh', 'aterm', 'guishow.sh') and timestamp_occured BETWEEN '$fecha_inicio' AND '$fecha_fin'  GROUP BY node_name,process_name, event order by (node_name);"  > running$fecha_inicio_$fecha_fin.csv
sed -i  's/\t/,/g' running$fecha_inicio_$fecha_fin.csv
mysql -u pruebas2022 -D pruebas2022 -p -e " SELECT node_name, process_name, event, COUNT(*)  FROM monitored  where event='warning' and process_name not in ('sleep', 'sh', 'aterm', 'guishow.sh') and timestamp_occured BETWEEN '$fecha_inicio' AND '$fecha_fin'  GROUP BY node_name,process_name, event order by (node_name);"  > warning$fecha_inicio_$fecha_fin.csv
sed -i  's/\t/,/g' warning$fecha_inicio_$fecha_fin.csv
mysql -u pruebas2022 -D pruebas2022 -p -e " SELECT node_name, process_name, event, COUNT(*)  FROM monitored  where event='fail' and process_name not in ('sleep', 'sh', 'aterm', 'guishow.sh') and timestamp_occured BETWEEN '$fecha_inicio' AND '$fecha_fin'  GROUP BY node_name,process_name, event order by (node_name);"  > fail$fecha_inicio_$fecha_fin.csv
sed -i  's/\t/,/g' fail$fecha_inicio_$fecha_fin.csv
}



execute_queries 2022-12-12:17:05 2022-12-12:19:06

execute_queries 2022-12-12:20:48 2022-12-12:22:52

execute_queries 2022-12-12:23:34 2022-12-13:04:35

execute_queries 2022-12-13:05:02 2022-12-13:07:12




