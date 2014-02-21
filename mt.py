#Script to test MongoDB connectivity
from pymongo import MongoClient

connection = MongoClient() 
print "connected to MongoDB"
db = connection.test

tests = db.names
#tst = {"id": "1",
#       "name": "OM.OrderAdd",
#       "description": "Add a limit buy order "}
#tests_id = tests.insert(tst)
item = tests.find_one()
print item['name']
print item
