# coding:utf8
import datetime

import pymongo
import pandas as pd
import xlwt
from pymongo import MongoClient

def getDailyResult(date):
    client = MongoClient()
    # now_time = datetime.datetime.now()
    # yes_time = now_time + datetime.timedelta(days=-1)
    # grab_time = yes_time.strftime('%m-%d')
    db = client[date]


    # 找到前20名
    threshold = 20
    wb = xlwt.Workbook()
    ws = wb.add_sheet('InputSheet')
    ws.write(0, 0, 'positive')
    ws.write(0, 1, 'value')
    ws.write(0, 2, 'negative')
    ws.write(0, 3, 'value')
    ws.write(0, 4, 'hottest')
    ws.write(0, 5, 'numPosts')
    ws.write(0, 6, 'positive_hottest')
    ws.write(0, 7, 'value')

    documents = db.DailyResult.find().sort([
        ("sentiment_factor", pymongo.DESCENDING)
    ]).limit(threshold)

    # 写入前２列
    i = 0
    for document in documents:
        # print document
        ws.write(i + 1, 0, str(document['stock_code']))
        ws.write(i + 1, 1, document['sentiment_factor'])
        i += 1

    # 写入后２列
    documents = db.DailyResult.find().sort([
        ("sentiment_factor", pymongo.ASCENDING)
    ]).limit(threshold)

    i = 0
    for document in documents:
        ws.write(i + 1, 2, str(document['stock_code']))
        ws.write(i + 1, 3, document['sentiment_factor'])
        i += 1

    # 写入最热门的股票
    # 写入最热门股票每天的帖子数
    documents = db.DailyResult.find().sort([
        ("daily_counts", pymongo.DESCENDING)
    ]).limit(threshold)

    i = 0
    for document in documents:
        ws.write(i + 1, 4, str(document['stock_code']))
        ws.write(i + 1, 5, str(document['daily_counts']))
        i += 1


    # 对最热门的股票按照情感值递减排序
    documents = db.DailyResult.aggregate([
        {"$sort" : {"daily_counts":pymongo.DESCENDING}},
        {"$limit" : threshold},
        {"$sort" : {"sentiment_factor":pymongo.DESCENDING}}
    ])

    i = 0
    for document in documents['result']:
        # print document
        ws.write(i + 1, 6, str(document['stock_code']))
        ws.write(i + 1, 7, str(document['sentiment_factor']))
        i += 1

    # 保存
    wb.save('data/'+date + 'result' + '.xls')

    print date+'result.xlsx'+'has been produced!'

def getDailyStockInfo(stockcode, date,type='sentiment'):
    client = MongoClient()
    db = client[date]
    cursor = db.DailyResult.find({"stock_code":stockcode})
    sentiment = None
    posts = None
    for document in cursor:
        if type == 'sentiment':
            sentiment = document['sentiment_factor']
        else:
            posts = document['daily_counts']
    if type == 'sentiment':
        return sentiment
    else:
        return posts


def getDailyAttachment(date):
    df = pd.read_excel("data/"+date+"result.xls",
       converters={'positive':str,'negative':str,'hottest':str})
    positive_stockcodes = df['positive'].tolist()
    negative_stockcodes = df['negative'].tolist()
    hottest_stockcodes = df['hottest'].tolist()

    dict_pos = getResultDict(positive_stockcodes,date)
    dict_neg = getResultDict(negative_stockcodes,date)
    dict_hot = getResultDict(hottest_stockcodes,date,type='hottest')

    writer = pd.ExcelWriter(date + 'attachment.xls')

    table_pos = pd.DataFrame(dict_pos)
    table_neg = pd.DataFrame(dict_neg)
    table_hot = pd.DataFrame(dict_hot)

    table_pos.to_excel(writer, 'positive')
    table_neg.to_excel(writer, 'negative')
    table_hot.to_excel(writer, 'hottest')

    writer.save()

def getResultDict(codes,date,type='sentiment'):
    result_dict = {'stockcodes':codes}
    now_time = datetime.datetime.strptime(date, '%m-%d')
    for i in range(20):
        yes_time = now_time + datetime.timedelta(days=-i)
        yes_time = yes_time.strftime('%m-%d')
        col_sentiments = []
        for stockcode in codes:
            dailysentiment = getDailyStockInfo(stockcode, yes_time,type=type)
            col_sentiments.append(dailysentiment)
        result_dict[yes_time] = col_sentiments
    return result_dict