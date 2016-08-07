from pymongo import MongoClient

BROKER_URL = 'redis://'
CELERY_RESULT_BACKEND = "redis://"
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']

from celery.schedules import crontab
stockCodes = []
client = MongoClient()
db = client['stockcodes']
documents = db.HS300.find()

for document in documents:
    stockCodes.append(document['stockcode'])


CELERYBEAT_SCHEDULE = {
    'every-24hours': {
        'task': 'tasks.main',
        'schedule': crontab(hour='*/24'),
        'args': (stockCodes),
    },
}