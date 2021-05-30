from flask import Flask
from flask_login import LoginManager

from db import users6


def configure_app_auth(app: Flask):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(found_user_id):
        return users6.query.get(int(found_user_id))
