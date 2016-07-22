import os

import datetime
from pymongo import MongoClient

def dump():
    client = MongoClient()
    db = client['stockcodes']
    documents = db.HS300.find()
    stockcodes = []
    for document in documents:
        stockcodes.append(document['stockcode'])

    now_time = datetime.datetime.now()
    yes_time = now_time + datetime.timedelta(days=-5)
    grab_time = yes_time.strftime('%m-%d')

    os.system('mkdir '+grab_time)

    for stockcode in stockcodes:
        os.system('mongodump --db '+stockcode+'eastmoney'+' --collection '+grab_time+'GuYouHui')
        os.system('mongodump --db '+stockcode+'eastmoney'+' --collection '+grab_time+'SentimentFactor')
        os.system('mongodump --db '+grab_time)

    os.system('mv dump '+grab_time)

def drop():
    client = MongoClient()
    db = client['stockcodes']
    documents = db.HS300.find()
    stockcodes = []
    for document in documents:
        stockcodes.append(document['stockcode'])

    now_time = datetime.datetime.now()
    yes_time = now_time + datetime.timedelta(days=-5)
    grab_time = yes_time.strftime('%m-%d')

    for stockcode in stockcodes:
        db = client[stockcode+'eastmoney']
        coll = db[grab_time+'GuYouHui']
        coll.drop()
        coll = db[grab_time+'SentimentFactor']
        coll.drop()
    client.drop_database(grab_time)