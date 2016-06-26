# coding:utf8
import datetime
from pymongo import MongoClient


def setDailyResult(stockcode):
    client = MongoClient()

    db = client[stockcode + 'eastmoney']
    # 获取昨天的日期
    now_time = datetime.datetime.now()
    yes_time = now_time + datetime.timedelta(days=-1)
    grab_time = yes_time.strftime('%m-%d')

    coll = db[grab_time + 'SentimentFactor2']

    cusor = coll.find({"last_date":grab_time})
    for document in cusor:
        sentimentFactor = document['sentiment_factor']

    coll = db[grab_time+'GuYouHui']

    dailyCounts =  coll.count()

    db = client[grab_time]
    db.DailyResult.insert_one(
        {
            "stock_code":stockcode,
            "sentiment_factor":sentimentFactor,
            "daily_counts":dailyCounts
        }
    )

