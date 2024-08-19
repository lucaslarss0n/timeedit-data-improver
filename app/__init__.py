from flask import Flask
from app.models import db  # Import the db object from models.py

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)  # Initialize the database with the Flask app

    with app.app_context():
        db.create_all()  # Create all database tables

    from .pages import bp as pages_bp
    app.register_blueprint(pages_bp)

    return app
