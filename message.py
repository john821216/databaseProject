from flask import Flask, flash, redirect, render_template, request, session, abort,g
from flask_socketio import SocketIO, send
import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)
dict={}

DATABASEURI = "postgresql://yc3379:2384@35.196.90.148/proj1part2"
engine = create_engine(DATABASEURI)

@socketio.on('message')
def handleMessage(msg):
	print('Message: ' + msg)
	if msg.split(" ")[0] == "<bid>":
		roomNumber = str(msg.split(" ")[3])
		id = str(msg.split(" ")[2])
		role = str(msg.split(" ")[1])
		list=[]
		if roomNumber not in dict:
			if role != "seller":
				list.append(id)
			dict[roomNumber] = list
		else:
			list = dict[roomNumber]
			if id not in dict[roomNumber]:
				if role != "seller":
					list.append(id)
				dict[roomNumber] = list	

		#insert into table
		g.conn = engine.connect()
		if role == "seller":
			cursor = g.conn.execute("SELECT count(*) FROM participateas WHERE arid = "+ roomNumber +"And sid =" + id)
			if cursor.scalar() == 0:
				g.conn.execute("INSERT INTO participateas VALUES ("+roomNumber+"," + id+")")
				print "Seller add successfully"
			else:
				print "Seller already in auctionRoom", id
				cursor.close()
		elif role == "buyer":
			cursor = g.conn.execute("SELECT count(*) FROM participateab WHERE arid = "+ roomNumber +"And bid =" + id)
			if cursor.scalar() == 0:
				g.conn.execute("INSERT INTO participateab VALUES ("+roomNumber+"," + id+")")
				print "Buyer add successfully"
			else :
				print "Buyer already in auctionRoom", id
			cursor.close()

		msg ="<bid> " + roomNumber +" "
		for i in range(len(list)):
			msg = msg + list[i] +" "
		send(msg, broadcast=True)

	elif msg.split(" ")[0] == "<bidLeave>":
		roomNumber = str(msg.split(" ")[3])
		id = str(msg.split(" ")[2])
		role = str(msg.split(" ")[1])
		print msg
		if role != "seller":
			dict[roomNumber].remove(id)
			msg ="<bid> " + roomNumber +" "
			for i in range(len(dict[roomNumber])):
				msg = msg + dict[roomNumber][i] +" "

		#insert into table
		g.conn = engine.connect()
		if role == "seller":
			cursor = g.conn.execute("SELECT count(*) FROM participateas WHERE arid = "+ roomNumber +"And sid =" + id)
			if cursor.scalar() != 0:
				g.conn.execute("DELETE FROM participateas WHERE arid = "+ roomNumber +"And sid =" + id)
				print "Seller delete successfully"
			else :
				print "Seller already been deleted in auctionRoom", id
			cursor.close()
		elif role == "buyer":
			cursor = g.conn.execute("SELECT count(*) FROM participateab WHERE arid = "+ roomNumber +"And bid =" + id)
			if cursor.scalar() != 0:
				g.conn.execute("DELETE FROM participateab WHERE arid = "+ roomNumber +"And bid =" + id)
				print "Buyer delete successfully"
			else :
				print "Buyer already been deleted in auctionRoom", id
			cursor.close()
		send(msg, broadcast=True)


	elif msg.split(" ")[0] == "<bidMoney>":
		#insert into database
		send(msg, broadcast=True)
	elif msg.split(" ")[0] == "<mainPagePP>":
		send(msg, broadcast=True)
	elif msg.split(" ")[0] == "<mainPagePM>":
		send(msg, broadcast=True)
	else:
		send(msg, broadcast=True)

if __name__ == '__main__':
	#socketio.run(app)
	http_server = WSGIServer(('',5000), app, handler_class=WebSocketHandler)
	http_server.serve_forever()