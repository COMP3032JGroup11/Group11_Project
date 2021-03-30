from webapp import app
from flask import render_template
from flask import render_template, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from webapp import app, db
from webapp.forms import LoginForm, RegisterForm
from webapp.models import User
from webapp.config import Config
import os

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user_in_db = User.query.filter(User.username == form.username.data).first()
		if not user_in_db:
			flash('No user found with username: {}'.format(form.username.data))
			return redirect(url_for('login'))
		if (check_password_hash(user_in_db.password_hash, form.password.data)):
			flash('Login success!')
			session["USERNAME"] = user_in_db.username
			return redirect(url_for('choice'))
		flash('Incorrect Password')
		return redirect(url_for('login'))
	return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		if form.password.data != form.password2.data:
			flash('Passwords do not match!')
			return redirect(url_for('signup'))
		passw_hash = generate_password_hash(form.password.data)
		user = User(username=form.username.data, email=form.email.data, password_hash=passw_hash)
		db.session.add(user)
		db.session.commit()
		flash('User registered with username:{}'.format(form.username.data))
		session["USERNAME"] = user.username
		print(session)
		return redirect(url_for('profile'))
	return render_template('register.html', title='Register a new user', form=form)