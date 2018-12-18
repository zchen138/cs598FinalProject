from flask import Flask, render_template, session, url_for, redirect, request
from flask_socketio import SocketIO, join_room, leave_room
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

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

'''
@app.route('/')
def sessions():
    users = db.session.query(User.username).all()
    usernames = [val for val, in users]
    return render_template('session.html')
'''

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/')
def index():
    if 'username' in session:
        return render_template("homepage.html")
    else:
        return render_template("login.html")

@app.route('/registerUser', methods=['POST'])
def registerUser():
    _username = request.form['username']
    _password = request.form['password']
    _userid = db.session.query(User.username).count()

    if _username and _password:
        numUsersWithSameName = User.query.filter_by(username=_username).count()
        if numUsersWithSameName==0:
            print("we should be registering the user")
            session['username'] = _username
            session['userid'] = _userid
            new_user = User(_userid, _username, _password)
            db.session.add(new_user)
            db.session.commit()
            return render_template('login.html')
        else:
            error = ("That username is taken. Try again")
            return render_template('register.html', error=error)
    else:
        error = "Enter a valid username and password."
        return render_template('register.html', error=error)

@app.route('/loginUser', methods=['GET', 'POST'])
def loginUser():

    if request.method == 'POST':
        _username = request.form['username']
        _password = request.form['password']

        user = User.query.filter_by(username=_username, password=_password).count()
        if user==0:
            error = "No user exist with the username and password"
            return render_template('login.html', error=error)
        if user==1:
            return render_template('homepage.html')
        else:
            error = "Invalid username or password"
            return render_template('login.html', error="what")

@app.route('/joinRoom/<roomNum>', methods=['GET', 'POST'])
def joinroom(roomNum):
    roomNum = _username = request.form['roomNum']
    session['room'] = roomNum
    return render_template('session.html', room=roomNum)


@socketio.on('connect to room')
def handle_my_custom_event(roomNum, methods=['GET', 'POST']):
    join_room(session['room'])

@socketio.on('message')
def message_test(json, methods=['GET', 'POST']):
     socketio.emit('my response', json, room=session['room'])

if __name__ == '__main__':
    socketio.run(app, debug=True)
