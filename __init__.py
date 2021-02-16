from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from td.client import TDClient
import os

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

TDSession = TDClient(
 client_id=os.environ.get('CLIENT_ID'),
 redirect_uri=os.environ.get('REDIRECT_URI'),
 credentials_path=os.environ.get('CREDENTIALS_PATH')
)

db = SQLAlchemy()

def create_app():
 app = Flask(__name__)

 app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
 app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

 db.init_app(app)

 login_manager = LoginManager()
 login_manager.login_view = 'auth.login'
 login_manager.init_app(app)

 from .models import User

 @login_manager.user_loader
 def load_user(user_id):
  return User.query.get(int(user_id))

 from .auth import auth as auth_blueprint
 app.register_blueprint(auth_blueprint)

 from .main import main as main_blueprint
 app.register_blueprint(main_blueprint)

 from .dt import dt as dt_blueprint
 app.register_blueprint(dt_blueprint)

 return app