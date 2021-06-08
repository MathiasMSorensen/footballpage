from flask import Flask
import os
from dotenv import load_dotenv
from flask_migrate import Migrate

from db import db

load_dotenv()


def configure_app_db(app: Flask):
    # app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Stor6612@localhost:5432/flask"
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    db.init_app(app)
    Migrate(app, db)
