# PROCESS-MONITORING
Este proyecto desarrolla el monitoreo de procesos específicos que caen


{
  "db_file": "base.db",
  "ring_base": false,
  "max_register":2000,
  "healthpc_period_verification": 5,   //, Tiempo de refresco de todos los procesos para la verificación de ocurrencias o eventos
  "healthpc_period_loging": 30,       //, Tiempo que registra el estado para guardar
  "processes_period_verification": 5,
  "max_process_consume_ram":100,  //, Consumo RAM por proceso: 100 MB
  "max_process_consume_cpu":5,    //, Consumo CPU por proceso 5 %
  "process_list":[
        {
          "name":"ospl",
          "period_loging":30,
          "monitoring_children":true
        },
        {
          "name":"Rms-node-run",
          "period_loging":30,
          "monitoring_children":true
        
        }
    ]
    
}

