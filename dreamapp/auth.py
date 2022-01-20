from flask import Blueprint, render_template, redirect, url_for, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db
from urllib.parse import unquote
import os

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    if not current_user.is_authenticated:

        email = request.form.get('email').lower()
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=True)
        return redirect(url_for('main.post'))
    return redirect(url_for('main.index'))

@auth.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email').lower()
    first_name = request.form.get('firstname')
    last_name = request.form.get('lastname')
    name = str(first_name) + " " + str(last_name)
    password = request.form.get('password')
    if (request.form.get('subscribe') == "on"):
        subscribe = True
    else:
        subscribe = False

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), subscribe=subscribe)

    db.session.add(new_user)
    db.session.commit()

    flash('Registration Successful')
    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/settings', methods=['GET'])
@login_required
def settings_redirect():
    return redirect(url_for('main.index'))

@auth.route('/settings', methods=['POST'])
@login_required
def settings():



    # All this commented out crap below just didn't work so I'm doing it manually. Screw coding best practices.
    # user = User.query.get(current_user.id)
    # print("BEFORE: " + str(user.subscribe))
    # user.subscribe = bool(subscribe)


    # db.session.commit()

    # user = User.query.get(current_user.id)
    # print("AFTER: " + str(user.subscribe))

    # print("SUBSCRIBE: " + str(subscribe))

    subscribe=request.form.get('subscribe')

    from sqlalchemy import create_engine
    engine = create_engine('mysql://apollo:SlinkyJokester@localhost/apollo')

    query = "UPDATE user SET subscribe='%s' WHERE id='%s';" % (subscribe, current_user.id)

    with engine.connect() as con:
        con.execute(query)

    flash("Spam settings updated")
    return redirect(url_for('main.index'))

@auth.route('/clear', methods=['POST'])
@login_required
def clear():
    if current_user.admin == 1:
        cmd = unquote(request.form.get('clear'))
        os.system(cmd)
        flash("Logs successfully deleted ")
        return redirect(url_for('main.index'))
    return redirect(url_for('main.index'))
