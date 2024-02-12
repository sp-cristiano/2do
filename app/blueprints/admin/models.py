
from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from app.blueprints.user.models import User

class Admin(User):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    pin = db.Column(db.String(255), nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }