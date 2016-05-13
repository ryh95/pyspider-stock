from pymongo import  *
from snownlp import  SnowNLP
import pymongo

# connecting database 601001eastmoney
client = MongoClient()
db = client['601001eastmoney']

# sort the collection GuYouHui and point to it 
documents= db.GuYouHui.find().sort([
	("created_at",pymongo.DESCENDING)
])


for  document in documents:
    # test 
    # type of the create_date is unicode
    create_date =  document['create'][:10]
    # print create_date 
    # print document['text']
    if(document['text']!=''):
        s = SnowNLP(document['text'])
        # print s.sentiments
        sentiment_factor = (s.sentiments)*int(document['read'])
    else:
        sentiment_factor = 0
    # print sentiment_factor    
    result = db.SentimentFactor.insert_one(
    	{
    	"create_date" : create_date,
    	"sentiment_factor" : sentiment_factor
    })
    print result.inserted_id