from flask import Flask, flash, redirect, render_template, request, session, abort,g
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)
dict={}
@socketio.on('message')
def handleMessage(msg):
	print('Message: ' + msg)
	if msg.split(" ")[0] == "<bid>":
		roomNumber = str(msg.split(" ")[2])
		id = str(msg.split(" ")[1])
		list=[]
		if roomNumber not in dict:
			list.append(id)
			dict[roomNumber] = list
		else:
			list = dict[roomNumber]
			if id not in dict[roomNumber]:
				list.append(id)
				dict[roomNumber] = list

		msg ="<bid> " + roomNumber +" "
		for i in range(len(list)):
			msg = msg + list[i] +" "
		send(msg, broadcast=True)

	elif msg.split(" ")[0] == "<bidLeave>":
		roomNumber = str(msg.split(" ")[2])
		id = str(msg.split(" ")[1])
		dict[roomNumber].remove(id)
		msg ="<bid> " + roomNumber +" "
		for i in range(len(dict[roomNumber])):
			msg = msg + dict[roomNumber][i] +" "
		send(msg, broadcast=True)

	elif msg.split(" ")[0] == "<bidMoney>":
		#insert into database
		send(msg, broadcast=True)
	elif msg.split(" ")[0] == "<mainPagePP>":
		send(msg, broadcast=True)
	else:
		send(msg, broadcast=True)
		


if __name__ == '__main__':
	socketio.run(app)