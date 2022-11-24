import psutil
import math
import re
from itertools import accumulate


disk_partitions = psutil.disk_partitions()
disk_free=[]
disk_used=[]
pattern = '/dev/sd'

# Información de cada partición
for partition in disk_partitions:
    text = partition.device
    match = re.search(pattern, text)
    if match:
        disk_usage = psutil.disk_usage(partition.mountpoint)
        disk_free.append(disk_usage.free)
        disk_used.append(disk_usage.used)

free=list(accumulate(disk_free))
used=list(accumulate(disk_used))
print(free[-1])
print(used[-1])
print(used[-1]/(used[-1]+free[-1])*100)
percent=math.ceil(round(used[-1]/(used[-1]+free[-1])*100,2))
print('% ',percent)




        
