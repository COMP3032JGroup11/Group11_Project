import secrets

import numpy as np
from flask_dropzone import random_filename
from sqlalchemy.sql.functions import current_user

from webapp import app
from flask import render_template, request, current_app
from flask import render_template, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from webapp import app, db
from webapp.forms import LoginForm, RegisterForm, ChangePasswordForm, MyProfileForm, AddHouseForm
from webapp.models import User, House
from django.contrib.auth.decorators import login_required
from webapp.config import Config
import os

from flask import Flask, request, jsonify, render_template
import pickle

model = pickle.load(open('model.pkl', 'rb'))

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


def upload_pic(form_picture):
    random_hex = secrets.token_hex(8)  # https://baijiahao.baidu.com/s?id=1616189755017671452&wfr=spider&for=pc
    _, fextension = os.path.splitext(form_picture.filename)
    # reference: https://www.cnblogs.com/liangmingshen/p/10215065.html
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

@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    user = {'username': 'User'}
    form = ChangePasswordForm()
    if not session.get("USERNAME") is None:
        if form.validate_on_submit():
            user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
            if not (check_password_hash(user_in_db.password_hash, form.password.data)):
                flash('Incorrect Password')
                return redirect(url_for('change_password'))
            if form.new_password1.data != form.new_password2.data:
                flash('Passwords do not match!')
                return redirect(url_for('change_password'))
            else:
                user_in_db.password_hash = generate_password_hash(form.new_password1.data)
                db.session.commit()
                return redirect(url_for('change_password'))
        return render_template('change-password.html', user=user, form=form)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('login'))

@app.route('/upload_house', methods=['GET', 'POST'])
def upload():
    form = AddHouseForm()
    if not session.get("USERNAME") is None:
        ph_dir = Config.PH_UPLOAD_DIR
        if form.validate_on_submit():
            file = form.imagename.data
            filename = random_filename(file.filename)
            file.save(os.path.join(ph_dir, filename))
            user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
            prediction = model.predict([[form.size.data, form.floorkind.data, form.roomnumber.data,
                            form.livingnumber.data, form.bathnumber.data, form.renttype.data,
                            form.districtid.data, form.communityid.data]])
            output = int(prediction[0])
            new_house = House(name=form.housename.data, size=form.size.data, floor_kind=form.floorkind.data,
                              floor_number=form.floornumber.data, room_number=form.roomnumber.data, living_number=form.livingnumber.data,
                              bath_number=form.bathnumber.data, rent_type=form.renttype.data, district_id=form.districtid.data,
                              community_id=form.communityid.data, price=form.price.data, predicted_price=output, image_name=filename,
                              user=user_in_db)
            db.session.add(new_house)
            db.session.commit()
            return redirect(url_for('my_profile'))
        else:
            return render_template('upload-house.html', title='Upload House', form=form)

@app.route('/house_list')
def house_list():
    if not session.get("USERNAME") is None:
        prev_posts = db.session.query(House).all()
        return render_template('house_list.html', title='record', prev_posts=prev_posts)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop("USERNAME", None)
    return redirect(url_for('index'))
