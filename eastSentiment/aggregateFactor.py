# coding:utf8
import datetime
from pymongo import MongoClient

def getSentimentFactor2(stockcode):
    client = MongoClient()
    # 获取昨天的日期
    now_time = datetime.datetime.now()
    yes_time = now_time + datetime.timedelta(days=-1)
    grab_time = yes_time.strftime('%m-%d')

    db = client[stockcode+'eastmoney']
    coll = db[grab_time+'SentimentFactor']

    documents = coll.aggregate(
        [
            {"$group": {"_id": "$last_date", "sentiment_factor": {"$sum": "$sentiment_factor"}}}
        ]
    )

    coll2 = db[grab_time+'SentimentFactor2']
    for result in documents['result']:
        coll2.insert_one({
            "sentiment_factor": result['sentiment_factor'],
            "last_date": result['_id']
        })

