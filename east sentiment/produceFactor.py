from pymongo import  *
import pymongo

# connecting database 601001eastmoney
client = MongoClient()
db = client['601001eastmoney']

# sort the collection GuYouHui and point to it 
documents= db.GuYouHui.find().sort([
	("created_at",pymongo.DESCENDING)
])

# print cursor[0]
for  document in documents:
    # test 
    # type of the create_date is unicode
    create_date =  document['create'][:10]
    print create_date 
 