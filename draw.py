# coding=utf-8

from matplotlib import pyplot as plt
from pymongo import *
import pymongo
import datetime as DT
from matplotlib.dates import date2num


def getPic(stockcode):
    client = MongoClient()
    db = client[stockcode+'eastmoney']

    # 首先获取数据库中的数据
    documents = db.priceAndsentimentFactor.find().sort([
        ('date', pymongo.ASCENDING)
    ])

    # x是日期，z是价格，y是当天的情感因子
    # 情感因子的计算方法：某一天内有很多帖子，一个帖子的正面倾向概率×那个帖子的阅读量，得到一个帖子的情感因子，将当天所有的帖子情感因子相加得到当天的情感因子
    data = []
    z = []
    for document in documents:
        info = (DT.datetime.strptime(document['date'], "%Y-%m-%d"), document['sentiment_factor'])
        z.append(document['price'])
        data.append(info)

    x = [date2num(date) for (date, value) in data]
    y = [value for (date, value) in data]

    # 下面的代码用于画图
    fig = plt.figure(figsize=(40, 8))

    graph = fig.add_subplot(111)

    # Plot the data as a red line with round markers
    graph.plot(x, y, 'r')
    graph.plot(x, z, 'b')
    # Set the xtick locations to correspond to just the dates you entered.
    graph.set_xticks(x)

    # graph.set_xticks([0,50,100,150,200,244])
    # graph.set_xticklabels(x,fontsize = 13)

    # Set the xtick labels to correspond to just the dates you entered.
    graph.set_xticklabels(
        [date.strftime("%Y-%m-%d") for (date, value) in data]
    )

    for label in graph.xaxis.get_ticklabels():
        label.set_rotation(45)

    plt.subplots_adjust(left=0.08, bottom=0.16)

    plt.show()

    fig.savefig(stockcode+'stockNLP.png')



