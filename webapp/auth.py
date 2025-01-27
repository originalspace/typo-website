from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.homepage'))
            else:
                flash('Incorrect password, try again!', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign_up',methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        userName = request.form.get('userName')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')

        if len(userName) < 4:
            flash('username must be greater than 4 characters.', category='error')
        elif len(email) < 2:
            flash('email must be greater than 2 characters.', category='error')
        elif len(password) < 4:
            flash('password must contain greater than 4 character.', category='error')
        else: 
            new_user = User(userName=userName, email=email, password=generate_password_hash(password, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)

            flash('Account Created', category='success')
            return redirect(url_for('views.homepage'))



    return render_template("signup.html", user=current_user)