from flask import Flask
from flask_bootstrap import Bootstrap

from auth.configure_app import configure_app_auth
from db.configure_app import configure_app_db


def configure_app(app: Flask):
    configure_app_db(app)
    Bootstrap(app)
    configure_app_auth(app)
