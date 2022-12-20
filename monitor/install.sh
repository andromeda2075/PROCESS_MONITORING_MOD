#!/bin/bash
sourcepath=$(dirname $(realpath $0))
currentpath=$PWD
cd $sourcepath

echo instalando  dependencias 
sudo apt update
sudo apt purge python3-psutil -y
sudo apt install python3 -y

gunzip psutil.tar.gz
tar -xf psutil.tar
cd psutil
sudo ./setup.py install
rm -rf psutil
cd ..

echo Creando carpetas de la aplicacion
sudo mkdir -p /usr/local/monitor 2> /dev/null
sudo mkdir -p /var/local/monitor


sudo cp *.py config.json /usr/local/monitor
sudo chmod a+x /usr/local/monitor/main.py
sudo chmod u+rw  /usr/local/monitor/config.json
sudo chown 1000:1000 /usr/local/monitor/config.json


sudo cp monitor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable monitor.service


sudo systemctl restart monitor.service


cd $currentpath
