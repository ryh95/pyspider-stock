# coding:utf8
import datetime
from pymongo import MongoClient


def setDailyResult(stockcode,date):
    client = MongoClient()

    db = client[stockcode + 'eastmoney']
    # 获取昨天的日期
    # now_time = datetime.datetime.now()
    # yes_time = now_time + datetime.timedelta(days=-1)
    # grab_time = yes_time.strftime('%m-%d')

    coll = db[date + 'SentimentFactor']

    cusor = coll.find({"last_date":date})
    for document in cusor:
        sentimentFactor = document['sentiment_factor']

    coll = db[date+'GuYouHui']

    dailyCounts =  coll.count()

    db = client[date]
    try:
        db.DailyResult.insert_one(
            {
                "stock_code": stockcode,
                "sentiment_factor": sentimentFactor,
                "daily_counts": dailyCounts
            }
        )
    except UnboundLocalError,e:
        pass


