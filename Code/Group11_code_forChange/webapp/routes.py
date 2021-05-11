import secrets

import numpy as np
from flask_dropzone import random_filename
from sqlalchemy.sql.functions import current_user

from webapp import app, db, whooshee, mail, bcrypt
from flask import render_template, request, current_app, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from webapp.forms import LoginForm, RegisterForm, ChangePasswordForm, MyProfileForm, AddHouseForm, CalculatorForm, \
    ChangeHouseForm, SearchForm, RequestResetForm, ResetPasswordForm, MessageForm
from webapp.models import User, House, District, Community, Floor, CusMessage, Save
from django.contrib.auth.decorators import login_required
from webapp.config import Config
from flask_mail import Message

from PIL import Image

import os
import re

import math

from flask import Flask, request, jsonify, render_template
import pickle

model = pickle.load(open('model.pkl', 'rb'))


#  ‘success’、‘info’、‘warning’、‘danger’ for flash format


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    username = session.get("USERNAME")
    if not db.session.query(Floor).first():
        floor_list = ['basement', 'low floor', 'mid floor', 'high floor']
        for index in range(len(floor_list) + 1):
            if index == 0:
                continue
            else:
                n_floor = Floor(id=index, floor=floor_list[index - 1])
                db.session.add(n_floor)
                db.session.commit()

    if not db.session.query(District).first():
        district_list = ['昌平', '朝阳', '大兴', '东城', '房山', '丰台', '海淀', '怀柔', '门头沟',
                         '密云', '平谷', '石景山', '顺义', '通州', '西城', '延庆', '亦庄开发区'
                         ]
        for index in range(len(district_list) + 1):
            if index == 0:
                continue
            else:
                n_district = District(id=index, district=district_list[index - 1])
                db.session.add(n_district)
                db.session.commit()

    if not db.session.query(Community).first():
        community_list = ['西关环岛', '北七家', '霍营', '鼓楼大街', '回龙观', '西三旗', '东关', '天通苑',
                          '沙河', '南邵', '昌平其它', '小汤山', '立水桥', '奥林匹克公园', '南口', '安宁庄',
                          '定福庄', '亚运村小营', '豆各庄', '双桥', '常营', '首都机场', '管庄', '十里河',
                          '芍药居', '垡头', '和平里', '亚运村', '红庙', '石佛营', '朝阳其它', '国展',
                          '东坝', '工体', '潘家园', '三元桥', '北苑', '华威桥', '十里堡', 'CBD', '惠新西街',
                          '十八里店', '酒仙桥', '劲松', '百子湾', '方庄', '朝青', '望京', '欢乐谷', '中央别墅区',
                          '甘露园', '四惠', '北工大', '成寿寺', '高碑店', '大望路', '太阳宫', '双井', '团结湖',
                          '南沙滩', '东大桥', '甜水园', '西坝河', '健翔桥', '三里屯', '安贞', '亮马桥', '未知',
                          '大山子', '建国门外', '朝阳门外', '东直门', '农展馆', '朝阳公园', '马甸', '燕莎',
                          '安定门', '南中轴机场商务区', '高米店', '黄村火车站', '枣园', '黄村中', '西红门',
                          '大兴其它', '瀛海', '天宫院', '义和庄', '大兴新机场', '科技园区', '旧宫', '观音寺',
                          '亦庄', '亦庄开发区其它', '和义', '大兴新机场洋房别墅区', '天宫院南', '永定门', '崇文门',
                          '东花市', '广渠门', '陶然亭', '左安门', '东四', '建国门内', '天坛', '前门', '地安门', '灯市口',
                          '金宝街', '交道口', '朝阳门内', '蒲黄榆', '东单', '长阳', '良乡', '阎村', '城关', '燕山',
                          '房山其它', '窦店', '青塔', '新宫', '木樨园', '花乡', '马家堡', '西罗园', '卢沟桥', '北大地',
                          '大红门', '看丹桥', '洋桥', '玉泉营', '刘家窑', '五里店', '赵公口', '宋家庄', '右安门外', '角门',
                          '六里桥', '七里庄', '丰台其它', '丽泽', '草桥', '北京南站', '太平桥', '菜户营', '马连道', '岳各庄',
                          '五棵松', '广安门', '马连洼', '西山', '定慧寺', '海淀北部新区', '军博', '上地', '清河', '厂洼',
                          '紫竹桥', '甘家口', '公主坟', '玉泉路', '田村', '小西天', '万寿路', '西直门', '二里庄', '皂君庙',
                          '双榆树', '四季青', '新街口', '苏州桥', '颐和园', '知春路', '五道口', '圆明园', '牡丹园', '西北旺',
                          '学院路', '万柳', '中关村', '西二旗', '杨庄', '魏公村', '世纪城', '白石桥', '北太平庄', '海淀其它',
                          '怀柔', '大峪', '石门营', '城子', '滨河西区', '冯村', '门头沟其它', '密云其它', '平谷其它', '鲁谷',
                          '八角', '苹果园', '石景山其它', '古城', '老山', '马坡', '顺义其它', '顺义城', '后沙峪', '天竺',
                          '李桥', '乔庄', '北关', '万达', '临河里', '武夷花园', '果园', '玉桥', '梨园', '九棵树(家乐福)',
                          '潞苑', '通州北苑', '通州其它', '马驹桥', '金融街', '牛街', '右安门内', '木樨地', '西单', '长椿街',
                          '月坛', '车公庄', '阜成门', '天宁寺', '宣武门', '官园', '白纸坊', '六铺炕', '德胜门', '西四',
                          '延庆其它']
        for index in range(len(community_list) + 1):
            if index == 0:
                continue
            else:
                n_community = Community(id=index, community=community_list[index - 1])
                db.session.add(n_community)
                db.session.commit()

    prev_posts = db.session.query(House).order_by(House.id.desc()).limit(6).all()
    dis_posts = db.session.query(District).all()
    com_posts = db.session.query(Community).all()
    floor_posts = db.session.query(Floor).all()
    return render_template('index.html', username=username, prev_posts=prev_posts, dis_posts=dis_posts,
                           com_posts=com_posts, floor_posts=floor_posts)


@app.route('/customer_index', methods=['GET', 'POST'])
def customer_index():
    username = session.get("USERNAME")
    if not session.get("USERNAME") is None:
        user_db = User.query.filter(User.username == session.get("USERNAME")).first()
        usertype = user_db.user_type
        # prev_posts = db.session.query(House, District, Community, Floor).all()
        if not db.session.query(Floor).first():
            floor_list = ['basement', 'low floor', 'mid floor', 'high floor']
            for index in range(len(floor_list) + 1):
                if index == 0:
                    continue
                else:
                    n_floor = Floor(id=index, floor=floor_list[index - 1])
                    db.session.add(n_floor)
                    db.session.commit()

        if not db.session.query(District).first():
            district_list = ['昌平', '朝阳', '大兴', '东城', '房山', '丰台', '海淀', '怀柔', '门头沟',
                             '密云', '平谷', '石景山', '顺义', '通州', '西城', '延庆', '亦庄开发区'
                             ]
            for index in range(len(district_list) + 1):
                if index == 0:
                    continue
                else:
                    n_district = District(id=index, district=district_list[index - 1])
                    db.session.add(n_district)
                    db.session.commit()

        if not db.session.query(Community).first():
            community_list = ['西关环岛', '北七家', '霍营', '鼓楼大街', '回龙观', '西三旗', '东关', '天通苑',
                              '沙河', '南邵', '昌平其它', '小汤山', '立水桥', '奥林匹克公园', '南口', '安宁庄',
                              '定福庄', '亚运村小营', '豆各庄', '双桥', '常营', '首都机场', '管庄', '十里河',
                              '芍药居', '垡头', '和平里', '亚运村', '红庙', '石佛营', '朝阳其它', '国展',
                              '东坝', '工体', '潘家园', '三元桥', '北苑', '华威桥', '十里堡', 'CBD', '惠新西街',
                              '十八里店', '酒仙桥', '劲松', '百子湾', '方庄', '朝青', '望京', '欢乐谷', '中央别墅区',
                              '甘露园', '四惠', '北工大', '成寿寺', '高碑店', '大望路', '太阳宫', '双井', '团结湖',
                              '南沙滩', '东大桥', '甜水园', '西坝河', '健翔桥', '三里屯', '安贞', '亮马桥', '未知',
                              '大山子', '建国门外', '朝阳门外', '东直门', '农展馆', '朝阳公园', '马甸', '燕莎',
                              '安定门', '南中轴机场商务区', '高米店', '黄村火车站', '枣园', '黄村中', '西红门',
                              '大兴其它', '瀛海', '天宫院', '义和庄', '大兴新机场', '科技园区', '旧宫', '观音寺',
                              '亦庄', '亦庄开发区其它', '和义', '大兴新机场洋房别墅区', '天宫院南', '永定门', '崇文门',
                              '东花市', '广渠门', '陶然亭', '左安门', '东四', '建国门内', '天坛', '前门', '地安门', '灯市口',
                              '金宝街', '交道口', '朝阳门内', '蒲黄榆', '东单', '长阳', '良乡', '阎村', '城关', '燕山',
                              '房山其它', '窦店', '青塔', '新宫', '木樨园', '花乡', '马家堡', '西罗园', '卢沟桥', '北大地',
                              '大红门', '看丹桥', '洋桥', '玉泉营', '刘家窑', '五里店', '赵公口', '宋家庄', '右安门外', '角门',
                              '六里桥', '七里庄', '丰台其它', '丽泽', '草桥', '北京南站', '太平桥', '菜户营', '马连道', '岳各庄',
                              '五棵松', '广安门', '马连洼', '西山', '定慧寺', '海淀北部新区', '军博', '上地', '清河', '厂洼',
                              '紫竹桥', '甘家口', '公主坟', '玉泉路', '田村', '小西天', '万寿路', '西直门', '二里庄', '皂君庙',
                              '双榆树', '四季青', '新街口', '苏州桥', '颐和园', '知春路', '五道口', '圆明园', '牡丹园', '西北旺',
                              '学院路', '万柳', '中关村', '西二旗', '杨庄', '魏公村', '世纪城', '白石桥', '北太平庄', '海淀其它',
                              '怀柔', '大峪', '石门营', '城子', '滨河西区', '冯村', '门头沟其它', '密云其它', '平谷其它', '鲁谷',
                              '八角', '苹果园', '石景山其它', '古城', '老山', '马坡', '顺义其它', '顺义城', '后沙峪', '天竺',
                              '李桥', '乔庄', '北关', '万达', '临河里', '武夷花园', '果园', '玉桥', '梨园', '九棵树(家乐福)',
                              '潞苑', '通州北苑', '通州其它', '马驹桥', '金融街', '牛街', '右安门内', '木樨地', '西单', '长椿街',
                              '月坛', '车公庄', '阜成门', '天宁寺', '宣武门', '官园', '白纸坊', '六铺炕', '德胜门', '西四',
                              '延庆其它']
            for index in range(len(community_list) + 1):
                if index == 0:
                    continue
                else:
                    n_community = Community(id=index, community=community_list[index - 1])
                    db.session.add(n_community)
                    db.session.commit()

        prev_posts = db.session.query(House).order_by(House.id.desc()).limit(6).all()
        dis_posts = db.session.query(District).all()
        com_posts = db.session.query(Community).all()
        floor_posts = db.session.query(Floor).all()
        return render_template('customer_index.html', username=username, prev_posts=prev_posts, dis_posts=dis_posts,
                               com_posts=com_posts, floor_posts=floor_posts, usertype=usertype,
                               nav_tittle="customer_index")

    flash("User needs to either login or signup first",  'warning')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_in_db = User.query.filter(User.username == form.username.data).first()
        if not user_in_db:
            flash('No user found with username: {}'.format(form.username.data), 'warning')
            return redirect(url_for('login'))
        elif check_password_hash(user_in_db.password_hash, form.password.data):
            flash('Login successful, {} welcome back!'.format(form.username.data), 'success')
            session["USERNAME"] = user_in_db.username
            return redirect(url_for('customer_index'))
        else:
            flash('Incorrect Password', 'warning')
            return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists! Please choose another username.', 'danger')
            return redirect(url_for('register'))
        elif User.query.filter_by(email=form.email.data).first():
            flash('This email already exists! Please check again.', 'danger')
            return redirect(url_for('register'))
        elif form.password.data != form.password2.data:
            flash('Passwords do not match! Please check again.', 'danger')
            return redirect(url_for('register'))
        else:
            passw_hash = generate_password_hash(form.password.data)
            user = User(username=form.username.data, email=form.email.data, password_hash=passw_hash,
                        user_type=form.user_type.data)
            db.session.add(user)
            db.session.commit()
            session["USERNAME"] = user.username
            flash('Login successful, {} welcome back!'.format(form.username.data), 'success')
            return redirect(url_for('customer_index'))
    return render_template('register.html', title='Register a new user', form=form)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  # sender='2101282494yyd@gmail.com',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    username = session.get("USERNAME")
    if not session.get("USERNAME") is None:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            user = User.query.filter_by(email=form.email.data).first()
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('login'))
        else:
            flash('This email does not exists! Please check again.', 'danger')
            return redirect(url_for('reset_request'))

    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if not session.get("USERNAME") is None:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        passw_hash = generate_password_hash(form.password.data)
        user.password_hash = passw_hash
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


def upload_pic(form_picture):
    random_hex = secrets.token_hex(8)  # https://baijiahao.baidu.com/s?id=1616189755017671452&wfr=spider&for=pc
    _, fextension = os.path.splitext(form_picture.filename)
    # reference: https://www.cnblogs.com/liangmingshen/p/10215065.html
    picture_name = random_hex + fextension
    picture_path = os.path.join(app.root_path, 'static/pic', picture_name)
    form_picture.save(picture_path)
    return picture_name


@app.route('/my_profile', methods=['GET', 'POST'])
def my_profile():
    username = session.get("USERNAME")
    form = MyProfileForm()

    if not session.get("USERNAME") is None:
        user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
        usertype = user_in_db.user_type
        if form.validate_on_submit():
            print(form.email.data)
            if form.email.data == '':
                flash('Please enter your email address, it can’t be empty', 'danger')
                return redirect(url_for('my_profile'))
            elif not re.match(r'^[\w]+[\w._]*@\w+\.[a-zA-Z]+$', form.email.data):
                flash('Please enter the correct email format', 'danger')
                return redirect(url_for('my_profile'))
            elif User.query.filter_by(email=form.email.data).first() and form.email.data != user_in_db.email:
                flash('This email already exists! Please check again.', 'danger')
                return redirect(url_for('my_profile'))
            elif User.query.filter_by(phone=form.phone.data).first() and form.phone.data != user_in_db.phone:
                flash('This phone number already exists! Please check again.', 'danger')
                return redirect(url_for('my_profile'))
            else:
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
                flash('personal information saved', 'success')
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
        return render_template("my_profile.html", username=username, form=form, usertype=usertype,
                               dash_tittle="my_profile")

    flash('User needs to either login or signup first', 'danger')
    return redirect(url_for('login'))


@app.route('/submit-new-property', methods=['GET', 'POST'])
def submit_new_property():
    return render_template('submit_new_property.html')


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    user = {'username': 'User'}
    username = session.get("USERNAME")
    form = ChangePasswordForm()
    if not session.get("USERNAME") is None:
        user_db = User.query.filter(User.username == session.get("USERNAME")).first()
        usertype = user_db.user_type
        if form.validate_on_submit():
            user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
            if not (check_password_hash(user_in_db.password_hash, form.password.data)):
                flash('Incorrect Password! Please check again.', 'warning')
                return redirect(url_for('change_password'))
            elif form.new_password1.data != form.new_password2.data:
                flash('Passwords do not match! Please check again.', 'warning')
                return redirect(url_for('change_password'))
            else:
                flash('Password changed successfully!', 'success')
                user_in_db.password_hash = generate_password_hash(form.new_password1.data)
                db.session.commit()
                return redirect(url_for('change_password'))
        return render_template('change_password.html', user=user, username=username, form=form,
                               usertype=usertype, dash_tittle="change_password")
    else:
        flash("User needs to either login or signup first", 'danger')
        return redirect(url_for('login'))


@app.route('/upload_house', methods=['GET', 'POST'])
def upload():
    username = session.get("USERNAME")
    form = AddHouseForm()
    if not session.get("USERNAME") is None:
        user_db = User.query.filter(User.username == session.get("USERNAME")).first()
        usertype = user_db.user_type
        ph_dir = Config.PH_UPLOAD_DIR
        if form.validate_on_submit():
            file = form.imagename.data
            filename = random_filename(file.filename)
            file.save(os.path.join(ph_dir, filename))
            sImg = Image.open(os.path.join(ph_dir, filename))
            dImg = sImg.resize((int(320), int(320)), Image.ANTIALIAS)
            dImg.save(os.path.join(ph_dir, filename))
            user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
            prediction = model.predict([[form.size.data, form.floorkind.data, form.roomnumber.data,
                                         form.livingnumber.data, form.bathnumber.data, form.renttype.data,
                                         form.districtid.data, form.communityid.data]])
            output = int(prediction[0])
            new_house = House(name=form.housename.data, size=form.size.data, floor_kind=form.floorkind.data,
                              floor_number=form.floornumber.data, room_number=form.roomnumber.data,
                              living_number=form.livingnumber.data,
                              bath_number=form.bathnumber.data, rent_type=form.renttype.data,
                              district_id=form.districtid.data,
                              community_id=form.communityid.data, price=form.price.data, predicted_price=output,
                              image_name=filename, description=form.description.data,
                              user=user_in_db)
            db.session.add(new_house)
            db.session.commit()
            return redirect(url_for('my_houselist'))
        else:
            return render_template('upload_house.html', username=username, title='Upload House', form=form,
                                   usertype=usertype, dash_tittle="upload_house")
    else:
        flash("User needs to either login or signup first", 'danger')
        return redirect(url_for('login'))


@app.route('/house_list', methods=['GET', 'POST'])
def house_list():
    username = session.get("USERNAME")
    if not session.get("USERNAME") is None:
        user_db = User.query.filter(User.username == session.get("USERNAME")).first()
        usertype = user_db.user_type
        # prev_posts = db.session.query(House, District, Community, Floor).all()
        if not db.session.query(Floor).first():
            floor_list = ['basement', 'low floor', 'mid floor', 'high floor']
            for index in range(len(floor_list) + 1):
                if index == 0:
                    continue
                else:
                    n_floor = Floor(id=index, floor=floor_list[index - 1])
                    db.session.add(n_floor)
                    db.session.commit()

        if not db.session.query(District).first():
            district_list = ['昌平', '朝阳', '大兴', '东城', '房山', '丰台', '海淀', '怀柔', '门头沟',
                             '密云', '平谷', '石景山', '顺义', '通州', '西城', '延庆', '亦庄开发区'
                             ]
            for index in range(len(district_list) + 1):
                if index == 0:
                    continue
                else:
                    n_district = District(id=index, district=district_list[index - 1])
                    db.session.add(n_district)
                    db.session.commit()

        if not db.session.query(Community).first():
            community_list = ['西关环岛', '北七家', '霍营', '鼓楼大街', '回龙观', '西三旗', '东关', '天通苑',
                              '沙河', '南邵', '昌平其它', '小汤山', '立水桥', '奥林匹克公园', '南口', '安宁庄',
                              '定福庄', '亚运村小营', '豆各庄', '双桥', '常营', '首都机场', '管庄', '十里河',
                              '芍药居', '垡头', '和平里', '亚运村', '红庙', '石佛营', '朝阳其它', '国展',
                              '东坝', '工体', '潘家园', '三元桥', '北苑', '华威桥', '十里堡', 'CBD', '惠新西街',
                              '十八里店', '酒仙桥', '劲松', '百子湾', '方庄', '朝青', '望京', '欢乐谷', '中央别墅区',
                              '甘露园', '四惠', '北工大', '成寿寺', '高碑店', '大望路', '太阳宫', '双井', '团结湖',
                              '南沙滩', '东大桥', '甜水园', '西坝河', '健翔桥', '三里屯', '安贞', '亮马桥', '未知',
                              '大山子', '建国门外', '朝阳门外', '东直门', '农展馆', '朝阳公园', '马甸', '燕莎',
                              '安定门', '南中轴机场商务区', '高米店', '黄村火车站', '枣园', '黄村中', '西红门',
                              '大兴其它', '瀛海', '天宫院', '义和庄', '大兴新机场', '科技园区', '旧宫', '观音寺',
                              '亦庄', '亦庄开发区其它', '和义', '大兴新机场洋房别墅区', '天宫院南', '永定门', '崇文门',
                              '东花市', '广渠门', '陶然亭', '左安门', '东四', '建国门内', '天坛', '前门', '地安门', '灯市口',
                              '金宝街', '交道口', '朝阳门内', '蒲黄榆', '东单', '长阳', '良乡', '阎村', '城关', '燕山',
                              '房山其它', '窦店', '青塔', '新宫', '木樨园', '花乡', '马家堡', '西罗园', '卢沟桥', '北大地',
                              '大红门', '看丹桥', '洋桥', '玉泉营', '刘家窑', '五里店', '赵公口', '宋家庄', '右安门外', '角门',
                              '六里桥', '七里庄', '丰台其它', '丽泽', '草桥', '北京南站', '太平桥', '菜户营', '马连道', '岳各庄',
                              '五棵松', '广安门', '马连洼', '西山', '定慧寺', '海淀北部新区', '军博', '上地', '清河', '厂洼',
                              '紫竹桥', '甘家口', '公主坟', '玉泉路', '田村', '小西天', '万寿路', '西直门', '二里庄', '皂君庙',
                              '双榆树', '四季青', '新街口', '苏州桥', '颐和园', '知春路', '五道口', '圆明园', '牡丹园', '西北旺',
                              '学院路', '万柳', '中关村', '西二旗', '杨庄', '魏公村', '世纪城', '白石桥', '北太平庄', '海淀其它',
                              '怀柔', '大峪', '石门营', '城子', '滨河西区', '冯村', '门头沟其它', '密云其它', '平谷其它', '鲁谷',
                              '八角', '苹果园', '石景山其它', '古城', '老山', '马坡', '顺义其它', '顺义城', '后沙峪', '天竺',
                              '李桥', '乔庄', '北关', '万达', '临河里', '武夷花园', '果园', '玉桥', '梨园', '九棵树(家乐福)',
                              '潞苑', '通州北苑', '通州其它', '马驹桥', '金融街', '牛街', '右安门内', '木樨地', '西单', '长椿街',
                              '月坛', '车公庄', '阜成门', '天宁寺', '宣武门', '官园', '白纸坊', '六铺炕', '德胜门', '西四',
                              '延庆其它']
            for index in range(len(community_list) + 1):
                if index == 0:
                    continue
                else:
                    n_community = Community(id=index, community=community_list[index - 1])
                    db.session.add(n_community)
                    db.session.commit()

        prev_posts = db.session.query(House).all()
        dis_posts = db.session.query(District).all()
        com_posts = db.session.query(Community).all()
        floor_posts = db.session.query(Floor).all()
        return render_template('house_list.html', username=username, prev_posts=prev_posts, dis_posts=dis_posts,
                               com_posts=com_posts, floor_posts=floor_posts, usertype=usertype)

    flash("User needs to either login or signup first", 'danger')
    return redirect(url_for('login'))


@app.route('/base_After', methods=['GET', 'POST'])
def base_after():
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        return render_template('base_After.html', title='Base', username=username)
    flash("User needs to either login or signup first", 'danger')
    return redirect(url_for('login'))


@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    username = session.get("USERNAME")
    form = CalculatorForm()
    total_repayment = 'Empty'
    total_interest = 'Empty'
    monthly_repayment = 'Empty'
    Total_repayment = 'Empty'
    Total_interest = 'Empty'
    First_month_repayment = 'Empty'
    Monthly_decrease = 'Empty'
    user_db = User.query.filter(User.username == session.get("USERNAME")).first()
    usertype = user_db.user_type
    if form.validate_on_submit():
        if not str(form.total_loans.data).isdigit():
            flash('Total Loans should be an integer positive number', 'warning')
            return redirect(url_for('calculator'))
        elif int(form.total_loans.data) < 1:
            flash('Total Loans should be an integer positive number', 'warning')
            return redirect(url_for('calculator'))
        elif not str(form.repayment_years.data).isdigit():
            flash('Repayment Years should be an integer positive number', 'warning')
            return redirect(url_for('calculator'))
        elif int(form.repayment_years.data) < 1:
            flash('Repayment Years should be an integer positive number', 'warning')
            return redirect(url_for('calculator'))
        else:
            total_loans = int(form.total_loans.data)  # 贷款总额
            annualized_rate = form.annualized_rate.data  # 年化率
            repayment_years = int(form.repayment_years.data)  # 还款年数
            types = form.types.data
            if types == 1:
                # 等额本息
                up = total_loans * math.pow((1 + annualized_rate / 1200), repayment_years * 12)
                # print("UP = ", up)
                down = 1
                for i in range(1, repayment_years * 12):
                    down = down + math.pow((1 + annualized_rate / 1200), i)
                A = up / down
                total_repayment = A * repayment_years * 12  # 还款总额
                total_interest = A * repayment_years * 12 - total_loans  # 利息总额
                monthly_repayment = A  # 月还款
                print(total_repayment, total_interest, monthly_repayment)

            elif types == 2:
                # 等额本金
                A = float(total_loans) / (repayment_years * 12)
                B = total_loans * (annualized_rate / 1200)
                C = A * (annualized_rate / 1200)
                D = (B + C) * repayment_years * 6
                Total_repayment = D + total_loans  # 还款总额
                Total_interest = D  # 利息总额
                First_month_repayment = A + B  # 首月还款
                Monthly_decrease = C  # 每月递减
                print(Total_repayment, Total_interest, First_month_repayment, Monthly_decrease)

    return render_template('calculator.html', title='Calculator', username=username, form=form,
                               total_repayment=total_repayment,
                               total_interest=total_interest, monthly_repayment=monthly_repayment,
                               Total_repayment=Total_repayment, Total_interest=Total_interest,
                               First_month_repayment=First_month_repayment, Monthly_decrease=Monthly_decrease,
                               usertype=usertype, dash_tittle="calculator")


@app.route('/my_houselist', methods=['GET', 'POST'])
def my_houselist():
    username = session.get("USERNAME")
    if not session.get("USERNAME") is None:
        user_db = User.query.filter(User.username == session.get("USERNAME")).first()
        usertype = user_db.user_type
        # prev_posts = db.session.query(House, District, Community, Floor).all()
        if not db.session.query(Floor).first():
            floor_list = ['basement', 'low floor', 'mid floor', 'high floor']
            for index in range(len(floor_list) + 1):
                if index == 0:
                    continue
                else:
                    n_floor = Floor(id=index, floor=floor_list[index - 1])
                    db.session.add(n_floor)
                    db.session.commit()

        if not db.session.query(District).first():
            district_list = ['昌平', '朝阳', '大兴', '东城', '房山', '丰台', '海淀', '怀柔', '门头沟',
                             '密云', '平谷', '石景山', '顺义', '通州', '西城', '延庆', '亦庄开发区'
                             ]
            for index in range(len(district_list) + 1):
                if index == 0:
                    continue
                else:
                    n_district = District(id=index, district=district_list[index - 1])
                    db.session.add(n_district)
                    db.session.commit()

        if not db.session.query(Community).first():
            community_list = ['西关环岛', '北七家', '霍营', '鼓楼大街', '回龙观', '西三旗', '东关', '天通苑',
                              '沙河', '南邵', '昌平其它', '小汤山', '立水桥', '奥林匹克公园', '南口', '安宁庄',
                              '定福庄', '亚运村小营', '豆各庄', '双桥', '常营', '首都机场', '管庄', '十里河',
                              '芍药居', '垡头', '和平里', '亚运村', '红庙', '石佛营', '朝阳其它', '国展',
                              '东坝', '工体', '潘家园', '三元桥', '北苑', '华威桥', '十里堡', 'CBD', '惠新西街',
                              '十八里店', '酒仙桥', '劲松', '百子湾', '方庄', '朝青', '望京', '欢乐谷', '中央别墅区',
                              '甘露园', '四惠', '北工大', '成寿寺', '高碑店', '大望路', '太阳宫', '双井', '团结湖',
                              '南沙滩', '东大桥', '甜水园', '西坝河', '健翔桥', '三里屯', '安贞', '亮马桥', '未知',
                              '大山子', '建国门外', '朝阳门外', '东直门', '农展馆', '朝阳公园', '马甸', '燕莎',
                              '安定门', '南中轴机场商务区', '高米店', '黄村火车站', '枣园', '黄村中', '西红门',
                              '大兴其它', '瀛海', '天宫院', '义和庄', '大兴新机场', '科技园区', '旧宫', '观音寺',
                              '亦庄', '亦庄开发区其它', '和义', '大兴新机场洋房别墅区', '天宫院南', '永定门', '崇文门',
                              '东花市', '广渠门', '陶然亭', '左安门', '东四', '建国门内', '天坛', '前门', '地安门', '灯市口',
                              '金宝街', '交道口', '朝阳门内', '蒲黄榆', '东单', '长阳', '良乡', '阎村', '城关', '燕山',
                              '房山其它', '窦店', '青塔', '新宫', '木樨园', '花乡', '马家堡', '西罗园', '卢沟桥', '北大地',
                              '大红门', '看丹桥', '洋桥', '玉泉营', '刘家窑', '五里店', '赵公口', '宋家庄', '右安门外', '角门',
                              '六里桥', '七里庄', '丰台其它', '丽泽', '草桥', '北京南站', '太平桥', '菜户营', '马连道', '岳各庄',
                              '五棵松', '广安门', '马连洼', '西山', '定慧寺', '海淀北部新区', '军博', '上地', '清河', '厂洼',
                              '紫竹桥', '甘家口', '公主坟', '玉泉路', '田村', '小西天', '万寿路', '西直门', '二里庄', '皂君庙',
                              '双榆树', '四季青', '新街口', '苏州桥', '颐和园', '知春路', '五道口', '圆明园', '牡丹园', '西北旺',
                              '学院路', '万柳', '中关村', '西二旗', '杨庄', '魏公村', '世纪城', '白石桥', '北太平庄', '海淀其它',
                              '怀柔', '大峪', '石门营', '城子', '滨河西区', '冯村', '门头沟其它', '密云其它', '平谷其它', '鲁谷',
                              '八角', '苹果园', '石景山其它', '古城', '老山', '马坡', '顺义其它', '顺义城', '后沙峪', '天竺',
                              '李桥', '乔庄', '北关', '万达', '临河里', '武夷花园', '果园', '玉桥', '梨园', '九棵树(家乐福)',
                              '潞苑', '通州北苑', '通州其它', '马驹桥', '金融街', '牛街', '右安门内', '木樨地', '西单', '长椿街',
                              '月坛', '车公庄', '阜成门', '天宁寺', '宣武门', '官园', '白纸坊', '六铺炕', '德胜门', '西四',
                              '延庆其它']
            for index in range(len(community_list) + 1):
                if index == 0:
                    continue
                else:
                    n_community = Community(id=index, community=community_list[index - 1])
                    db.session.add(n_community)
                    db.session.commit()

        user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
        prev_posts = db.session.query(House).filter(House.user_id == user_in_db.id).all()
        dis_posts = db.session.query(District).all()
        com_posts = db.session.query(Community).all()
        floor_posts = db.session.query(Floor).all()
        return render_template('my_houselist.html', username=username, prev_posts=prev_posts, dis_posts=dis_posts,
                               com_posts=com_posts, floor_posts=floor_posts, usertype=usertype,
                               dash_tittle="my_houselist")
    flash("User needs to either login or signup first", 'danger')
    return redirect(url_for('login'))


@app.route('/deleteHouse', methods=['GET', 'POST'])
def deleteHouse():
    s = request.form.get('s')
    stored_house = House.query.filter(House.id == s).first()
    db.session.delete(stored_house)
    db.session.commit()
    return jsonify(s)


@app.route('/house_change/<house_id>', methods=['GET', 'POST'])
def house_change(house_id):
    form = ChangeHouseForm()
    username = session.get("USERNAME")
    if not session.get("USERNAME") is None:
        user_db = User.query.filter(User.username == session.get("USERNAME")).first()
        usertype = user_db.user_type
        houseid = house_id
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
            house_in_db = House.query.filter(House.id == houseid).first()
            house_in_db.name = form.housename.data
            house_in_db.size = form.size.data
            house_in_db.floor_kind = form.floorkind.data
            house_in_db.floor_number = form.floornumber.data
            house_in_db.room_number = form.roomnumber.data
            house_in_db.living_number = form.livingnumber.data
            house_in_db.bath_number = form.bathnumber.data
            house_in_db.rent_type = form.renttype.data
            house_in_db.district_id = form.districtid.data
            house_in_db.community_id = form.communityid.data
            house_in_db.price = form.price.data
            house_in_db.predicted_price = output
            house_in_db.image_name = filename
            house_in_db.description = form.description.data
            house_in_db.user_id = user_in_db.id
            db.session.commit()
            return redirect(url_for('my_houselist'))
        else:
            house_in_db = House.query.filter(House.id == houseid).first()
            form.housename.data = house_in_db.name
            form.size.data = house_in_db.size
            form.floorkind.data = house_in_db.floor_kind
            form.floornumber.data = house_in_db.floor_number
            form.roomnumber.data = house_in_db.room_number
            form.livingnumber.data = house_in_db.living_number
            form.bathnumber.data = house_in_db.bath_number
            form.renttype.data = house_in_db.rent_type
            form.districtid.data = house_in_db.district_id
            form.communityid.data = house_in_db.community_id
            form.price.data = house_in_db.price
            form.imagename.data = house_in_db.image_name
            form.description.data = house_in_db.description
        house_in_db = House.query.filter(House.id == houseid).first()
        predrictprice = house_in_db.predicted_price
        return render_template("house_change.html", username=username, houseid=houseid, predrictprice=predrictprice,
                               form=form, usertype=usertype, dash_tittle="house_change")


@app.route('/search_house', methods=['GET', 'POST'])
def search():
    username = session.get("USERNAME")
    form = SearchForm()
    if not session.get("USERNAME") is None:
        if not db.session.query(Floor).first():
            floor_list = ['basement', 'low floor', 'mid floor', 'high floor']
            for index in range(len(floor_list) + 1):
                if index == 0:
                    continue
                else:
                    n_floor = Floor(id=index, floor=floor_list[index - 1])
                    db.session.add(n_floor)
                    db.session.commit()

        if not db.session.query(District).first():
            district_list = ['昌平', '朝阳', '大兴', '东城', '房山', '丰台', '海淀', '怀柔', '门头沟',
                             '密云', '平谷', '石景山', '顺义', '通州', '西城', '延庆', '亦庄开发区'
                             ]
            for index in range(len(district_list) + 1):
                if index == 0:
                    continue
                else:
                    n_district = District(id=index, district=district_list[index - 1])
                    db.session.add(n_district)
                    db.session.commit()

        if not db.session.query(Community).first():
            community_list = ['西关环岛', '北七家', '霍营', '鼓楼大街', '回龙观', '西三旗', '东关', '天通苑',
                              '沙河', '南邵', '昌平其它', '小汤山', '立水桥', '奥林匹克公园', '南口', '安宁庄',
                              '定福庄', '亚运村小营', '豆各庄', '双桥', '常营', '首都机场', '管庄', '十里河',
                              '芍药居', '垡头', '和平里', '亚运村', '红庙', '石佛营', '朝阳其它', '国展',
                              '东坝', '工体', '潘家园', '三元桥', '北苑', '华威桥', '十里堡', 'CBD', '惠新西街',
                              '十八里店', '酒仙桥', '劲松', '百子湾', '方庄', '朝青', '望京', '欢乐谷', '中央别墅区',
                              '甘露园', '四惠', '北工大', '成寿寺', '高碑店', '大望路', '太阳宫', '双井', '团结湖',
                              '南沙滩', '东大桥', '甜水园', '西坝河', '健翔桥', '三里屯', '安贞', '亮马桥', '未知',
                              '大山子', '建国门外', '朝阳门外', '东直门', '农展馆', '朝阳公园', '马甸', '燕莎',
                              '安定门', '南中轴机场商务区', '高米店', '黄村火车站', '枣园', '黄村中', '西红门',
                              '大兴其它', '瀛海', '天宫院', '义和庄', '大兴新机场', '科技园区', '旧宫', '观音寺',
                              '亦庄', '亦庄开发区其它', '和义', '大兴新机场洋房别墅区', '天宫院南', '永定门', '崇文门',
                              '东花市', '广渠门', '陶然亭', '左安门', '东四', '建国门内', '天坛', '前门', '地安门', '灯市口',
                              '金宝街', '交道口', '朝阳门内', '蒲黄榆', '东单', '长阳', '良乡', '阎村', '城关', '燕山',
                              '房山其它', '窦店', '青塔', '新宫', '木樨园', '花乡', '马家堡', '西罗园', '卢沟桥', '北大地',
                              '大红门', '看丹桥', '洋桥', '玉泉营', '刘家窑', '五里店', '赵公口', '宋家庄', '右安门外', '角门',
                              '六里桥', '七里庄', '丰台其它', '丽泽', '草桥', '北京南站', '太平桥', '菜户营', '马连道', '岳各庄',
                              '五棵松', '广安门', '马连洼', '西山', '定慧寺', '海淀北部新区', '军博', '上地', '清河', '厂洼',
                              '紫竹桥', '甘家口', '公主坟', '玉泉路', '田村', '小西天', '万寿路', '西直门', '二里庄', '皂君庙',
                              '双榆树', '四季青', '新街口', '苏州桥', '颐和园', '知春路', '五道口', '圆明园', '牡丹园', '西北旺',
                              '学院路', '万柳', '中关村', '西二旗', '杨庄', '魏公村', '世纪城', '白石桥', '北太平庄', '海淀其它',
                              '怀柔', '大峪', '石门营', '城子', '滨河西区', '冯村', '门头沟其它', '密云其它', '平谷其它', '鲁谷',
                              '八角', '苹果园', '石景山其它', '古城', '老山', '马坡', '顺义其它', '顺义城', '后沙峪', '天竺',
                              '李桥', '乔庄', '北关', '万达', '临河里', '武夷花园', '果园', '玉桥', '梨园', '九棵树(家乐福)',
                              '潞苑', '通州北苑', '通州其它', '马驹桥', '金融街', '牛街', '右安门内', '木樨地', '西单', '长椿街',
                              '月坛', '车公庄', '阜成门', '天宁寺', '宣武门', '官园', '白纸坊', '六铺炕', '德胜门', '西四',
                              '延庆其它']
            for index in range(len(community_list) + 1):
                if index == 0:
                    continue
                else:
                    n_community = Community(id=index, community=community_list[index - 1])
                    db.session.add(n_community)
                    db.session.commit()
        prev_posts = db.session.query(House).all()
        dis_posts = db.session.query(District).all()
        com_posts = db.session.query(Community).all()
        floor_posts = db.session.query(Floor).all()
        user_db = User.query.filter(User.username == session.get("USERNAME")).first()
        usertype = user_db.user_type
        if form.validate_on_submit():
            floor_kind_d = form.floorkind.data
            rent_type_d = form.renttype.data
            district_id_d = form.districtid.data
            community_id_d = form.communityid.data
            Houses = House.query.filter(House.floor_kind == floor_kind_d, House.rent_type == rent_type_d,
                                        House.district_id == district_id_d,
                                        House.community_id == community_id_d).all()
            if len(Houses) < 4:
                Houses = House.query.filter(House.rent_type == rent_type_d, House.district_id == district_id_d,
                                            House.community_id == community_id_d).all()
                note = 'The number of suitable houses is too small, so we recommend some relevant houses!'
                if len(Houses) < 4:
                    Houses = House.query.filter(House.district_id == district_id_d,
                                                House.community_id == community_id_d).all()
                    if len(Houses) < 4:
                        Houses = House.query.filter(House.district_id == district_id_d).all()
                        if len(Houses) == 0:
                            note = 'Sorry, there is no suitable house!'
                    else:
                        pass
                else:
                    pass
            else:
                pass
            return render_template('search_houselist.html', form=form, username=username, Houses=Houses,
                                   dis_posts=dis_posts, usertype=usertype,
                                   com_posts=com_posts, floor_posts=floor_posts, note=note,
                                   nav_tittle="search_houselist")

        else:
            return render_template('search_houselist.html', form=form, username=username, prev_posts=prev_posts,
                                   dis_posts=dis_posts, usertype=usertype,
                                   com_posts=com_posts, floor_posts=floor_posts,
                                   nav_tittle="search_houselist")
    else:
        flash("User needs to either login or signup first", 'danger')
        return redirect(url_for('login'))


@app.route('/house_detail/<house_id>', methods=['GET', 'POST'])
def house_detail(house_id):
    form = MessageForm()
    username = session.get("USERNAME")
    if not session.get("USERNAME") is None:
        user_db = User.query.filter(User.username == session.get("USERNAME")).first()
        usertype = user_db.user_type
        uid = user_db.id
        houseid = house_id
        house_in_db = House.query.filter(House.id == houseid).first()
        owner_in_db = User.query.filter(User.id == house_in_db.user_id).first()
        dis_posts = db.session.query(District).all()
        com_posts = db.session.query(Community).all()
        floor_posts = db.session.query(Floor).all()
        if form.validate_on_submit():
            new_message = CusMessage(name=form.name.data, email=form.email.data, phone=form.phone.data,
                                     detail=form.information.data, user_id=owner_in_db.id)
            db.session.add(new_message)
            db.session.commit()
            flash('Message has been sent!', 'success')
            return redirect(url_for('house_detail', house_id=houseid))
        return render_template("house_detail.html", username=username, houseid=houseid, house_in_db=house_in_db,
                               owner_in_db=owner_in_db, form=form, usertype=usertype, dash_tittle="house_detail",
                               uid=uid, dis_posts=dis_posts, com_posts=com_posts, floor_posts=floor_posts)
    else:
        flash("User needs to either login or signup first", 'danger')
        return redirect(url_for('login'))


@app.route('/saveHouse', methods=['GET', 'POST'])
def saveHouse():
    s = request.form.get('s')
    u = request.form.get('u')
    save = Save(house_id=s, user_id=u)
    db.session.add(save)
    db.session.commit()
    return jsonify(s)


@app.route('/deleteSave', methods=['GET', 'POST'])
def deleteSave():
    s = request.form.get('s')
    stored_save = Save.query.filter(Save.house_id == s).first()
    db.session.delete(stored_save)
    db.session.commit()
    return jsonify(s)


@app.route('/my_message', methods=['GET', 'POST'])
def my_message():
    username = session.get("USERNAME")
    if not session.get("USERNAME") is None:
        user_db = User.query.filter(User.username == session.get("USERNAME")).first()
        usertype = user_db.user_type
        message = CusMessage.query.filter(CusMessage.user_id == user_db.id).order_by(CusMessage.id.desc()).limit(
            10).all()
        return render_template('my_message.html', username=username, message=message,
                               usertype=usertype, dash_tittle="my_message")
    else:
        flash("User needs to either login or signup first", 'danger')
        return redirect(url_for('login'))


@app.route('/my_save', methods=['GET', 'POST'])
def my_save():
    username = session.get("USERNAME")
    if not session.get("USERNAME") is None:
        user_db = User.query.filter(User.username == session.get("USERNAME")).first()
        usertype = user_db.user_type
        # prev_posts = db.session.query(House, District, Community, Floor).all()
        if not db.session.query(Floor).first():
            floor_list = ['basement', 'low floor', 'mid floor', 'high floor']
            for index in range(len(floor_list) + 1):
                if index == 0:
                    continue
                else:
                    n_floor = Floor(id=index, floor=floor_list[index - 1])
                    db.session.add(n_floor)
                    db.session.commit()

        if not db.session.query(District).first():
            district_list = ['昌平', '朝阳', '大兴', '东城', '房山', '丰台', '海淀', '怀柔', '门头沟',
                             '密云', '平谷', '石景山', '顺义', '通州', '西城', '延庆', '亦庄开发区'
                             ]
            for index in range(len(district_list) + 1):
                if index == 0:
                    continue
                else:
                    n_district = District(id=index, district=district_list[index - 1])
                    db.session.add(n_district)
                    db.session.commit()

        if not db.session.query(Community).first():
            community_list = ['西关环岛', '北七家', '霍营', '鼓楼大街', '回龙观', '西三旗', '东关', '天通苑',
                              '沙河', '南邵', '昌平其它', '小汤山', '立水桥', '奥林匹克公园', '南口', '安宁庄',
                              '定福庄', '亚运村小营', '豆各庄', '双桥', '常营', '首都机场', '管庄', '十里河',
                              '芍药居', '垡头', '和平里', '亚运村', '红庙', '石佛营', '朝阳其它', '国展',
                              '东坝', '工体', '潘家园', '三元桥', '北苑', '华威桥', '十里堡', 'CBD', '惠新西街',
                              '十八里店', '酒仙桥', '劲松', '百子湾', '方庄', '朝青', '望京', '欢乐谷', '中央别墅区',
                              '甘露园', '四惠', '北工大', '成寿寺', '高碑店', '大望路', '太阳宫', '双井', '团结湖',
                              '南沙滩', '东大桥', '甜水园', '西坝河', '健翔桥', '三里屯', '安贞', '亮马桥', '未知',
                              '大山子', '建国门外', '朝阳门外', '东直门', '农展馆', '朝阳公园', '马甸', '燕莎',
                              '安定门', '南中轴机场商务区', '高米店', '黄村火车站', '枣园', '黄村中', '西红门',
                              '大兴其它', '瀛海', '天宫院', '义和庄', '大兴新机场', '科技园区', '旧宫', '观音寺',
                              '亦庄', '亦庄开发区其它', '和义', '大兴新机场洋房别墅区', '天宫院南', '永定门', '崇文门',
                              '东花市', '广渠门', '陶然亭', '左安门', '东四', '建国门内', '天坛', '前门', '地安门', '灯市口',
                              '金宝街', '交道口', '朝阳门内', '蒲黄榆', '东单', '长阳', '良乡', '阎村', '城关', '燕山',
                              '房山其它', '窦店', '青塔', '新宫', '木樨园', '花乡', '马家堡', '西罗园', '卢沟桥', '北大地',
                              '大红门', '看丹桥', '洋桥', '玉泉营', '刘家窑', '五里店', '赵公口', '宋家庄', '右安门外', '角门',
                              '六里桥', '七里庄', '丰台其它', '丽泽', '草桥', '北京南站', '太平桥', '菜户营', '马连道', '岳各庄',
                              '五棵松', '广安门', '马连洼', '西山', '定慧寺', '海淀北部新区', '军博', '上地', '清河', '厂洼',
                              '紫竹桥', '甘家口', '公主坟', '玉泉路', '田村', '小西天', '万寿路', '西直门', '二里庄', '皂君庙',
                              '双榆树', '四季青', '新街口', '苏州桥', '颐和园', '知春路', '五道口', '圆明园', '牡丹园', '西北旺',
                              '学院路', '万柳', '中关村', '西二旗', '杨庄', '魏公村', '世纪城', '白石桥', '北太平庄', '海淀其它',
                              '怀柔', '大峪', '石门营', '城子', '滨河西区', '冯村', '门头沟其它', '密云其它', '平谷其它', '鲁谷',
                              '八角', '苹果园', '石景山其它', '古城', '老山', '马坡', '顺义其它', '顺义城', '后沙峪', '天竺',
                              '李桥', '乔庄', '北关', '万达', '临河里', '武夷花园', '果园', '玉桥', '梨园', '九棵树(家乐福)',
                              '潞苑', '通州北苑', '通州其它', '马驹桥', '金融街', '牛街', '右安门内', '木樨地', '西单', '长椿街',
                              '月坛', '车公庄', '阜成门', '天宁寺', '宣武门', '官园', '白纸坊', '六铺炕', '德胜门', '西四',
                              '延庆其它']
            for index in range(len(community_list) + 1):
                if index == 0:
                    continue
                else:
                    n_community = Community(id=index, community=community_list[index - 1])
                    db.session.add(n_community)
                    db.session.commit()

        user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
        save = Save.query.filter(Save.user_id == user_in_db.id).order_by(Save.id.desc()).all()
        prev_posts = db.session.query(House).all()
        dis_posts = db.session.query(District).all()
        com_posts = db.session.query(Community).all()
        floor_posts = db.session.query(Floor).all()
        return render_template('my_save.html', username=username, prev_posts=prev_posts, dis_posts=dis_posts,
                               com_posts=com_posts, floor_posts=floor_posts, usertype=usertype,
                               dash_tittle="my_save", save=save)
    flash("User needs to either login or signup first", 'danger')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop("USERNAME", None)
    flash('Logout Success', 'success')
    return redirect(url_for('index'))


@app.errorhandler(500)
def error(e):
    username = session.get("USERNAME")
    user_db = User.query.filter(User.username == session.get("USERNAME")).first()
    usertype = user_db.user_type
    return render_template('error.html', username=username, usertype=usertype)


@app.errorhandler(404)
def error(e):
    username = session.get("USERNAME")
    user_db = User.query.filter(User.username == session.get("USERNAME")).first()
    usertype = user_db.user_type
    return render_template('error.html', username=username, usertype=usertype)


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    username = session.get("USERNAME")
    return render_template('contacts.html', username=username)

@app.route('/rule', methods=['GET', 'POST'])
def rule():
    username = session.get("USERNAME")
    return render_template('rule.html', username=username)
