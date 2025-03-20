from datetime import datetime
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="User")
    access_token = db.Column(db.Text, nullable=True)
    refresh_token = db.Column(db.Text, nullable=True)

    tasks = db.relationship("Task", back_populates="user", cascade="all, delete-orphan")  

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(sefl, password):
        return check_password_hash(sefl.password_hash, password)
    
class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.String(36), primary_key=True,  default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(256), nullable=True)
    status = db.Column(db.String(20), nullable=False, default="pending")# in_progress, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = db.relationship("User", back_populates="tasks") 


