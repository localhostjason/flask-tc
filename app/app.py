# -*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment

from .assets import assets_env, bundles
from .error_handle import ErrorHandler
from config import Config
from .jinja_env import JinjaEnv
from .base_model import BaseModel

bootstrap = Bootstrap()
db = SQLAlchemy(model_class=BaseModel)
moment = Moment()

error_handler = ErrorHandler()
jinja_env = JinjaEnv()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
# message in warning, error, success
login_manager.login_message = {'warning': "您还未登录!"}
login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Config.init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)

    assets_env.init_app(app)
    assets_env.register(bundles)
    error_handler.init_app(app)
    jinja_env.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
