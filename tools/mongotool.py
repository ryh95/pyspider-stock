import os

import datetime
from pymongo import MongoClient

def dump(dump_time):
    client = MongoClient()
    db = client['stockcodes']
    documents = db.HS300.find()
    documents_it = db.IT.find()
    stockcodes = []
    for document in documents:
        stockcodes.append(document['stockcode'])
    # add IT stocks
    for document in documents_it:
        stockcodes.append(document['stockcode'])


    os.system('mkdir '+dump_time)

    for stockcode in stockcodes:
        os.system('mongodump --db '+stockcode+'eastmoney'+' --collection '+dump_time+'GuYouHui')
        os.system('mongodump --db '+stockcode+'eastmoney'+' --collection '+dump_time+'SentimentFactor')
    os.system('mongodump --db '+dump_time)
    os.system('mongodump --db '+dump_time+'IT')

    os.system('mv dump '+dump_time)

    print dump_time+'data has been dumped!'
    print dump_time +'IT'+ 'data has been dumped!'

def drop(drop_time):
    client = MongoClient()
    db = client['stockcodes']
    documents = db.HS300.find()
    documents_it = db.IT.find()
    stockcodes = []
    for document in documents:
        stockcodes.append(document['stockcode'])

    # add IT stocks
    for document in documents_it:
        stockcodes.append(document['stockcode'])


    for stockcode in stockcodes:
        db = client[stockcode+'eastmoney']
        coll = db[drop_time+'GuYouHui']
        coll.drop()
        coll = db[drop_time+'SentimentFactor']
        coll.drop()
    client.drop_database(drop_time)

    client.drop_database(drop_time+'IT')

    print drop_time+'data has been dropped!'
    print drop_time+'IT'+'data has been dropped!'
