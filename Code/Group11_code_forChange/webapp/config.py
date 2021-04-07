import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
	'sqlite:///' + os.path.join(basedir, 'RentingHouse.db')

	SQLALCHEMY_TRACK_MODIFICATIONS = False

	PH_UPLOAD_DIR = os.path.join(basedir, 'static', 'Uploaded_PH')