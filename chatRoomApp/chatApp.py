"""
  * Author :Ravindra
  * Date   :25-11-2020
  * Time   :15:34
  * Package:ChatRoomApp
  * Statement:Design and implement Chat room Application
"""
import os

from flask import Flask, render_template, request,url_for, redirect
from flask_mysqldb import MySQL
from flask_socketio import SocketIO, join_room, leave_room
from pymsgbox import *

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
#Database Connection

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.environ['user']
app.config['MYSQL_PASSWORD'] = os.environ['password']
app.config['MYSQL_DB'] = 'mydatabase'

mysql = MySQL(app)

@app.route('/')
def home():
    """Method Definition"
       home Page
       :return:render template
    """
    return render_template("index.html")

@app.route('/chat')
def chat():
    """Method Definition
       to enter in chat room
       :return:render template
    """
    global room
    username = request.args.get('username')
    room = int(request.args.get('room'))
    if username and room >0 and room <= 10:
        try:
            #Insert Query Operation
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO RoomInfo (roomId, username) VALUES (%s, %s)"
            val = (room, username)
            cursor.execute(sql, val)
            mysql.connection.commit()
            cursor.close()
        except Exception:
            alert(text='UserName AllReady Available', title='Exception', button='OK')
            return redirect(url_for('home'))
        return render_template('chat.html',username=username, room=room)

    else:
        alert(text='Room range Between 1 to 10', title='Wrong Input', button='OK')
        return redirect(url_for('home'))

@socketio.on('send_message')
def handle_send_message_event(data):
    """Method Definition
        sending message
        :parameter:
        :return:render template
    """
    app.logger.info("{} Has sent Messages to the room {}: {}".format(data['username'], data['room'], data['message']))
    socketio.emit('received_message', data, room=data['room'])
    msg = data['message']
    cursor = mysql.connection.cursor()
    sql = "INSERT INTO MessageInfo (roomId, message) VALUES (%s, %s)"
    val = (room, msg)
    cursor.execute(sql, val)
    mysql.connection.commit()
    cursor.close()

@socketio.on('join_room')
def handle_join_room_event(data):
    """Method Definition
        join room
        :parameter:
        :return:render template
     """
    app.logger.info("{} has join the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement',data)


@socketio.on('leave_room')
def handle_leave_room_event(data):
    """Method Definition
        leave room
        :parameter:
        :return:render template
     """
    app.logger.info("{} has leave the room {}".format(data['username'], data['room']))
    leave_room(data['room'])
    socketio.emit('leave_room_announcement',data)

if __name__ == '__main__':
    """Mian Method"""
    socketio.run(app,debug=True)
