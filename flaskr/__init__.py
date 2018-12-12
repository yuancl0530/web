from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
def create_app():
    app = Flask(__name__,
                template_folder="../templates",
                static_folder="../static")

    from . import auth
    app.register_blueprint(auth.bp)
    from . import blog
    app.register_blueprint(blog.bp)
    app.config.from_object('config.DevelopmentConfig')

    db.init_app(app)


    login_manager.init_app(app)

    return app

