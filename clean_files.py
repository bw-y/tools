#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,time


def Usage():
  print '''Usage: %s /path/dir 10 [-m|-d]
  -m minutes
  -d days [default]
''' % sys.argv[0]
  sys.exit(1)

def remainTime():
  now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) 
  timeArray = time.strptime(now, "%Y-%m-%d %H:%M:%S")
  if action == '-m':
    time_point = int(time.mktime(timeArray)) - unit * 60
  elif action == '-d':
    time_point = int(time.mktime(timeArray)) - unit * 24 * 60 * 60
  return time_point

def fetchTime(file_name):
  os.chdir(dir_path)
  if os.path.isfile(file_name):
    f_list = file_name.split('.') 
    for s in f_list:
      f_date = s[0] + s[1]
      if f_date == '20' and len(s) == 12:
        f_time = time.mktime(time.strptime(s, "%Y%m%d%H%M"))
        return int(f_time) 

def autoClean():
  time_point = remainTime() 
  for f in os.listdir(dir_path):
    f_date = fetchTime(f) 
    if type(f_date) == int and f_date <= time_point:
      os.chdir(dir_path)
      os.remove(f)
      print "%s deleted" % f 

def main():
  if action in ('-m', '-d'):
    autoClean()
  else:
    print 'Invalid params %s' % action
    Usage()

if __name__ == '__main__':
  if len(sys.argv) == 4:
    action = str(sys.argv[3])
  elif len(sys.argv) == 3:
    action = '-d'
  else:
    Usage()
  unit = abs(int(sys.argv[2]))
  dir_path = str(sys.argv[1])
  main()
