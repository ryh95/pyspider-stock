#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-02-02 11:38:51
# Project: HelloWorld
import re
from pyspider.libs.base_handler import *
from lxml import etree
from pymongo import *

#num = 0
class Handler(BaseHandler):
    crawl_config = {
    }






    @every(minutes = 20)
    def on_start(self):

        self.crawl('http://guba.sina.com.cn/?s=bar&name=sz000001&type=0&page=1',callback = self.index_page)

    @config(age = 3*60)
    def index_page(self, response):
        selector = etree.HTML(response.text)
        content_field =  selector.xpath('//*[@id="blk_list_02"]/table/tbody/tr')


        # 提取每一页的所有帖子
        for each in content_field[1:]:
            item = {}
            read = each.xpath('td[1]/span/text()')[0]
            comment = each.xpath('td[2]/span/text()')[0]
            title = each.xpath('td[3]/a/text()')[0]
            # author容易因为结构出现异常
            # if each.xpath('td[4]/div/a[1]/text()'):
            #     author = each.xpath('td[4]/div/a[1]/text()')[0]
            # elif each.xpath('td[4]/div/text()'):
            #     author = each.xpath('td[4]/div/text()')[0]
            # else:
            #     author = ''
            if each.xpath('td[4]/div/text()'):
                author = each.xpath('td[4]/div/text()')[0]
            elif each.xpath('td[4]/div/a[1]/text()'):
                author = each.xpath('td[4]/div/a[1]/text()')[0]
            else:
                author = ''


            # 将数据放入item
            item['read'] = read
            item['comment'] = comment
            item['title'] = title
            item['author'] = author
            item['url'] = response.url

            Url = 'http://guba.sina.com.cn'+each.xpath('td[3]/a/@href')[0]

            # 提取内容
            self.crawl(Url,callback=self.detail_page,save={'item':item})

        page = int(response.url.split('&')[3].split('=')[1])
        next_page = int(selector.xpath('//*[@id="blk_list_02"]/div[@class="blk_01_b"]/p/a[last()]/@href')[0].split('&')[3].split('=')[1])
        if(page<next_page):
            page+=1
            url = 'http://guba.sina.com.cn/?s=bar&name=sz000001&type=0&page=' + str(page)
            self.crawl(url,callback = self.index_page)


    def detail_page(self, response):
        selector =  etree.HTML(response.text)
        data = selector.xpath('//*[@id="thread_content"]')[0]
        text =  data.xpath('string(.)').replace('\n','').replace('\r','').replace('t','')
        item = response.save['item']
        item['text'] = text
        #time = response.doc('.iltp_time > span').text()
        time = re.findall('<div class=\'fl_left iltp_time\'><span>(.*?)</span></div>',response.text)[0]
        #time = selector.xpath('//*[@id="thread"]/div[@class="il_txt"]/div[@class="ilt_panel clearfix"]/div[@class="fl_left iltp_time"]/span/text()')
        item['time'] = time
        item['tid'] = int(re.findall('tid=(.*?)&bid',response.url)[0])
        return item

