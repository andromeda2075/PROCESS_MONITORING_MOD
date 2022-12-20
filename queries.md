SELECT node_name, process_name, event, COUNT(*)  FROM monitored 
where event="fail" and process_name not in ("sleep", "sh", "aterm", "guishow.sh") and timestamp_occured BETWEEN '2022-12-12 14:04:00' AND '2022-12-12 16:39:00' GROUP BY node_name,process_name, event order by (node_name);


SELECT node_name, process_name, event, COUNT(*)  FROM monitored 
where event="running" and process_name not in ("sleep", "sh", "aterm", "guishow.sh","fluxbox") and timestamp_occured BETWEEN '2022-12-12:14:04' AND '2022-12-12:16:39' 
GROUP BY node_name,process_name, event order by (node_name);


inicio="'2022-12-12 14:04:00'"
fin="'2022-12-15 04:15:00'"
event="'fail'"

DIA 1 

2022-12-12:14:04
2022-12-12:16:39

2022-12-12:17:05
2022-12-12:19:06

2022-12-12:20:48
2022-12-12:22:52

2022-12-12:23:34
2022-12-13:04:35

2022-12-13:05:02
2022-12-13:07:12


mysql -u pruebas2022 -D pruebas2022 -p -e " SELECT node_name, process_name, event, COUNT(*) 
 FROM monitored  where event='start' and process_name not in ('sleep', 'sh', 'aterm', 'guishow.sh') and timestamp_occured 
 BETWEEN '2022-12-12:17:05' AND '2022-12-12:19:06'  GROUP BY node_name,process_name, event order by (node_name)"> start.txt