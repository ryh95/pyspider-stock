from pymongo import MongoClient

client = MongoClient()
db = client['stockcodes']
documents = db.HS300.find()
stockcodes = []
for document in documents:
    stockcodes.append(document['stockcode'])

for stockcode in stockcodes:
    client = MongoClient()
    client.drop_database(stockcode+'eastmoney')

