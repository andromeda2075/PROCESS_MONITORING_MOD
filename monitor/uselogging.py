import logging

class logging_monitored:
    name_file=''
    mode_log=''
    date=''


    def __init__(self,outputfile):
        self.name_file=outputfile #'log_monitor.log'
        self.mode_log='DEBUG'
        self.date='%m/%d/%Y %I:%M:%S %p'

    def main_config(self):
        logging.basicConfig(filename=self.name_file,format='%(asctime)s %(message)s',datefmt=self.date,level=self.mode_log)

    def diagnostic_info_child(self,proc_child,proc_parent):
        #logging.info('Se registra el proceso %s cuyo hijo es %s',proc,child)
        logging.info('Se registra el proceso hijo %s cuyo padre es  %s',proc_child,proc_parent)

    def diagnostic_debug(self,message):
        logging.debug(message)

    def event(self,event,proc):
        logging.debug('Guardado procesos %s con evento %s',proc,event)
