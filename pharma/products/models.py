from pharma import db, app
from datetime import datetime


class Addproduct(db.Model):
    __searchable__ = ['name','desc']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
        nullable=False)
    category = db.relationship('Category',
        backref=db.backref('category', lazy=True))

    image = db.Column(db.String(150), nullable=False, default='image.jpg')

    def __repr__(self):
        return '<Post %r>' % self.name

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(38), nullable=False, unique=True)


with app.app_context():
    db.create_all()
