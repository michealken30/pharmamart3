from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, TextAreaField, validators, DecimalField, SubmitField
from flask_wtf import FlaskForm

class Addproducts(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    price = DecimalField('Price', [validators.DataRequired()])
    stock = IntegerField('Stocks', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])

    image = FileField('image', validators=[FileRequired(), FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Add Product')
