import datetime
from pymongo import  *
from snownlp import  SnowNLP
import pymongo

# connecting database 601001eastmoney
def getSentimentFactor(stockcode,date):
    client = MongoClient()

    # now_time = datetime.datetime.now()
    # yes_time = now_time + datetime.timedelta(days=-1)
    # grab_time = yes_time.strftime('%m-%d')

    db = client[stockcode+'eastmoney']

    # sort the collection GuYouHui and point to it
    coll = db[date+'GuYouHui']

    documents = coll.find().sort([
        ("created_at", pymongo.DESCENDING)
    ])

    for document in documents:
        # test
        # type of the create_date is unicode
        create_date = document['create'][:10]
        last = document['last'][:5]
        # print create_date
        # print document['text']
        if (document['text'] != ''):
            s = SnowNLP(document['text'])
            # print s.sentiments
            sentiment_factor = (s.sentiments) * int(document['read'])
        else:
            sentiment_factor = 0
        # print sentiment_factor
        coll2 = db[date+'SentimentFactor']

        result = coll2.insert_one(
            {
                "create_date": create_date,
                "sentiment_factor": sentiment_factor,
                "last_date": last
            })
        print result.inserted_id
