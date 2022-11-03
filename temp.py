#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2009, Giampaolo Rodola'. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""
A clone of 'sensors' utility on Linux printing hardware temperatures.
$ python3 scripts/sensors.py
asus
    asus                 47.0 °C (high = None °C, critical = None °C)
acpitz
    acpitz               47.0 °C (high = 103.0 °C, critical = 103.0 °C)
coretemp
    Physical id 0        54.0 °C (high = 100.0 °C, critical = 100.0 °C)
    Core 0               47.0 °C (high = 100.0 °C, critical = 100.0 °C)
    Core 1               48.0 °C (high = 100.0 °C, critical = 100.0 °C)
    Core 2               47.0 °C (high = 100.0 °C, critical = 100.0 °C)
    Core 3               54.0 °C (high = 100.0 °C, critical = 100.0 °C)
"""


import psutil
import sys
'''
temperaturas= list()
temps = psutil.sensors_temperatures()
for name, entries in temps.items():
       if name !='': 
                for entry in entries:
                        temperaturas.append(entry)
             
print(temperaturas)
'''
'''
def main():
    if not hasattr(psutil, "sensors_temperatures"):
        sys.exit("platform not supported")
    temps = psutil.sensors_temperatures()
    if not temps:
        sys.exit("can't read any temperature")
    for name, entries in temps.items():
        print(name)
        for entry in entries:
            print("    %-20s %s °C (high = %s °C, critical = %s °C)" % (
                entry.label or name, entry.current, entry.high,
                entry.critical))
        print()


if __name__ == '__main__':
    main()

print(str(psutil.sensors_temperatures()[ 'coretemp' ][n].label) + " has a temperature of " + str(psutil.sensors_temperatures()[ 'coretemp' ][n].current) + "C")  
    if psutil.sensors_temperatures()[ 'coretemp' ][n].current > psutil.sensors_temperatures()[ 'coretemp' ][n].high:  
        print("Temperature is too high")


'''
import psutil  
temperatures_names_partitions=list() 
temperatures_values_partitions=list()
# monitoring temperature  
for n in range(len(psutil.sensors_temperatures()[ 'coretemp' ])):  
        temperatures_names_partitions.append(psutil.sensors_temperatures()[ 'coretemp' ][n].label)
        temperatures_values_partitions.append(psutil.sensors_temperatures()[ 'coretemp' ][n].current)
print(temperatures_names_partitions)
print(temperatures_values_partitions)
  
