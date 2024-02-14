
from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.blueprints.user.models import User

class Admin(User):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    _pin = db.Column(db.String(255), nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

    def __init__(self, _pin, **kwargs):
        super(Admin, self).__init__(**kwargs)
        self._pin = _pin

    # setting pin shashing system
    @property
    def pin(self):
        raise AttributeError('Pin is not a readable attribute')

    @pin.setter
    def pin(self, pin):
        self._pin = generate_password_hash(pin, method='pbkdf2:sha256', salt_length=16)

    # This will check the hashed pin
    def verify_pin(self, pin):
        return check_password_hash(self._pin, pin)
