from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify, current_app
from flask_login import login_user, logout_user, current_user, login_required
from .models import Admin

admin_bp = Blueprint('admin', __name__, static_folder='./static/', template_folder='./templates/', url_prefix='/admin')

@admin_bp.route('/home', methods=('GET', 'POST'))
def index():
    if current_user.is_authenticated:
        user_role = current_user.user_role
        if user_role == 'admin':
            admin_user_id = current_user.id
            return redirect(url_for('admin.dashboard'))
        elif user_role == 'user':
            user_id = current_user.id
            return redirect(url_for('user.dashboard'))
    return render_template('admin/index.html')

@admin_bp.route('/admins')
def get_user():
    return jsonify({
        'name': 'Admin Voldamort',
        'age': 23,
        'city': 'Santo Domingo',
        'role': 'Admin'
    })