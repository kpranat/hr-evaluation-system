from flask import Flask,blueprints, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .extensions import db,mail
from .config import Config
import os


def create_app():
    app = Flask(__name__)

# Enable CORS for all routes


    #postgrss config
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": {"sslmode": "require"}
    }
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    #initializing the extensions file 
    db.init_app(app)
    mail.init_app(app)

    #blueprints

    # Import models before creating tables
    from . import models
    
    with app.app_context():
        db.create_all()


    return app