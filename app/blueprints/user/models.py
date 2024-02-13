from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# from passlib.hash import argon2



# Creating the user model
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    user_role = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    last_updated = db.Column(db.DateTime, index=True, default=datetime.utcnow(), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True, cascade="all, delete")

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': user_role
        }

    # setting password hashing system
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

    # this will check the hashed password
    def verify_password(self, password):
        return check_password_hash(self._password, password)


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
