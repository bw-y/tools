#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,time,math

check_path = sys.argv[1]
check_time = sys.argv[2]
ignore_file = '/etc/check_rsync_invalid.ini'

if len(sys.argv)<3:
  sys.exit('usage: %s path minute' % sys.argv[0])

def timeCheck():
  '''调用find查询当前目录是否有变更'''
  stat = os.popen('find %s/ ! -name ".*" -mmin -"%s"' % (check_path,check_time)).read().strip().replace(check_path,'')
  if stat == '/':
    print "Too long time no synchronization"
    sys.exit(2)
  elif len(stat) == 0:
    print "Too long time no synchronization"
    sys.exit(2)
  else:
    print "rsync OK in %s minute" % sys.argv[2]
    sys.exit(0)



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
        for t in range(int(p[0]),int(p[1])):
          if len(str(t)) == 1:
            t = '0' + str(t)
            res.append(str(t))
          else:
            res.append(str(t))
    elif len(s) == 2:
      res.append(s)
  return res

def noCheck():
  '''读取内置文件,并获取匹配路径的忽略时间列表'''
  file_content = open(ignore_file, "r")
  for c in file_content:
    c = c.split()
    if c[0] == check_path:
      file_content.close()
      return timeFetch(c[1])
  file_content.close()
  return '-- https://github.com/bw-y --'

if os.path.isfile(ignore_file):
  time_period = noCheck()
  now = time.strftime("%H",time.localtime())
  if now in time_period:
    print 'No check: %s, Now Hour: %s, Ignore list: %s' % (check_path, now, time_period)
    sys.exit(0)
  else:
    timeCheck()
else:
  timeCheck()
