import re
from pymongo import *
# import pymongo

# this script is used to insert the HS300 stockcodes into MongoDB
client = MongoClient()
db = client['stockcodes']

f= open('HS300.txt','r')
all_text = f.read()
stockcodes = re.findall('\d{6}',all_text)
for stockcode in stockcodes:
    result = db.HS300.insert_one({
        "stockcode" : stockcode
    })
    print result.inserted_id
f.close()