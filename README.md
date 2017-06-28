# zbxapi
zabbix api 

# set user,passwd in api.py  

# usage 
python main.py -h
usage: main.py [-h] [-a {agent,snmp,delete,clean}] [-l LIST] [-m TMPID]
               [-g GRPID] [-f FILE] [-v]

This is zabbix api !!

optional arguments:
  -h, --help            show this help message and exit
  -a {agent,snmp,delete,clean}, --action {agent,snmp,delete,clean}
                        this is an optional argument.
  -l LIST, --list LIST  check host from zabbix server.
  -m TMPID, --tmpid TMPID
                        show all templates in zabbix server.
  -g GRPID, --grpid GRPID
                        show all groups in zabbix server.
  -f FILE, --file FILE  need to add or delete hosts file.
  -v, --version         show version.
