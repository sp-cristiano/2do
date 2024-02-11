from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify, current_app

admin_bp = Blueprint('admin', __name__, static_folder='./static/', template_folder='./templates/', url_prefix='/admin')

@admin_bp.route('/')
def index():
    return render_template('admin/index.html')

@admin_bp.route('/admins')
def get_user():
    return jsonify({
        'name': 'Admin Voldamort',
        'age': 23,
        'city': 'Santo Domingo',
        'role': 'Admin'
    })