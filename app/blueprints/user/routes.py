from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify, current_app
from flask_login import login_user, logout_user, current_user, login_required
from .models import User, Task, Status
from .forms import UserForm, TaskForm, LoginForm

user_bp = Blueprint('user', __name__, static_folder='./static/', template_folder='./templates/', url_prefix='/user')

@user_bp.route('/home', methods=('GET', 'POST'))
def index():
    # if user is authenticated, the would be redirected to its dashboard else remain in the homepage
    if current_user.is_authenticated:
        user_role = current_user.user_role
        if user_role == 'admin':
            admin_user_id = current_user.id
            return redirect(url_for('admin.dashboard'))
        elif user_role == 'user':
            user_id = current_user.id
            return redirect(url_for('user.dashboard'))
    return render_template('user/index.html')

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
