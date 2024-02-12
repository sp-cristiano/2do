from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from passlib.hash import argon2



# Creating the user model
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    user_role = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    last_updated = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    tasks = db.relationship('Task', backref='user', lazy=True, cascade="all, delete")

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': user_role
        }
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
