import os
from flask import Flask
from flask_migrate import Migrate
from .configurations import Config
from .extensions import db, jwt, cache, mail 
from .celery_config import make_celery   
from .error_handlers import register_error_handlers

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Khởi tạo các extension
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    cache.init_app(app)

    # Tạo Celery
    celery = make_celery(app)
    # Khởi tạo Flask-Migrate
    migrate = Migrate(app, db)

    # Đăng ký error handlers
    register_error_handlers(app)

    from .routes import register_routes
    register_routes(app)

    # with app.app_context():
    #     if not os.getenv("TESTING"):  # Chỉ tạo table nếu không phải môi trường test
    #         db.create_all()
        
    return app, celery, migrate
