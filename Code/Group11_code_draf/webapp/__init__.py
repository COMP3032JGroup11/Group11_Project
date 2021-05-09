import pickle
import os
import numpy as np

from flask import Flask
from flask_bcrypt import Bcrypt
from webapp.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_dropzone import Dropzone
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
whooshee = Whooshee(app)
dropzone = Dropzone(app)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '2101282494yyd@gmail.com'
app.config['MAIL_PASSWORD'] = '13156676990Yyd'
# app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
# app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

from webapp import routes, models
from flask_avatars import Avatars

avatars = Avatars(app)


def register_extensions(app):
    db.init_app(app)
