#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

def rec(_path):
  print _path
  if os.path.isfile(_path):
    return
  for i in os.listdir(_path):
    now_path = _path + i
    if os.path.isfile(now_path):
      print now_path
    elif os.path.isdir(now_path):
      print now_path
      rec(now_path + '/')


rec(sys.argv[1])
