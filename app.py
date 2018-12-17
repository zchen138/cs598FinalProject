from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretKey'

socketio = SocketIO(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:pass@localhost/classroomchat'

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column('iduser', db.Integer, primary_key=True)
    username = db.Column('username', db.Unicode)
    password = db.Column('password', db.Unicode)

@app.route('/')
def sessions():
    users = db.session.query(User.username).all()
    usernames = [val for val, in users]
    return render_template('session.html', usernames=usernames)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)
