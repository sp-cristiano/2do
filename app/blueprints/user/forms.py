from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField, EmailField, DateField, IntegerField, DecimalField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, Optional, NumberRange
from wtforms_validators import Regexp, AlphaNumeric, Integer, AlphaSpace, Alpha
from wtforms_sqlalchemy.fields import QuerySelectField
from app.blueprints.user.models import User, Task