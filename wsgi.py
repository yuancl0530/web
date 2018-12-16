from flask import Flask
from config import config
import os
from flaskr import db, login_manager


app = Flask(__name__,
            template_folder="templates",
            static_folder="static")

from flaskr import auth
app.register_blueprint(auth.bp)
from flaskr import blog
app.register_blueprint(blog.bp)

app.config.from_object(config[os.getenv('FLASK_ENV')])

db.init_app(app)

login_manager.init_app(app)


if __name__ == '__main__':
    app = create_app()
    app.run()