"""
This file creates a new Flask object, and returns it after it's loaded up with configuration
settings using app.config and connected to the DB using db.init_app(app)
"""
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from config.config import app_config

db = SQLAlchemy()

def create_app(configuration):
    app = Flask(__name__)
    app.config.from_object(app_config[configuration])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # This sets performance overhead, set to True for debugging

    db.init_app(app)

    # Import the auth blueprint and register it
    # from .auth import auth_blueprint
    # app.register_blueprint(auth_blueprint)

    return app
