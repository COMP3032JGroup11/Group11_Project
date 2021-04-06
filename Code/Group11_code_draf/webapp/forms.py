from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, RadioField, FileField, \
    TextAreaField, SelectField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf.file import FileRequired, FileAllowed


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired()])
    accept_rules = BooleanField('I accept the site rules', validators=[DataRequired()] )
    submit = SubmitField('Register')


class ChangePasswordForm(FlaskForm):
    password = PasswordField('Origin Password', validators=[DataRequired()])
    new_password1 = PasswordField('New Password', validators=[DataRequired(), EqualTo('new_password2', message='Passwords must match')])
    new_password2 = PasswordField('Repeat New Password', validators=[DataRequired()])
    submit = SubmitField('Reset')


# class IndexLoginForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     remember_me = BooleanField('Remember Me')
#     submit = SubmitField('Sign In')
#
#
# class IndexRegisterForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     email = StringField('Email', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     password2 = PasswordField('Repeat Password', validators=[DataRequired()])
#     accept_rules = BooleanField('I accept the site rules', validators=[DataRequired()])
#     submit = SubmitField('Register')


class MyProfileForm(FlaskForm):
    nickname = StringField('Your Nickname', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    address = StringField('Your Address', validators=[DataRequired()])
    city = StringField('Your City', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    zip = StringField('Zip of Your Area', validators=[DataRequired()])
    about = TextAreaField('Your Information', validators=[DataRequired()])
    facebook = StringField('Facebook Account', validators=[DataRequired()])
    twitter = StringField('Twitter Account', validators=[DataRequired()])
    google = StringField('Google Account', validators=[DataRequired()])
    linkedin = StringField('LinkedIn Account', validators=[DataRequired()])
    submit = SubmitField('Save Information')


class AddHouseForm(FlaskForm):
    housename = StringField('House Detail', validators=[DataRequired()])
    size = StringField('House Size', validators=[DataRequired()])
    floorkind = SelectField('Floor Kind', validators=[DataRequired()],
                            choices=[(1, 'basement'), (2, 'low floor'), (3, 'medium floor'), (4, 'high floor')],
                            coerce=int)
    floornumber = StringField('Floor Number', validators=[DataRequired()])
    roomnumber = StringField('Room Number', validators=[DataRequired()])
    livingnumber = StringField('Living Room Number', validators=[DataRequired()])
    bathnumber = StringField('Bath Room Number', validators=[DataRequired()])
    renttype = SelectField('Rent Type', validators=[DataRequired()],
                           choices=[(1, 'whole rent'), (2, 'sharing rent')],
                           coerce=int)
    districtid = SelectField('District', validators=[DataRequired()],
                             choices=[(1, '昌平'), (2, '朝阳'), (3, '大兴'), (4, '东城'), (5, '房山'), (6, '丰台'), (7, '海淀'), (8, '怀柔'),
                                      (9, '门头沟'), (10, '密云'), (11, '平谷'), (12, '石景山'), (13, '顺义'), (14, '通州'), (15, '西城'), (16, '延庆'), (17, '亦庄开发区')],
                             coerce=int)
    communityid = SelectField('Community', validators=[DataRequired()],
                              choices=[(1, '西关环岛'), (2, '北七家'), (3, '霍营'), (4, '鼓楼大街'), (5, '回龙观'), (6, '西三旗'), (7, '东关'), (8, '天通苑'),
                                       (9, '沙河'), (10, '南邵'), (11, '昌平其它'), (12, '小汤山'), (13, '立水桥'), (14, '奥林匹克公园'), (15, '南口'),
                                       (16, '安宁庄'), (17, '定福庄'), (18, '亚运村小营'), (19, '豆各庄'), (20, '双桥'), (21, '常营'), (22, '首都机场'),
                                       (23, '管庄'), (24, '十里河'), (25, '芍药居'), (26, '垡头'), (27, '和平里'), (28, '亚运村'), (29, '红庙'),
                                       (30, '石佛营'), (31, '朝阳其它'), (32, '国展'), (33, '东坝'), (34, '工体'), (35, '潘家园'), (36, '三元桥'), (37, '北苑'),
                                       (38, '华威桥'), (39, '十里堡'), (40, 'CBD'), (41, '惠新西街'), (42, '十八里店'), (43, '酒仙桥'), (44, '劲松'),
                                       (45, '百子湾'), (46, '方庄'), (47, '朝青'), (48, '望京'), (49, '欢乐谷'), (50, '中央别墅区'), (51, '甘露园'), (52, '四惠'),
                                       (53, '北工大'), (54, '成寿寺'), (55, '高碑店'), (56, '大望路'), (57, '太阳宫'), (58, '双井'), (59, '团结湖'), (60, '南沙滩'),
                                       (61, '东大桥'), (62, '甜水园'), (63, '西坝河'), (64, '健翔桥'), (65, '三里屯'), (66, '安贞'), (67, '亮马桥'), (68, 'nan'),
                                       (69, '大山子'), (70, '建国门外'), (71, '朝阳门外'), (72, '东直门'), (73, '农展馆'), (74, '朝阳公园'), (75, '马甸'),
                                       (76, '燕莎'), (77, '安定门'), (78, '南中轴机场商务区'), (79, '高米店'), (80, '黄村火车站'), (81, '枣园'), (82, '黄村中'),
                                       (83, '西红门'), (84, '大兴其它'), (85, '瀛海'), (86, '天宫院'), (87, '义和庄'), (88, '大兴新机场'), (89, '科技园区'),
                                       (90, '旧宫'), (91, '观音寺'), (92, '亦庄'), (93, '亦庄开发区其它'), (94, '和义'), (95, '大兴新机场洋房别墅区'),
                                       (96, '天宫院南'), (97, '永定门'), (98, '崇文门'), (99, '东花市'), (100, '广渠门'), (101, '陶然亭'), (102, '左安门'),
                                       (103, '东四'), (104, '建国门内'), (105, '天坛'), (106, '前门'), (107, '地安门'), (108, '灯市口'), (109, '金宝街'),
                                       (110, '交道口'), (111, '朝阳门内'), (112, '蒲黄榆'), (113, '东单'), (114, '长阳'), (115, '良乡'), (116, '阎村'),
                                       (117, '城关'), (118, '燕山'), (119, '房山其它'), (120, '窦店'), (121, '青塔'), (122, '新宫'), (123, '木樨园'),
                                       (124, '花乡'), (125, '马家堡'), (126, '西罗园'), (127, '卢沟桥'), (128, '北大地'), (129, '大红门'), (130, '看丹桥'),
                                       (131, '洋桥'), (132, '玉泉营'), (133, '刘家窑'), (134, '五里店'), (135, '赵公口'), (136, '宋家庄'), (137, '右安门外'),
                                       (138, '角门'), (139, '六里桥'), (140, '七里庄'), (141, '丰台其它'), (142, '丽泽'), (143, '草桥'), (144, '北京南站'),
                                       (145, '太平桥'), (146, '菜户营'), (147, '马连道'), (148, '岳各庄'), (149, '五棵松'), (150, '广安门'), (151, '马连洼'),
                                       (152, '西山'), (153, '定慧寺'), (154, '海淀北部新区'), (155, '军博'), (156, '上地'), (157, '清河'), (158, '厂洼'),
                                       (159, '紫竹桥'), (160, '甘家口'), (161, '公主坟'), (162, '玉泉路'), (163, '田村'), (164, '小西天'), (165, '万寿路'),
                                       (166, '西直门'), (167, '二里庄'), (168, '皂君庙'), (169, '双榆树'), (170, '四季青'), (171, '新街口'), (172, '苏州桥'),
                                       (173, '颐和园'), (174, '知春路'), (175, '五道口'), (176, '圆明园'), (177, '牡丹园'), (178, '西北旺'), (179, '学院路'),
                                       (180, '万柳'), (181, '中关村'), (182, '西二旗'), (183, '杨庄'), (184, '魏公村'), (185, '世纪城'), (186, '白石桥'),
                                       (187, '北太平庄'), (188, '海淀其它'), (189, '怀柔'), (190, '大峪'), (191, '石门营'), (192, '城子'), (193, '滨河西区'),
                                       (194, '冯村'), (195, '门头沟其它'), (196, '密云其它'), (197, '平谷其它'), (198, '鲁谷'), (199, '八角'), (200, '苹果园'),
                                       (201, '石景山其它'), (202, '古城'), (203, '老山'), (204, '马坡'), (205, '顺义其它'), (206, '顺义城'), (207, '后沙峪'),
                                       (208, '天竺'), (209, '李桥'), (210, '乔庄'), (211, '北关'), (212, '万达'), (213, '临河里'), (214, '武夷花园'),
                                       (215, '果园'), (216, '玉桥'), (217, '梨园'), (218, '九棵树(家乐福)'), (219, '潞苑'), (220, '通州北苑'), (221, '通州其它'),
                                       (222, '马驹桥'), (223, '金融街'), (224, '牛街'), (225, '右安门内'), (226, '木樨地'), (227, '西单'), (228, '长椿街'), (229, '月坛'),
                                       (230, '车公庄'), (231, '阜成门'), (232, '天宁寺'), (233, '宣武门'), (234, '官园'), (235, '白纸坊'), (236, '六铺炕'), (237, '德胜门'),
                                       (238, '西四'), (239, '延庆其它')],
                              coerce=int)
    price = StringField('Price', validators=[DataRequired()])
    imagename = FileField('House Image', validators=[FileRequired(), FileAllowed(['jpg'], 'Only JPG files please')])
    upload = SubmitField('Upload House')
