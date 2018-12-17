from . import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(10), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    sex = db.Column(db.Enum("male", "female"), nullable=False)
    school = db.Column(db.String(20), nullable=False)
    major = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(11), nullable=False)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def password(self):
        return '****'

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


class Blog(db.Model):
    __tablename__='blogs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.TEXT, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    public = db.Column(db.Boolean, nullable=False)


class Log(db.Model):
    __tablename__='logs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event = db.Column(db.Text, nullable=False)
    uid = db.Column(db.Integer, nullable=True)
    time = db.Column(db.DateTime, default=datetime.now)
