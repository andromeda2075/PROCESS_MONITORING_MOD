#!/bin/bash
sourcepath=$(dirname $(realpath $0))
currentpath=$PWD
cd $sourcepath

echo instalando  dependencias 
sudo apt update
sudo apt install python3 python3-psutil -y

echo Creando carpetas de la aplicacion
sudo mkdir -p /usr/local/monitor 2> /dev/null
sudo mkdir -p /var/local/monitor 2> /dev/null


sudo cp main.py configuration.py repository.py config.json system_monitor_mod.py process_monitor.py README.md /usr/local/monitor
sudo chmod a+x /usr/local/monitor/main.py
sudo chmod u+rw  /usr/local/monitor/config.json
sudo chown 1000:1000 /usr/local/monitor/config.json


sudo cp monitor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable monitor.service


sudo systemctl start monitor.service
sudo systemctl status monitor.service


cd $currentpath
