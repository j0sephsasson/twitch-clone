from flask_login import UserMixin
from . import db

## user table ##
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

## stream table ##
class Stream(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    session_id = db.Column(db.Text, nullable=False) # session ID --> to join a stream

## profile images table ##
class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True) # users email
    img = db.Column(db.Text, nullable=False) # image data
    name = db.Column(db.Text, nullable=False) # image name
    mimetype = db.Column(db.Text, nullable=False) # file type (.jpg , .png , etc..)