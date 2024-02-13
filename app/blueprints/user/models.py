from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Defining an association table for many to many relationship between Users and Tasks
users_tasks =  db.Table('users_tasks',
                        db.Column('users_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                        db.Column('tasks_id', db.Integer, db.ForeignKey('tasks.id'), primary_key=True))

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
    date_created = db.Column(db.DateTime, index=True, default=datetime.utcnow(), nullable=False)
    last_updated = db.Column(db.DateTime, index=True, default=datetime.utcnow(), nullable=False)

    # defining the many to many relationship between users and tasks
    tasks = db.relationship('Task', secondary=users_tasks, backref='user', cascade='all, delete', lazy=True)

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
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    last_updated = db.Column(db.DateTime, index=True, default=datetime.utcnow(), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)

    # defining a many to one relationship between task and status
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False, default=1)

class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    # defining a one to many relationship between status and tasks
    tasks = db.relationship('Task', backref='status', lazy=True, cascade='all, delete')
