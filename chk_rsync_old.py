#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import signal
import time
from re import compile

def nscaSend(msg):
  print msg
  send_cmd = os.popen('echo "%s"|/usr/sbin/send_nsca -H 10.8.8.8 -d ";"' % msg)
  print send_cmd.read(),

def file_date(_file, _pattern, _len=12):
  f = _file.split('.')
  for i in f:
    if len(i) == _len:
      if _pattern.findall(i):
        return i

def last_info(_path):
  _files = os.listdir(_path)
  if not _files:
    return 'none'
  _valid = []
  _tmp = []
  for i in _files:
    if '.gz' not in i:
      continue
    if i[0] == '.':
      _tmp.append(i)
    else:
      _valid.append(i)
  _valid.sort()
  pattern = compile(r'^20\d+')
  _res = str(len(_tmp)) + ' ' + file_date(_valid[-1], pattern)
  return _res

def Sig_Handler(sig, frame):
  if os.path.exists(pid_file):
    os.remove(pid_file)
  sys.exit(0)

def Exit():
  if os.path.isfile(pid_file):
    os.remove(pid_file)
  sys.exit() 

def PidCheck():
  signal.signal(signal.SIGTERM, Sig_Handler)
  signal.signal(signal.SIGINT, Sig_Handler)
  signal.signal(signal.SIGQUIT, Sig_Handler)
  try:
    pf = file(pid_file, 'r')
    pid = int(pf.read().strip())
    pf.close()
  except IOError:
    pid = None
  if pid:
    try:
      os.kill(pid, 0)
    except OSError:
      file(pid_file, 'w+').write('%s\n' % os.getpid()) 
      return
    else:
      sys.stdout.write('pid(%d) is running...\n' % pid) 
      sys.exit()
  file(pid_file, 'w+').write('%s\n' % os.getpid()) 

def timeCheck(check_ip, check_path, check_tag, check_time):
  '''调用find查询当前目录是否有变更'''
  res_path = list()
  for p in check_path.split(','):
    if not os.path.isdir(p) or p == '/':
      res_path.append(p + ' - No such directory')
      continue
    stat = os.popen('find %s/ ! -name ".*" -mmin -"%s"' % (p,check_time)).read().strip().replace(p,'')
    if stat == '/' or len(stat) == 0:
      res_path.append(p)
  if "," in check_path:
    if len(res_path):
      host = last_info(res_path[0]) + ' ' + os.popen('hostname').read()
    else:
      host = last_info(check_path.split(",")[0]) + ' ' + os.popen('hostname').read()
  else:
    host = last_info(check_path) + ' ' + os.popen('hostname').read()

  if len(res_path) != 0:
    msg = "%s;%s;2;%s rsync timeout %s minutes - %s" % (check_ip, check_tag, ','.join(res_path), check_time, host)
  else:
    msg = "%s;%s;0;%s rsync OK %s minutes - %s" % (check_ip, check_tag, check_path, check_time, host)
  nscaSend(msg)

def timeFetch(t):
  '''
  解析内置文件的第二个字段,返回一个有效时间列表
  Exam:
    t = ['0-3','21-23',8]
    res = timeFetch(t)
  Would be result:
    res : [00, 01, 02, 03, 21, 22, 23, 8] 
'''
  res = list()
  l = t.split(',')
  for s in l:
    if len(s) in [3,4,5] and '-' in s:
      p = s.split('-')
      if int(p[0]) < int(p[1]):
        for t in range(int(p[0]),int(p[1]) + 1):
          if len(str(t)) == 1:
            t = '0' + str(t)
            res.append(str(t))
          else:
            res.append(str(t))
    elif len(s) == 2:
      res.append(s)
    elif len(s) == 1:
      s = '0' + str(s)
      res.append(s)
  return res

def TaskProc(line):
  n = line.split()
  if len(n) == 4:
    timeCheck(n[0], n[1], n[2], n[3]) 
  elif len(n) == 5: 
    time_period = timeFetch(n[4])
    now = time.strftime("%H",time.localtime())
    if now in time_period:
      msg = "%s;%s;0;No check: %s, Ignore list: %s" % (n[0], n[2], n[1], time_period)
      nscaSend(msg)
    else:
      timeCheck(n[0], n[1], n[2], n[3])
  else:
    return False

def Main(conf_file):
  PidCheck()
  if not os.path.isfile(conf_file):
    sys.stdout.write('%s no such file\n' % conf_file) 
    Exit() 
  file_content = open(conf_file, "r")
  file_list = file_content.readlines()
  if len(file_list) == 0:
    Exit()
  for line in file_list:
    TaskProc(line) 
  Exit()

if __name__ == '__main__':
  global pid_file
  pid_file = '/tmp/' + os.path.basename(sys.argv[0]) + '.pid'
  Main(sys.argv[1])
