import psutil
import math

disks=[]
# Discos duros
disk_partitions = psutil.disk_partitions()

# Información de cada partición
for partition in disk_partitions:
    disk_usage = psutil.disk_usage(partition.mountpoint)
    
    if disk_usage==100:
        print("* {0}, uso%: {1}".format(partition.device, disk_usage.percent, "%"))
        disks.append(disk_usage.percent)
    else:
        print("* {0}, uso%: {1}".format(partition.device, math.ceil(disk_usage.percent), "%"))
        disks.append(math.ceil(math.ceil(disk_usage.percent)))
    
mean=sum(disks)/float(len(disks))
print("uso total promedio de disco: ", mean, ' %')

        
