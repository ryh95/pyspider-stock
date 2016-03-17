# coding=utf-8

from pymongo import  *
from snownlp import  SnowNLP
import pymongo
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# connecting database 601001eastmoney
client = MongoClient()
db = client['601001eastmoney']

# sort the collection GuYouHui and point to it
documents= db.GuYouHui.find().sort([
	("created_at",pymongo.ASCENDING)
])

f=open('text.txt','w')
for document in documents:
    f.write(document['text'])
f.close()