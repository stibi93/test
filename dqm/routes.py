from dqm import app
from flask import render_template, redirect, url_for, flash, request
from dqm.models import User
from dqm.forms import RegisterForm, LoginForm
from dqm import db
from flask_login import login_user, logout_user, login_required, current_user
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/dqm')
@login_required
def dqm_page():
    return render_template('dqm.html')


@app.route('/register', methods=['POST', 'GET'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! You are now logged in as {user_to_create.username}', category='success')
        return redirect(url_for('dqm_page'))
    if form.errors != {}: #Error occured during the validation
        for err_msg in form.errors.values():
            flash(f'There was an error during creating the user: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success. You are logged in as {attempted_user.username}', category='success')
            return redirect(url_for('dqm_page'))
        else:
            flash('Username and password does not match! Please try again!', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('home_page'))
