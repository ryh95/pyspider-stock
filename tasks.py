import datetime
import os

from celery import Celery
from pymongo import MongoClient

import dailyResult
import outputResult
import sendMail
from eastSentiment import produceFactor,aggregateFactor
from tools import mongotool

celery = Celery('tasks')
celery.config_from_object('celeryconfig')

@celery.task
def main(*stockCodes):
    now_time = datetime.datetime.now()
    yes_time = now_time + datetime.timedelta(days=-1)
    grab_time = yes_time.strftime('%m-%d')
    for stockCode in stockCodes:
        produceFactor.getSentimentFactor(stockCode, grab_time)
        aggregateFactor.aggregate(stockCode, grab_time)
        dailyResult.setDailyResult(stockCode, grab_time)

    outputResult.getDailyResult(grab_time)

    sendMail.send(grab_time)

    client = MongoClient()
    db = client.taskdb
    db.east.drop()
    print 'east collection has been dropped!'

    mongotool.dump()
    mongotool.drop()

    os.system('mv data/'+grab_time+'result.xls'+' /var/www/html')