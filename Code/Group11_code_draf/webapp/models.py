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
    about = db.Column(db.String(500), index=True)
    houses = db.relationship('House', back_populates='user')
    # facebook = db.Column(db.String(120), index=True, unique=True)
    # twitter = db.Column(db.String(120), index=True, unique=True)
    # google = db.Column(db.String(120), index=True, unique=True)
    # linkedin = db.Column(db.String(120), index=True, unique=True)


class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), index=True)
    size = db.Column(db.Integer, index=True)
    floor_kind = db.Column(db.Integer, index=True)
    floor_number = db.Column(db.String(10), index=True)
    room_number = db.Column(db.Integer, index=True)
    living_number = db.Column(db.Integer, index=True)
    bath_number = db.Column(db.Integer, index=True)
    rent_type = db.Column(db.Boolean, default=False)
    district_number = db.Column(db.Integer, index=True)
    community__number = db.Column(db.Integer, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='houses')

    def __repr__(self):
        return '<User {}>'.format(self.username)
