from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_msearch import Search
from flask_migrate import Migrate
from flask_login import LoginManager



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SECRET_KEY'] = 'thkklkklsdhhhikdsoooid3'

db = SQLAlchemy(app)


bcrypt = Bcrypt(app)
search = Search(db=db)
search.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view ='customerLogin'
login_manager.needs_refresh_message_category ='info'
login_manager.login_message = u"Please login first"




from pharma.admin import routes
from pharma.products import routes
from pharma.carts import carts
from pharma.customers import routes

