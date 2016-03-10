#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-02-02 11:38:51
# Project: HelloWorld
import re
from pyspider.libs.base_handler import *
from lxml import etree

#num = 0
class Handler(BaseHandler):
    crawl_config = {
    }
    
   

    @every(minutes = 5)
    def on_start(self):
        initcode = '601001'
        StockCodes = []
        temp = initcode
        
        for i in range(1):
            StockCodes.append(temp)
            temp = str(int(temp)+1)
        #print StockCodes
        
        for stockcode in StockCodes:
            self.crawl('http://guba.eastmoney.com/list,' + stockcode + ',5_1.html', callback=self.index_page)
        #global num
        #num += 1

    @config(age = 2*60)
    def index_page(self, response):
        selector = etree.HTML(response.text)
        content_field =  selector.xpath('//*[@id="articlelistnew"]/div[starts-with(@class,"articleh")]')
       
        # 提取每一页的所有帖子
        for each in content_field:
            item = {}
            read = each.xpath('span[1]/text()')[0]
            comment = each.xpath('span[2]/text()')[0]
            title = each.xpath('span[3]/a/text()')[0]
            # author容易因为结构出现异常
            if each.xpath('span[4]/a/text()'):
                author = each.xpath('span[4]/a/text()')[0]
            else:
                author = each.xpath('span[4]/span/text()')[0]

            #date = each.xpath('span[5]/text()')[0]
            last = each.xpath('span[6]/text()')[0]
            address = each.xpath('span[3]/a/@href')[0]
            baseUrl = 'http://guba.eastmoney.com'
            Url = baseUrl+address
            # 将数据放入item
            item['read'] = read
            item['comment'] = comment
            item['title'] = title
            item['author'] = author
            # item['date'] = date
            item['last'] = last
            item['url'] = response.url

            # 提取内容
            self.crawl(Url,callback=self.detail_page,save={'item':item})
            
        #if num == 1:    
        # 生成下一页链接
        info = selector.xpath('//*[@id="articlelistnew"]/div[@class="pager"]/span/@data-pager')[0]
        List = info.split('|')
        if int(List[2])*int(List[3])<int(List[1]):
            nextLink = response.url.split('_')[0] +  '_'  + str(int(List[3])+1) + '.html'
            self.crawl(nextLink,callback = self.index_page)

   
    def detail_page(self, response):
        selector =  etree.HTML(response.text)
        info = selector.xpath('//div[@class="stockcodec"]')[0]
        data = info.xpath('string(.)').replace('\n','').replace('\r','').replace('\t','')
        time_text = selector.xpath('//*[@id="zwconttb"]/div[@class="zwfbtime"]/text()')[0]
        time = re.findall('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',time_text)[0]
        item = response.save['item']
        item['text'] = data
        item['create'] = time
        item['created_at'] = int(re.findall('\d{9}',response.url)[0])
        return item
