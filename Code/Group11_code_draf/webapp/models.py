from datetime import time

from flask import current_app
from jwt import jwt

from webapp import db
from webapp import whooshee


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(128), index=True)
# Here is for profile.html
    nickname = db.Column(db.String(120), index=True)
    phone = db.Column(db.String(120), index=True, unique=True)
    address = db.Column(db.String(120), index=True)
    city = db.Column(db.String(120), index=True)
    zip = db.Column(db.String(120), index=True)
    about = db.Column(db.String(500), index=True)
    facebook = db.Column(db.String(120), index=True)
    twitter = db.Column(db.String(120), index=True)
    google = db.Column(db.String(120), index=True)
    linkedin = db.Column(db.String(120), index=True)
    houses = db.relationship('House', backref='user', lazy='dynamic')

class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    size = db.Column(db.Integer, index=True)
    floor_kind = db.Column(db.Integer, index=True)
    floor_number = db.Column(db.String, index=True)
    room_number = db.Column(db.Integer, index=True)
    living_number = db.Column(db.Integer, index=True)
    bath_number = db.Column(db.Integer, index=True)
    rent_type = db.Column(db.Integer, index=True)
    district_id = db.Column(db.Integer, index=True)
    community_id = db.Column(db.Integer, index=True)
    price = db.Column(db.Integer, index=True)
    predicted_price = db.Column(db.Integer, index=True)
    image_name = db.Column(db.String, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    district = db.Column(db.Integer, index=True)

class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community = db.Column(db.Integer, index=True)

class Floor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    floor = db.Column(db.Integer, index=True)


