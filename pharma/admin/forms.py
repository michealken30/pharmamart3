from wtforms import Form,  StringField, PasswordField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError



class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address',  validators=[DataRequired(), Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class LoginForm(Form):
    email = StringField('Email Address',  validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
