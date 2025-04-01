import logging
import os
from flask import Flask, request
from flask_migrate import Migrate

from app.exceptions import BadRequest
from .configurations import Config
from .extensions import db, jwt, cache, mail 
from .celery_config import make_celery   
from .error_handlers import register_error_handlers

def setup_logging():
    # Cấu hình log
    log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    # Đảm bảo các handler được khởi tạo
    app_log_handler =  logging.FileHandler("logs/app.log")
    app_log_handler.setLevel(logging.DEBUG)   # Log từ INFO trở lên

    error_log_handler = logging.FileHandler("logs/error.log")
    error_log_handler.setLevel(logging.ERROR)   # Log lỗi (ERROR, CRITICAL)

    log_handlers = [
        logging.StreamHandler(),  # Hiển thị log ra terminal
        app_log_handler,
        error_log_handler
    ]

    logging.basicConfig(
        level=logging.DEBUG,  # Log từ INFO trở lên
        format=log_format,
        handlers=log_handlers
    )
    
    # Thiết lập log cho Flask
    werkzeug_logger = logging.getLogger("werkzeug")  # Log của Flask
    werkzeug_logger.setLevel(logging.INFO)

    # Log lỗi Gunicorn (nếu chạy bằng Gunicorn)
    gunicorn_logger = logging.getLogger("gunicorn.error")
    gunicorn_logger.setLevel(logging.INFO)

def create_app(config_class=Config):
    setup_logging()
    logger = logging.getLogger("api_logger")

    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config["DEBUG"] = True  # Bật debug mode (Chỉ khi phát triển)
    # Khởi tạo các extension
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    cache.init_app(app)

    # Middleware để log request API
    #@app.before_request
    #def log_request_info():
       # logging.info(f"API Request: {request.method} {request.path} - Data: {request.get_json()}")
    @app.before_request
    def check_json():
        if request.method in ["POST", "PUT", "PATCH"]:  # Chỉ kiểm tra với request có body
            try:
                if request.is_json:  # Kiểm tra header Content-Type: application/json
                    request.get_json()  # Cố gắng parse JSON
                else:
                    raise BadRequest("Content-Type must be application/json")
            except BadRequest as e:
                logging.warning(f"Bad Request - Detail: {str(e)}")
                return
    # Tạo Celery
    celery = make_celery(app)
    # Khởi tạo Flask-Migrate
    migrate = Migrate(app, db)

    # Đăng ký error handlers
    register_error_handlers(app)

    from .routes import register_routes
    register_routes(app)
 
    
    with app.app_context():
        if not os.getenv("TESTING"):  # Chỉ tạo table nếu không phải môi trường test
            db.create_all()
            
    logger.info("Flask app đã khởi động.")
    return app, celery, migrate
