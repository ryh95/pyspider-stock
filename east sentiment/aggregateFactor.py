from pymongo import MongoClient

client = MongoClient()
db = client['601001eastmoney']

documents =  db.SentimentFactor.aggregate(
	[
		{"$group" : {"_id" : "$create_date", "sentiment_factor" : { "$sum" : "$sentiment_factor"}}}
	]
)

for result in documents['result']:
     db.SentimentFactor2.insert_one({
    	"sentiment_factor" : result['sentiment_factor'],
    	"create_date" : result['_id']
    })
    