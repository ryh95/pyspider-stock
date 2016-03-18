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

i = 0
f=open('text.txt','w')
for document in documents:
    f.write(str(i+1))
    f.write('\n')
    f.write(document['text'])
    f.write('\n')
    i+=1
    if i==100:
        break
f.close()