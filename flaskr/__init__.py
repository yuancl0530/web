from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


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
    return app

