#Program to store results from a test run
from pymongo import MongoClient
import os,inspect
from datetime import datetime

connection = MongoClient('localhost',27017)

db = connection.test

testruns = db.testruns
class tstRun:
    def __init__(self,testname, pathname, description, date, result=None):
        self.testname = os.path.basename(pathname) 
        self.description = ''
        self.date = datetime.today()
        self.result = None

def store_result(testname, description, date, result, message):
    res = {'testname':testname, 'description':description, 'date': date,
           'result':result, 'message':message}
    testruns.insert(res)
    return res

