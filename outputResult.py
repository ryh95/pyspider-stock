# coding:utf8
import datetime

import pymongo
import xlwt
from pymongo import MongoClient

def getResult():
    client = MongoClient()
    now_time = datetime.datetime.now()
    yes_time = now_time + datetime.timedelta(days=-1)
    grab_time = yes_time.strftime('%m-%d')
    db = client[grab_time]

    documents = db.DailyResult.find().sort([
        ("sentiment_factor", pymongo.DESCENDING)
    ])

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
        ws.write(i + 1, 0, document['stock_code'])
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
        ws.write(i + 1, 2, document['stock_code'])
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
        ws.write(i + 1, 4, document['stock_code'])
        i += 1
        if i == threshold:
            break
    # 保存
    wb.save('data/'+grab_time + 'result' + '.xls')


