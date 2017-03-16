#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib2
import json


class Tools(object):
    @staticmethod
    def get_active(nn_urls):
        nn = nn_urls
        if "," in nn:
            nn = nn.split(",")
        else:
            url = 'http://' + nn
            return url
        for u in nn:
            url = 'http://' + u
            check_url = url + '/jmx?qry=Hadoop:service=NameNode,name=NameNodeStatus'
            try:
                res = json.load(urllib2.urlopen(check_url))
                if res['beans'][0]['State'] == 'active':
                    return url
            except:
                continue

    @staticmethod
    def hdfs_status(nn, path, user='hdfs'):
        url = nn + '/webhdfs/v1' + path + '?op=LISTSTATUS' + '&user.name=' + user
        raw = urllib2.urlopen(url)
        res = json.loads(raw.read())
        return res[u'FileStatuses'][u'FileStatus']


class Base(object):
    def __init__(self, nn_urls, hdfs_path, local_path, action='sync', user='hdfs'):
        self.nn_urls = nn_urls
        self.action = action
        self.hdfs_path = hdfs_path
        self.local_path = local_path
        self.user = user

    def start(self):
        if self.action == 'sync':
            self.route(self.hdfs_path)

    def route(self, _path):
        url = Tools.get_active(self.nn_urls) + '/webhdfs/v1' + _path + '?op=LISTSTATUS' + '&user.name=' + self.user
        res = json.load(urllib2.urlopen(url))
        for d in res[u'FileStatuses'][u'FileStatus']:
            _now_path = "%s%s" % (_path, d['pathSuffix'])
            if d['type'] == 'FILE':
                print "%s" % _now_path
            elif d['type'] == 'DIRECTORY':
                print "%s/" % _now_path
                self.route(_now_path + '/')

if __name__ == '__main__':
    instance = Base(nn_urls='10.123.59.17:50070,10.123.72.244:50070', hdfs_path=sys.argv[1], local_path=sys.argv[2])
    instance.start()
