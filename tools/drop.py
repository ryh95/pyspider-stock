from pymongo import MongoClient

client = MongoClient()
db = client['stockcodes']
documents = db.HS300.find()
documents_IT = db.IT.find()
stockcodes = []
for document in documents:
    stockcodes.append(document['stockcode'])
for document in documents_IT:
    stockcodes.append(document['stockcode'])

for stockcode in stockcodes:
    client = MongoClient()
    client.drop_database(stockcode+'eastmoney')

