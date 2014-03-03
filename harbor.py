import bottle
from pymongo import MongoClient

connection = MongoClient('localhost', 27017)
db = connection.test
testruns = db.testruns

def show_results():
    items = []
    rest = testruns.find()
    for res in rest:
       item = []
       item.append(res['testname'])
       item.append(res['description'])
       item.append(res['result'])
       d = res['date']
       dt = '%s %02d:%02d:%02d' % (d.date(), d.hour, d.minute, d.second)
       item.append(dt)
       item.append(res['message'])
       items.append(item)
    return items   
#    print item


@bottle.route('/')
def home_page():
    mythings = ['Workspace','MDTrader','AutoSpreader','Market Grid']
    return bottle.template('hello_world',username='Debesys',things=mythings)

@bottle.route('/test_results')
def test_results():
    results = show_results()
    return bottle.template('test_results',name='NexTraderWeb',testresults=results)

@bottle.post('/favorite_test')
def favorite_test():
    test = bottle.request.forms.get("result") 
    if (test == None or test == ""):
       test="No test Selected"

    bottle.response.set_cookie("test", test)
    bottle.redirect("/show_fruit")

@bottle.route('/show_fruit')
def show_fruit():
    fruit = bottle.request.get_cookie("fruit")

    return bottle.template('fruit_selection.tpl', {'fruit':fruit})

bottle.debug(True)
bottle.run(host='localhost',port=8080)
