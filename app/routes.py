from . import app, db, login
from flask import render_template, request, redirect, url_for, flash
from .models import User
from flask_login import login_user, logout_user

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me')

        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            flash('Either your email address or password is incorrect. Try again.', 'warning')
            return redirect(url_for('login'))
        login_user(user, remember=remember_me)
        flash('User logged in successfully.', 'info')
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        user = User.query.filter_by(email=email).first()
        if user is not None:
            flash('Email already exists. Use another one.', 'danger')
            return redirect(url_for('register'))
        if confirm_password != password:
            flash("Your passwords don't match. Try again.", 'warning')
            return redirect(url_for('register'))
        else:
            u = User(name=name, email=email, password=password)
            u.generate_password(u.password)

            db.session.add(u)
            db.session.commit()
            flash('User registered successfully.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))