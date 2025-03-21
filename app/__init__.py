from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_mail import Mail  # Thêm Flask-Mail
from .configurations import Config
from .extensions import db, jwt
from .celery_config import make_celery   # Import make_celery


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt.init_app(app)
mail = Mail(app)  # Khởi tạo Flask-Mail
celery = make_celery(app)  # Khởi tạo Celery
celery.conf.update(app.config)  # Cập nhật cấu hình Celery

# Import tasks sau khi celery được khởi tạo
from app.tasks import send_task_creation_email, delete_overdue_tasks

# Thêm dòng này để kích hoạt Flask-Migrate
migrate = Migrate(app, db)

def create_app():
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    with app.app_context():
        db.create_all() # Create tables

    return app
