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
            return redirect(url_for('index'))
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
        return redirect(url_for('index'))
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
@login_required
def my_profile():
    form = MyProfileForm()
    if not session.get("USERNAME") is None:
        if form.validate_on_submit():

            username = form.username.data
            phone = form.phone.data
            address = form.address.data
            city = form.city.data
            email = form.email.data
            zip = form.zip.data
            about = form.about.data
            facebook = form.facebook.data
            twitter = form.twitter.data
            google = form.google.data
            linkedin = form.linkedin.data
            flash('personal information saved')
            # now we add the object to the database
            user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
            user_profile = User.query.filter(User.username == user_in_db).first()
            # check if user already has a profile
            # stored_profile = Profile.query.filter(Profile.user == user_in_db).first()
            # if not stored_profile:
            #     # if no profile exists, add a new object
            #     profile = Profile(dob=form.dob.data, gender=form.gender.data, cv=cv_filename, user=user_in_db)
            #     db.session.add(profile)
            # else:
                # else, modify the existing object with form data

            user_profile.username = form.username.data
            user_profile.phone = form.phone.data
            user_profile.address = form.address.data
            user_profile.city = form.city.data
            user_profile.email = form.email.data
            user_profile.zip = form.zip.data
            user_profile.about = form.about.data
            user_profile.facebook = form.facebook.data
            user_profile.twitter = form.twitter.data
            user_profile.google = form.google.data
            user_profile.linkedin = form.linkedin.data

            # remember to commit
            db.session.commit()
            return redirect(url_for('my-profile'))
        else:
            user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
            stored_profile = Profile.query.filter(Profile.user == user_in_db).first()
            if not stored_profile:
                return render_template('my-profile.html', title='Add your profile', form=form)
            else:
                form.username.data = stored_profile.username
                form.phone.data = stored_profile.phone
                form.address.data = stored_profile.address
                form.city.data = stored_profile.city
                form.email.data = stored_profile.email
                form.zip.data = stored_profile.zip
                form.about.data = stored_profile.about
                form.facebook.data = stored_profile.facebook
                form.twitter.data = stored_profile.twitter
                form.google.data = stored_profile.google
                form.linkedin.data = stored_profile.linkedin

                return render_template('my-profile.html', title='Modify your profile', form=form)

    else:
        flash("User needs to either login or signup first")
    return render_template("my-profile.html", form=form)



# @app.route('/index', methods=['GET', 'POST'])
# def index_login():
#     form1 = LoginForm()
#     if form1.validate_on_submit():
#         user_in_db = User.query.filter(User.username == form1.username.data).first()
#         if not user_in_db:
#             flash('No user found with username: {}'.format(form1.username.data))
#             return redirect(url_for('index'))
#         if (check_password_hash(user_in_db.password_hash, form1.password.data)):
#             flash('Login success!')
#             session["USERNAME"] = user_in_db.username
#             return redirect(url_for('???'))
#         flash('Incorrect Password')
#         return redirect(url_for('index'))
#     return render_template('index.html', title='Sign In', form1=form1)


# @app.route('/index', methods=['GET', 'POST'])
# def index_register():
#     form2 = RegisterForm()
#     if form2.validate_on_submit():
#         if form2.password.data != form2.password2.data:
#             flash('Passwords do not match!')
#             return redirect(url_for('index'))
#         passw_hash = generate_password_hash(form2.password.data)
#         user = User(username=form2.username.data, email=form2.email.data, password_hash=passw_hash)
#         db.session.add(user)
#         db.session.commit()
#         flash('User registered with username:{}'.format(form2.username.data))
#         session["USERNAME"] = user.username
#         print(session)
#         return redirect(url_for('???'))
#     return render_template('index.html', title='Register a new user', form2=form2)


@app.route('/submit-new-property', methods=['GET', 'POST'])
def submit_new_property():
    return render_template('submit-new-property.html')


@app.route('/change-password', methods=['GET', 'POST'])
# @login_required  # Only login_user can change password
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            # 这里引入user的上下文，这个概念不太懂，暂且当成全局变量来用
            current_user.password = form.new_password1.data
            # 修改密码
            db.session.add(current_user)
            # 加入数据库的session，这里不需要.commit()，在配置文件中已经配置了自动保存
            flash('Your password has been updated.')
            return redirect(url_for('change-password'))
        else:
            flash('Invalid password.')
    return render_template("change-password.html", form=form)


@app.route('/logout')
def logout():
    session.pop("USERNAME", None)
    return redirect(url_for('index'))
