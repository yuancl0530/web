from . import db
import hashlib, os
from datetime import datetime


def password_hash(password):
    ha = hashlib.md5()
    ha.update(bytes(password+os.getenv('FLASK_SALT'), encoding='utf-8'))
    return ha.hexdigest()


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(10), nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
    sex = db.Column(db.Enum("male", "female"), nullable=False)
    school = db.Column(db.String(20), nullable=False)
    major = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(11), nullable=False)

    def verify_password(self, value):
        return self.password_hash == password_hash(value)

    @property
    def password(self):
        return '****'

    @password.setter
    def password(self, password):
        self.password_hash = password_hash(password)


class Blog(db.Model):
    __tablename__='blogs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.TEXT, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    public = db.Column(db.Boolean, nullable=False)





