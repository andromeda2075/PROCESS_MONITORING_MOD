import psutil
lista={}
for proc in psutil.process_iter():
    print(proc.name(), proc.pid)
   