from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from app.timeNow import getToday


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    def __repr__(self):
        return '<User {}>'.format(self.username)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    verified = db.Column(db.Boolean)
    room_in = db.Column(db.Integer, db.ForeignKey('room.id'))
    name = db.Column(db.String(50))
    lastLogin = db.Column(db.DateTime, default=getToday())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Room(db.Model):
    def __init__(self, location, capacity=None):
        building, floor_number = location.split(' ')
        floor, number = floor_number.split('/')
        self.building = building
        self.floor = int(floor)
        self.number = int(number)
        self.capacity = capacity

    def __repr__(self):
        return f'<Room {self.building} {self.floor}/{self.number}>'

    id = db.Column(db.Integer, primary_key=True)
    building = db.Column(db.String(10))
    floor = db.Column(db.Integer)
    number = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    occupants = db.relationship('User', backref='in_room', lazy='dynamic')
    comments = db.relationship('Comment', backref='room', lazy='dynamic')


class Comment(db.Model):
    def __repr__(self):
        return f'<Comment {self.text}>'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))


class Schedule(db.Model):
    def __repr__(self):
        return f'<Schedule {self.day} {self.start_time} - {self.end_time} in {self.room_id}>'

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    day = db.Column(db.String(2))
    start_time = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.Integer, nullable=False)
