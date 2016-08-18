#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from re import compile
from signal import SIGUSR1


class Base(object):
    def __init__(self, log_file_path, tag="chk_ngx_timeout", trigger=0.1, warn=50, critical=100, nginx_pid_path="/var/run/nginx.pid"):
        self.log = log_file_path
        self.pid_file = nginx_pid_path
        self.tag = tag
        self.trigger = trigger
        self.warn = warn
        self.critical = critical
        self.log_tmp = log_file_path + '.9999'

    def check_timeout(self, _dict):
        host = _dict['name'].split(":")[0]
        count = _dict['count']
        timeout_sum = 0
        for k in _dict.keys():
            if k in ["name", "count"]:
                continue
            if float(k) > self.trigger:
                timeout_sum += 1
        res = "%.2f" % (timeout_sum / float(count) * 10000)
        if float(res) >= float(self.critical):
            status = 2
        elif float(res) > float(self.warn) < float(self.critical):
            status = 1
        else:
            status = 0
        nagios_info = "%s;%s;%d;%s => %s ~ %d/%d" % (host, self.tag, status, self.trigger, res, timeout_sum, count)
        return nagios_info

    def check_log(self):
        """ 统计每个ip的每个请求的时间消耗.

        Return: 一个list类型数据,其中包含N个json结果
        """
        res = list()
        f = open(self.log_tmp)
        pattern = compile(r'^\d\.\d\d\d \d.*:8080$')
        for raw_line in f.readlines():
            if not pattern.match(raw_line):
                continue
            raw_line = raw_line.split()
            list_dict_key = str(raw_line[0])
            list_dict_name = raw_line[1]
            Tools.generate_res_list(res, list_dict_name, list_dict_key)
        return res

    def run(self):
        os.rename(self.log, self.log_tmp)
        Tools.notice_nginx_reopen_log_file(self.pid_file)
        for i in self.check_log():
            Tools.send_nagios(self.check_timeout(i))
        os.remove(self.log_tmp)


class Tools(object):
    @staticmethod
    def notice_nginx_reopen_log_file(pid_file):
        os.kill(int(open(pid_file).read()), SIGUSR1)

    @staticmethod
    def set_key_name(_list, _str, _key='name'):
        n = 0
        for i in _list:
            if _str == i[_key]:
                n += 1
        if not n:
            _list.append({_key: _str})

    @staticmethod
    def generate_res_list(_list, _name, _elapsed):
        Tools.set_key_name(_list, _name)
        for i in _list:
            if _name == i['name']:
                if 'count' in i:
                    i['count'] += 1
                else:
                    i['count'] = 1
                if _elapsed in i:
                    i[_elapsed] += 1
                else:
                    i[_elapsed] = 1

    @staticmethod
    def send_nagios(msg):
        print msg
        send_cmd = os.popen('echo "%s"|/usr/sbin/send_nsca -H 10.8.8.8 -d ";"' % msg)
        print send_cmd.read(),

if __name__ == '__main__':
    obj = Base("/var/log/nginx/wujian.log", trigger=0.1, warn=50, critical=100)
    obj.run()