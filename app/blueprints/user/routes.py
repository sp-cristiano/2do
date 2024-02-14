from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify, current_app
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import or_
from .models import User, Task, Status
from .forms import UserForm, TaskForm, LoginForm
from app.global_functions import generate_random_alphanumeric_token

user_bp = Blueprint('user', __name__, static_folder='./static/', template_folder='./templates/', url_prefix='/user')

token = generate_random_alphanumeric_token()

@user_bp.route('/', methods=('GET', 'POST'))
@user_bp.route('/home', methods=('GET', 'POST'))
def index():
    # if user is authenticated, the would be redirected to its dashboard else remain in the homepage
    if current_user.is_authenticated:
        user_role = current_user.user_role
        if user_role == 'admin':
            admin_user_id = current_user.id
            username = current_user.username
            return redirect(url_for('admin.dashboard',username=username,token=token))
        elif user_role == 'user':
            user_id = current_user.id
            username = current_user.username
            return redirect(url_for('user.dashboard',username=username,token=token))
    else:
        username_input = None
        password_input = None
        form = LoginForm()
        if form.validate_on_submit():
            username_input = form.username.data
            password_input = form.password.data
            remember_me_input = True if form.remember_me.data else False

            # converting the user's input to lowercase
            username_input = username_input.lower()

            # querying the database for the user using either username, email or phone number
            user = User.query.filter(or_(User.username==username_input, User.email==username_input, User.phone==username_input)).first()

            if user == None:
                flash(f'user {username_input} does not exist', 'danger')
                username_input = None
                password_input = None
                return redirect(url_for('user.index'))
            elif user:
                if not user.verify_password(password_input):
                    flash('Incorrect password', 'danger')
                    username_input = None
                    password_input = None
                    return redirect(url_for('user.index'))
            else:
                login_user(user, remember=remember_me_input)
                username = current_user.usename
                user_role = current_user.user_role
                email = current_user.email
                # TODO: send email notification to login users
                if user_role == 'user':
                    return redirect(url_for('user.dashboard', username=username, token=token))
                if user_role == 'admin':
                    return redirect(url_for('admin.dashboard', username=username, token=token))
                flash(f'Welcome {username_input}!', 'success')
    return render_template('user/index.html', form=form)

@user_bp.route('/register', methods=('GET', 'POST'))
def register():
    return render_template('user/register.html')

# login route
@user_bp.route('/login', methods=('GET', 'POST'))
def login():
    return render_template('user/index.html')


# User route
@user_bp.route('/dashboard', methods=('GET', 'POST'))
def dashboard():
    return render_template('user/dashboard.html')


@user_bp.route('logout', methods=('GET', 'POST'))
def logout():
    logout_user()
    return redirect(url_for('user.index'))

@user_bp.route('/users')
@login_required
def get_user():
    return jsonify({
        'name': 'Voldamort',
        'age': 23,
        'city': 'Santo Domingo',
        'role': 'user'
    })
