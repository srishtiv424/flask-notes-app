from flask import Flask, Blueprint, redirect, render_template, request, flash, url_for
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password =request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password , password):
                flash("User successfully logged in ", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
                
            else:
                flash("Incorrect password", category= 'error')
        else:
            flash("User does not exist" , category='error')



    return render_template("login.html" , user = current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up' , methods= ['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash("User already exist" , category = 'error')
            return redirect(url_for('auth.login'))
        elif len(email) < 1:
            flash("Enter a valid email" , category= 'error')
        elif len(firstName) < 1:
            flash("Enter a valid name", category= 'error')
        elif  password1 != password2:
            flash("Passwords should match", category= 'error')
        elif  len(password1) < 1:
            flash("Enter a strong password", category= 'error')
        else:
            new_user = User(email=email , first_name=firstName , password=generate_password_hash(password1 , method='sha256') )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created successfully !!", category= 'success')
            return redirect(url_for('views.home'))


    return render_template("signup.html" , user = current_user)