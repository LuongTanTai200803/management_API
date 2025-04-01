from datetime import timedelta
from flask import app
import os
from dotenv import load_dotenv
load_dotenv() 

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("MYSQL_PUBLIC_URL")
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'connect_timeout': 10,  # Thời gian chờ kết nối ban đầu, 10 giây
            'read_timeout': 60,     # Tăng thời gian chờ đọc lên 60 giây
        },
        'pool_recycle': 7200,  # Tái sử dụng kết nối sau 2 giờ
    }
    
    REDIS_URL = os.getenv("REDIS_URL")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("SECRET_KEY")

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)  # Access Token hết hạn sau 15 phút
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # Refresh Token hết hạn sau 30 ngày
    JSONIFY_PRETTYPRINT_REGULAR = True  # Định dạng JSON đẹp
    JSON_AS_ASCII = False  # Tắt escape Unicode (quan trọng)
    # app.config['JSON_SORT_KEYS'] = False  # Tắt sắp xếp key trong JSON
    
    # Cấu hình cache
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = "redis://localhost:6379/0"
    CACHE_DEFAULT_TIMEOUT = 300  # Thời gian cache mặc định (giây)

    # Cấu hình celery
    CELERY_BROKER_URL = "redis://localhost:6379/0"  # Địa chỉ Redis broker
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"  # Địa chỉ Redis backend
    CELERY_CONFIG = {
    'task_serializer': 'json',
    'accept_content': ['json'],
    'result_serializer': 'json',
    'timezone': 'UTC',
    # 'broker_connection_retry_on_startup': True  # Thêm dòng này
    }

    # Cấu hình celery Beat
    from celery.schedules import crontab
    CELERY_BEAT_SCHEDULE = {
    'delete-overdue-tasks-every-hour': {
        'task': 'app.tasks.delete_overdue_tasks',
        'schedule': 30.0,  # Chạy mỗi giờ (3600 giây)
    },
    } 

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # Hoặc PostgreSQL test DB