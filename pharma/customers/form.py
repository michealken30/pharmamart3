from wtforms import Form,  StringField, PasswordField, TextAreaField, validators, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm
from .models import RegisterCustomer


class CustomerRegisterForm(FlaskForm):
    first_name = StringField('First Name', [validators.DataRequired()])
    last_name = StringField('Last Name', [validators.DataRequired()])
    username = StringField('Username:', [validators.DataRequired()])
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired(),
                                          validators.EqualTo('confirm', message='Both password must match! ')])
    confirm = PasswordField('Repeat Password: ', [validators.DataRequired()])
    country = StringField('Country:', [validators.DataRequired()])
    state = StringField('State:', [validators.DataRequired()])
    city = StringField('City:', [validators.DataRequired()])
    contact = StringField('Contact:', [validators.DataRequired()])
    address = StringField('Address:', [validators.DataRequired()])
    zipcode = StringField('Zipcode:', [validators.DataRequired()])

    submit = SubmitField('Register')

    def validate_username(self, username):
        user = RegisterCustomer.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken')


    def validate_email(self, email):
        user=RegisterCustomer.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email address is already taken')


class CustomerLoginForm(FlaskForm):
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

    submit = SubmitField('Login')
