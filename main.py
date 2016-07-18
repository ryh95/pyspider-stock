import datetime
from pymongo import MongoClient

import dailyResult
import outputResult
import sendMail
import time
from eastSentiment import stockClose,produceFactor,aggregateFactor,combine
import draw
stockCodes = []
# stockCodes = ['000001','000002','000009','000046','000063','000069','000333','000402','000559','000568','000623','000630','000651','000686','000712','000725','000738','000776','000783','000792','000793',
              # '000800','000858','000895','000898','000937','000999','002007','002065','002142','002236','002292','002294','002385','002465','002736','300015','300017','300024','300058','300070']

# stockCodes = ['000001','000002','000009','000027','000039','000046','000060','000061','000063','000069']
client = MongoClient()
db = client['stockcodes']
documents = db.HS300.find()

for document in documents:
    stockCodes.append(document['stockcode'])



while True:
    now_time = datetime.datetime.now()
    yes_time = now_time + datetime.timedelta(days=-1)
    grab_time = yes_time.strftime('%m-%d')
    for stockCode in stockCodes:

        produceFactor.getSentimentFactor(stockCode,grab_time)
        aggregateFactor.getSentimentFactor2(stockCode,grab_time)
        dailyResult.setDailyResult(stockCode,grab_time)

    outputResult.getDailyResult(grab_time)

    sendMail.send(grab_time)
    
    client = MongoClient()
    db = client.taskdb
    db.east.drop()
    print 'east collection has been dropped!'

    time.sleep(24*60*60)
