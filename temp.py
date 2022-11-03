

import psutil
temps = psutil.sensors_temperatures()

for name, entries in temps.items():
      
        print(name)
        #print(entries[0].current)
        print(entries)
        print()
        