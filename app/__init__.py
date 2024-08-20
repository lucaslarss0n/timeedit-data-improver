from flask import Flask
from app.models import db  # Import the db object from models.py
from config import Config  # Import the Config class from config.py

def create_app():
    print("Creating Flask app...")
    app = Flask(__name__)

    print("Loading configuration...")
    app.config.from_object(Config)

    print("Initializing database...")
    db.init_app(app)

    print("Creating tables...")
    with app.app_context():
        db.create_all()  # Create all database tables

    print("Registering blueprints...")
    from .pages import bp as pages_bp
    app.register_blueprint(pages_bp)

    print("App created successfully.")
    return app

