from sqlalchemy.orm import relationship
from flask_login import UserMixin
from . import db
import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    subscribe = db.Column(db.Boolean(), default=True)
    posts = db.relationship("Post", back_populates="user")
    admin = db.Column(db.Boolean(), default=False)

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    contents = db.Column(db.Text)
    date = db.Column(db.Date, default=datetime.date.today())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship("User", back_populates="posts")
