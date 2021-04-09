from flask import Flask, logging
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import Config
import sys

bootstrap = Bootstrap()
db = SQLAlchemy()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    Config.Load()
    app.config.from_object(Config)

    csrf.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .scripts import scripts as scripts_blueprint
    app.register_blueprint(scripts_blueprint)

    return app
