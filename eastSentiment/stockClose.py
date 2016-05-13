import tushare as ts
from pymongo import MongoClient
import pymongo
import tushare as ts


def getStockClose(stockCode):
    client = MongoClient()
    db = client[stockCode+'east']

    # Todo:fix the time
    dates = ts.get_hist_data(stockCode,start = '2014-03-13',end  = '2016-03-10').index.tolist()
    prices = ts.get_hist_data(stockCode,start = '2014-03-13',end  = '2016-03-10')['close'].tolist()

    for i in range(len(dates)):
        result =  db.price.insert_one({
        "close" : prices[i],
        "create_date" : dates[i]
     })
        print result.inserted_id