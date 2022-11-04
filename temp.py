
import psutil

temperatures_names_partitions=list() 
temperatures_values_partitions=list()
temperatures_states=list()
# monitoring temperature  
for n in range(len(psutil.sensors_temperatures()[ 'coretemp' ])):
        temp=psutil.sensors_temperatures()[ 'coretemp' ][n].current
        if 24<=temp and temp <=41:
                temperatures_states.append('Reposo')
        elif 42<=temp and temp <=70:
                temperatures_states.append('Normal')
        elif 71<=temp and temp<=75:
                temperatures_states.append('Maximo')
        elif temp>75:
                temperatures_states.append('Alerta')
        temperatures_names_partitions.append(psutil.sensors_temperatures()[ 'coretemp' ][n].label)
        temperatures_values_partitions.append(psutil.sensors_temperatures()[ 'coretemp' ][n].current)
print(str(temperatures_names_partitions))
print(str(temperatures_values_partitions))
print(str(temperatures_states))      

