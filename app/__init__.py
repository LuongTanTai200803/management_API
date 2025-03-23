from flask import Flask
from flask_migrate import Migrate
from .configurations import Config
from .extensions import db, jwt, cache, mail 
from .celery_config import make_celery   # Import make_celery

from logging import setup_logging
from error_handlers import register_error_handlers

app = Flask(__name__)
app.config.from_object(Config)

# Cấu hình Flask-Caching dùng Redis (dùng cùng Redis từ Celery)
setup_logging()
register_error_handlers(app)

db.init_app(app)    # Khởi tạo db
jwt.init_app(app)   # Khởi tạo jwt
mail.init_app(app)  # Khởi tạo Flask-Mail
cache.init_app(app) # Khởi tạo cache

celery = make_celery(app)  # Khởi tạo Celery
app.celery = celery 

# Import tasks sau khi celery được khởi tạo

from app.tasks import send_task_creation_email, delete_overdue_tasks
# Import tasks sau khi celery được khởi tạo

# Thêm dòng này để kích hoạt Flask-Migrate
migrate = Migrate(app, db)

def create_app():
    app.config.from_object(Config)
    
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    with app.app_context():
        db.create_all() # Create tables

    return app
