from flask import Flask
from webapp.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_dropzone import Dropzone

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
dropzone = Dropzone(app)

from webapp import routes, models
