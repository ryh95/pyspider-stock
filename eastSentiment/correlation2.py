from pymongo import  *
from snownlp import  SnowNLP
import pymongo
from matplotlib import pyplot as plt
import pandas as pd

# connecting database 601001eastmoney
client = MongoClient()
db = client['601001eastmoney']

# sort the collection GuYouHui and point to it 
documents= db.GuYouHui.find().sort([
	("created_at",pymongo.ASCENDING)
])

sentiment_snow = []
i=0
for  document in documents:
    if(document['text']!=''):
        s = SnowNLP(document['text'])
        sentiment_snow.append(s.sentiments)
        i+=1
        # print document['create']
    if i==100:
        break
# print sentiment_snow
f = open('sentiment_person.txt','r')
all_text = f.read().replace('\r\n',' ').split(' ')

sentiment_person = []
for  text in all_text:
    num =  float(text)
    sentiment_person.append(num)

x = []
for i in range(100):
    x.append(i)

fig = plt.figure()

graph = fig.add_subplot(111)

# Plot the data as a red line with round markers
graph.plot(x,sentiment_snow,'r')
graph.plot(x,sentiment_person,'b')

S_snow = pd.Series(sentiment_snow)
S_person = pd.Series(sentiment_person)


print S_person.corr(S_snow,method='pearson')

plt.show()