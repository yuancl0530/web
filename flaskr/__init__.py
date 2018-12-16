from flask_sqlalchemy import SQLAlchemy
from flask_login.login_manager import LoginManager

db = SQLAlchemy(use_native_unicode='utf8')
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
