#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time


class RsyncCheck(object):
    def __init__(self, list_file, nagios='10.8.8.8'):
        self.list_file = list_file
        self.nagios = nagios
        self.pid_file = '/tmp/' + os.path.basename(sys.argv[0]) + '.pid'
        self.__pid_check()

    def __pid_check(self):
        try:
            pf = file(self.pid_file, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        if pid:
            try:
                os.kill(pid, 0)
            except OSError:
                file(self.pid_file, 'w+').write('%s\n' % os.getpid())
                return
            else:
                sys.stdout.write('pid(%d) is running...\n' % pid)
                sys.exit()
        file(self.pid_file, 'w+').write('%s\n' % os.getpid())

    def quit(self):
        if os.path.isfile(self.pid_file):
            os.remove(self.pid_file)
        sys.exit()


if __name__ == '__main__':
    obj = RsyncCheck(sys.argv[1])