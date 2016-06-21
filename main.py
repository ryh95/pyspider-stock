from pymongo import MongoClient

from eastSentiment import stockClose,produceFactor,aggregateFactor,combine
import draw
stockCodes = ['000002','000009','000046','000063','000069','000333','000402','000559','000568','000623','000630','000651','000686','000712','000725','000738','000776','000783','000792','000793',
              '000800','000858','000895','000898','000937','000999','002007','002065','002142','002236','002292','002294','002385','002465','002736','300015','300017','300024','300058','300070']
# stockCodes = ['000800']
# client = MongoClient()
# db = client['stockcodes']
# documents = db.HS300.find()
#
# for document in documents:
#     stockCodes.append(document['stockcode'])

for stockCode in stockCodes:
    stockClose.getStockClose(stockCode)
    produceFactor.getSentimentFactor(stockCode)
    aggregateFactor.getSentimentFactor2(stockCode)
    combine.getPriceAndSentimentFactor(stockCode)
    draw.getPic(stockCode)

