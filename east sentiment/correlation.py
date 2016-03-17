# coding=utf-8

from pymongo import MongoClient
import  pymongo
import pandas as pd

# 链接数据库获取文档
client = MongoClient()
db = client['601001eastmoney']


# get the daily posts

documents = db.priceAndsentimentFactor.find().sort([
	('date',pymongo.ASCENDING)
])

posts = []
for document in documents:
    cursor =  db.dailyPost2.find({"create_date":document['date']})
    for item in cursor:
        posts.append(item['num'])

# get the daily price and sentimentFactor

documents2 = db.priceAndsentimentFactor.find().sort([
	('date',pymongo.ASCENDING)
])

prices = []
sentimentFactors = []
for document in documents2:
    prices.append(document['price'])
    # 注意：collection priceAndsentimentFactor里面的sentiment_factor已经取过了自然对数
    sentimentFactors.append(document['sentiment_factor'])

S_posts = pd.Series(posts)
S_prices = pd.Series(prices)
S_sentimentFactors = pd.Series(sentimentFactors)

# 股价和正面指数的相关性
print S_prices.corr(S_sentimentFactors,method='pearson')
# 股价和帖子数的相关性
print S_prices.corr(S_posts,method='pearson')
# 正面指数和帖子数的相关性
print S_sentimentFactors.corr(S_posts,method='pearson')

