from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Define your models here
class FileUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    user_ip = db.Column(db.String(45), nullable=False)
    processed = db.Column(db.Boolean, default=False)
    class_groups = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<FileUpload {self.filename}>"
