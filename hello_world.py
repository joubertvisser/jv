import bottle

@bottle.route('/')
def home_page():
    mythings = ['apple','orange','pear','grape']
    return bottle.template('hello_world',username='Joubert',things=mythings)

@bottle.route('/testpage')
def test_page():
    return "this is a test page"

@bottle.post('/favorite_fruit')
def favorite_fruit():
    fruit = bottle.request.forms.get("fruit") 
    if (fruit == None or fruit == ""):
       fruit="No fruit Selected"

    return bottle.template('fruit_selection.tpl', {'fruit':fruit})

bottle.debug(True)
bottle.run(host='localhost',port=8080)
