from datetime import time

from flask import current_app
from jwt import jwt

from webapp import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    name = db.Column(db.String(120), index=True)
    phone = db.Column(db.String(120), index=True, unique=True)
    address = db.Column(db.String(120), index=True)
    city = db.Column(db.String(120), index=True)
    state = db.Column(db.String(120), index=True)
    zip = db.Column(db.String(120), index=True)
    about = db.Column(db.String(500), index=True, unique=True)
    # facebook = db.Column(db.String(120), index=True, unique=True)
    # twitter = db.Column(db.String(120), index=True, unique=True)
    # google = db.Column(db.String(120), index=True, unique=True)
    # linkedin = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)
