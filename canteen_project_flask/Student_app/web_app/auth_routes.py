from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from core.auth_handler import login_user, register_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = login_user(username, password)
        if user:
            session['user_id'] = user.get('user_id') or user.get('id')
            session['user_name'] = user['username'].capitalize()
            return redirect(url_for('menu.menu_page'))
        flash("Invalid username or password")
    return render_template('user/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        success, message = register_user(username, email, password)
        if success:
            flash("Registration successful! Please log in.")
            return redirect(url_for('auth.login'))
        flash(f"Error: {message}")
    return render_template('user/register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))