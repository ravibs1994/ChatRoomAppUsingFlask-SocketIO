"""
  * Author :Ravindra
  * Date   :25-11-2020
  * Time   :15:34
  * Package:ChatRoomApp
  * Statement:Design and implement Chat room Apllication
"""

from flask import Flask, render_template, request,url_for, redirect
from flask_socketio import SocketIO, join_room

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

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
    username = request.args.get('username')
    room = request.args.get('room')
    if username and room:
        return render_template('chat.html',username=username, room=room)
    else:
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


if __name__ == '__main__':
    """Mian Method"""
    socketio.run(app,debug=True)