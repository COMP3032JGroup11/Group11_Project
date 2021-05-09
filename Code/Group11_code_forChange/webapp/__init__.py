import pickle
import numpy as np

from flask import Flask
from webapp.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_dropzone import Dropzone
from flask_whooshee import Whooshee


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
dropzone = Dropzone(app)
whooshee = Whooshee(app)


from webapp import routes, models
