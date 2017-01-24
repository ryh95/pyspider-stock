from pymongo import MongoClient

client = MongoClient()
db = client['stockcodes']
documents = db.HS300.find()
# read and store hs300 stocks in 'hs300' map
hs300 = {}
for document in documents:
    hs300[document['stockcode']] = 1

it_file =  open('IT_code.txt','r')
out = file('IT_unique.txt','a+')

num = 0
for line in it_file:
    line = line.replace('\n','')
    line = line.decode('utf8')
    if line not in hs300:
        print line
        out.write(str(line)+'\n')
        num+=1
print num