#!/usr/bin/env python
#coding=utf-8
#Date: 2014.10.11
__version__=1.0
__author__='Yusong Xie'
import json
import urllib2
import sys

class zabbix_api():
    def __init__(self):
        self.url = "http://172.16.33.10/api_jsonrpc.php"
        self.header = {"Content-Type": "application/json"}
        self.authID = self.__login__()

    """ 提交POST数据模板 """
    def req_data(self, method, params):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "auth": self.authID,
            "id": 1 })
        return data

    """ 获取用户权限Id """
    def __login__(self):
        data = json.dumps({
                    "jsonrpc": "2.0",
                    "method": "user.login",
                    "params": {"user": "admin", "password": "admin"},
                    "id": 1 })
        authID = self.get_data(data)['result']
        return authID

    """ 提交请求，获取返回信息 """
    def get_data(self, data, hostip=""):
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key,self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'Error code: ', e.code
            return 0
            #sys.exit(1)
        res = json.loads(result.read())
        return res
        result.close()

    """ 根据IP，获取hostId """
    def host_get(self, hostip):
        method = "host.get"
        params =  { "output": "extend",
                    "filter": {"host": hostip}
        }

        data = self.req_data(method, params)
        res = self.get_data(data, hostip)['result']
        if res and res != 0:
            host = res[0]
            return host['hostid']
        else:
            print '\t',"\033[1;31;40mNot found the host: %s\033[0m" % hostip
            return 0

    """ 更新host模板信息 """
    def host_update(self, hostip, tmp_id, action):
        mod = ""
        hostid = self.host_get(hostip)
        method = "host.update"
        if hostid != 0:
            if action == 'clean':
                mod = "templates_clear"
            elif action == 'add':
                mod = "templates"
            tid_list = []
            tmp_id = tmp_id.split(",")
            for i in tmp_id:
                tid_list.append({"templateid": i})
            
            params = {"hostid": hostid,
                      mod: tid_list,
                      #"inventory_mode": 1, # -1 - disabled;  0 - (default) manual; 1 - automatic.
                      #"inventory": {"location": "Latvia, Riga"}
            }
            data = self.req_data(method, params)
            res = self.get_data(data, hostip)
            if not res or res == 0:
                print u"\tupdate faild %s %s" % (hostip, e)
            else:
                print u"\ttemplate id %s %s OK" % (tmp_id, action)

    """ 删除host """
    def host_del(self, hostip):
        method = "host.delete"
        hostid = self.host_get(hostip)
        if hostid != 0:
            params = [hostid]
            data = self.req_data(method, params)
            res = self.get_data(data, hostip)
            if not res or res == 0:
                print u"delete %s faild." % hostip
            else:
                print u"Host:\033[041m %s\033[0m  已删除 !" % hostip 
        #else: print "\t\033[1;31;40m%s\033[0m" % "This host cannot find in zabbix,please check it !"

    """ 获取主机群组信息 """
    def hostgroup_get(self):
        data = json.dumps({
                    "jsonrpc": "2.0",
                    "method": "hostgroup.get",
                    "params": {"output": "extend",},
                    "auth": self.authID,
                    "id": 1,
        })
        res = self.get_data(data)
        if 'result' in res.keys():
            res = res['result']
            if (res !=0) or (len(res) != 0):
                print "\033[1;32;40m%s\033[0m" % "Number Of Group: ", "\033[1;31;40m%d\033[0m" % len(res)
                for host in res:
                    print "\t","HostGroup_id:",host['groupid'],"\t","HostGroup_Name:",host['name'].encode('utf-8')
                print
        else:
            print "Get HostGroup Error, please check !"

    """ 获取模板信息 """
    def template_get(self):
        method = "template.get"
        params = { "output": "extend", }
        data = self.req_data(method, params)
        res = self.get_data(data)
        if 'result' in res.keys():
            res = res['result']
            if (res !=0) or (len(res) != 0):
                print "\033[1;32;40m%s\033[0m" % "Number Of Template: ", "\033[1;31;40m%d\033[0m" % len(res)
                for host in res:
                    print "\t","Template_id:",host['templateid'],"\t","Template_Name:",host['name'].encode('utf-8')
                print
        else:
            print "Get Template Error,please check !"

    """ 增加主机监控 """
    def host_create(self, hostip, g_id, m_id, type, port):
        method = "host.create"
        hostip = hostip
        groupid = g_id
        templateid = m_id
        type = type
        port = port
        g_list=[]
        t_list=[]
        for i in groupid.split(','):
            var = {}
            var['groupid'] = i
            g_list.append(var)
        for i in templateid.split(','):
            var = {}
            var['templateid'] = i
            t_list.append(var)
        if hostip and groupid and templateid:
            params = {"host": hostip,
                      "interfaces": [{"type": type, "main": 1, "useip": 1, "ip": hostip, "dns": "", "port": port}],
                      "groups": g_list,
                      "templates": t_list
            }
            data = self.req_data(method, params)
            res = self.get_data(data, hostip)
            if 'result' in res.keys():
                res = res['result']
                if 'hostids' in res.keys():
                    print "\033[1;32;40m%s\033[0m" % "Create host: %s success" % hostip
            else:
                print "\033[1;31;40m%s\033[0m" % "Create host: %s failure: %s" % (hostip,res['error']['data'])
        else:
            print "\033[1;31;40m%s\033[0m" % "Enter Error: ip or groupid or tempateid is NULL,please check it !"

    def history_get(self, itemid, time_from, time_till, i=3, limit=100):
        method = "history.get"
        params = {
               "output": "extend",
               "history": i,
               "itemids": itemid,
               "sortfield": "clock",
               "sortorder": "DESC",
               "time_from": time_from,
               "time_till": time_till,
               "limit": limit,
               "search": {'value': 'clock'}
               }
        data = self.req_data(method, params)
        rs = self.get_data(data)['result']
        return rs

def Useage():
    print """Usage: 
    main.py [option]... [[-m <tmplate id>] [-g <group id>] [-f <hosts>]] [arg]...
    Options and arguments (and corresponding environment variables):

    ./main.py -h help : get help\n""" 

if __name__ == '__main__':
        Useage()
