from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    reputation_score = db.Column(db.Integer, default=100)
    is_banned = db.Column(db.Boolean, default=False)
    muted_until = db.Column(db.Float, default=0.0)
    
    def to_dict(self):
        return {
            'username': self.username,
            'reputation_score': self.reputation_score,
            'is_banned': self.is_banned,
            'muted_until': self.muted_until
        }

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Nullable for anonymous/legacy support if needed
    username = db.Column(db.String(80), nullable=False) # Store username directly for display speed/simplicity
    content = db.Column(db.Text, nullable=False)
    is_toxic = db.Column(db.Boolean, default=False)
    toxicity_score = db.Column(db.Float)
    severity = db.Column(db.String(20), nullable=True) # High, Medium, Low
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'content': self.content,
            'is_toxic': self.is_toxic,
            'severity': self.severity,
            'timestamp': self.timestamp.isoformat()
        }
