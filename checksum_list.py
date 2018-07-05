#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
from subprocess import Popen, PIPE

class Base(object):
    def __init__(self, httpfs, hdfs_path, action='start'):
        self.httpfs = httpfs
        self.action = action
        self.hdfs_path = hdfs_path
        self.curl_cmd = 'curl --negotiate -u :'

    def start(self):
        if self.action == 'start':
            self.route(self.hdfs_path)

    def route(self, _path):
        _path = _path.replace("$", "\\$")
        _path = _path.replace("%", "%25")
        url = self.httpfs + _path + '?op=LISTSTATUS'
        cmd_run = Popen("%s %s" % (self.curl_cmd, url), shell=True, stderr=PIPE, stdout=PIPE)
        cmd_run.wait()
        res = json.loads(cmd_run.stdout.read())
        #print "%s %s" % (self.curl_cmd, url)
        #print res
        for d in res[u'FileStatuses'][u'FileStatus']:
            _now_path = "%s%s" % (_path, d['pathSuffix'])
            #print "- %s -> %s " % (d['type'], _now_path)
            if d['type'] == 'FILE':
                #print "--F %s " % _now_path
                file_path = _now_path.replace("$", "\\$")
                file_path = file_path.replace("%", "%25")
                get_checksum = Popen('%s %s%s?op=GETFILECHECKSUM' % (self.curl_cmd, self.httpfs, file_path), shell=True, stderr=PIPE, stdout=PIPE )
                get_checksum.wait()
                checksum_res = json.loads(get_checksum.stdout.read())
                #print checksum_res
                print "%s %s" % (checksum_res[u'FileChecksum'][u'bytes'], _now_path)
            elif d['type'] == 'DIRECTORY':
                #print "--D %s/" % _now_path
                self.route(_now_path + '/')

if __name__ == '__main__':
    instance = Base(httpfs='http://n2:14000/webhdfs/v1', hdfs_path=sys.argv[1])
    instance.start()
