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

    documents = db.DailyResult.find().sort([
        ("sentiment_factor", pymongo.DESCENDING)
    ])
    # 找到前20名
    threshold = 20
    wb = xlwt.Workbook()
    ws = wb.add_sheet('InputSheet')
    ws.write(0, 0, 'positive')
    ws.write(0, 1, 'value')
    ws.write(0, 2, 'negative')
    ws.write(0, 3, 'value')
    ws.write(0, 4, 'hottest')

    # 写入前２列
    i = 0
    for document in documents:
        # print document
        ws.write(i + 1, 0, str(document['stock_code']))
        ws.write(i + 1, 1, document['sentiment_factor'])
        i += 1
        if i == threshold:
            break
    # 写入后２列
    documents = db.DailyResult.find().sort([
        ("sentiment_factor", pymongo.ASCENDING)
    ])

    i = 0
    for document in documents:
        # print document
        ws.write(i + 1, 2, str(document['stock_code']))
        ws.write(i + 1, 3, document['sentiment_factor'])
        i += 1
        if i == threshold:
            break

    # 写入最后１列
    documents = db.DailyResult.find().sort([
        ("daily_counts", pymongo.DESCENDING)
    ])
    i = 0
    for document in documents:
        # print document
        ws.write(i + 1, 4, str(document['stock_code']))
        i += 1
        if i == threshold:
            break
    # 保存
    wb.save('data/'+date + 'result' + '.xls')

def getDailyStockSentiment(stockcode, date):
    client = MongoClient()
    db = client[date]
    cursor = db.DailyResult.find({"stock_code":stockcode})
    sentiment = None
    for document in cursor:
        sentiment = document['sentiment_factor']
    return sentiment

def getDailyAttachment(date):
    df = pd.read_excel("data/"+date+"result.xls",
       converters={'positive':str,'negative':str,'hottest':str})
    positive_stockcodes = df['positive'].tolist()
    negative_stockcodes = df['negative'].tolist()
    hottest_stockcodes = df['hottest'].tolist()

    dict_pos = getResultDict(positive_stockcodes,date)
    dict_neg = getResultDict(negative_stockcodes,date)
    dict_hot = getResultDict(hottest_stockcodes,date)

    writer = pd.ExcelWriter(date + 'attachment.xls')

    table_pos = pd.DataFrame(dict_pos)
    table_neg = pd.DataFrame(dict_neg)
    table_hot = pd.DataFrame(dict_hot)

    table_pos.to_excel(writer, 'positive')
    table_neg.to_excel(writer, 'negative')
    table_hot.to_excel(writer, 'hottest')

    writer.save()

def getResultDict(codes,date):
    result_dict = {'stockcodes':codes}
    now_time = datetime.datetime.strptime(date, '%m-%d')
    for i in range(20):
        yes_time = now_time + datetime.timedelta(days=-i)
        yes_time = yes_time.strftime('%m-%d')
        col_sentiments = []
        for stockcode in codes:
            dailysentiment = getDailyStockSentiment(stockcode, yes_time)
            col_sentiments.append(dailysentiment)
        result_dict[yes_time] = col_sentiments
    return result_dict