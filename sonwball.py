#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-02-24 14:54:21
# Project: Snowball
import  datetime
import time
import re
from pyspider.libs.base_handler import *
from lxml import etree


class Handler(BaseHandler):
    crawl_config = {
        'headers' : {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36','X-Requested-With' : 'XMLHttpRequest','Referer' : 'http://xueqiu.com/S/SH601001','Host' : 'xueqiu.com','cache-control' : 'no-cache'}
    }
    
    def __init__(self):
        self.stockcode=['000003']


#这个函数用于产生cookie，为后面做准备
    @every(minutes=5)
    def on_start(self):
        for stockcode in self.stockcode:
            self.crawl('http://xueqiu.com/S/'+'SH'+stockcode,callback=self.first_scrape,save = {'stockcode':stockcode})

#这个函数用来将on_start函数中产生的cookie传入，用于得到最大的页面数
    @config(age=3*60)
    def first_scrape(self, response):
        List = ['%E8%87%AA%E9%80%89%E8%82%A1%E6%96%B0%E9%97%BB','%E5%85%AC%E5%91%8A','%E7%A0%94%E6%8A%A5']

        self.crawl('http://xueqiu.com/statuses/search.json?count=10&comment=0&symbol=SH'+response.save['stockcode']+'&hl=0&source=' +  'user' + '&sort=time&page=' + '1' +'&_=' + str(int(time.time()*1000)),headers = {'Cookie' : str(response.cookies).replace('\'','').replace(',',';').replace('{','').replace('}','').replace(':','=')},callback = self.produce_page,save={'stockcode':response.save['stockcode']})
        self.crawl('http://xueqiu.com/statuses/search.json?count=10&comment=0&symbol=SH'+response.save['stockcode']+'&hl=0&source=' +  'trans' + '&page=' + '1' +'&_=' + str(int(time.time()*1000)),headers = {'Cookie' : str(response.cookies).replace('\'','').replace(',',';').replace('{','').replace('}','').replace(':','=')},callback = self.produce_page,save={'stockcode':response.save['stockcode']})
        for module in List:
            self.crawl('http://xueqiu.com/statuses/stock_timeline.json?symbol_id=SH'+response.save['stockcode']+'&count=10&source=' +  module + '&page=' + '1' +'&_=' + str(int(time.time()*1000)),headers = {'Cookie' : str(response.cookies).replace('\'','').replace(',',';').replace('{','').replace('}','').replace(':','=')},callback = self.produce_page,save={'stockcode':response.save['stockcode']})

#这个函数抓取所有板块的有用信息
    @config(priority=2)
    def produce_page(self, response):

        flag = re.findall('source=(.*?)&',response.url)[0]

        if flag == 'user':
            for i in range(1,int(response.json['maxPage']+1)):

                url = 'http://xueqiu.com/statuses/search.json?count=10&comment=0&symbol=SH'+response.save['stockcode']+'&hl=0&source=' +  flag + '&sort=time&page=' + str(i)+'&_=' + str(int(time.time()*1000))

                self.crawl(url,headers = {'Cookie' : str(response.cookies).replace('\'','').replace(',',';').replace('{','').replace('}','').replace(':','=')},callback = self.deal_page)

        elif flag == 'trans':

            for i in range(1,int(response.json['maxPage']+1)):

                url = 'http://xueqiu.com/statuses/search.json?count=10&comment=0&symbol=SH'+response.save['stockcode']+'&hl=0&source=' +  flag + '&page=' + str(i) +'&_=' + str(int(time.time()*1000))

                self.crawl(url,headers = {'Cookie' : str(response.cookies).replace('\'','').replace(',',';').replace('{','').replace('}','').replace(':','=')},callback = self.deal_page)

        elif flag == '%E8%87%AA%E9%80%89%E8%82%A1%E6%96%B0%E9%97%BB':

            for i in range(1,int(response.json['maxPage']+1)):

                url = 'http://xueqiu.com/statuses/stock_timeline.json?symbol_id=SH'+response.save['stockcode']+'&count=10&source=' +  flag + '&page=' + str(i) +'&_=' + str(int(time.time()*1000))

                self.crawl(url,headers = {'Cookie' : str(response.cookies).replace('\'','').replace(',',';').replace('{','').replace('}','').replace(':','=')},callback = self.deal_page)

        elif flag ==  '%E5%85%AC%E5%91%8A':

             for i in range(1,int(response.json['maxPage']+1)):

                url = 'http://xueqiu.com/statuses/stock_timeline.json?symbol_id=SH'+response.save['stockcode']+'&count=10&source=' +  flag + '&page=' + str(i) +'&_=' + str(int(time.time()*1000))

                self.crawl(url,headers = {'Cookie' : str(response.cookies).replace('\'','').replace(',',';').replace('{','').replace('}','').replace(':','=')},callback = self.deal_page)

        elif flag == '%E7%A0%94%E6%8A%A5':

             for i in range(1,int(response.json['maxPage']+1)):

                url = 'http://xueqiu.com/statuses/stock_timeline.json?symbol_id=SH'+response.save['stockcode']+'&count=10&source=' +  flag + '&page=' + str(i) +'&_=' + str(int(time.time()*1000))

                self.crawl(url,headers = {'Cookie' : str(response.cookies).replace('\'','').replace(',',';').replace('{','').replace('}','').replace(':','=')},callback = self.deal_page)

#这个函数用于格式化数据
    def deal_page(self,response):

         url = ''
         for item in  response.url.split('&')[:-2]:
                temp = item+'&'
                url+=temp

         if re.findall('source=(.*?)&',response.url)[0]=='%E8%87%AA%E9%80%89%E8%82%A1%E6%96%B0%E9%97%BB':
             for each in response.json['list']:
                self.send_message(self.project_name,{
                    'name' : each['user']['screen_name'],
                    'text' : etree.HTML(each['text']).xpath('string(.)'),
                    'time' : each['created_at'],
                    'title' : each['title']
                    }, url = "%s" % (url+str(each['created_at'])))
         else:
              for each in response.json['list']:
                self.send_message(self.project_name,{
                    'name' : each['user']['screen_name'],
                    'text' : etree.HTML(each['text']).xpath('string(.)'),
                    'time' : each['created_at'],
                    #'title' : each['title']
                    }, url = "%s" % (url+str(each['created_at'])))
#返回数据到数据库
    def  on_message(self,project,msg):
        return msg