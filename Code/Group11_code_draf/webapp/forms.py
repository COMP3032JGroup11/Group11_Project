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
    username = StringField('Your Name', validators=[DataRequired()])
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

