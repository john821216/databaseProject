#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
#from flask import Flask, request, render_template, g, redirect, Response, session, abort
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort,g
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user 
from flask_socketio import SocketIO, send
from flask_basic_roles import BasicRoleAuth


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
socketio = SocketIO(app)
#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@104.196.18.7/w4111
#
# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@104.196.18.7/w4111"
#
DATABASEURI = "postgresql://yc3379:2384@35.196.90.148/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
#engine.execute("""CREATE TABLE IF NOT EXISTS test (
#  id serial,
#  name text
#);""")
#engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  if not session.get('logged_in'):
    return render_template('signIn.html')
  else:
    role = session.get('role')
    if role == 'buyer':
      return buyerMain()
    elif role == 'seller':
      return sellerMain()
    elif role == 'admin':
      return adminMain()
    else :
      return render_template('signIn.html')
  print request.args



@app.route('/buyer')
def buyerMain():
  if session.get('role') != "buyer":
    return index()
  else:
    cursor = g.conn.execute("SELECT * FROM auctionroom").fetchall()
    numberOfAuctionRoom = g.conn.execute("SELECT count(*) FROM auctionRoom")
    lenOfAuctionRoom = numberOfAuctionRoom.scalar()
    newcursor = g.conn.execute("SELECT * FROM item WHERE arid>=1 And arid<='" + str(lenOfAuctionRoom)+"'ORDER BY (iid)").fetchall()
    peoplecursor = g.conn.execute("SELECT arid, count(*) FROM participateab GROUP BY arid ORDER BY (arid)")
    auctionroomsPPList=[]
    for i in range(lenOfAuctionRoom):
    	auctionroomsPPList.append(0)
    for a in peoplecursor:
    	auctionroomsPPList[a['arid']-1] = int(a['count'])
    	print str(a['arid'])+" " + str(a['count'])
    print auctionroomsPPList
    return render_template("buyer.html", username = session['username'],  money = session['money'],items=newcursor, auctionrooms=cursor, auctionroomList=auctionroomsPPList)

@app.route('/seller')
def sellerMain():
  if session.get('role') != "seller":
    return index()
  else:
    cursor = g.conn.execute("SELECT * FROM auctionroom").fetchall()
    numberOfAuctionRoom = g.conn.execute("SELECT count(*) FROM auctionRoom")
    lenOfAuctionRoom = numberOfAuctionRoom.scalar()
    newcursor = g.conn.execute("SELECT * FROM item WHERE arid>=1 And arid<='" + str(lenOfAuctionRoom)+"'ORDER BY (iid)").fetchall()
    peoplecursor = g.conn.execute("SELECT arid, count(*) FROM participateab GROUP BY arid")
    auctionroomsPPList=[]
    for i in range(lenOfAuctionRoom):
    	auctionroomsPPList.append(0)
    for a in peoplecursor:
    	auctionroomsPPList[a['arid']-1] = int(a['count'])
    	print str(a['arid']-1)+" " + str(a['count'])
    print auctionroomsPPList
    return render_template("seller.html", username = session['username'], money = session['money'], items=newcursor, auctionrooms=cursor,auctionPeopleCount=peoplecursor,auctionroomList=auctionroomsPPList)

@app.route('/admin')
def adminMain():
  if session.get('role') != "admin":
    return index()
  else:
    aid = session.get('id')
    name = session.get('username')
    cursor = g.conn.execute("SELECT * FROM setting WHERE aid = "+ aid).fetchall();
    cursorr = g.conn.execute("SELECT * FROM auctionroom A, setting S, applysetting AST WHERE AST.sid = S.sid AND A.arid = AST.arid AND A.aid = " + aid).fetchall()
    return render_template("admin.html", username = name, mysetting = cursor, myrooms = cursorr) ;

@app.route('/biddingRoom/<int:id>')
def biddingRoom(id):
	cursor = g.conn.execute("SELECT * FROM auctionroom WHERE arid='"+str(id)+"'").fetchall()
	newcursor = g.conn.execute("SELECT * FROM item WHERE arid='"+str(id)+"'").fetchall()
	return render_template("biddingRoom.html", id = session['id'], role = session['role'],username = session['username'], money = session['money'],items=newcursor, auctionrooms=cursor)

@app.route('/bid',methods=['POST'] )
def bidMoney():
	price = request.form['item-price']
	room = request.form['room']
	cbid = request.form['cbid']
	cursor = g.conn.execute("UPDATE item SET current_bidding ='" +str(price) +"',cbid='"+str(cbid)+"' WHERE arid='"+str(room)+"'")
	print price 
	print room
	print cbid
	return ""
  #
  # example of a database query
  #

  #cursor = g.conn.execute("SELECT name FROM test")
  #names = []
  #for result in cursor:
  #  names.append(result['name'])  # can also be accessed using result[0]
  #cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  #context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  #return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/login', methods=['POST'])
def do_login():
  id = request.form['id']
  password = request.form['password']
  type = request.form['type']

  if type == "buyer":
    cursor = g.conn.execute("SELECT count(*) FROM Buyer Where bid='"+id+"' And password='"+password+"'")
    count =  cursor.scalar()
    if count != 0:
      cursor = g.conn.execute("SELECT * FROM Buyer Where bid='"+id+"' And password='"+password+"'")
      session['logged_in'] = True
      session['role'] = "buyer"
      session['id'] = id

      nameCursor = g.conn.execute("SELECT name FROM Buyer Where bid='"+id+"' And password='"+password+"'")    
      for name in nameCursor:
        session['username'] = name['name']
      for result in cursor:
        session['money'] = result['money']
      cursor.close()
    else:
      flash('wrong password!')

  elif type == "seller":
    cursor = g.conn.execute("SELECT count(*) FROM Seller Where sid='"+id+"' And password='"+password+"'")
    count =  cursor.scalar()
    if count != 0:
      cursor = g.conn.execute("SELECT * FROM Seller Where sid='"+id+"' And password='"+password+"'")
      session['logged_in'] = True
      session['role'] = "seller"
      session['id'] = id
      nameCursor = g.conn.execute("SELECT name FROM Seller Where sid='"+id+"' And password='"+password+"'")
      for name in nameCursor:
        session['username'] = name['name']
      for result in cursor:
        session['money'] = result['money']
      cursor.close()

    else:
      	flash('wrong password!')
  return index()


@app.route('/add', methods=['POST'])
def addItem():
	itemName = request.form['item-name']
	itemCategory = request.form['item-category']
	itemPrice = request.form['item-price']
	durationFrom = request.form['item-du-from']
	durationTo = request.form['item-du-to']
	print itemName + " " + itemCategory +" " + itemPrice +" " + durationFrom +" " + durationTo
	##insert into item table and auctionroom table
	return index()

@app.route('/adminlogin', methods=['POST'])
def ad_login():
  id = request.form['id']
  password = request.form['password']
  session['id'] = id

  cursor = g.conn.execute("SELECT count(*) FROM Admin WHERE aid= " + id + " AND password= \'" + password + "\'")
  count =  cursor.scalar()
  
  if count == 1:
    cursor = g.conn.execute("SELECT name FROM Admin WHERE aid= " + id + " AND password= \'" + password + "\'")
    session['logged_in'] = True
    session['role'] = "admin"
    session['username'] = cursor.fetchone()['name']
    cursor.close()
  else:
    flash('wrong password!')
  return index()


@app.route('/register',methods=['POST'])
def register():
  id = request.form['id']
  username = request.form['username']
  password = request.form['password']
  type = request.form['type']
  if type == "buyer":
    cursor = g.conn.execute("INSERT INTO Buyer(bid, name, password, money) VALUES ('"+id+ "','" + username +"','" + password+"',10000)")
  elif type == "seller":
    cursor = g.conn.execute("INSERT INTO Seller(sid, name, password, money) VALUES ('"+id+ "','" + username +"','" + password+"',10000)")
  cursor.close()

  return index()

@app.route('/signup')
def signup():
  return render_template("signup.html")

@app.route('/adminSignIn')
def signin():
  return render_template("adminSignIn.html")

#@app.route('/another')
#def another():
#  return render_template("another.html")

@app.route('/enterRoom')
def enterRoom():
  #insert people into chatroom
  role = session.get('role')
  id = session.get('id')

  if role == "buyer":
    cursor = g.conn.execute("SELECT count(*) FROM participatecb WHERE bid = "+ id)
    if cursor.scalar() == 0 :
      print "Buyer add to chat room", id
      g.conn.execute("INSERT INTO participatecb VALUES (1, " + id + ")")
    else :
      print "Buyer already in chat room", id
    cursor.close()

  elif role == "seller":
    cursor = g.conn.execute("SELECT count(*) FROM participatecs WHERE sid = " + id)
    if cursor.scalar() == 0 :
      print "Buyer add to chat room", id
      g.conn.execute("INSERT INTO participatecs VALUES (1, "+ id + ")")
    else :
      print "Seller already in chat room", id
    cursor.close()

  return ""

@app.route('/leaveRoom')
def leaveRoom():
  #leave people into chatroom
  role = session.get('role')
  id = session.get('id')
  if role == "buyer":
    cursor = g.conn.execute("SELECT count(*) FROM participatecb WHERE bid = " + id)
    if cursor.scalar() != 0 :
      g.conn.execute("DELETE FROM participatecb WHERE bid = " + id)
      print "Buyer leave chat room", id
    else :
      print "Buyer not in chat room", id
    cursor.close()

  elif role == "seller":
    cursor = g.conn.execute("SELECT count(*) FROM participatecs WHERE sid = " + id)
    if cursor.scalar() != 0 :
      g.conn.execute("DELETE FROM participatecs WHERE sid = " + id)
      print "Seller leave chat room", id
    else :
      print "Seller not in chat room", id
    cursor.close()

  return ""

# Example of adding new data to the database
#@app.route('/add', methods=['POST'])
#def add():
#  name = request.form['name']
#  g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
#  return redirect('/')


#@app.route('/login')
#def login():
#    abort(401)
#    this_is_never_executed()


if __name__ == "__main__":
  import click
  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)
  run()




