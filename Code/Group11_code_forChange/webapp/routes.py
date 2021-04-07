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
from webapp.models import User, House, District, Community, Floor
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
        # prev_posts = db.session.query(House, District, Community, Floor).all()
        if not db.session.query(Floor).first():
            floor_list = ['basement', 'low floor', 'medium floor', 'high floor']
            for index in range(len(floor_list)+1):
                if index == 0:
                        continue
                else:
                    n_floor = Floor(id=index, floor=floor_list[index-1])
                    db.session.add(n_floor)
                    db.session.commit()

        if not db.session.query(District).first():
            district_list = ['昌平', '朝阳', '大兴', '东城', '房山', '丰台', '海淀', '怀柔', '门头沟',
                             '密云', '平谷', '石景山', '顺义', '通州', '西城', '延庆', '亦庄开发区'
                             ]
            for index in range(len(district_list)+1):
                if index == 0:
                        continue
                else:
                    n_district = District(id=index, district=district_list[index-1])
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
            for index in range(len(community_list)+1):
                if index == 0:
                        continue
                else:
                    n_community = Community(id=index, community=community_list[index-1])
                    db.session.add(n_community)
                    db.session.commit()

        prev_posts = db.session.query(House).all()
        dis_posts = db.session.query(District).all()
        com_posts = db.session.query(Community).all()
        floor_posts = db.session.query(Floor).all()
        return render_template('house_list.html', title='record', prev_posts=prev_posts, dis_posts=dis_posts, com_posts=com_posts, floor_posts=floor_posts)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop("USERNAME", None)
    return redirect(url_for('index'))
