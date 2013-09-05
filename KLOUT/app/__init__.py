from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://klout:Pass@123@localhost/klout'
db = SQLAlchemy(app)

app.secret_key = 'abcd'
login_manager = LoginManager()
login_manager.init_app(app)

from app.views import *
from app.homeview import *
