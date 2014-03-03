import pymongo
from pymongo import MongoClient
import datetime

connection = MongoClient('localhost',27017)

db = connection.test

testruns = db.testruns


recs = db.testruns.find()
#print 'recs ',recs
i = 0
for item in recs:
#    print item
    i = i + 1
    print i 
    print item['testname']
    print item['result']
    print item['description']
    a = item['date']
    print a.date()
