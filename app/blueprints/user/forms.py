from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField, EmailField, DateField, IntegerField, DecimalField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, Optional, NumberRange
from wtforms_validators import Regexp, AlphaNumeric, Integer, AlphaSpace, Alpha
from wtforms_sqlalchemy.fields import QuerySelectField
from app.blueprints.user.models import User, Task
from werkzeug.security import generate_password_hash, check_password_hash


# user form
class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message='Name is required.'),AlphaSpace(message='Name can only contain alphabets and spaces.'), Length(min=2, max=200, message='The minimum and maximum lenght is %(min)d and %(max)d')])

    username = StringField('Username', validators=[DataRequired(message='Username is required.'), AlphaNumeric(message='Username can only contain alphabets and numbers.'), Length(min=2, max=200, message='The minimum and maximum lenght is %(min)d and %(max)d')])

    email = EmailField('Email', validators=[DataRequired(message='Email is required.'), Email(), Length(min=2, max=200, message='The minimum and maximum lenght is %(min)d and %(max)d')])

    password = PasswordField('Password', validators=[DataRequired(message='Password is required.'), Length(min=2, max=200, message='The minimum and maximum lenght is %(min)d and %(max)d'), EqualTo('confirm_password', message='Passwords must match.')])

    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(message='Confirm Password is required.'), Length(min=2, max=200, message='The minimum and maximum lenght is %(min)d and %(max)d'), EqualTo('password', message='Passwords must match.')])

    phone = StringField('Phone', validators=[DataRequired(message='Phone number is required.'), Regexp(r'^\d{2,20}$', message='Phone number must be between 2 and 20 digits long.'), Length(min=2, max=20, message='The minimum and maximum lenght is %(min)d and %(max)d')])

    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], validators=[DataRequired(message='Gender is required.')])

    submit = SubmitField('Register')

    # Custom Validations

    # validating username
    def validate_username(self, username):
        user_name_input = username.data
        user_name_input = user_name_input.lower()

        # Querrying user database table
        user = User.query.filter_by(username=user_name_input).first()

        if user:
            raise ValidationError(f'This username "{user_name_input}" is already taken. Please choose a different username.')

    # validating email
    def validate_email(self, email, username):
        user_name_input = username.data
        user_name_input = user_name_input.lower()
        user_email_input = email.data

        # Querrying user database table
        user = User.query.filter_by(username=user_name_input).first()

        if user:
            db_email = user.email
            is_used = check_password_hash(db_email, user_email_input)
            if is_used:
                raise ValidationError(f'This email "{user_email_input}" is already taken. Please choose a differnt email.')

    # validating phone
    def validate_phone(self, phone, username):
        user_name_input = username.data
        user_name_input = user_name_input.lower()
        user_phone_input = phone.data

        # Querrying user database table
        user = User.query.filter_by(username=user_name_input).first()

        if user:
            db_phone = user.phone
            is_used = check_password_hash(db_phone, user_phone_input)
            if is_used:
                raise ValidationError(f'This phone number "{user_phone_input}" is already taken. Please choose a differnt phone number.')


# user login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Username is required.'), AlphaNumeric(message='Username can only contain alphabets and numbers.'), Length(min=2, max=200, message='The minimum and maximum lenght is %(min)d and %(max)d')])

    password = PasswordField('Password', validators=[DataRequired(message='Password is required.'), Length(min=2, max=200, message='The minimum and maximum lenght is %(min)d and %(max)d'), EqualTo('confirm_password', message='Passwords must match.')])

    remember_me = BooleanField('Remember Me')

    submit = SubmitField('Login')

class TaskForm(FlaskForm):
    title =  StringField('Title', validators=[DataRequired(message='Task title is required.'), Length(min=2, max=200, message='The minimum and maximum lenght is %(min)d and %(max)d')])
    
    description = TextAreaField('Description', validators=[DataRequired(message='Task description is required.'), Length(min=2, max=500, message='The minimum and maximum lenght is %(min)d and %(max)d')])

    submit = SubmitField('Create TODO')
