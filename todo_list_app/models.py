from db_config import db
from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    done = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_limit = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<<Task {self.title} {'✓' if self.done else '✗'}>"