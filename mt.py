#Script to test MongoDB connectivity
from pymongo import MongoClient

client = MongoClient() 
print "connected to MongoDB"
db = client.test_database
tst = {"id": "1",
       "name": "OM.OrderAdd",
       "description": "Add a limit buy order "}
tests = db.tests
tests_id = tests.insert(tst)
for a in tests.find():
    print a
