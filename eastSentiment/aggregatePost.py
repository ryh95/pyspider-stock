from pymongo import MongoClient

client = MongoClient()
db = client['601001eastmoney']

documents =  db.dailyPost.aggregate(
	[
		{"$group" : {"_id" : "$create_date", "num" : { "$sum" : "$post_count"}}}
	]
)

for result in documents['result']:
    item = db.dailyPost2.insert_one({
    	"num" : result['num'],
    	"create_date" : result['_id']
    })
    print item.inserted_id