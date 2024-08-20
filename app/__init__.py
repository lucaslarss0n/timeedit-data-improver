from flask import Flask
from app.models import db  # Import the db object from models.py
from config import Config  # Import the Config class from config.py

def create_app():
    app = Flask(__name__)
    
    # Load configuration from Config class
    app.config.from_object(Config)

    # Initialize the database with the Flask app
    db.init_app(app)

    # Ensure that the tables are created within the app context
    with app.app_context():
        db.create_all()  # Create all database tables
    
    # Import and register the pages blueprint
    from .pages import bp as pages_bp
    app.register_blueprint(pages_bp)

    return app
