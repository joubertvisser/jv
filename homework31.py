import pymongo
from pymongo import MongoClient
import datetime

connection = MongoClient('localhost',27017)

db = connection.school

students = db.students


recs = db.students.find()
for rec in recs:
    minval = 100 
    for i,item in enumerate(rec['scores']):
        if item['type'] == 'homework':
            if item['score'] < minval:
               minval = item['score']
               idx = i
    print rec['scores']
    print rec['scores'][i]
    rec['scores'].remove(i)
    db.students.update({'_id':rec['_id']},{$et{'scores':rec['scores']})

db.close()
