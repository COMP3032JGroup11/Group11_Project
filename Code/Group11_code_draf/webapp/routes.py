from sqlalchemy.sql.functions import current_user

from webapp import app
from flask import render_template, request
from flask import render_template, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from webapp import app, db
from webapp.forms import LoginForm, RegisterForm, ChangePasswordForm, MyProfileForm
from webapp.models import User
from django.contrib.auth.decorators import login_required
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
        if check_password_hash(user_in_db.password_hash, form.password.data):
            flash('Login success!')
            session["USERNAME"] = user_in_db.username
            return redirect(url_for('my_profile'))
        flash('Incorrect Password')

        return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password2.data:
            flash('Passwords do not match!')
            return redirect(url_for('register'))
        passw_hash = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password_hash=passw_hash)
        db.session.add(user)
        db.session.commit()
        flash('User registered with username:{}'.format(form.username.data))
        session["USERNAME"] = user.username
        print(session)
        return redirect(url_for('my_profile'))
    return render_template('register.html', title='Register a new user', form=form)


# @app.route('/my-profile', methods=['GET', 'POST'])
# # @login_required
# def my_profile():
#     form = MyProfileForm()
#     return render_template('my-profile.html', form=form)

def upload_pic(form_picture):
    random_hex = secrets.token_hex(8)   #https://baijiahao.baidu.com/s?id=1616189755017671452&wfr=spider&for=pc
    _, fextension = os.path.splitext(form_picture.filename)
    #reference: https://www.cnblogs.com/liangmingshen/p/10215065.html
    picture_name = random_hex + fextension
    picture_path = os.path.join(app.root_path, 'static/pic', picture_name)
    form_picture.save(picture_path)
    return picture_name


@app.route('/my-profile', methods=['GET', 'POST'])
# @login_required
def my_profile():
    user = {'username': 'User'}
    form = MyProfileForm()

    if not session.get("USERNAME") is None:
        if form.validate_on_submit():
            user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
            user_in_db.nickname = form.nickname.data
            user_in_db.phone = form.phone.data
            user_in_db.address = form.address.data
            user_in_db.city = form.city.data
            user_in_db.email = form.email.data
            user_in_db.zip = form.zip.data
            user_in_db.about = form.about.data
            user_in_db.facebook = form.facebook.data
            user_in_db.twitter = form.twitter.data
            user_in_db.google = form.google.data
            user_in_db.linkedin = form.linkedin.data
            db.session.commit()
            flash('personal information saved')
            return redirect(url_for('my_profile'))

        elif request.method == 'GET':
            user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
            form.nickname.data = user_in_db.nickname
            form.phone.data = user_in_db.phone
            form.address.data = user_in_db.address
            form.city.data = user_in_db.city
            form.email.data = user_in_db.email
            form.zip.data = user_in_db.zip
            form.about.data = user_in_db.about
            form.facebook.data = user_in_db.facebook
            form.twitter.data = user_in_db.twitter
            form.google.data = user_in_db.google
            form.linkedin.data = user_in_db.linkedin

    else:
        flash("User needs to either login or signup first")
    return render_template("my-profile.html", form=form)


@app.route('/submit-new-property', methods=['GET', 'POST'])
def submit_new_property():
    return render_template('submit-new-property.html')


@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()
    if request.method == 'GET':
        return render_template('change-password.html')
    else:
        o_password = form.password.data
        password1 = form.new_password1.data
        password2 = form.new_password2.data
        validate_func(o_password, password1, password2)
        g.user.password = generate_password_hash(password1)
        db.session.commit()

        return render_template("change-password.html", form=form)


@app.route('/logout')
def logout():
    session.pop("USERNAME", None)
    return redirect(url_for('index'))
