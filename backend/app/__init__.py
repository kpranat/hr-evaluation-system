from flask import Flask, blueprints, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .extensions import db
from .config import Config
import os


def create_app():
    app = Flask(__name__)
    
    # Load configuration from Config class
    app.config.from_object(Config)
    
    # Enable CORS for all routes (allow frontend to communicate)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # PostgreSQL config (override if needed for SSL)
    if app.config["SQLALCHEMY_DATABASE_URI"]:
        # Only add SSL if using a cloud database
        if "localhost" not in app.config["SQLALCHEMY_DATABASE_URI"]:
            app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
                "connect_args": {"sslmode": "require"}
            }

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    # Candidate authentication routes
    from .CandidateAuth import CandidateAuth
    app.register_blueprint(CandidateAuth, url_prefix='/api/candidate')
    
    # Recruiter authentication routes
    from .RecruiterAuth import RecruiterAuth
    app.register_blueprint(RecruiterAuth, url_prefix='/api/recruiter')
    
    # Recruiter dashboard routes (separate from auth)
    from .RecruiterDashboard import RecruiterDashboard
    app.register_blueprint(RecruiterDashboard, url_prefix='/api/recruiter')

    # Import models before creating tables
    from . import models
    
    with app.app_context():
        db.create_all()

    return app