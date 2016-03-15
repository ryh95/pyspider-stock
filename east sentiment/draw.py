# coding=utf-8

import datetime as DT
from matplotlib import pyplot as plt
from matplotlib.dates import date2num
from pymongo import MongoClient
import  pymongo
import numpy as np
import tushare as ts
import pandas as pd

client = MongoClient()
db = client['601001eastmoney']

documents = db.price.find().sort([
	('create_date',pymongo.ASCENDING)
])

data = []
# dates用于存放既有股价又有舆论的那一天的日期
dates= []
# 这是将股票时间比对舆论时间，找到既有股价又有舆论的那一天，然后将日期|舆论因子的自然对数放入data，后面画出图像日期舆论图想
for document in documents:
    cursor =  db.SentimentFactor2.find({"create_date":document['create_date']})
    for item in cursor:
        info = (DT.datetime.strptime(item['create_date'],"%Y-%m-%d"),np.log(item['sentiment_factor']))
        data.append(info)
        dates.append(item['create_date']) 

# # print values
# data = []
# for value in values:
#     date = (DT.datetime.strptime(value['create_date'],"%Y-%m-%d"),np.log10(value['sentiment_factor']))
#     data.append(date)
# print data 
# data = [(DT.datetime.strptime('2010-02-05', "%Y-%m-%d"), 123),
#         (DT.datetime.strptime('2010-02-19', "%Y-%m-%d"), 678),
#         (DT.datetime.strptime('2010-03-05', "%Y-%m-%d"), 987),
#         (DT.datetime.strptime('2010-03-19', "%Y-%m-%d"), 345)]
 

x = [date2num(date) for (date, value) in data]
y = [value for (date, value) in data]

z = []
# 找到既有股价又有舆论的那一天的股价，存入z，后面画出日期|股价图像
for  date in dates:
    cursor = db.price.find({"create_date":date})
    for item in cursor:
        z.append(item['close']) 

fig = plt.figure(figsize = (40,8))

graph = fig.add_subplot(111)

# Plot the data as a red line with round markers
graph.plot(x,y,'r')
graph.plot(x,z,'b')
# Set the xtick locations to correspond to just the dates you entered.
graph.set_xticks(x)

# graph.set_xticks([0,50,100,150,200,244])
# graph.set_xticklabels(x,fontsize = 13)

# Set the xtick labels to correspond to just the dates you entered.
graph.set_xticklabels(
        [date.strftime("%Y-%m-%d") for (date, value) in data]
        )

for  label in graph.xaxis.get_ticklabels():
    label.set_rotation(45)


plt.subplots_adjust(left=0.08,bottom=0.16)

plt.show()