#!/usr/bin/env python
#coding=utf-8
#Date: 2014.10.11
__version__ = 3.0
__author__ = 'Yusong Xie'
import json, urllib2, sys, argparse
from api import zabbix_api

def main():
    zbxapi = zabbix_api()
    parser = argparse.ArgumentParser(description="This is zabbix api !!")
    #parser.add_argument("-d", "--del", help="this is an optional argument.", action="store_true")
    parser.add_argument("-a", "--action", help="this is an optional argument.", choices=['agent', 'snmp', 'delete', 'clean'])
    parser.add_argument('-l', '--list', help='check host from zabbix server.')
    parser.add_argument('-m', '--tmpid', help='show all templates in zabbix server.')
    parser.add_argument('-g', '--grpid', help='show all groups in zabbix server.')
    parser.add_argument('-f', '--file', help='need to add or delete hosts file.')
    parser.add_argument('-v', '--version', help='show version.', action="store_true")
    args = parser.parse_args()
    if args.version:
        print __version__
    elif args.list:
        res = zbxapi.host_get(args.list)
        if res != 0: print "\t\033[1;32;40mHost_IP: %s \tStat: %s\033[0m" % (args.list, u'已存在.')

    elif args.tmpid == 'list':
        zbxapi.template_get()

    elif args.grpid == 'list':
        zbxapi.hostgroup_get()

    elif args.file:
        f = file(args.file, 'r')
        hosts = f.readlines()
        mid = args.tmpid
        gid = args.grpid
        if args.action == 'agent':
            for ip in hosts:
                ip = ip.strip()
                host_id = zbxapi.host_get(ip)
                if host_id == 0:
                    zbxapi.host_create(ip, gid, mid, type=1, port='10050')
                else:
                    zbxapi.host_update(ip, tmp_id=mid, action='add')

        elif args.action == 'snmp':
            for ip in hosts:
                ip = ip.strip()
                zbxapi.host_create(ip, gid, mid, type=2, port='161')

        elif args.action == 'delete':
            for ip in hosts:
                zbxapi.host_del(ip.strip())

        elif args.action == 'clean':
            for ip in hosts:
                zbxapi.host_update(ip.strip(), mid, action='clean')
    
if __name__ == '__main__':
        main()
