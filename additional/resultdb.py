#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
# Created on 2014-10-13 22:18:36

import json
import logging
import time
import re

import datetime
from pymongo import MongoClient
from pyspider.database.base.resultdb import ResultDB as BaseResultDB
from .mongodbbase import SplitTableMixin
logger = logging.getLogger("result")

class ResultDB(SplitTableMixin, BaseResultDB):
    collection_prefix = ''

    def __init__(self, url, database='resultdb'):
        self.conn = MongoClient(url)
        self.database = self.conn[database]
        self.projects = set()

        self._list_project()

    def _parse(self, data):
        data['_id'] = str(data['_id'])
        if 'result' in data:
            data['result'] = json.loads(data['result'])
        return data

    def _stringify(self, data):
        if 'result' in data:
            data['result'] = json.dumps(data['result'])
        return data

    def save(self, project, taskid, url, result):

        #logger.info('url : %s',url)

#(1) deal with guba.eastmoney.com
        if url.split('/')[2] == 'guba.eastmoney.com':
#1.specify the database_name
            stockCode = url.split(',')[1]
            self.database = self.conn[stockCode+'eastmoney']

#2.specify the collection_name
            flag = result['url'].split(',')[2][0]

            # add time for GuYouHui
            now_time = datetime.datetime.now()
            yes_time = now_time + datetime.timedelta(days=-1)
            grab_time = yes_time.strftime('%m-%d')

            if flag == '5':
                collection_name = grab_time+'GuYouHui'
            elif flag == '1':
                collection_name = 'XinWen'
            elif flag == '2':
                collection_name = 'YanBao'
            elif flag == '3':
                collection_name = 'GongGao'
            else:
                collection_name = self._collection_name(project)

#3.create the item which is going to insert to the mongoDB
            obj = {
                # 'taskid': taskid,
                # 'url': url,
                # 'result': result,
                # 'updatetime': time.time(),
                # here has changed
                'read' : result['read'],
                'comment' : result['comment'],
                'title' : result['title'],
                'author' : result['author'],
                # 'date' : result['date'],
                'last' : result['last'],
                'text' : result['text'],
                'url' : result['url'],
                'create' : result['create'],
                'created_at' :result['created_at']
            }
#(2) deal with xueqiu.com
        elif url.split('/')[2] == 'xueqiu.com':

#1.specify the database_name
            stockCode = re.findall('\d{6}',url)[0]
            self.database = self.conn[stockCode+'xueqiu']
#2.specify the collection_name
            flag = re.findall('source=(.*?)&',url)[0]

            logger.info('flag : %s',flag)

            if flag == 'user':
                collection_name = 'TaoLun'
            elif flag == 'trans':
                collection_name = 'JiaoYi'
            elif flag == '%E8%87%AA%E9%80%89%E8%82%A1%E6%96%B0%E9%97%BB':
                collection_name = 'XinWen'
            elif flag == '%E5%85%AC%E5%91%8A':
                collection_name = 'GongGao'
            elif flag == '%E7%A0%94%E6%8A%A5':
                collection_name = 'YanBao'
            else:
                collection_name = self._collection_name(project)

#3.create the item which is going to insert to the mongoDB
            if flag == '%E8%87%AA%E9%80%89%E8%82%A1%E6%96%B0%E9%97%BB':

                obj = {
                    'name' : result['name'],
                    'text' : result['text'],
                    'time' : long(result['time']),
                    'title' : result['title'],

                }
            else:
                obj = {
                    'name' : result['name'],
                    'text' : result['text'],
                    'time' : long(result['time']),
                    # 'title' : result['title'],

                }
# (3)deal with guba.sina.com
        elif url.split('/')[2] == 'guba.sina.com.cn':
# 1.specify the database name
            stockCode = re.findall('name=(.*?)&type',result['url'])[0]
            self.database = self.conn[stockCode+'sina']
# 2.specify the collection name
            collection_name = 'TaoLun'

# 3.create the item which is going to insert to the mongoDB
            obj = {
                    'author' : result['author'],
                    'comment' : result['comment'],
                    'read' : long(result['read']),
                    'title' : result['title'],
                    'text' : result['text'],
                    'tid' : result['tid'],
                    'time' : result['time'],
                    'url' : result['url']
                }


        return self.database[collection_name].update(
            {'taskid': taskid}, {"$set": self._stringify(obj)}, upsert=True
        )

    def select(self, project, fields=None, offset=0, limit=0):
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            return
        collection_name = self._collection_name(project)
        for result in self.database[collection_name].find(fields=fields, skip=offset, limit=limit):
            yield self._parse(result)

    def count(self, project):
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            return
        collection_name = self._collection_name(project)
        return self.database[collection_name].count()

    def get(self, project, taskid, fields=None):
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            return
        collection_name = self._collection_name(project)
        ret = self.database[collection_name].find_one({'taskid': taskid}, fields=fields)
        if not ret:
            return ret
        return self._parse(ret)
