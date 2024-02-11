from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify, current_app

user_bp = Blueprint('user', __name__, static_folder='./static/', template_folder='./templates/', url_prefix='/user')

@user_bp.route('/')
def index():
    return render_template('user/index.html')

@user_bp.route('/users')
def get_user():
    return jsonify({
        'name': 'Voldamort',
        'age': 23,
        'city': 'Santo Domingo',
        'role': 'user'
    })