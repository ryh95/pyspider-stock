import datetime as DT
from matplotlib import pyplot as plt
from matplotlib.dates import date2num
from pymongo import MongoClient
import  pymongo

client = MongoClient()
db = client['601001eastmoney']

documents = db.SentimentFactor2.find().sort([
	('create_date',pymongo.ASCENDING)
])

values = []
for document in documents:
    # date = document['create_date']
    # sentiment_factor = documents['sentiment_factor']
    # value = (DT.datetime.strptime(document['create_date'],"%Y-%m-%d"),documents['sentiment_factor'])
    values.append(document)
    # print date
# print values

data = []
for value in values:
    date = (DT.datetime.strptime(value['create_date'],"%Y-%m-%d"),value['sentiment_factor'])
    data.append(date)
# print data 
# data = [(DT.datetime.strptime('2010-02-05', "%Y-%m-%d"), 123),
#         (DT.datetime.strptime('2010-02-19', "%Y-%m-%d"), 678),
#         (DT.datetime.strptime('2010-03-05', "%Y-%m-%d"), 987),
#         (DT.datetime.strptime('2010-03-19', "%Y-%m-%d"), 345)]
 

x = [date2num(date) for (date, value) in data]
y = [value for (date, value) in data]

fig = plt.figure(figsize = (40,8))

graph = fig.add_subplot(111)

# Plot the data as a red line with round markers
graph.plot(x,y,'r-o')

# Set the xtick locations to correspond to just the dates you entered.
graph.set_xticks(x)

# Set the xtick labels to correspond to just the dates you entered.
graph.set_xticklabels(
        [date.strftime("%Y-%m-%d") for (date, value) in data]
        )

for  label in graph.xaxis.get_ticklabels():
    label.set_rotation(45)


plt.subplots_adjust(left=0.08,bottom=0.16)

plt.show()